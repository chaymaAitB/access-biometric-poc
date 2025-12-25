import { createContext, useContext, useState, ReactNode } from "react";

type ExamState = { sessionId: number | null; startVerified: boolean; endVerified: boolean };
type ExamCtx = ExamState & {
  setSessionId: (id: number) => void;
  setStartVerified: (v: boolean) => void;
  setEndVerified: (v: boolean) => void;
};

const ExamSessionContext = createContext<ExamCtx | undefined>(undefined);

export function ExamSessionProvider({ children }: { children: ReactNode }) {
  const [sessionId, setSessionId_] = useState<number | null>(null);
  const [startVerified, setStartVerified_] = useState(false);
  const [endVerified, setEndVerified_] = useState(false);
  function setSessionId(id: number) { setSessionId_(id); }
  function setStartVerified(v: boolean) { setStartVerified_(v); }
  function setEndVerified(v: boolean) { setEndVerified_(v); }
  return (
    <ExamSessionContext.Provider value={{ sessionId, startVerified, endVerified, setSessionId, setStartVerified, setEndVerified }}>
      {children}
    </ExamSessionContext.Provider>
  );
}

export function useExamSession() {
  const ctx = useContext(ExamSessionContext);
  if (!ctx) throw new Error("ExamSessionContext");
  return ctx;
}
