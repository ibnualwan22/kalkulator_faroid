"""
Main API Router untuk V1
"""

from fastapi import APIRouter
from app.api.v1.endpoints import calculation, heirs

api_router = APIRouter()

# Include routers
api_router.include_router(
    calculation.router,
    prefix="/calculation",
    tags=["Calculation"]
)

api_router.include_router(
    heirs.router,
    prefix="/heirs",
    tags=["Heirs"]
)
