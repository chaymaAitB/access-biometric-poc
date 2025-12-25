import { createContext, useContext, useState, ReactNode } from "react";

type AuthState = { authenticatedUserId: number | null };
type AuthCtx = AuthState & { setAuthenticated: (id: number) => void; logout: () => void };

const AuthContext = createContext<AuthCtx | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [authenticatedUserId, setAuthenticatedUserId] = useState<number | null>(null);
  function setAuthenticated(id: number) { setAuthenticatedUserId(id); }
  function logout() { setAuthenticatedUserId(null); }
  return <AuthContext.Provider value={{ authenticatedUserId, setAuthenticated, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("AuthContext");
  return ctx;
}
