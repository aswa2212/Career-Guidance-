from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    interests: Optional[List[str]] = None

class UserInDB(UserBase):
    id: int
    is_active: bool = True
    role: str = "user"
    created_at: datetime
    updated_at: datetime
    interests: Optional[List[str]] = None

    model_config = ConfigDict(from_attributes=True)

class UserResponse(UserInDB):
    pass

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserInterestsUpdate(BaseModel):
    interests: List[str]