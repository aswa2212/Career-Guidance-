from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.college_service import CollegeService
from app.schemas.college import CollegeResponse
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(tags=["Colleges"])

@router.get("/colleges", response_model=list[CollegeResponse])
async def search_colleges(
    query: str = Query(None, description="Search by name, city, or state"),
    state: str = Query(None, description="Filter by state"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = CollegeService(db)
    return await service.search_colleges(query, state)