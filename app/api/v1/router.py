from fastapi import APIRouter
from app.api.v1.endpoints import health, auth

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health", tags=["Health"])
v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])