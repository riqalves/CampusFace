from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class Code(BaseModel):
    userID: str
    code:str
    verified: bool = False
    expirationDate: datetime 
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None



