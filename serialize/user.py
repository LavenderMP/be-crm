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
