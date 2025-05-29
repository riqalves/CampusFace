from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Request(BaseModel):
    userID: str
    hubID: str
    isAccepted: bool | None = None
    isDenied: bool | None = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None






