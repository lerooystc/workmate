from fastapi import APIRouter

from .v1 import route_trade

api_router = APIRouter()
api_router.include_router(route_trade.router, prefix="", tags=["trades"])
