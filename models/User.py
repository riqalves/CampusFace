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
    name: str
    username: str
    email: EmailStr
    password: str
    birthDate: Optional[datetime]
    cpf: str
    role: str
    disabled: bool | None = None
    imagePath: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

