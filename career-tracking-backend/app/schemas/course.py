from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CourseBase(BaseModel):
    title: str
    description: Optional[str] = None
    duration: Optional[str] = None
    provider: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[str] = None
    provider: Optional[str] = None
    category: Optional[str] = None
    difficulty_level: Optional[str] = None


class CourseResponse(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)