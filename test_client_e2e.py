from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def run():
    email = f"user_{int(time.time())}@example.com"
    password = "secretpassword"
    r = client.post("/api/v1/auth/register", json={"email": email, "password": password, "full_name": "User"})
    assert r.status_code == 200, r.text
    user_id = r.json()["id"]
    fd = {"user_id": (None, str(user_id)), "duration_minutes": (None, "60"), "schedule_type": (None, "start_end")}
    r = client.post("/api/v1/exam/session/start", files=fd)
    assert r.status_code == 200, r.text
    session_id = r.json()["session_id"]
    image_bytes = b"\xff\xd8\xff\xdb" + b"0" * 2048
    files = {"file": ("user1_selfie.jpg", image_bytes, "image/jpeg")}
    r = client.post("/api/v1/enroll/face", files=files, data={"user_id": str(user_id)})
    assert r.status_code == 200, r.text
    audio_bytes = b"VOICE" * 1024
    vfiles = {"file": ("voice.webm", audio_bytes, "audio/webm")}
    r = client.post("/api/v1/enroll/voice", files=vfiles, data={"user_id": str(user_id)})
    assert r.status_code == 200, r.text
    files = {"file": ("user1_snapshot.jpg", image_bytes, "image/jpeg")}
    r = client.post("/api/v1/verify/authenticate/face/start", files=files, data={"user_id": str(user_id), "session_id": str(session_id)})
    assert r.status_code == 200, r.text
    face_start = r.json()
    vfiles = {"file": ("voice_capture.webm", audio_bytes, "audio/webm")}
    r = client.post("/api/v1/verify/authenticate/voice/start", files=vfiles, data={"user_id": str(user_id), "session_id": str(session_id)})
    assert r.status_code == 200, r.text
    voice_start = r.json()
    files = {"file": ("user1_snapshot2.jpg", image_bytes, "image/jpeg")}
    r = client.post("/api/v1/verify/authenticate/face/end", files=files, data={"user_id": str(user_id), "session_id": str(session_id)})
    assert r.status_code == 200, r.text
    face_end = r.json()
    vfiles = {"file": ("voice_capture2.webm", audio_bytes, "audio/webm")}
    r = client.post("/api/v1/verify/authenticate/voice/end", files=vfiles, data={"user_id": str(user_id), "session_id": str(session_id)})
    assert r.status_code == 200, r.text
    voice_end = r.json()
    fd = {"user_id": (None, str(user_id)), "session_id": (None, str(session_id))}
    r = client.post("/api/v1/exam/session/submit", files=fd)
    assert r.status_code == 200, r.text
    r = client.get(f"/api/v1/exam/metrics/session/{session_id}")
    assert r.status_code == 200, r.text
    metrics = r.json()
    print("RESULTS")
    print("face_start:", face_start)
    print("voice_start:", voice_start)
    print("face_end:", face_end)
    print("voice_end:", voice_end)
    print("metrics:", metrics)

if __name__ == "__main__":
    run()
