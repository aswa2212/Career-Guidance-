from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(prefix="/suggestions", tags=["Career Suggestions"])

@router.get("/")
async def get_career_suggestions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized career suggestions based on user profile and aptitude tests"""
    return {"message": "Career suggestions endpoint - implementation pending"}

@router.get("/courses")
async def get_course_suggestions(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get course recommendations based on career interests"""
    return {"message": "Course suggestions endpoint - implementation pending"}