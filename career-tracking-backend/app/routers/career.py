from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.career import Career
import json

router = APIRouter(prefix="/careers", tags=["Career Management"])

@router.get("/")
async def get_careers(
    db: AsyncSession = Depends(get_db)
):
    """Get list of available careers"""
    try:
        result = await db.execute(select(Career))
        careers = result.scalars().all()
        
        career_list = []
        for career in careers:
            career_data = {
                "id": career.id,
                "title": career.title,
                "description": career.description,
                "field": career.field,
                "median_salary": career.median_salary,
                "job_outlook": career.job_outlook,
                "required_skills": json.loads(career.required_skills) if career.required_skills else []
            }
            career_list.append(career_data)
        
        return career_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching careers: {str(e)}")

@router.get("/{career_id}")
async def get_career_details(
    career_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific career"""
    try:
        result = await db.execute(select(Career).where(Career.id == career_id))
        career = result.scalar_one_or_none()
        
        if not career:
            raise HTTPException(status_code=404, detail="Career not found")
        
        return {
            "id": career.id,
            "title": career.title,
            "description": career.description,
            "field": career.field,
            "median_salary": career.median_salary,
            "job_outlook": career.job_outlook,
            "required_skills": json.loads(career.required_skills) if career.required_skills else []
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching career details: {str(e)}")

@router.get("/suggestions")
async def get_career_suggestions(
    db: AsyncSession = Depends(get_db)
):
    """Get career suggestions"""
    try:
        # For now, return top 3 careers as suggestions
        result = await db.execute(select(Career).limit(3))
        careers = result.scalars().all()
        
        suggestions = []
        for career in careers:
            career_data = {
                "id": career.id,
                "title": career.title,
                "description": career.description,
                "field": career.field,
                "median_salary": career.median_salary,
                "job_outlook": career.job_outlook,
                "required_skills": json.loads(career.required_skills) if career.required_skills else []
            }
            suggestions.append(career_data)
        
        return suggestions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching career suggestions: {str(e)}")