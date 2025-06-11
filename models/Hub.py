from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from models.User import User

class Hub(BaseModel):
    hubAdmin: str
    name: str
    employees: List[Optional[str]] = None
    clients: List[Optional[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# Padrão de retorno da classe hub
class HubOut(BaseModel):
    hubAdmin: str
    id: str
    name: str
    employees: List[Optional[User]]
    clients: List[Optional[User]]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True



