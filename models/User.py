from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from models.Badge import Badge

class User (BaseModel):
    name: str
    email: EmailStr
    password: str
    birthDate: datetime
    imagePath: Optional[str] = None
    created_at: Optional[datetime] = None

class UserLogin(BaseModel):
    username: EmailStr
    password: str

    bio: Optional[str] = None


class UpdateUserCredentials(BaseModel):
    email: EmailStr
    password: str



# Esqueci a senha
class ForgotPassword(BaseModel):
    email: EmailStr

class ResetCode(BaseModel):
    email: EmailStr
    reset_code: str
    status: bool
    expired_in: Optional[datetime] = None