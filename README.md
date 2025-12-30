# Multimodal Biometric Access API

## 📌 Project Overview
This project is a **Secure Backend API** designed to control access to online exams using **Multimodal Biometrics** (Face and Voice). It ensures that the examinee is the legitimate candidate through rigorous enrollment, authentication, and continuous verification processes.

The system is built with **Privacy by Design** principles:
*   **No raw biometric data storage**: Only encrypted descriptors are stored.
*   **Encryption at rest**: Sensitive data is encrypted using high-standard cryptography.
*   **Traceability**: Comprehensive logging of all access attempts.

---

## 🏗️ Technical Architecture

### Stack
*   **Language**: Python 3.10+
*   **Framework**: FastAPI (High-performance, async support)
*   **Database**: SQLite (Dev) / PostgreSQL (Prod)
*   **ORM**: SQLAlchemy
*   **Security**: Python-Jose (JWT), Passlib (Hashing), Cryptography (Fernet)
*   **Containerization**: Docker

### Project Structure
```
access-biometric-poc/
├── app/
├── api/            # API Route handlers (v1)
│   ├── core/           # Config & Security settings
│   ├── db/             # Database connection & sessions
│   ├── models/         # SQLAlchemy Database Models
│   ├── schemas/        # Pydantic Data Schemas
│   ├── services/       # Business Logic (Biometric extraction)
│   └── main.py         # Application Entry Point
├── static/             # Frontend Static Files
├── tests/              # Test Suite
├── Dockerfile          # Docker Build
├── docker-compose.yml  # Docker Compose Config
├── requirements.txt    # Project Dependencies
└── .env                # Environment Variables (Secrets)
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10+ OR Docker

### 2. Local Setup (No Docker)

**Setup Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

**Install Dependencies**
```bash
pip install -r requirements.txt
```

**Run Server**
```bash
uvicorn app.main:app --reload
```

### 3. Docker Setup (Recommended)

**Build and Run**
```bash
docker-compose up --build
```

The API will be available at `http://127.0.0.1:8000`.

### 4. Configuration
Create a `.env` file (see `.env.example` or below):
```ini
PROJECT_NAME="Multimodal Biometric Access"
API_V1_STR="/api/v1"
SECRET_KEY="your_super_secret_jwt_key"
ENCRYPTION_KEY="your_fernet_key"
DEBUG=True
DATABASE_URL="sqlite:///./sql_app.db"
# Thresholds
FACE_EUCLIDEAN_THRESHOLD=0.6
FACE_COSINE_THRESHOLD=0.3
LIVENESS_MOTION_THRESHOLD=5.0
```

---

## 🧪 Testing

Run the test suite with:
```bash
pytest
```

## 🧹 Code Quality

Linting and formatting:
```bash
ruff check .
```

## 🖥️ Usage

1.  Open `http://127.0.0.1:8000/` in your browser.
2.  **Register** a new user.
3.  **Enroll** Face and Voice.
4.  **Start Session** (Pass Liveness Check).
5.  **Verify** identity periodically.
