from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .base import BaseModel


class Course(BaseModel):
    __tablename__ = "courses"

    title = Column(String(200), nullable=False)
    description = Column(Text)
    duration = Column(String(50))  # e.g., "6 months"
    provider = Column(String(100))  # e.g., "Coursera", "edX"
    category = Column(String(100))  # e.g., "Programming", "Data Science"
    difficulty_level = Column(String(20))  # e.g., "Beginner", "Intermediate", "Advanced"

    # careers = relationship("Career", secondary="course_career", back_populates="courses")


class CourseCareer(BaseModel):
    __tablename__ = "course_career"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    career_id = Column(Integer, ForeignKey("careers.id"), primary_key=True)