from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from app.core.database import Base

class EmailCampaign(Base):
    __tablename__ = "email_campaigns"

    id = Column(Integer, primary_key=True)
    filters = Column(JSONB)  # Store filter criteria
    subject = Column(String(200))
    body = Column(String(5000))
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, server_default="now()")
    sent_count = Column(Integer, default=0)
    total_recipients = Column(Integer, default=0)
