from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Request(BaseModel):
    userID: str
    hubID: str
    status: str = "pending"  # default status is 'pending'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None






