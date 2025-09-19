from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.course_service import CourseService
from app.schemas.course import CourseResponse, CourseCreate, CourseUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.get("/", response_model=List[CourseResponse])
async def get_courses(
    limit: int = Query(default=50, ge=1, le=100, description="Number of courses to return"),
    category: Optional[str] = Query(default=None, description="Filter by category"),
    difficulty_level: Optional[str] = Query(default=None, description="Filter by difficulty level"),
    search: Optional[str] = Query(default=None, description="Search in title and description"),
    db: AsyncSession = Depends(get_db)
):
    """Get all courses with optional filters"""
    try:
        if search or category or difficulty_level:
            courses = await CourseService.search_courses(
                db=db,
                query=search,
                category=category,
                difficulty_level=difficulty_level,
                limit=limit
            )
        else:
            courses = await CourseService.get_all_courses(db, limit)
        
        return [CourseResponse.from_orm(course) for course in courses]
        
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch courses")

@router.get("/{course_id}", response_model=CourseResponse)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific course by ID"""
    try:
        course = await CourseService.get_course_by_id(db, course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        return CourseResponse.from_orm(course)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course {course_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch course")

@router.get("/recommendations/for-me")
async def get_recommended_courses(
    limit: int = Query(default=10, ge=1, le=20, description="Number of recommendations"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get course recommendations based on user interests"""
    try:
        user_interests = current_user.interests or []
        
        if not user_interests:
            # Return popular courses if no interests
            courses = await CourseService.get_all_courses(db, limit)
        else:
            courses = await CourseService.get_courses_by_interests(db, user_interests, limit)
        
        # Convert to response format with additional recommendation info
        recommendations = []
        for i, course in enumerate(courses):
            course_data = CourseResponse.from_orm(course).dict()
            course_data.update({
                'match_percentage': max(95 - i * 5, 60),  # Simple scoring for now
                'match_reasons': user_interests[:3] if user_interests else ['Popular course']
            })
            recommendations.append(course_data)
        
        return {
            'recommendations': recommendations,
            'user_interests': user_interests,
            'total_count': len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Error getting course recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get recommendations")

@router.get("/categories/")
async def get_course_categories(db: AsyncSession = Depends(get_db)):
    """Get all available course categories"""
    try:
        from sqlalchemy import select, func
        from app.models.course import Course
        
        result = await db.execute(
            select(Course.category, func.count(Course.id).label('count'))
            .filter(Course.category.isnot(None))
            .group_by(Course.category)
            .order_by(func.count(Course.id).desc())
        )
        
        categories = [
            {'name': row.category, 'count': row.count}
            for row in result.fetchall()
        ]
        
        return {'categories': categories}
        
    except Exception as e:
        logger.error(f"Error fetching course categories: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch categories")
