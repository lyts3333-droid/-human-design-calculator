"use client";

import { FormEvent, useState } from "react";
import Image from "next/image";
import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";
import { useAuth } from "@/components/auth/auth-provider";
import { Button } from "@/components/ui/button";
import { FieldLabel, Input } from "@/components/ui/input";
import { CosmicBackground } from "@/components/layout/cosmic-background";

export function AuthGate() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [remember, setRemember] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function onSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);

    const u = username.trim();
    const p = password.trim();
    if (!u || !p) {
      setError("請輸入用戶名和密碼");
      return;
    }

    setSubmitting(true);
    const err =
      mode === "login"
        ? await login(u, p, remember)
        : await register(u, p, email.trim() || undefined);
    setSubmitting(false);
    if (err) setError(err);
  }

  const isLogin = mode === "login";

  return (
    <main className="relative flex min-h-screen items-center justify-center overflow-hidden px-5 py-12">
      <CosmicBackground />
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.55 }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="rounded-[28px] border border-white/10 bg-white/[0.05] p-8 shadow-[0_24px_80px_rgba(0,0,0,0.45)] backdrop-blur-2xl md:p-10">
          <div className="mb-8 flex flex-col items-center text-center">
            <Image
              src="/logo.png"
              alt="玩轉人生"
              width={88}
              height={88}
              className="mb-5 h-[88px] w-[88px] rounded-full object-contain shadow-[0_0_36px_rgba(199,168,111,0.4)]"
              priority
            />
            <div className="text-lg font-semibold tracking-[0.22em] text-accent-light">
              玩轉人生
            </div>
            <h1 className="mt-4 text-2xl font-semibold tracking-wide text-foreground">
              {isLogin ? "登入" : "註冊"}
            </h1>
            <p className="mt-2 text-sm text-muted">
              使用帳號密碼登入，查詢紀錄會保存在你的帳號中
            </p>
          </div>

          <form onSubmit={onSubmit} className="space-y-4">
            <div>
              <FieldLabel htmlFor="auth-username">用戶名</FieldLabel>
              <Input
                id="auth-username"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="請輸入用戶名"
                required
              />
            </div>
            <div>
              <FieldLabel htmlFor="auth-password">密碼</FieldLabel>
              <Input
                id="auth-password"
                type="password"
                autoComplete={isLogin ? "current-password" : "new-password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={isLogin ? "請輸入密碼" : "至少 6 個字元"}
                required
              />
            </div>

            {!isLogin && (
              <div>
                <FieldLabel htmlFor="auth-email">郵箱（選填）</FieldLabel>
                <Input
                  id="auth-email"
                  type="email"
                  autoComplete="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="選填"
                />
              </div>
            )}

            {isLogin && (
              <label className="flex cursor-pointer items-center gap-2 text-sm text-muted">
                <input
                  type="checkbox"
                  checked={remember}
                  onChange={(e) => setRemember(e.target.checked)}
                  className="h-4 w-4 rounded border-white/20 bg-transparent accent-[var(--primary)]"
                />
                記住我
              </label>
            )}

            {error && (
              <p className="rounded-2xl border border-red-400/30 bg-red-500/10 px-4 py-3 text-sm text-red-200">
                {error}
              </p>
            )}

            <Button type="submit" className="w-full" disabled={submitting}>
              {submitting ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  處理中…
                </>
              ) : isLogin ? (
                "登入"
              ) : (
                "註冊"
              )}
            </Button>
          </form>

          <div className="mt-6 text-center text-sm text-muted">
            {isLogin ? "還沒有帳號？" : "已有帳號？"}{" "}
            <button
              type="button"
              className="text-accent-light underline-offset-4 transition hover:underline"
              onClick={() => {
                setMode(isLogin ? "register" : "login");
                setError(null);
              }}
            >
              {isLogin ? "立即註冊" : "立即登入"}
            </button>
          </div>
        </div>
      </motion.div>
    </main>
  );
}
