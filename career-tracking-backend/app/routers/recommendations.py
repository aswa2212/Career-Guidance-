from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.recommendation_engine import recommendation_engine

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/")
async def get_user_recommendations(
    limit: int = Query(default=10, ge=1, le=20, description="Number of recommendations to return"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized course recommendations for the current user"""
    try:
        # Get user interests from database
        user_interests = current_user.interests or []
        
        # If no interests, provide some default recommendations
        if not user_interests:
            user_interests = ["programming", "technology", "career development"]
        
        # Get fresh user interests from database if available
        if current_user.id:
            fresh_interests = await recommendation_engine.get_user_interests_from_db(current_user.id, db)
            if fresh_interests:
                user_interests = fresh_interests

        # Get recommendations from the engine
        recommendations = await recommendation_engine.get_recommendations(
            user_interests=user_interests,
            user_id=current_user.id,
            top_k=limit,
            db=db
        )
        
        if not recommendations:
            # Fallback to mock recommendations if engine fails
            recommendations = _get_fallback_recommendations(limit)
        
        return {
            "recommendations": recommendations,
            "user_interests": user_interests,
            "total_count": len(recommendations)
        }
        
    except Exception as e:
        logger.error(f"Error getting recommendations for user {current_user.id}: {str(e)}")
        # Return fallback recommendations on error
        return {
            "recommendations": _get_fallback_recommendations(limit),
            "user_interests": current_user.interests or [],
            "total_count": limit,
            "error": "Using fallback recommendations"
        }

@router.get("/course/{course_id}")
async def get_course_details(
    course_id: int,
    current_user: User = Depends(get_current_user)
):
    """Get detailed information about a specific course"""
    try:
        course = recommendation_engine.get_course_by_id(course_id)
        
        if not course:
            raise HTTPException(status_code=404, detail="Course not found")
        
        return course
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting course details for ID {course_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get course details")

@router.post("/refresh")
async def refresh_recommendations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Refresh the recommendation engine data"""
    try:
        # Reset the data loaded flag to force reload
        recommendation_engine.data_loaded = False
        
        # Try to load from database first, then fallback to CSV
        success = await recommendation_engine.load_data_from_db(db)
        if not success:
            success = recommendation_engine.load_data()
        
        if success:
            return {"message": "Recommendation engine refreshed successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to refresh recommendation engine")
            
    except Exception as e:
        logger.error(f"Error refreshing recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to refresh recommendations")

def _get_fallback_recommendations(limit: int = 10) -> List[dict]:
    """Provide fallback recommendations when the ML engine is not available"""
    fallback_courses = [
        {
            "course_id": 1,
            "course_name": "Computer Science Engineering",
            "description": "Comprehensive program covering programming, algorithms, data structures, and software engineering",
            "required_skills": ["Programming", "Algorithms", "Data Structures", "Software Engineering"],
            "career_paths": ["Software Developer", "Data Scientist", "System Architect", "Tech Lead"],
            "duration": "4 years",
            "level": "Undergraduate",
            "similarity_score": 0.85,
            "final_score": 0.90,
            "match_percentage": 90
        },
        {
            "course_id": 2,
            "course_name": "Data Science",
            "description": "Master data analysis, machine learning, statistics, and big data technologies",
            "required_skills": ["Python", "Statistics", "Machine Learning", "Data Analysis"],
            "career_paths": ["Data Scientist", "ML Engineer", "Business Analyst", "Research Scientist"],
            "duration": "2 years",
            "level": "Undergraduate",
            "similarity_score": 0.82,
            "final_score": 0.87,
            "match_percentage": 87
        },
        {
            "course_id": 4,
            "course_name": "Web Development",
            "description": "Full-stack web development with modern frameworks and technologies",
            "required_skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
            "career_paths": ["Frontend Developer", "Backend Developer", "Full Stack Developer", "Web Designer"],
            "duration": "6 months",
            "level": "Certificate",
            "similarity_score": 0.78,
            "final_score": 0.83,
            "match_percentage": 83
        },
        {
            "course_id": 3,
            "course_name": "Artificial Intelligence",
            "description": "Advanced AI concepts including neural networks, deep learning, and cognitive computing",
            "required_skills": ["Python", "Mathematics", "Neural Networks", "Deep Learning"],
            "career_paths": ["AI Engineer", "ML Researcher", "Robotics Engineer", "AI Consultant"],
            "duration": "2 years",
            "level": "Undergraduate",
            "similarity_score": 0.80,
            "final_score": 0.82,
            "match_percentage": 82
        },
        {
            "course_id": 5,
            "course_name": "Mobile App Development",
            "description": "Native and cross-platform mobile application development",
            "required_skills": ["Java", "Kotlin", "Swift", "React Native"],
            "career_paths": ["Mobile Developer", "App Designer", "iOS Developer", "Android Developer"],
            "duration": "8 months",
            "level": "Certificate",
            "similarity_score": 0.75,
            "final_score": 0.80,
            "match_percentage": 80
        }
    ]
    
    return fallback_courses[:limit]
