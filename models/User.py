from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRegister (BaseModel):
    name: str
    email: EmailStr
    password: str
    birthDate: datetime
    imagePath: Optional[str] = None
    created_at: Optional[datetime] = None

class UserLogin(BaseModel):
    username: EmailStr
    password: str

class UpdateUserCredentials(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    created_at: Optional[datetime] = None
    disabled: bool | None = None

# Esqueci a senha
class ForgotPassword(BaseModel):
    email: EmailStr

class ResetCode(BaseModel):
    email: EmailStr
    reset_code: str
    status: bool
    expired_in: Optional[datetime] = None