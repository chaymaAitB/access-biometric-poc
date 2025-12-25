import requests
import random
import string
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def random_string(length=10):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def run_test():
    # 1. Register User
    email = f"user_{random_string()}@example.com"
    password = "secretpassword"
    full_name = "Test User"
    
    print(f"1. Registering user: {email}")
    try:
        resp = requests.post(f"{BASE_URL}/auth/register", json={
            "email": email,
            "password": password,
            "full_name": full_name
        })
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server. Is it running?")
        return
    
    if resp.status_code != 200:
        print(f"Registration failed: {resp.text}")
        return
    
    user_data = resp.json()
    user_id = user_data["id"]
    print(f"   User created with ID: {user_id}")
    
    # 2. Start Session
    print("\n2. Starting session...")
    fd = {"user_id": (None, str(user_id)), "duration_minutes": (None, "60"), "schedule_type": (None, "start_end")}
    resp = requests.post(f"{BASE_URL}/exam/session/start", files=fd)
    if resp.status_code != 200:
        print(f"Start session failed: {resp.text}")
        return
    session_id = resp.json()["session_id"]
    print(f"   Session started: {session_id}")

    # 3. Enroll Face & Voice
    print("\n2. Enrolling face...")
    img_url = "https://raw.githubusercontent.com/ageitgey/face_recognition/master/examples/obama.jpg"
    img_resp = requests.get(img_url, timeout=20)
    image_bytes = img_resp.content
    files = {"file": ("obama.jpg", image_bytes, "image/jpeg")}
    data = {"user_id": user_id}
    resp = requests.post(f"{BASE_URL}/enroll/face", files=files, data=data)
    
    if resp.status_code != 200:
        print(f"Enrollment failed: {resp.text}")
        return
    
    enroll_data = resp.json()
    print(f"   Enrollment success: {enroll_data}")
    
    print("\n2b. Enrolling voice...")
    voice_bytes = b"this is a simple voice blob for deterministic test"
    vfiles = {"file": ("voice.webm", voice_bytes, "audio/webm")}
    vdata = {"user_id": user_id}
    vresp = requests.post(f"{BASE_URL}/enroll/voice", files=vfiles, data=vdata)
    if vresp.status_code != 200:
        print(f"Voice enrollment failed: {vresp.text}")
        return
    print(f"   Voice enrollment success: {vresp.json()}")

    # 4. Verify Start (Face & Voice)
    print("\n3. Verifying face at start...")
    files = {"file": ("obama.jpg", image_bytes, "image/jpeg")}
    data = {"user_id": user_id, "session_id": session_id}
    resp = requests.post(f"{BASE_URL}/verify/authenticate/face/start", files=files, data=data)
    if resp.status_code != 200:
        print(f"Verification request failed: {resp.text}")
        return
    verify_data = resp.json()
    print(f"   Start Verification Result: {verify_data}")
    print("\n3b. Verifying voice at start...")
    vfiles = {"file": ("voice.webm", voice_bytes, "audio/webm")}
    vdata = {"user_id": user_id, "session_id": session_id}
    vresp = requests.post(f"{BASE_URL}/verify/authenticate/voice/start", files=vfiles, data=vdata)
    if vresp.status_code != 200:
        print(f"Voice start verification failed: {vresp.text}")
        return
    print(f"   Voice Start Verification: {vresp.json()}")

    # 5. Verify End (Face & Voice)
    print("\n4. Verifying face at end...")
    files = {"file": ("obama.jpg", image_bytes, "image/jpeg")}
    data = {"user_id": user_id, "session_id": session_id}
    resp = requests.post(f"{BASE_URL}/verify/authenticate/face/end", files=files, data=data)
    if resp.status_code != 200:
        print(f"End face verification failed: {resp.text}")
        return
    print(f"   End Face Verification: {resp.json()}")
    print("\n4b. Verifying voice at end...")
    vfiles = {"file": ("voice.webm", voice_bytes, "audio/webm")}
    vdata = {"user_id": user_id, "session_id": session_id}
    vresp = requests.post(f"{BASE_URL}/verify/authenticate/voice/end", files=vfiles, data=vdata)
    if vresp.status_code != 200:
        print(f"End voice verification failed: {vresp.text}")
        return
    print(f"   End Voice Verification: {vresp.json()}")

    # 6. Submit Session
    print("\n5. Submitting session...")
    resp = requests.post(f"{BASE_URL}/exam/session/submit", data={"user_id": user_id, "session_id": session_id})
    if resp.status_code != 200:
        print(f"Submit failed: {resp.text}")
        return
    print(f"   Submit: {resp.json()}")

    # 7. Metrics
    print("\n6. Session metrics...")
    resp = requests.get(f"{BASE_URL}/exam/metrics/session/{session_id}")
    print(f"   Metrics: {resp.json()}")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test failed with exception: {e}")
