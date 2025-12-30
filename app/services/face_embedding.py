import cv2
import numpy as np
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HAS_DEEPFACE = False
try:
    from deepface import DeepFace
    HAS_DEEPFACE = True
except ImportError:
    pass

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
    """
    Computes a face embedding.
    Priority:
    1. DeepFace (VGG-Face) - High Accuracy
    2. OpenCV ORB - Low Accuracy (Fallback)
    """
    # Decode image
    img_array = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        return None

    # Try DeepFace
    if HAS_DEEPFACE:
        try:
            # DeepFace expects path or numpy array (BGR is fine for opencv backend, but DeepFace usually prefers RGB)
            # DeepFace.represent returns a list of dicts
            # enforce_detection=False allows it to process the image even if it can't find a clear face (it uses the whole img)
            # but for security we might want enforce_detection=True. 
            # However, _detect_face above is a Haar cascade which is fast. 
            # Let's let DeepFace handle detection if possible, or skip it.
            
            # Convert BGR to RGB for DeepFace
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            embeddings = DeepFace.represent(
                img_path=img_rgb,
                model_name="VGG-Face",
                enforce_detection=False,
                detector_backend="opencv"
            )
            
            if embeddings and len(embeddings) > 0:
                # Return the first face's embedding
                return embeddings[0]["embedding"]
        except Exception as e:
            logger.warning(f"DeepFace failed: {e}")
            pass

    # Fallback: ORB (Legacy/POC method)
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
