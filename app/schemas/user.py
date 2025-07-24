from pydantic import BaseModel
from typing import Optional


class UserFilters(BaseModel):
    company: Optional[str] = None
    job_title: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    hosted_events_min: Optional[int] = None
    hosted_events_max: Optional[int] = None
    attended_events_min: Optional[int] = None
    attended_events_max: Optional[int] = None


class UserBase(BaseModel):
    first_name: str
    last_name: str
    phone_numer: Optional[int] = None
    email: str
    avatar: Optional[str]
    job_title: Optional[str] = None
    company: str
    city: str
    state: str


class UserCreate(UserBase):
    pass
