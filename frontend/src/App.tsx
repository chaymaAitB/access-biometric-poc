import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import { ExamSessionProvider } from "./context/ExamSessionContext";
import VerifyStartPage from "./routes/VerifyStartPage";
import ExamSessionPage from "./routes/ExamSessionPage";
import VerifyEndPage from "./routes/VerifyEndPage";
import BiometricSessionGuard from "./components/BiometricSessionGuard";

export default function App() {
  return (
    <AuthProvider>
      <ExamSessionProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/verify-start" element={<VerifyStartPage />} />
            <Route
              path="/exam-session"
              element={
                <BiometricSessionGuard>
                  <ExamSessionPage />
                </BiometricSessionGuard>
              }
            />
            <Route path="/verify-end" element={<VerifyEndPage />} />
            <Route path="*" element={<Navigate to="/verify-start" replace />} />
          </Routes>
        </BrowserRouter>
      </ExamSessionProvider>
    </AuthProvider>
  );
}
