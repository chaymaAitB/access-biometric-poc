from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.v1.endpoints import auth, enrollment, verification, exam
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware

# Create tables (for dev only - use Alembic in prod)
if settings.DEBUG:
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Configuration
origins = ["*"] if settings.DEBUG else [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(enrollment.router, prefix=f"{settings.API_V1_STR}/enroll", tags=["enrollment"])
app.include_router(verification.router, prefix=f"{settings.API_V1_STR}/verify", tags=["verification"])
app.include_router(exam.router, prefix=f"{settings.API_V1_STR}/exam", tags=["exam"])

@app.get("/")
def read_root():
    return FileResponse("static/index.html")
