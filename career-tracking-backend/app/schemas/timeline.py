from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime, date


class TimelineBase(BaseModel):
    user_id: int
    college_id: int
    course_id: int
    deadline: Optional[date] = None
    status: Optional[str] = None
    notification_sent: bool = False


class TimelineCreate(BaseModel):
    college_id: int
    course_id: int
    deadline: Optional[date] = None
    status: Optional[str] = None


class TimelineResponse(TimelineBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)