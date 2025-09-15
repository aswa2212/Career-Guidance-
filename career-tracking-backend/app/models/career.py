from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from .base import BaseModel


class Career(BaseModel):
    __tablename__ = "careers"

    title = Column(String(200), nullable=False)
    description = Column(Text)
    field = Column(String(100))  # e.g., "Technology", "Healthcare"
    median_salary = Column(String(50))  # e.g., "$70,000"
    job_outlook = Column(String(50))  # e.g., "Growing"
    required_skills = Column(Text)  # JSON string of required skills

    # courses = relationship("Course", secondary="course_career", back_populates="careers")