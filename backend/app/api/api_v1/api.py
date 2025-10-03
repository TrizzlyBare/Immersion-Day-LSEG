from fastapi import APIRouter
from app.api.api_v1.endpoints import travelplans

api_router = APIRouter()
api_router.include_router(travelplans.router, prefix="/v1", tags=["travel-plans"])
