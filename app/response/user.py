from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    company: Optional[str]
    job_title: Optional[str]
    city: Optional[str]
    state: Optional[str]
    hosted_events_count: int
    attended_events_count: int


class UserFilters(BaseModel):
    company: Optional[str] = None
    job_title: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    hosted_events_min: Optional[int] = None
    hosted_events_max: Optional[int] = None
    attended_events_min: Optional[int] = None
    attended_events_max: Optional[int] = None
