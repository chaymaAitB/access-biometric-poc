import numpy as np
import io
import soundfile as sf
import librosa

def compute_embedding(audio_bytes: bytes) -> list[float] | None:
    if not audio_bytes:
        return None
    try:
        data, sr = sf.read(io.BytesIO(audio_bytes), dtype="float32", always_2d=False)
    except Exception:
        return None
    if data is None:
        return None
    if np.ndim(data) > 1:
        data = np.mean(data, axis=1).astype(np.float32)
    target_sr = 16000
    try:
        y = librosa.resample(data, orig_sr=sr, target_sr=target_sr)
    except Exception:
        y = data
        target_sr = sr
    try:
        mfcc = librosa.feature.mfcc(y=y, sr=target_sr, n_mfcc=40)
        d1 = librosa.feature.delta(mfcc)
        d2 = librosa.feature.delta(mfcc, order=2)
        v1 = np.mean(mfcc, axis=1)
        v2 = np.mean(d1, axis=1)
        v3 = np.mean(d2, axis=1)
        vec = np.concatenate([v1, v2, v3]).astype(np.float32)
    except Exception:
        return None
    norm = float(np.linalg.norm(vec))
    if norm > 1e-8:
        vec = vec / norm
    return vec.tolist()
