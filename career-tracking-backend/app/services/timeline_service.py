from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.timeline import Timeline
from app.schemas.timeline import TimelineCreate, TimelineResponse
from app.utils.notifications import send_notification

class TimelineService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_timeline(self, user_id: int, timeline_data: TimelineCreate) -> TimelineResponse:
        new_timeline = Timeline(
            user_id=user_id,
            college_id=timeline_data.college_id,
            course_id=timeline_data.course_id,
            deadline=timeline_data.deadline,
            status="pending"
        )
        self.db.add(new_timeline)
        await self.db.commit()
        await self.db.refresh(new_timeline)
        
        # Send notification
        await send_notification(
            user_id,
            "Timeline Created",
            f"Admission timeline created for deadline {timeline_data.deadline}"
        )
        return TimelineResponse.model_validate(new_timeline)