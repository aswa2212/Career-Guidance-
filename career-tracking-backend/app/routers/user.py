from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate, UserInterestsUpdate

router = APIRouter(prefix="/users", tags=["User Management"])

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's profile"""
    try:
        # Update user fields
        for field, value in user_update.model_dump(exclude_unset=True).items():
            setattr(current_user, field, value)
        
        # Add to session and commit
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update profile: {str(e)}"
        )

@router.put("/me/interests", response_model=UserResponse)
async def update_user_interests(
    interests_update: UserInterestsUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user's interests"""
    try:
        # Update the user's interests
        current_user.interests = interests_update.interests
        
        # Add to session and commit
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)
        
        return current_user
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to update interests: {str(e)}"
        )

@router.get("/me/interests")
async def get_user_interests(
    current_user: User = Depends(get_current_user)
):
    """Get current user's interests"""
    return {"interests": current_user.interests or []}