# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime, time, date
from typing import Optional

class BeltBase(BaseModel):
    name: str
    is_stripe: bool
    korean_name: str
    primary_colour: str
    hangul: Optional[str] = None
    belt_abbreviation: Optional[str] = None

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
    belt_name: Optional[str] = None

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
    student_id: Optional[str] = None
    black_belt_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class PersonUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    dob: Optional[datetime] = None
    age_category_id: Optional[int] =None
    role_id: Optional[int] = None
    active: Optional[bool] = None
    student_id: Optional[str] = None
    black_belt_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ClassBase(BaseModel):
    title: str
    description: Optional[str]
    day_number: int
    start_time: time
    end_time: time
    location_id: int
    instructor_id: int
    active_from: Optional[time] = None
    active_to: Optional[time] = None

class ClassCreate(ClassBase):
    age_categories: list[int]

class ClassOut(ClassBase):
    id:int
    day: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ClassUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    day: Optional[str] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    location_id: Optional[int] = None
    instructor_id: Optional[int] = None
    age_categories: Optional[list[int]] = None

class AgeCategoryBase(BaseModel):
    cat_name: str

class AgeCategoryCreate(AgeCategoryBase):
    pass

class AgeCategoryOut(AgeCategoryBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class RoleBase(BaseModel):
    name: str

class RoleCreate(RoleBase):
    pass

class RoleOut(RoleBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class LocationBase(BaseModel):
    title: str
    is_dojang: bool
    instructor_id: Optional[int]
    address_id: Optional[int]


class LocationCreate(LocationBase):
    pass

class LocationOut(LocationBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class EventBase(BaseModel):
    title: str
    description: Optional[str]
    event_start: datetime
    event_end: datetime
    location_id: Optional[int]
    event_type_id: int

class EventCreate(EventBase):
    age_categories: list[int]

class EventUpdate(EventBase):
    age_categories: Optional[list[int]] = None

class EventOut(EventBase):
    id: int
    created_at: datetime
    modified_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)

class FullCalendarOut(BaseModel):
    date: date
    class_id: Optional[int] = None
    class_name: str
    start_time: time
    end_time: time
    instructor_id: Optional[int] = None
    description: str
    event_id: Optional[int] = None
    event_type: Optional[str] = None
    location_id: Optional[int] = None
    location_name: Optional[str] = None
    is_dojang: Optional[bool] = None
    day_name: Optional[str] = None
    day_of_week: Optional[int] = None # 0 is Sunday, 1 is Monday, etc.
    calendar_type: str  # "class" or "event"
    instructor_name: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ClassExceptionOut(BaseModel):
    id: int
    class_id: int
    date: date
    cancelled: bool
    note: Optional[str] = None
    created_at: Optional[datetime] = None
    modified_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)