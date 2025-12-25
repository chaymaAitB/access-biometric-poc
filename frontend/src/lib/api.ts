async function json(r: Response) {
  const j = await r.json();
  return j;
}

const BASE = (import.meta as any).env?.VITE_API_BASE ?? "/api/v1";
export const api = {
  async loginOrRegister(email: string, password: string) {
    const r = await fetch(`${BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, full_name: "User" })
    });
    const j = await json(r);
    return j.id as number;
  },
  async startSession(userId: number, durationMinutes: number, scheduleType: "start_end" | "interval") {
    const fd = new FormData();
    fd.append("user_id", String(userId));
    fd.append("duration_minutes", String(durationMinutes));
    fd.append("schedule_type", scheduleType);
    const r = await fetch(`${BASE}/exam/session/start`, { method: "POST", body: fd });
    const j = await json(r);
    return j.session_id as number;
  },
  async verifyFaceStart(userId: number, sessionId: number, face: Blob) {
    const fd = new FormData();
    fd.append("user_id", String(userId));
    fd.append("session_id", String(sessionId));
    fd.append("file", face);
    const r = await fetch(`${BASE}/verify/authenticate/face/start`, { method: "POST", body: fd });
    const j = await json(r);
    return Boolean(j.match);
  },
  async verifyVoiceStart(userId: number, sessionId: number, voice: Blob) {
    const fd = new FormData();
    fd.append("user_id", String(userId));
    fd.append("session_id", String(sessionId));
    fd.append("file", voice);
    const r = await fetch(`${BASE}/verify/authenticate/voice/start`, { method: "POST", body: fd });
    const j = await json(r);
    return Boolean(j.match);
  },
  async verifyFaceEnd(userId: number, sessionId: number, face: Blob) {
    const fd = new FormData();
    fd.append("user_id", String(userId));
    fd.append("session_id", String(sessionId));
    fd.append("file", face);
    const r = await fetch(`${BASE}/verify/authenticate/face/end`, { method: "POST", body: fd });
    const j = await json(r);
    return Boolean(j.match);
  },
  async verifyVoiceEnd(userId: number, sessionId: number, voice: Blob) {
    const fd = new FormData();
    fd.append("user_id", String(userId));
    fd.append("session_id", String(sessionId));
    fd.append("file", voice);
    const r = await fetch(`${BASE}/verify/authenticate/voice/end`, { method: "POST", body: fd });
    const j = await json(r);
    return Boolean(j.match);
  },
  async submitSession(userId: number, sessionId: number) {
    const fd = new FormData();
    fd.append("user_id", String(userId));
    fd.append("session_id", String(sessionId));
    const r = await fetch(`${BASE}/exam/session/submit`, { method: "POST", body: fd });
    const j = await json(r);
    return Boolean(j.status);
  }
};
