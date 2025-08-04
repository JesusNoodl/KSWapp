from pydantic import BaseModel
from typing import Optional
import datetime

class BeltCreate(BaseModel):
    name: str
    is_stripe: bool
    korean_name: str
    primary_colour: str
    created_at: Optional[datetime.datetime] = None
    modified_at: Optional[datetime.datetime] = None

class BeltResponse(BeltCreate):
    id: int

    class Config:
        orm_mode = True
