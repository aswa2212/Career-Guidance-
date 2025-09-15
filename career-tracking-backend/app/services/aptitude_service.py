from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.aptitude import AptitudeTest
from app.schemas.aptitude import AptitudeResultCreate, AptitudeResultResponse

class AptitudeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def submit_aptitude_result(self, user_id: int, result_data: AptitudeResultCreate) -> AptitudeResultResponse:
        # Create new aptitude result
        new_result = AptitudeTest(
            user_id=user_id,
            test_name=result_data.test_name,
            scores=str(result_data.scores) if result_data.scores else "{}",
            overall_score=result_data.overall_score
        )
        self.db.add(new_result)
        await self.db.commit()
        await self.db.refresh(new_result)
        return AptitudeResultResponse.model_validate(new_result)

    async def get_user_aptitude_results(self, user_id: int) -> list[AptitudeResultResponse]:
        # Get all aptitude results for a user
        results = await self.db.execute(select(AptitudeTest).filter(AptitudeTest.user_id == user_id))
        return [AptitudeResultResponse.model_validate(result) for result in results.scalars().all()]