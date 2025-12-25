import { useNavigate } from "react-router-dom";
import { useExamSession } from "../context/ExamSessionContext";

export default function ExamSessionPage() {
  const navigate = useNavigate();
  const { sessionId } = useExamSession();
  function goSubmit() {
    navigate("/verify-end");
  }
  return (
    <div className="container">
      <div className="title">Exam Session</div>
      <div className="subtitle">Answer your questions. Click Submit when ready.</div>
      <div className="card">
        <div>Session ID: {sessionId}</div>
        <div className="spacer"></div>
        <div className="actions">
          <button className="btn btn-primary" onClick={goSubmit}>Submit Exam</button>
        </div>
      </div>
    </div>
  );
}
