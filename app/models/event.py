from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from core.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(String(1000))
    start_at = Column(DateTime, nullable=False)
    end_at = Column(DateTime, nullable=False)
    venue = Column(String(200))
    max_capacity = Column(Integer)

    # Relationships
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="hosted_events")
    hosts = relationship("EventHost", back_populates="event")
    attendees = relationship("EventAttendance", back_populates="event")


class EventHost(Base):
    __tablename__ = "event_hosts"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    event = relationship("Event", back_populates="hosts")
    user = relationship("User")


class EventAttendance(Base):
    __tablename__ = "event_attendances"

    id = Column(Integer, primary_key=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    attended = Column(Boolean, default=False)

    event = relationship("Event", back_populates="attendees")
    user = relationship("User", back_populates="event_attendances")
