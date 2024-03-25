from fastapi import APIRouter

from app.api.api_v1.endpoints import assistant


api_router = APIRouter(prefix="/api/v1")

api_router.include_router(assistant.router, tags=["Assistant"])
