from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.aptitude_service import AptitudeService
from app.schemas.aptitude import AptitudeResultCreate, AptitudeResultResponse
from app.services.auth_service import get_current_user
from app.models.user import User

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