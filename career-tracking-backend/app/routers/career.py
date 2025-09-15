from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/careers", tags=["Career Management"])

@router.get("/")
async def get_careers(
    db: AsyncSession = Depends(get_db)
):
    """Get list of available careers"""
    return {"message": "Career listing endpoint - implementation pending"}

@router.get("/{career_id}")
async def get_career_details(
    career_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific career"""
    return {"message": f"Career details for ID {career_id} - implementation pending"}