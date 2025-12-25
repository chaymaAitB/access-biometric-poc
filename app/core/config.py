import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Multimodal Biometric Access"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./sql_app.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "changethis_secret_key_for_jwt")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ENCRYPTION_KEY: str = os.getenv("ENCRYPTION_KEY", "please_change_this_encryption_key_32_bytes_len")
    DEBUG: bool = False
    FACE_EUCLIDEAN_THRESHOLD: float = float(os.getenv("FACE_EUCLIDEAN_THRESHOLD", "0.6"))
    FACE_COSINE_THRESHOLD: float = float(os.getenv("FACE_COSINE_THRESHOLD", "0.3"))
    VOICE_EUCLIDEAN_THRESHOLD: float = float(os.getenv("VOICE_EUCLIDEAN_THRESHOLD", "0.6"))
    VOICE_COSINE_THRESHOLD: float = float(os.getenv("VOICE_COSINE_THRESHOLD", "0.3"))
    LIVENESS_MOTION_THRESHOLD: float = float(os.getenv("LIVENESS_MOTION_THRESHOLD", "5.0"))

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
