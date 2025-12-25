import { useRef, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { useExamSession } from "../context/ExamSessionContext";
import { api } from "../lib/api";
import { useNavigate } from "react-router-dom";

export default function VerifyStartPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [faceBlob, setFaceBlob] = useState<Blob | null>(null);
  const [voiceBlob, setVoiceBlob] = useState<Blob | null>(null);
  const [busy, setBusy] = useState(false);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const [recording, setRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);
  const { setAuthenticated, authenticatedUserId } = useAuth();
  const { setSessionId, setStartVerified, sessionId } = useExamSession();
  const navigate = useNavigate();

  async function onLogin() {
    setBusy(true);
    const userId = await api.loginOrRegister(email, password);
    setAuthenticated(userId);
    const sessionId = await api.startSession(userId, 60, "start_end");
    setSessionId(sessionId);
    setBusy(false);
  }

  async function onVerifyStart() {
    if (!authenticatedUserId || !faceBlob || !voiceBlob) return;
    setBusy(true);
    const faceOk = await api.verifyFaceStart(authenticatedUserId, sessionId as number, faceBlob);
    const voiceOk = await api.verifyVoiceStart(authenticatedUserId, sessionId as number, voiceBlob);
    const ok = faceOk && voiceOk;
    if (ok) {
      setStartVerified(true);
      navigate("/exam-session");
    }
    setBusy(false);
  }

  async function startCamera() {
    const s = await navigator.mediaDevices.getUserMedia({ video: true });
    setStream(s);
    if (videoRef.current) {
      (videoRef.current as any).srcObject = s;
      (videoRef.current as any).play();
    }
  }
  function stopCamera() {
    stream?.getTracks().forEach(t => t.stop());
    setStream(null);
  }
  async function takeSnapshot() {
    if (!videoRef.current) return;
    const video = videoRef.current;
    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;
    ctx.drawImage(video, 0, 0);
    const blob: Blob = await new Promise(resolve => canvas.toBlob(b => resolve(b as Blob), "image/jpeg"));
    setFaceBlob(blob);
  }
  async function startRecording() {
    const s = await navigator.mediaDevices.getUserMedia({ audio: true });
    const rec = new MediaRecorder(s);
    mediaRecorderRef.current = rec;
    audioChunksRef.current.length = 0;
    rec.ondataavailable = e => audioChunksRef.current.push(e.data);
    rec.onstop = () => {
      const blob = new Blob(audioChunksRef.current, { type: "audio/webm" });
      setVoiceBlob(blob);
      s.getTracks().forEach(t => t.stop());
    };
    rec.start();
    setRecording(true);
  }
  function stopRecording() {
    mediaRecorderRef.current?.stop();
    setRecording(false);
  }
  return (
    <div className="container">
      <div className="title">Pre‑Flight Check</div>
      <div className="subtitle">Login and capture Face and Voice to begin the exam.</div>
      <div className="grid">
        <div className="card">
          <div className="section-title">Login</div>
          <div className="row">
            <input className="input" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          </div>
          <div className="row">
            <input className="input" placeholder="Password" value={password} type="password" onChange={e => setPassword(e.target.value)} />
          </div>
          <div className="actions">
            <button className="btn btn-primary" disabled={busy} onClick={onLogin}>Login</button>
          </div>
          <div className="helper">Use a valid email. Account will be created if it does not exist.</div>
        </div>
        <div className="card">
          <div className="section-title">Capture Biometrics</div>
          <video className="video" ref={videoRef} />
          <div className="actions">
            <button className="btn btn-secondary" onClick={startCamera}>Open Camera</button>
            <button className="btn btn-secondary" onClick={takeSnapshot}>Take Snapshot</button>
            <button className="btn btn-secondary" onClick={stopCamera}>Close Camera</button>
          </div>
          <div className="spacer"></div>
          <input className="file" type="file" accept="image/*" onChange={e => setFaceBlob(e.target.files?.[0] ?? null)} />
          <div className="spacer"></div>
          <div className="actions">
            {!recording ? (
              <button className="btn btn-secondary" onClick={startRecording}>Record Voice</button>
            ) : (
              <button className="btn btn-secondary" onClick={stopRecording}>Stop Recording</button>
            )}
          </div>
          <div className="spacer"></div>
          <input className="file" type="file" accept="audio/*" onChange={e => setVoiceBlob(e.target.files?.[0] ?? null)} />
          <div className="spacer"></div>
          <div className="actions">
            <button className="btn btn-primary" disabled={busy} onClick={onVerifyStart}>Verify Start</button>
          </div>
          <div className="helper">You must pass both checks to enter the exam.</div>
        </div>
      </div>
    </div>
  );
}
