# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime, time, date
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

class PromotionBase(BaseModel):
    promotion_date : datetime
    student_id: int
    location_id: int
    belt_id: int
    tabs: int

    model_config = ConfigDict(from_attributes=True)

class PromotionOut(PromotionBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class StandardPromotionRequest(BaseModel):
    person_id: int
    location_id: int
    promotion_date: Optional[datetime]

class SetPromotionRequest(StandardPromotionRequest):
    belt_id: int
    tabs: int

class PersonBase(BaseModel):
    first_name: str
    last_name: str
    dob: datetime
    age_category_id: int

class PersonCreate(PersonBase):
    pass

class PersonOut(PersonBase):
    id: int
    created_at: datetime
    active: bool
    role_id: int
    belt_level_id: int

    model_config = ConfigDict(from_attributes=True)

class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    age_category_id: Optional[int] =None
    role_id: Optional[int] = None
    active: Optional[bool] = None
    student_id: Optional[str] = None
    black_belt_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ClassBase(BaseModel):
    title: str
    description: Optional[str]
    day: str
    start_time: time
    end_time: time
    location_id: int
    instructor_id: int

class ClassCreate(ClassBase):
    age_categories: list[int]

class ClassOut(ClassBase):
    id:int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AgeCategoryBase(BaseModel):
    cat_name: str

class AgeCategoryCreate(AgeCategoryBase):
    pass

class AgeCategoryOut(AgeCategoryBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
