from fastapi import FastAPI, Depends, Query
from typing import Optional, List, Dict, Any

from .db import get_database
from .services.menu_service import get_menu_digest_service
from .services.venue_service import get_venue_profile_service, search_service


app = FastAPI(title="Roxy Digest API", version="0.1.0")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/menu/{venue_id}/digest")
def get_menu_digest(venue_id: str, db=Depends(get_database)) -> Dict[str, Any]:
    return get_menu_digest_service(venue_id=venue_id, db=db)


@app.get("/venue/{venue_id}/profile")
def venue_profile(venue_id: str, db=Depends(get_database)) -> Dict[str, Any]:
    return get_venue_profile_service(venue_id=venue_id, db=db)


@app.get("/search")
def search(
    venue_id: Optional[str] = Query(default=None),
    order_type: Optional[str] = Query(default=None, regex="^(delivery|takeout|dine-in)$"),
    reservation: Optional[bool] = Query(default=None),
    db=Depends(get_database),
) -> List[Dict[str, Any]]:
    return search_service(venue_id=venue_id, order_type=order_type, reservation=reservation, db=db)


