from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
import logging

from app.models.course import Course
from app.models.college import College

logger = logging.getLogger(__name__)

class CourseService:
    """Service for handling course-related operations"""
    
    @staticmethod
    async def get_all_courses(db: AsyncSession, limit: int = 100) -> List[Course]:
        """Get all courses from database"""
        try:
            result = await db.execute(
                select(Course)
                .limit(limit)
                .order_by(Course.created_at.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching courses: {str(e)}")
            return []
    
    @staticmethod
    async def get_course_by_id(db: AsyncSession, course_id: int) -> Optional[Course]:
        """Get a specific course by ID"""
        try:
            result = await db.execute(select(Course).filter(Course.id == course_id))
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error fetching course {course_id}: {str(e)}")
            return None
    
    @staticmethod
    async def search_courses(
        db: AsyncSession, 
        query: str = None, 
        category: str = None,
        difficulty_level: str = None,
        limit: int = 50
    ) -> List[Course]:
        """Search courses with filters"""
        try:
            stmt = select(Course)
            
            if query:
                stmt = stmt.filter(
                    Course.title.ilike(f"%{query}%") |
                    Course.description.ilike(f"%{query}%")
                )
            
            if category:
                stmt = stmt.filter(Course.category.ilike(f"%{category}%"))
            
            if difficulty_level:
                stmt = stmt.filter(Course.difficulty_level == difficulty_level)
            
            stmt = stmt.limit(limit).order_by(Course.created_at.desc())
            
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error searching courses: {str(e)}")
            return []
    
    @staticmethod
    async def get_courses_by_interests(
        db: AsyncSession, 
        interests: List[str], 
        limit: int = 20
    ) -> List[Course]:
        """Get courses that match user interests"""
        try:
            if not interests:
                return await CourseService.get_all_courses(db, limit)
            
            # Create a filter for courses that match any of the interests
            interest_filters = []
            for interest in interests:
                interest_filters.extend([
                    Course.title.ilike(f"%{interest}%"),
                    Course.description.ilike(f"%{interest}%"),
                    Course.category.ilike(f"%{interest}%")
                ])
            
            # Combine filters with OR
            from sqlalchemy import or_
            stmt = select(Course).filter(or_(*interest_filters)).limit(limit)
            
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching courses by interests: {str(e)}")
            return []

class CollegeService:
    """Service for handling college-related operations"""
    
    @staticmethod
    async def get_all_colleges(db: AsyncSession, limit: int = 100) -> List[College]:
        """Get all colleges from database"""
        try:
            result = await db.execute(
                select(College)
                .limit(limit)
                .order_by(College.created_at.desc())
            )
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error fetching colleges: {str(e)}")
            return []
    
    @staticmethod
    async def get_college_by_id(db: AsyncSession, college_id: int) -> Optional[College]:
        """Get a specific college by ID"""
        try:
            result = await db.execute(select(College).filter(College.id == college_id))
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error fetching college {college_id}: {str(e)}")
            return None
    
    @staticmethod
    async def search_colleges(
        db: AsyncSession,
        query: str = None,
        city: str = None,
        state: str = None,
        limit: int = 50
    ) -> List[College]:
        """Search colleges with filters"""
        try:
            stmt = select(College)
            
            if query:
                stmt = stmt.filter(College.name.ilike(f"%{query}%"))
            
            if city:
                stmt = stmt.filter(College.city.ilike(f"%{city}%"))
            
            if state:
                stmt = stmt.filter(College.state.ilike(f"%{state}%"))
            
            stmt = stmt.limit(limit).order_by(College.created_at.desc())
            
            result = await db.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Error searching colleges: {str(e)}")
            return []
