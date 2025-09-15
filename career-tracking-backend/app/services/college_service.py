from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.models.college import College
from app.schemas.college import CollegeResponse

class CollegeService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_colleges(self, query: str, state: str = None) -> list[CollegeResponse]:
        # Search colleges by name, city, or state
        stmt = select(College)
        if query:
            stmt = stmt.filter(or_(
                College.name.ilike(f"%{query}%"),
                College.city.ilike(f"%{query}%"),
                College.state.ilike(f"%{query}%")
            ))
        if state:
            stmt = stmt.filter(College.state == state)
            
        result = await self.db.execute(stmt)
        colleges = result.scalars().all()
        return [CollegeResponse.from_orm(college) for college in colleges]