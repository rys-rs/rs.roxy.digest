import json
from typing import Any

from bson import json_util


def to_extended_json(data: Any) -> Any:
    """Convert MongoDB types (ObjectId, datetime) to Extended JSON-compatible Python structures.

    This returns dicts/lists with fields like {"$oid": "..."}, {"$date": "..."}, matching
    the format seen in dump files and typical database exports.
    """
    return json.loads(json_util.dumps(data))


