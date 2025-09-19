from sqlalchemy import Column, String, Integer, Boolean, DateTime, func, JSON
from sqlalchemy.orm import relationship
import enum

from .base import BaseModel

class RoleEnum(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(BaseModel):
    __tablename__ = "users"
    
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user", nullable=False)
    last_login = Column(DateTime, nullable=True)
    interests = Column(JSON, nullable=True, default=list)
    
    # Relationships
    # aptitude_results = relationship("AptitudeTest", back_populates="user")
    # timelines = relationship("Timeline", back_populates="user")