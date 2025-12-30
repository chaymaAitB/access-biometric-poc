from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.exam_session import ExamSession, ExamStatus, ScheduleType
from app.models.verification_event import VerificationEvent
import datetime
from app.core.config import settings

router = APIRouter()

@router.post("/session/start")
def start_session(user_id: int = Form(...), duration_minutes: int | None = Form(None), schedule_type: str = Form("start_end"), interval_minutes: int | None = Form(None), liveness_ok: bool = Form(False), liveness_score: float | None = Form(None), db: Session = Depends(get_db)):
    now = datetime.datetime.now().isoformat()
    try:
        sched = ScheduleType(schedule_type)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid schedule_type")
    if not liveness_ok or (liveness_score is None) or (liveness_score < settings.LIVENESS_MOTION_THRESHOLD):
        raise HTTPException(status_code=400, detail="Liveness check failed or missing")
    session = ExamSession(
        user_id=user_id,
        started_at=now,
        ended_at=None,
        duration_minutes=duration_minutes,
        status=ExamStatus.ACTIVE,
        schedule_type=sched,
        interval_minutes=interval_minutes
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "status": session.status.value}

@router.post("/session/submit")
def submit_session(session_id: int = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    session = db.query(ExamSession).filter(ExamSession.id == session_id, ExamSession.user_id == user_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    if session.status == ExamStatus.COMPLETED:
        return {"session_id": session.id, "status": session.status.value}
    session.ended_at = datetime.datetime.now().isoformat()
    session.status = ExamStatus.COMPLETED
    db.add(session)
    db.commit()
    db.refresh(session)
    return {"session_id": session.id, "status": session.status.value}

@router.get("/metrics/session/{session_id}")
def session_metrics(session_id: int, db: Session = Depends(get_db)):
    events = db.query(VerificationEvent).filter(VerificationEvent.session_id == session_id).all()
    if not events:
        return {"session_id": session_id, "events": 0, "frr": None, "far": None}
    total = len(events)
    failures = sum(1 for e in events if not e.match)
    frr = failures / total if total > 0 else None
    far = None
    return {"session_id": session_id, "events": total, "frr": frr, "far": far}

@router.get("/session/{session_id}/details")
def session_details(session_id: int, db: Session = Depends(get_db)):
    events = db.query(VerificationEvent).filter(VerificationEvent.session_id == session_id).all()
    data = []
    for e in events:
        data.append({
            "id": e.id,
            "modality": e.modality,
            "phase": e.phase,
            "match": e.match,
            "score": e.score,
            "threshold": e.threshold,
            "metric": e.metric,
            "mock_used": e.mock_used,
            "created_at": e.created_at
        })
    return {"session_id": session_id, "log": data}
