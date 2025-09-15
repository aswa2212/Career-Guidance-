from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .base import BaseModel


class Timeline(BaseModel):
    __tablename__ = "timelines"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    college_id = Column(Integer, ForeignKey("colleges.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    deadline = Column(Date)
    status = Column(String(50))  # e.g., "applied", "accepted", "rejected"
    notification_sent = Column(Boolean, default=False)

    # user = relationship("User", back_populates="timelines")
    # college = relationship("College")
    # course = relationship("Course")