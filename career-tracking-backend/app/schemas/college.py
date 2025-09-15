from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


class CollegeBase(BaseModel):
    name: str
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    pincode: Optional[str] = None
    website: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class CollegeCreate(CollegeBase):
    pass


class CollegeResponse(CollegeBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)