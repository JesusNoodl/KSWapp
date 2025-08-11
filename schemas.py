# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class BeltBase(BaseModel):
    name: str
    is_stripe: bool
    korean_name: str
    primary_colour: str

class BeltCreate(BeltBase):
    pass

class BeltOut(BeltBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
