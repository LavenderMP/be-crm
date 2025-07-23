from pydantic import BaseModel
from typing import Optional


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
