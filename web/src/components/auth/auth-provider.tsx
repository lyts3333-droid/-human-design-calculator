"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import {
  fetchCurrentUser,
  loginWithPassword,
  logoutUser,
  registerWithPassword,
  type AuthUser,
} from "@/lib/auth";

type AuthStatus = "loading" | "authenticated" | "guest" | "unauthenticated";

type AuthContextValue = {
  status: AuthStatus;
  user: AuthUser | null;
  /** 資料庫未啟用時可免登入使用 */
  dbDisabled: boolean;
  login: (username: string, password: string, remember?: boolean) => Promise<string | null>;
  register: (username: string, password: string, email?: string) => Promise<string | null>;
  logout: () => Promise<string | null>;
  continueAsGuest: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("loading");
  const [user, setUser] = useState<AuthUser | null>(null);
  const [dbDisabled, setDbDisabled] = useState(false);

  useEffect(() => {
    let cancelled = false;

    (async () => {
      const result = await fetchCurrentUser();
      if (cancelled) return;

      if (result.ok) {
        if (result.data) {
          setUser(result.data);
          setStatus("authenticated");
        } else {
          setUser(null);
          setStatus("unauthenticated");
        }
        return;
      }

      if (result.dbDisabled || result.status === 0) {
        // 資料庫未啟用或後端暫時無法連線：允許直接使用
        setDbDisabled(Boolean(result.dbDisabled));
        setUser(null);
        setStatus("guest");
        return;
      }

      setUser(null);
      setStatus("unauthenticated");
    })();

    return () => {
      cancelled = true;
    };
  }, []);

  const login = useCallback(async (username: string, password: string, remember = true) => {
    const result = await loginWithPassword(username, password, remember);
    if (!result.ok) {
      if (result.dbDisabled) {
        setDbDisabled(true);
        setStatus("guest");
        return null;
      }
      return result.error;
    }
    setUser(result.data);
    setStatus("authenticated");
    return null;
  }, []);

  const register = useCallback(async (username: string, password: string, email?: string) => {
    const result = await registerWithPassword(username, password, email);
    if (!result.ok) {
      if (result.dbDisabled) {
        setDbDisabled(true);
        setStatus("guest");
        return null;
      }
      return result.error;
    }
    setUser(result.data);
    setStatus("authenticated");
    return null;
  }, []);

  const logout = useCallback(async () => {
    // 無論 API 成功與否都清掉本機登入狀態，避免卡在已登入畫面
    const result = await logoutUser();
    setUser(null);
    setStatus(dbDisabled ? "guest" : "unauthenticated");
    if (!result.ok) return result.error;
    return null;
  }, [dbDisabled]);

  const continueAsGuest = useCallback(() => {
    setStatus("guest");
  }, []);

  const value = useMemo(
    () => ({
      status,
      user,
      dbDisabled,
      login,
      register,
      logout,
      continueAsGuest,
    }),
    [status, user, dbDisabled, login, register, logout, continueAsGuest]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
