import os
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database


_client: Optional[MongoClient] = None


def _get_mongo_uri() -> Optional[str]:
    return os.getenv("MONGO_URI")


def _get_db_name() -> str:
    return os.getenv("MONGO_DB_NAME", "roxy")


def get_database() -> Optional[Database]:
    uri = _get_mongo_uri()
    if not uri:
        return None
    global _client
    if _client is None:
        _client = MongoClient(uri)

    db = _client[_get_db_name()]
    try:
        db.command("ping")
    except Exception:
        return None
    return db


