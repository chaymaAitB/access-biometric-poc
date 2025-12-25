# Multimodal Biometric Access API

## 📌 Project Overview
This project is a **Secure Backend API** designed to control access to online exams using **Multimodal Biometrics** (Face, Voice, Fingerprint). It ensures that the examinee is the legitimate candidate through rigorous enrollment, authentication, and continuous verification processes.

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

### Project Structure
```
access-biometric-poc/
├── app/
│   ├── api/            # API Route handlers (v1)
│   ├── core/           # Config & Security settings
│   ├── db/             # Database connection & sessions
│   ├── models/         # SQLAlchemy Database Models
│   ├── schemas/        # Pydantic Data Schemas
│   ├── services/       # Business Logic (Biometric extraction)
│   └── main.py         # Application Entry Point
├── django_poc/         # Legacy Django Proof of Concept (Archived)
├── requirements.txt    # Project Dependencies
└── .env                # Environment Variables (Secrets)
```

---

## 🚀 Installation & Setup

### 1. Prerequisites
- Python 3.10 or higher
- Virtualenv
- Node.js 18+ (for frontend)

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create a `.env` file in the root directory:
```ini
PROJECT_NAME="Multimodal Biometric Access"
API_V1_STR="/api/v1"
SECRET_KEY="your_super_secret_jwt_key"
ENCRYPTION_KEY="your_fernet_key"  # Generate using cryptography.fernet.Fernet.generate_key()
DEBUG=True
DATABASE_URL="sqlite:///./sql_app.db"
```

### 5. Run the Server
```bash
uvicorn app.main:app --reload
```

The API will be available at:
- Root: http://127.0.0.1:8000/
- Docs (Swagger UI): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### 6. Frontend (React)
```bash
cd frontend
npm install
npm run dev
```
Dev server runs on `http://localhost:5173/` and proxies API calls to `http://127.0.0.1:8001`.

If you prefer preview with a built bundle:
```bash
npm run build
npm run preview
```
Preview runs on `http://localhost:4173/`. It uses `frontend/.env` (`VITE_API_BASE=http://127.0.0.1:8001/api/v1`) to reach the backend.

---

## 🔑 Key Features (In Progress)
- User Management: Registration & Login.
- Biometric Enrollment:
  - `/api/v1/enroll/face`
  - `/api/v1/enroll/voice`
- Verification:
  - Start of exam:
    - `/api/v1/verify/authenticate/face/start`
    - `/api/v1/verify/authenticate/voice/start`
  - End of exam:
    - `/api/v1/verify/authenticate/face/end`
    - `/api/v1/verify/authenticate/voice/end`
  - Identification:
    - `/api/v1/verify/identify/face`

Frontend routes:
- `/verify-start`: Login and biometric start verification (camera/mic capture)
- `/exam-session`: Guarded exam interface
- `/verify-end`: Final biometric verification and submission

---

## 🧪 Testing

To run the end-to-end test workflow (Register -> Enroll -> Verify), ensure the server is running and then execute:

```bash
# 1. Start the server (if not running)
uvicorn app.main:app --reload --port 8001

# 2. Run the test script (in a separate terminal)
python test_workflow.py
```

This script will:
1.  Register a new user with a random email.
2.  Enroll a face image.
3.  Verify a face image against the stored biometric data.
4.  Output "MATCH CONFIRMED" in Mock Mode when using the same filename prefix.

### Web Test Console
- Open `http://127.0.0.1:8001/` to use a simple UI for testing.
- Step 1 registers a user; Steps 2–3 enroll and verify a face image.
- The UI calls API endpoints under `/api/v1/...`.

### Mock Mode (no face_recognition)
- If `face_recognition` is not installed, the system runs in Mock Mode.
- Mock descriptors are deterministic based on the file name prefix.
- To produce a match: use two images starting with the same prefix, e.g. `user1_photo.jpg` and `user1_selfie.jpg`.
- To produce a non-match: use different prefixes, e.g. `userA_1.jpg` vs `userB_1.jpg`.
- Responses include `"mock_used": true` indicating Mock Mode is active.

### Expected Results in Mock Mode
- Enroll returns: `{"message":"Face enrolled successfully", "biometric_id": <id>, "mock_used": true}`.
- Verify returns: `{"match": true, "score": 0.0, "threshold": 0.6, "mock_used": true}` when prefixes match.
- Verify returns: `{"match": false, "score": <number>, "threshold": 0.6, "mock_used": true}` when prefixes differ.

### Enable Real Face Recognition (Windows)
- Option A (dlib/face_recognition):
  - Install CMake and Visual Studio Build Tools (C++), add CMake to PATH.
  - `pip install dlib==19.24.2`
  - `pip install face_recognition`
  - Restart the server; responses show `"mock_used": false` and metric `"euclidean"`.
- Option B (InsightFace/ONNX, recommended on Windows):
  - `pip install opencv-python onnxruntime insightface==0.7.3`
  - First run downloads model files automatically.
  - Restart the server; responses show `"mock_used": false` and metric `"cosine"`.

### Real Matching Behavior
- When using `face_recognition` (128-d embeddings), matching uses Euclidean distance with threshold `0.6`.
- When using `insightface` (512-d embeddings), matching uses Cosine similarity with threshold `0.3`.
- API responses include:
  - `"metric"`: `"euclidean"` or `"cosine"`
  - `"mock_used"`: `false` when real embeddings are used

### Performance Metrics
- Verification attempts are logged per session (`verification_events`) for FRR/FAR analysis.
- Session FRR endpoint:
  - `GET /api/v1/exam/metrics/session/{session_id}`
- FAR requires enrolled impostor datasets; extend metrics endpoints as needed.

## 📂 Legacy
The original Django POC has been moved to the `django_poc/` folder for reference.
