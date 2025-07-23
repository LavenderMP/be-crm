from pydantic import BaseModel
from response.user import UserFilters


class EmailRequest(BaseModel):
    filters: UserFilters
    subject: str
    body: str


class EmailResponse(BaseModel):
    campaign_id: int
    status: str
    message: str
