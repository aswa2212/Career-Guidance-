from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.models.course import Course
from app.models.college import College
from app.models.career import Career

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/populate-data")
async def populate_sample_data(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Populate database with sample data (no scrapers)"""
    try:
        # Add sample courses
        result = await db.execute(select(Course))
        existing_courses = result.scalars().all()
        
        if len(existing_courses) < 5:
            sample_courses = [
                Course(
                    title="Computer Science Engineering",
                    description="Comprehensive program covering programming, algorithms, and software engineering",
                    duration="4 years",
                    provider="Various Universities",
                    category="Engineering",
                    difficulty_level="Intermediate"
                ),
                Course(
                    title="Data Science",
                    description="Master data analysis, machine learning, and statistics",
                    duration="2 years",
                    provider="Tech Institutes",
                    category="Technology",
                    difficulty_level="Advanced"
                ),
                Course(
                    title="Web Development",
                    description="Full-stack web development with modern frameworks",
                    duration="6 months",
                    provider="Online Platforms",
                    category="Programming",
                    difficulty_level="Beginner"
                ),
                Course(
                    title="Digital Marketing",
                    description="Learn modern digital marketing strategies and tools",
                    duration="3 months",
                    provider="Marketing Institutes",
                    category="Marketing",
                    difficulty_level="Beginner"
                ),
                Course(
                    title="Mechanical Engineering",
                    description="Traditional engineering discipline focusing on mechanical systems",
                    duration="4 years",
                    provider="Engineering Colleges",
                    category="Engineering",
                    difficulty_level="Intermediate"
                )
            ]
            
            for course in sample_courses:
                db.add(course)
        
        # Add sample colleges
        result = await db.execute(select(College))
        existing_colleges = result.scalars().all()
        
        if len(existing_colleges) < 5:
            sample_colleges = [
                College(
                    name="Government College for Women, Parade Ground",
                    address="Parade, Jammu",
                    city="Jammu",
                    state="Jammu and Kashmir",
                    pincode="180001",
                    website="http://gcwparade.org/",
                    latitude=32.7300,
                    longitude=74.8700,
                    scholarship_details="State and central government scholarships available"
                ),
                College(
                    name="Government Gandhi Memorial Science College",
                    address="Canal Road, Jammu",
                    city="Jammu",
                    state="Jammu and Kashmir",
                    pincode="180001",
                    website="http://ggm.sc.in/",
                    latitude=32.7305,
                    longitude=74.8655,
                    scholarship_details="Merit-based and need-based scholarships available"
                ),
                College(
                    name="Amar Singh College",
                    address="Gogji Bagh, Srinagar",
                    city="Srinagar",
                    state="Jammu and Kashmir",
                    pincode="190008",
                    website="http://amarsinghcollege.ac.in/",
                    latitude=34.0700,
                    longitude=74.8200,
                    scholarship_details="Government and UGC scholarships available"
                ),
                College(
                    name="Sri Pratap College",
                    address="M.A. Road, Srinagar",
                    city="Srinagar",
                    state="Jammu and Kashmir",
                    pincode="190001",
                    website="http://spcollege.edu.in/",
                    latitude=34.0850,
                    longitude=74.7970,
                    scholarship_details="Merit scholarships and financial aid"
                ),
                College(
                    name="Government College for Women, M.A. Road",
                    address="M.A. Road, Srinagar",
                    city="Srinagar",
                    state="Jammu and Kashmir",
                    pincode="190001",
                    website="http://gcwmaroad.edu.in/",
                    latitude=34.0800,
                    longitude=74.8050,
                    scholarship_details="Various state government scholarships available"
                )
            ]
            
            for college in sample_colleges:
                db.add(college)
        
        # Add sample careers
        result = await db.execute(select(Career))
        existing_careers = result.scalars().all()
        
        if len(existing_careers) < 5:
            sample_careers = [
                Career(
                    title="Software Developer",
                    description="Design, develop, and maintain software applications",
                    field="Technology",
                    median_salary="₹8,50,000",
                    job_outlook="Excellent",
                    required_skills="Programming, Problem Solving, Software Design"
                ),
                Career(
                    title="Data Scientist",
                    description="Analyze complex data to help organizations make decisions",
                    field="Technology",
                    median_salary="₹12,00,000",
                    job_outlook="Very Good",
                    required_skills="Python, Statistics, Machine Learning"
                ),
                Career(
                    title="Digital Marketing Specialist",
                    description="Create and manage online marketing campaigns",
                    field="Marketing",
                    median_salary="₹6,00,000",
                    job_outlook="Good",
                    required_skills="SEO, Social Media, Content Marketing"
                ),
                Career(
                    title="Mechanical Engineer",
                    description="Design and develop mechanical systems and devices",
                    field="Engineering",
                    median_salary="₹7,00,000",
                    job_outlook="Stable",
                    required_skills="CAD Design, Thermodynamics, Manufacturing"
                ),
                Career(
                    title="UI/UX Designer",
                    description="Design user interfaces and user experiences for digital products",
                    field="Design",
                    median_salary="₹6,50,000",
                    job_outlook="Very Good",
                    required_skills="Design Tools, User Research, Prototyping"
                )
            ]
            
            for career in sample_careers:
                db.add(career)
        
        await db.commit()
        return {
            "message": "Sample data added successfully", 
            "scrapers_used": False,
            "note": "Using sample data only - no web scraping"
        }
        
    except Exception as e:
        logger.error(f"Error populating data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to populate data: {str(e)}")

@router.get("/data-status")
async def get_data_status(db: AsyncSession = Depends(get_db)):
    """Get current data counts in database"""
    try:
        # Count courses
        result = await db.execute(select(Course))
        courses_count = len(result.scalars().all())
        
        # Count colleges
        result = await db.execute(select(College))
        colleges_count = len(result.scalars().all())
        
        # Count careers
        result = await db.execute(select(Career))
        careers_count = len(result.scalars().all())
        
        return {
            "courses": courses_count,
            "colleges": colleges_count,
            "careers": careers_count,
            "total": courses_count + colleges_count + careers_count
        }
        
    except Exception as e:
        logger.error(f"Error getting data status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get data status")
