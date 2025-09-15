from sqlalchemy import Column, Integer, String, Text, Float
from .base import BaseModel


class College(BaseModel):
    __tablename__ = "colleges"

    name = Column(String(200), nullable=False)
    address = Column(String(500))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    website = Column(String(200))
    latitude = Column(Float)  # for nearby search
    longitude = Column(Float)  # for nearby search