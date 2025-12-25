from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class ExamStatus(str, enum.Enum):
    ACTIVE = "active"
    COMPLETED = "completed"

class ScheduleType(str, enum.Enum):
    START_END = "start_end"
    INTERVAL = "interval"

class ExamSession(Base):
    __tablename__ = "exam_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    started_at = Column(String, nullable=False)
    ended_at = Column(String, nullable=True)
    duration_minutes = Column(Integer, nullable=True)
    status = Column(Enum(ExamStatus), nullable=False, default=ExamStatus.ACTIVE)
    schedule_type = Column(Enum(ScheduleType), nullable=False, default=ScheduleType.START_END)
    interval_minutes = Column(Integer, nullable=True)

    user = relationship("User", backref="exam_sessions")
