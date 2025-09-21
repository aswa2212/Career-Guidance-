from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Any, Optional

from app.database import get_db
from app.services.aptitude_service import AptitudeService
from app.schemas.aptitude import AptitudeResultCreate, AptitudeResultResponse
from app.services.auth_service import get_current_user
from app.models.user import User
# Scrapers disabled - using sample data only
SCRAPER_AVAILABLE = False
AptitudeScraper = None

router = APIRouter(tags=["Aptitude"])

@router.post("/aptitude", response_model=AptitudeResultResponse, status_code=status.HTTP_201_CREATED)
async def submit_aptitude_result(
    result_data: AptitudeResultCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AptitudeService(db)
    return await service.submit_aptitude_result(current_user.id, result_data)

@router.get("/aptitude", response_model=list[AptitudeResultResponse])
async def get_aptitude_results(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = AptitudeService(db)
    return await service.get_user_aptitude_results(current_user.id)

@router.get("/aptitude/questions")
async def get_aptitude_questions(
    subject: Optional[str] = Query(None, description="Filter by subject"),
    difficulty: Optional[str] = Query(None, description="Filter by difficulty"),
    count: int = Query(20, description="Number of questions to return")
) -> Dict[str, Any]:
    """
    Get aptitude questions for testing
    """
    if not SCRAPER_AVAILABLE:
        # Return mock data when scraper is not available
        mock_questions = [
            {
                "id": 1,
                "question": "What is 2 + 2?",
                "options": ["3", "4", "5", "6"],
                "correct_answer": "4",
                "subject": "Mathematics",
                "difficulty": "Easy"
            },
            {
                "id": 2,
                "question": "Which planet is closest to the Sun?",
                "options": ["Venus", "Earth", "Mercury", "Mars"],
                "correct_answer": "Mercury",
                "subject": "General Knowledge",
                "difficulty": "Medium"
            }
        ]
        return {
            "questions": mock_questions[:count],
            "total_count": len(mock_questions),
            "subjects_available": ["Mathematics", "General Knowledge"],
            "difficulties_available": ["Easy", "Medium"],
            "note": "Using mock data - scraper not available"
        }
    
    try:
        scraper = AptitudeScraper()
        all_questions = scraper.scrape()
        
        # Filter questions based on parameters
        filtered_questions = all_questions
        
        if subject:
            filtered_questions = [q for q in filtered_questions if q.get('subject', '').lower() == subject.lower()]
        
        if difficulty:
            filtered_questions = [q for q in filtered_questions if q.get('difficulty', '').lower() == difficulty.lower()]
        
        # Limit the number of questions
        filtered_questions = filtered_questions[:count]
        
        return {
            "questions": filtered_questions,
            "total_count": len(filtered_questions),
            "subjects_available": list(set(q.get('subject', 'Unknown') for q in all_questions)),
            "difficulties_available": list(set(q.get('difficulty', 'Unknown') for q in all_questions))
        }
        
    except Exception as e:
        return {
            "error": f"Failed to fetch aptitude questions: {str(e)}",
            "questions": [],
            "total_count": 0,
            "subjects_available": [],
            "difficulties_available": []
        }

@router.get("/aptitude/test/{test_type}")
async def get_aptitude_test(
    test_type: str,
    count: int = Query(10, description="Number of questions for the test")
) -> Dict[str, Any]:
    """
    Get a specific aptitude test (e.g., 'mathematics', 'logical_reasoning', 'general_knowledge')
    """
    if not SCRAPER_AVAILABLE:
        # Return mock test data when scraper is not available
        mock_questions = [
            {
                "id": 1,
                "question": f"Sample {test_type} question 1",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Option A",
                "subject": test_type.title(),
                "difficulty": "Medium"
            },
            {
                "id": 2,
                "question": f"Sample {test_type} question 2",
                "options": ["Choice 1", "Choice 2", "Choice 3", "Choice 4"],
                "correct_answer": "Choice 2",
                "subject": test_type.title(),
                "difficulty": "Medium"
            }
        ]
        return {
            "test_type": test_type,
            "questions": mock_questions[:count],
            "total_questions": len(mock_questions[:count]),
            "time_limit_minutes": count * 2,
            "instructions": "Choose the best answer for each question. You have 2 minutes per question.",
            "note": "Using mock data - scraper not available"
        }
    
    try:
        scraper = AptitudeScraper()
        all_questions = scraper.scrape()
        
        # Filter by test type
        if test_type.lower() == 'mixed':
            # Get a mix of different subjects
            test_questions = all_questions[:count]
        else:
            # Filter by specific subject
            test_questions = [q for q in all_questions if test_type.lower() in q.get('subject', '').lower()]
            test_questions = test_questions[:count]
        
        return {
            "test_type": test_type,
            "questions": test_questions,
            "total_questions": len(test_questions),
            "time_limit_minutes": count * 2,  # 2 minutes per question
            "instructions": "Choose the best answer for each question. You have 2 minutes per question."
        }
        
    except Exception as e:
        return {
            "error": f"Failed to generate {test_type} test: {str(e)}",
            "questions": [],
            "total_questions": 0
        }