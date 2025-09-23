
from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    has_google_calendar: Optional[bool] = False

class AuthResponse(BaseModel):
    status: str
    message: str
    user: Optional[UserResponse] = None