from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UpdateUserCredentials(BaseModel):
    email: EmailStr
    password: str
    updated_at: Optional[datetime] = None

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str
    disabled: bool | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class ResetCode(BaseModel):
    email: EmailStr
    reset_code: str
    status: bool
    expired_in: Optional[datetime] = None