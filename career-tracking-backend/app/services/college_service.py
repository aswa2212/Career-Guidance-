from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List, Optional
from app.models.college import College
import logging

logger = logging.getLogger(__name__)

# Sample college data for fallback - Jammu and Kashmir colleges
SAMPLE_COLLEGES_DATA = [
    {
        "id": 1,
        "name": "Government College for Women, Parade Ground",
        "address": "Parade, Jammu",
        "city": "Jammu",
        "state": "Jammu and Kashmir",
        "pincode": "180001",
        "website": "http://gcwparade.org/",
        "latitude": 32.7300,
        "longitude": 74.8700,
        "scholarship_details": "State and central government scholarships available"
    },
    {
        "id": 2,
        "name": "Government Gandhi Memorial Science College",
        "address": "Canal Road, Jammu",
        "city": "Jammu",
        "state": "Jammu and Kashmir",
        "pincode": "180001",
        "website": "http://ggm.sc.in/",
        "latitude": 32.7305,
        "longitude": 74.8655,
        "scholarship_details": "Merit-based and need-based scholarships available"
    },
    {
        "id": 3,
        "name": "Amar Singh College",
        "address": "Gogji Bagh, Srinagar",
        "city": "Srinagar",
        "state": "Jammu and Kashmir",
        "pincode": "190008",
        "website": "http://amarsinghcollege.ac.in/",
        "latitude": 34.0700,
        "longitude": 74.8200,
        "scholarship_details": "Government and UGC scholarships available"
    },
    {
        "id": 4,
        "name": "Sri Pratap College",
        "address": "M.A. Road, Srinagar",
        "city": "Srinagar",
        "state": "Jammu and Kashmir",
        "pincode": "190001",
        "website": "http://spcollege.edu.in/",
        "latitude": 34.0850,
        "longitude": 74.7970,
        "scholarship_details": "Merit scholarships and financial aid"
    },
    {
        "id": 5,
        "name": "Government College for Women, M.A. Road",
        "address": "M.A. Road, Srinagar",
        "city": "Srinagar",
        "state": "Jammu and Kashmir",
        "pincode": "190001",
        "website": "http://gcwmaroad.edu.in/",
        "latitude": 34.0800,
        "longitude": 74.8050,
        "scholarship_details": "Various state government scholarships available"
    }
]

def create_college_from_dict(data: dict) -> College:
    """Create a College object from dictionary data"""
    from datetime import datetime
    
    college = College()
    for key, value in data.items():
        if hasattr(college, key):
            setattr(college, key, value)
    
    # Set required timestamps if not present
    if not hasattr(college, 'created_at') or college.created_at is None:
        college.created_at = datetime.utcnow()
    if not hasattr(college, 'updated_at') or college.updated_at is None:
        college.updated_at = datetime.utcnow()
    
    return college

class CollegeService:
    @staticmethod
    async def get_all_colleges(db: AsyncSession, limit: int = 50) -> List[College]:
        """Get all colleges with optional limit"""
        try:
            stmt = select(College).limit(limit)
            result = await db.execute(stmt)
            colleges = result.scalars().all()
            
            # If no colleges in database, return sample data
            if not colleges:
                logger.info("No colleges in database, returning sample data")
                sample_colleges = [create_college_from_dict(data) for data in SAMPLE_COLLEGES_DATA[:limit]]
                return sample_colleges
            
            return colleges
        except Exception as e:
            logger.error(f"Database error, returning sample colleges: {e}")
            # Always return sample data on any error
            try:
                sample_colleges = [create_college_from_dict(data) for data in SAMPLE_COLLEGES_DATA[:limit]]
                return sample_colleges
            except Exception as fallback_error:
                logger.error(f"Fallback error: {fallback_error}")
                # Return empty list as last resort
                return []
    
    @staticmethod
    async def get_college_by_id(db: AsyncSession, college_id: int) -> Optional[College]:
        """Get a college by ID"""
        try:
            stmt = select(College).filter(College.id == college_id)
            result = await db.execute(stmt)
            college = result.scalars().first()
            
            # If not found in database, check sample data
            if not college:
                for data in SAMPLE_COLLEGES_DATA:
                    if data["id"] == college_id:
                        return create_college_from_dict(data)
            
            return college
        except Exception as e:
            logger.error(f"Database error, checking sample data: {e}")
            for data in SAMPLE_COLLEGES_DATA:
                if data["id"] == college_id:
                    return create_college_from_dict(data)
            return None
    
    @staticmethod
    async def search_colleges(
        db: AsyncSession, 
        query: Optional[str] = None, 
        city: Optional[str] = None, 
        state: Optional[str] = None, 
        limit: int = 50
    ) -> List[College]:
        """Search colleges by name, city, or state"""
        try:
            stmt = select(College)
            
            conditions = []
            if query:
                conditions.append(or_(
                    College.name.ilike(f"%{query}%"),
                    College.city.ilike(f"%{query}%"),
                    College.state.ilike(f"%{query}%")
                ))
            
            if city:
                conditions.append(College.city.ilike(f"%{city}%"))
                
            if state:
                conditions.append(College.state.ilike(f"%{state}%"))
            
            if conditions:
                stmt = stmt.filter(*conditions)
                
            stmt = stmt.limit(limit)
            result = await db.execute(stmt)
            colleges = result.scalars().all()
            
            # If no results from database, search sample data
            if not colleges:
                logger.info("No colleges found in database, searching sample data")
                filtered_data = SAMPLE_COLLEGES_DATA
                
                if query:
                    query_lower = query.lower()
                    filtered_data = [
                        data for data in filtered_data
                        if query_lower in data["name"].lower() or 
                           query_lower in data["city"].lower() or 
                           query_lower in data["state"].lower()
                    ]
                
                if city:
                    city_lower = city.lower()
                    filtered_data = [
                        data for data in filtered_data
                        if city_lower in data["city"].lower()
                    ]
                
                if state:
                    state_lower = state.lower()
                    filtered_data = [
                        data for data in filtered_data
                        if state_lower in data["state"].lower()
                    ]
                
                sample_colleges = [create_college_from_dict(data) for data in filtered_data[:limit]]
                return sample_colleges
            
            return colleges
        except Exception as e:
            logger.error(f"Database error, searching sample data: {e}")
            # Return all sample colleges if there's an error
            sample_colleges = [create_college_from_dict(data) for data in SAMPLE_COLLEGES_DATA[:limit]]
            return sample_colleges