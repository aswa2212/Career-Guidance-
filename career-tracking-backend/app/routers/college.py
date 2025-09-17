from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.college import College

router = APIRouter(prefix="/colleges", tags=["College Management"])

@router.get("/")
async def get_colleges(
    db: AsyncSession = Depends(get_db)
):
    """Get list of available colleges"""
    try:
        result = await db.execute(select(College))
        colleges = result.scalars().all()
        
        college_list = []
        for college in colleges:
            college_data = {
                "id": college.id,
                "name": college.name,
                "address": college.address,
                "city": college.city,
                "state": college.state,
                "pincode": college.pincode,
                "website": college.website,
                "latitude": college.latitude,
                "longitude": college.longitude
            }
            college_list.append(college_data)
        
        return college_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching colleges: {str(e)}")

@router.get("/{college_id}")
async def get_college_details(
    college_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific college"""
    try:
        result = await db.execute(select(College).where(College.id == college_id))
        college = result.scalar_one_or_none()
        
        if not college:
            raise HTTPException(status_code=404, detail="College not found")
        
        return {
            "id": college.id,
            "name": college.name,
            "address": college.address,
            "city": college.city,
            "state": college.state,
            "pincode": college.pincode,
            "website": college.website,
            "latitude": college.latitude,
            "longitude": college.longitude
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching college details: {str(e)}")

@router.get("/search")
async def search_colleges(
    query: str = Query(None, description="Search by name, city, or state"),
    state: str = Query(None, description="Filter by state"),
    db: AsyncSession = Depends(get_db)
):
    """Search colleges by query and filters"""
    try:
        sql_query = select(College)
        
        if query:
            sql_query = sql_query.where(
                College.name.ilike(f"%{query}%") |
                College.city.ilike(f"%{query}%") |
                College.state.ilike(f"%{query}%")
            )
        if state:
            sql_query = sql_query.where(College.state.ilike(f"%{state}%"))
        
        result = await db.execute(sql_query)
        colleges = result.scalars().all()
        
        college_list = []
        for college in colleges:
            college_data = {
                "id": college.id,
                "name": college.name,
                "address": college.address,
                "city": college.city,
                "state": college.state,
                "pincode": college.pincode,
                "website": college.website,
                "latitude": college.latitude,
                "longitude": college.longitude
            }
            college_list.append(college_data)
        
        return college_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching colleges: {str(e)}")