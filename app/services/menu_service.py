from collections import Counter
from typing import Any, Dict, List, Optional

from .shared import iter_prices_from_item, normalize_oid

from bson import ObjectId


def _fetch_items_from_db(venue_id: str, db) -> Optional[List[Dict[str, Any]]]:
    if db is None:
        return None
    try:
        venue_oid = None
        try:
            venue_oid = ObjectId(venue_id)
        except Exception:
            venue_oid = None

        pipeline_oid = [
            {"$unwind": "$items"},
            {"$match": {"items.venueId": venue_oid}},
            {"$replaceRoot": {"newRoot": "$items"}},
        ] if venue_oid is not None else None

        items: List[Dict[str, Any]] = []
        if pipeline_oid is not None:
            for doc in db["menu-digest"].aggregate(pipeline_oid):
                items.append(doc)

        if not items:
            # Fallback match by string id in embedded Extended JSON or string field
            pipeline_str = [
                {"$unwind": "$items"},
                {"$match": {"items.venueId": venue_id}},
                {"$replaceRoot": {"newRoot": "$items"}},
            ]
            for doc in db["menu-digest"].aggregate(pipeline_str):
                items.append(doc)

        return items
    except Exception:
        return None


def _build_digest(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    total_items = len(items)
    category_counter: Counter[str] = Counter()
    all_prices: List[int] = []
    facets: Counter[str] = Counter()

    for item in items:
        category = (item.get("category") or "Uncategorized").strip() or "Uncategorized"
        category_counter[category] += 1
        for price in iter_prices_from_item(item):
            all_prices.append(price)
        for facet in item.get("facets") or []:
            if isinstance(facet, str):
                facets[facet] += 1

    categories = [
        {"name": name, "count": count}
        for name, count in category_counter.most_common()
    ]

    digest: Dict[str, Any] = {
        "total_items": total_items,
        "categories": categories,
        "facets": [{"name": name, "count": count} for name, count in facets.most_common()],
    }
    if all_prices:
        digest.update(
            {
                "price": {
                    "min": min(all_prices),
                    "max": max(all_prices),
                    "avg": int(sum(all_prices) / len(all_prices)),
                    "currency": "USD",
                }
            }
        )
    return digest


def get_menu_digest_service(venue_id: str, db) -> Dict[str, Any]:
    items = _fetch_items_from_db(venue_id, db)
    return _build_digest(items)


