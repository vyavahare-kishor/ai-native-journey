from pydantic import BaseModel
from typing import Optional
import uuid


class UserCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None


class UserResponse(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    age: Optional[int] = None

    class Config:
        from_attributes = True  # like Rails' as_json


class UserUpdate(BaseModel):
    name: Optional[str] = None   # all fields optional for PATCH
    email: Optional[str] = None
    age: Optional[int] = None
