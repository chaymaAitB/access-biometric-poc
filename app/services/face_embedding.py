import cv2
import numpy as np
import os

def _detect_face(image_bgr):
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
    cascade_url = "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml"
    cascade_path = os.path.join(os.path.dirname(__file__), "haarcascade_frontalface_default.xml")
    if not os.path.exists(cascade_path):
        try:
            import requests
            r = requests.get(cascade_url, timeout=10)
            if r.ok:
                with open(cascade_path, "wb") as f:
                    f.write(r.content)
        except Exception:
            pass
    face_cascade = cv2.CascadeClassifier(cascade_path) if os.path.exists(cascade_path) else cv2.CascadeClassifier()
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    if len(faces) == 0:
        return image_bgr
    x, y, w, h = max(faces, key=lambda b: b[2] * b[3])
    return image_bgr[y:y+h, x:x+w]

def compute_embedding(image_bytes: bytes) -> list[float]:
    img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        return None
    face = _detect_face(img)
    face_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face_gray = cv2.resize(face_gray, (224, 224), interpolation=cv2.INTER_AREA)
    orb = cv2.ORB_create(nfeatures=1024, scaleFactor=1.2, nlevels=8)
    keypoints, descriptors = orb.detectAndCompute(face_gray, None)
    vec = np.zeros((512,), dtype=np.float32)
    if descriptors is not None and descriptors.size > 0:
        flat = descriptors.flatten().astype(np.float32)
        if flat.size >= 512:
            vec[:] = flat[:512]
        else:
            vec[:flat.size] = flat
    else:
        vec[:] = face_gray.flatten().astype(np.float32)[:512]
    norm = np.linalg.norm(vec)
    if norm > 1e-6:
        vec = vec / norm
    return vec.tolist()
