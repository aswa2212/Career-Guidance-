from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["Course Management"])

@router.get("/")
async def get_courses(
    db: AsyncSession = Depends(get_db)
):
    """Get list of available courses"""
    try:
        result = await db.execute(select(Course))
        courses = result.scalars().all()
        
        course_list = []
        for course in courses:
            course_data = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "duration": course.duration,
                "provider": course.provider,
                "category": course.category,
                "difficulty_level": course.difficulty_level
            }
            course_list.append(course_data)
        
        return course_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching courses: {str(e)}")

@router.get("/{course_id}")
async def get_course_details(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific course"""
    try:
        result = await db.execute(select(Course).where(Course.id == course_id))
        course = result.scalar_one_or_none()
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        return {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "duration": course.duration,
            "provider": course.provider,
            "category": course.category,
            "difficulty_level": course.difficulty_level
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching course details: {str(e)}")

@router.get("/search")
async def search_courses(
    q: str = None,
    category: str = None,
    difficulty_level: str = None,
    db: AsyncSession = Depends(get_db)
):
    """Search courses by query and filters"""
    try:
        query = select(Course)
        
        if q:
            query = query.where(Course.title.ilike(f"%{q}%"))
        if category:
            query = query.where(Course.category.ilike(f"%{category}%"))
        if difficulty_level:
            query = query.where(Course.difficulty_level.ilike(f"%{difficulty_level}%"))
        
        result = await db.execute(query)
        courses = result.scalars().all()
        
        course_list = []
        for course in courses:
            course_data = {
                "id": course.id,
                "title": course.title,
                "description": course.description,
                "duration": course.duration,
                "provider": course.provider,
                "category": course.category,
                "difficulty_level": course.difficulty_level
            }
            course_list.append(course_data)
        
        return course_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching courses: {str(e)}")
