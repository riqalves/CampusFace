from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Request(BaseModel):
    userID: str
    hubID: str
    userRole: Optional[str] = None  # default role is None, can be set later
    status: str = "pending"  # default status is 'pending'
    approved_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None






