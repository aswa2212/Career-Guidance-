from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.timeline_service import TimelineService
from app.schemas.timeline import TimelineCreate, TimelineResponse
from app.services.auth_service import get_current_user
from app.models.user import User

router = APIRouter(tags=["Admission Timeline"])

@router.post("/timeline", response_model=TimelineResponse, status_code=status.HTTP_201_CREATED)
async def create_timeline(
    timeline_data: TimelineCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    service = TimelineService(db)
    return await service.create_timeline(current_user.id, timeline_data)