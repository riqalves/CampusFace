from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Hub(BaseModel):
    name: str
    employees: List[Optional[str]] = None
    clients: List[Optional[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

