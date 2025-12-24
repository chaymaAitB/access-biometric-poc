from sqlalchemy import Column, Integer, String, ForeignKey, LargeBinary, Enum
from sqlalchemy.orm import relationship
from app.db.base import Base
import enum

class BiometricType(str, enum.Enum):
    FACE = "face"
    VOICE = "voice"
    FINGERPRINT = "fingerprint"

class BiometricData(Base):
    __tablename__ = "biometric_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    modality = Column(Enum(BiometricType), nullable=False)
    
    # Encrypted descriptor data
    encrypted_descriptor = Column(LargeBinary, nullable=False)
    
    # Metadata for better traceability
    created_at = Column(String, nullable=False) # Store ISO timestamp
    device_info = Column(String, nullable=True)

    user = relationship("User", backref="biometrics")
