from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import logging

from app.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.services.college_service import CollegeService
from app.schemas.college import CollegeResponse, CollegeCreate, CollegeUpdate

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/colleges", tags=["Colleges"])

@router.get("/", response_model=List[CollegeResponse])
async def get_colleges(
    limit: int = Query(default=50, ge=1, le=100, description="Number of colleges to return"),
    city: Optional[str] = Query(default=None, description="Filter by city"),
    state: Optional[str] = Query(default=None, description="Filter by state"),
    search: Optional[str] = Query(default=None, description="Search in college name"),
    db: AsyncSession = Depends(get_db)
):
    """Get all colleges with optional filters"""
    try:
        if search or city or state:
            colleges = await CollegeService.search_colleges(
                db=db,
                query=search,
                city=city,
                state=state,
                limit=limit
            )
        else:
            colleges = await CollegeService.get_all_colleges(db, limit)
        
        # Convert to response format
        college_responses = []
        for college in colleges:
            try:
                college_responses.append(CollegeResponse.from_orm(college))
            except Exception as conv_error:
                logger.error(f"Error converting college to response: {conv_error}")
                # Skip problematic colleges
                continue
        
        return college_responses
        
    except Exception as e:
        logger.error(f"Error fetching colleges: {str(e)}")
        # Return empty list instead of error to prevent frontend crashes
        return []

@router.get("/{college_id}", response_model=CollegeResponse)
async def get_college(
    college_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get a specific college by ID"""
    try:
        college = await CollegeService.get_college_by_id(db, college_id)
        
        if not college:
            raise HTTPException(status_code=404, detail="College not found")
        
        return CollegeResponse.from_orm(college)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching college {college_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch college")

@router.get("/search/nearby")
async def search_nearby_colleges(
    latitude: float = Query(..., description="User's latitude"),
    longitude: float = Query(..., description="User's longitude"),
    radius_km: float = Query(default=50.0, description="Search radius in kilometers"),
    limit: int = Query(default=20, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Search for colleges near a location"""
    try:
        # For now, return all colleges since we don't have geospatial queries implemented
        # In a real implementation, you'd use PostGIS or similar
        colleges = await CollegeService.get_all_colleges(db, limit)
        
        # Simple distance calculation (placeholder)
        results = []
        for college in colleges:
            college_data = CollegeResponse.from_orm(college).dict()
            # Add mock distance for now
            college_data['distance_km'] = 25.5  # Mock distance
            results.append(college_data)
        
        return {
            'colleges': results,
            'search_center': {'latitude': latitude, 'longitude': longitude},
            'radius_km': radius_km,
            'total_count': len(results)
        }
        
    except Exception as e:
        logger.error(f"Error searching nearby colleges: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to search nearby colleges")

@router.get("/states/")
async def get_states(db: AsyncSession = Depends(get_db)):
    """Get all states where colleges are located"""
    try:
        from sqlalchemy import select, func
        from app.models.college import College
        
        result = await db.execute(
            select(College.state, func.count(College.id).label('count'))
            .filter(College.state.isnot(None))
            .group_by(College.state)
            .order_by(College.state)
        )
        
        states = [
            {'name': row.state, 'count': row.count}
            for row in result.fetchall()
        ]
        
        return {'states': states}
        
    except Exception as e:
        logger.error(f"Error fetching states: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch states")

@router.get("/sample")
async def get_sample_colleges():
    """Get sample colleges (for testing)"""
    try:
        from datetime import datetime
        
        # Sample college data - Jammu and Kashmir colleges
        sample_data = [
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
                "scholarship_details": "State and central government scholarships available",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
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
                "scholarship_details": "Merit-based and need-based scholarships available",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
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
                "scholarship_details": "Government and UGC scholarships available",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
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
                "scholarship_details": "Merit scholarships and financial aid",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
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
                "scholarship_details": "Various state government scholarships available",
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        return sample_data
        
    except Exception as e:
        logger.error(f"Error returning sample colleges: {str(e)}")
        return []

@router.get("/cities/")
async def get_cities(
    state: Optional[str] = Query(default=None, description="Filter cities by state"),
    db: AsyncSession = Depends(get_db)
):
    """Get all cities where colleges are located"""
    try:
        from sqlalchemy import select, func
        from app.models.college import College
        
        stmt = select(College.city, College.state, func.count(College.id).label('count')).filter(
            College.city.isnot(None)
        )
        
        if state:
            stmt = stmt.filter(College.state.ilike(f"%{state}%"))
        
        stmt = stmt.group_by(College.city, College.state).order_by(College.city)
        
        result = await db.execute(stmt)
        
        cities = [
            {'name': row.city, 'state': row.state, 'count': row.count}
            for row in result.fetchall()
        ]
        
        return {'cities': cities}
        
    except Exception as e:
        logger.error(f"Error fetching cities: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch cities")
