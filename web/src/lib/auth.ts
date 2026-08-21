const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "";
const AUTH_TIMEOUT_MS = 8000;

export type AuthUser = {
  id: number;
  username: string;
  email?: string | null;
};

type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; error: string; status: number; dbDisabled?: boolean };

async function parseJson(response: Response) {
  try {
    return await response.json();
  } catch {
    return null;
  }
}

function authSignal() {
  return AbortSignal.timeout(AUTH_TIMEOUT_MS);
}

export async function fetchCurrentUser(): Promise<ApiResult<AuthUser | null>> {
  try {
    const response = await fetch(`${API_BASE}/api/user`, {
      method: "GET",
      credentials: "include",
      signal: authSignal(),
    });
    const payload = await parseJson(response);

    if (response.status === 503) {
      return { ok: false, error: payload?.error || "資料庫未啟用", status: 503, dbDisabled: true };
    }
    if (response.status === 401) {
      return { ok: true, data: null };
    }
    if (!response.ok) {
      return {
        ok: false,
        error: payload?.error || `伺服器錯誤 (${response.status})`,
        status: response.status,
      };
    }
    return { ok: true, data: payload?.user ?? null };
  } catch {
    return { ok: false, error: "無法連線伺服器", status: 0 };
  }
}

export async function loginWithPassword(
  username: string,
  password: string,
  remember = true
): Promise<ApiResult<AuthUser>> {
  try {
    const response = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, remember }),
      signal: authSignal(),
    });
    const payload = await parseJson(response);

    if (response.status === 503) {
      return { ok: false, error: payload?.error || "資料庫未啟用", status: 503, dbDisabled: true };
    }
    if (!response.ok) {
      return {
        ok: false,
        error: payload?.error || "登入失敗",
        status: response.status,
      };
    }
    return { ok: true, data: payload.user };
  } catch {
    return { ok: false, error: "網路錯誤，請稍後再試", status: 0 };
  }
}

export async function registerWithPassword(
  username: string,
  password: string,
  email?: string
): Promise<ApiResult<AuthUser>> {
  try {
    const response = await fetch(`${API_BASE}/api/register`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username,
        password,
        email: email?.trim() || null,
      }),
      signal: authSignal(),
    });
    const payload = await parseJson(response);

    if (response.status === 503) {
      return { ok: false, error: payload?.error || "資料庫未啟用", status: 503, dbDisabled: true };
    }
    if (!response.ok) {
      return {
        ok: false,
        error: payload?.error || "註冊失敗",
        status: response.status,
      };
    }
    return { ok: true, data: payload.user };
  } catch {
    return { ok: false, error: "網路錯誤，請稍後再試", status: 0 };
  }
}

export async function logoutUser(): Promise<ApiResult<true>> {
  try {
    const response = await fetch(`${API_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",
      signal: authSignal(),
    });
    const payload = await parseJson(response);
    if (!response.ok) {
      return {
        ok: false,
        error: payload?.error || "登出失敗",
        status: response.status,
      };
    }
    return { ok: true, data: true };
  } catch {
    return { ok: false, error: "網路錯誤，請稍後再試", status: 0 };
  }
}
