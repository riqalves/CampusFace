from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Card(BaseModel):
    
    userID: str
    expirationDate: datetime 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class User(BaseModel):
    username: str
    email: EmailStr
    password: str
    birthDate: Optional[datetime]
    cpf: str
    roles: Optional[List[str]]
    disabled: bool | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

