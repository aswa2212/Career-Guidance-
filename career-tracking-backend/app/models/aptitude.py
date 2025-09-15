from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class AptitudeTest(BaseModel):
    __tablename__ = "aptitude_tests"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    test_name = Column(String(100), nullable=False)
    scores = Column(String(1000))  # JSON string of scores per category
    overall_score = Column(Float)

    # user = relationship("User", back_populates="aptitude_tests")