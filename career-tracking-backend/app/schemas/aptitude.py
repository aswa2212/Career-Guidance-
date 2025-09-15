from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from datetime import datetime


class AptitudeResultBase(BaseModel):
    test_name: str
    scores: Dict[str, Any]  # JSON object for scores
    overall_score: Optional[float] = None


class AptitudeResultCreate(AptitudeResultBase):
    pass


class AptitudeResultResponse(AptitudeResultBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)