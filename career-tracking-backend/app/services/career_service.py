from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional

from app.models.career import Career


async def get_all_careers(db: AsyncSession) -> List[Career]:
    """Get all available careers"""
    result = await db.execute(select(Career))
    return result.scalars().all()


async def get_career_by_id(db: AsyncSession, career_id: int) -> Optional[Career]:
    """Get career by ID"""
    result = await db.execute(select(Career).filter(Career.id == career_id))
    return result.scalars().first()


async def search_careers_by_field(db: AsyncSession, field: str) -> List[Career]:
    """Search careers by field/domain"""
    result = await db.execute(
        select(Career).filter(Career.field.ilike(f"%{field}%"))
    )
    return result.scalars().all()


async def get_careers_by_skills(db: AsyncSession, skills: List[str]) -> List[Career]:
    """Get careers matching specific skills"""
    # This would need more complex logic based on your skill matching algorithm
    result = await db.execute(select(Career))
    return result.scalars().all()