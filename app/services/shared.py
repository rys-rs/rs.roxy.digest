from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional

try:
    from bson import ObjectId
except Exception:  # pragma: no cover - bson may not be installed in fallback usage
    ObjectId = None  # type: ignore


def normalize_oid(value: Any) -> Optional[str]:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if ObjectId is not None and isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, dict) and "$oid" in value:
        return value.get("$oid")
    return None


def parse_extended_date(value: Any) -> Optional[datetime]:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, dict) and "$date" in value:
        try:
            return datetime.fromisoformat(str(value["$date"]).replace("Z", "+00:00"))
        except Exception:
            return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except Exception:
            return None
    return None


def iter_prices_from_item(item: Dict[str, Any]) -> Iterable[int]:
    sizes = item.get("sizes") or []
    for size in sizes:
        item_attrs = size.get("itemMenuAttributes") or []
        for attr in item_attrs:
            price = attr.get("price") or {}
            amount = price.get("amount")
            if isinstance(amount, (int, float)):
                yield int(amount)


