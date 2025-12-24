import requests
import random
import string
import time

BASE_URL = "http://127.0.0.1:8001/api/v1"

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
    
    # 2. Enroll Face
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
    
    # 3. Verify Face
    print("\n3. Verifying face...")
    files = {"file": ("obama.jpg", image_bytes, "image/jpeg")}
    data = {"user_id": user_id}
    resp = requests.post(f"{BASE_URL}/verify/authenticate/face", files=files, data=data)
        
    if resp.status_code != 200:
        print(f"Verification request failed: {resp.text}")
        return
        
    verify_data = resp.json()
    print(f"   Verification Result: {verify_data}")
    
    if verify_data["match"]:
        print("   -> MATCH CONFIRMED")
    else:
        print("   -> NO MATCH (Expected if using random Mock)")

if __name__ == "__main__":
    try:
        run_test()
    except Exception as e:
        print(f"Test failed with exception: {e}")
