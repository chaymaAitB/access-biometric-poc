from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.base import Base
from app.models.biometric_data import BiometricType
import enum

class VerificationPhase(str, enum.Enum):
    START = "start"
    END = "end"
    RANDOM = "random"

class VerificationEvent(Base):
    __tablename__ = "verification_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("exam_sessions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    modality = Column(Enum(BiometricType), nullable=False)
    phase = Column(Enum(VerificationPhase), nullable=False)
    match = Column(Boolean, nullable=False)
    score = Column(Float, nullable=False)
    threshold = Column(Float, nullable=False)
    metric = Column(String, nullable=False)
    mock_used = Column(Boolean, nullable=False)
    created_at = Column(String, nullable=False)

    session = relationship("ExamSession", backref="verification_events")
    user = relationship("User", backref="verification_events")
