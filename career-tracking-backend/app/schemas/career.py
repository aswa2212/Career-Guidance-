from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class CareerBase(BaseModel):
    title: str
    description: Optional[str] = None
    field: Optional[str] = None
    median_salary: Optional[str] = None
    job_outlook: Optional[str] = None
    required_skills: Optional[str] = None


class CareerCreate(CareerBase):
    pass


class CareerResponse(CareerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)