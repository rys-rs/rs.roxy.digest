from typing import Any, Dict, List, Optional

from .shared import normalize_oid

from bson import ObjectId
from ..utils.serialization import to_extended_json


def _fetch_venue_from_db(venue_id: str, db) -> Optional[Dict[str, Any]]:
    if db is None:
        return None
    try:
        try:
            doc = db["venue"].find_one({"_id": ObjectId(venue_id)})
            if doc:
                return doc
        except Exception:
            pass
        return db["venue"].find_one({"_id": venue_id})
    except Exception:
        return None


def get_venue_profile_service(venue_id: str, db) -> Dict[str, Any]:
    doc = _fetch_venue_from_db(venue_id, db)
    if not doc:
        return {}
    return to_extended_json(doc)


def _order_type_supported(venue: Dict[str, Any], order_type: str) -> bool:
    supported = set(venue.get("supportedOrderTypes") or [])
    if order_type in supported:
        return True
    availability = venue.get("availability") or {}
    if order_type == "delivery":
        return bool(availability.get("deliveryServices"))
    if order_type == "takeout":
        return bool(availability.get("takeoutServices"))
    if order_type == "dine-in":
        return True if "dine-in" in supported else False
    return False


def _shape_search_result(v: Dict[str, Any]) -> Dict[str, Any]:
    addr = v.get("address") or {}
    integrations = v.get("integrations") or {}
    digital = integrations.get("digitalOrdering") or {}
    return {
        "id": normalize_oid(v.get("_id")),
        "name": v.get("name"),
        "city": addr.get("city"),
        "state": addr.get("state"),
        "supportedOrderTypes": v.get("supportedOrderTypes") or [],
        "reservation": v.get("reservation"),
        "websiteURL": digital.get("websiteURL"),
    }


def search_service(
    venue_id: Optional[str],
    order_type: Optional[str],
    reservation: Optional[bool],
    db,
) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []

    # Try DB first
    if db is not None:
        try:
            query: Dict[str, Any] = {}
            if venue_id:
                # Try ObjectId
                if ObjectId is not None:
                    try:
                        query["_id"] = ObjectId(venue_id)
                    except Exception:
                        query["_id"] = venue_id
                else:
                    query["_id"] = venue_id

            if reservation is not None:
                query["reservation"] = reservation

            cursor = db["venue"].find(query)
            venues: List[Dict[str, Any]] = list(cursor)

            if order_type:
                venues = [v for v in venues if _order_type_supported(v, order_type)]

            results = [to_extended_json(v) for v in venues]
        except Exception:
            results = []

    return results


