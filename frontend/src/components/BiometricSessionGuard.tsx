import { ReactNode } from "react";
import { useAuth } from "../context/AuthContext";
import { useExamSession } from "../context/ExamSessionContext";
import { Navigate } from "react-router-dom";

export default function BiometricSessionGuard({ children }: { children: ReactNode }) {
  const { authenticatedUserId } = useAuth();
  const { sessionId, startVerified } = useExamSession();
  if (!authenticatedUserId) return <Navigate to="/verify-start" replace />;
  if (!sessionId) return <Navigate to="/verify-start" replace />;
  if (!startVerified) return <Navigate to="/verify-start" replace />;
  return <>{children}</>;
}
