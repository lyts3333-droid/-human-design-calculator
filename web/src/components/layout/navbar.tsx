"use client";

import Image from "next/image";
import Link from "next/link";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/components/auth/auth-provider";

export function Navbar() {
  const { user, status, logout } = useAuth();

  return (
    <motion.header
      initial={{ y: -16, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="sticky top-0 z-50 border-b border-white/8 bg-background/70 backdrop-blur-2xl"
    >
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5 md:h-20 md:px-8">
        <Link href="/" className="flex items-center gap-3">
          <Image
            src="/logo.png"
            alt="玩轉人生"
            width={44}
            height={44}
            className="h-11 w-11 rounded-full object-contain shadow-[0_0_24px_rgba(199,168,111,0.35)]"
            priority
          />
          <div>
            <div className="text-base font-semibold tracking-[0.18em] text-accent-light md:text-lg">
              玩轉人生
            </div>
            <div className="text-[10px] uppercase tracking-[0.32em] text-muted">
              Life Design Lab
            </div>
          </div>
        </Link>

        <nav className="hidden items-center gap-8 text-sm text-muted md:flex">
          <a href="#form" className="transition hover:text-foreground">
            免費人生圖
          </a>
          <a href="#about" className="transition hover:text-foreground">
            認識人類圖
          </a>
          <a href="#faq" className="transition hover:text-foreground">
            常見問題
          </a>
        </nav>

        <div className="flex items-center gap-2 md:gap-3">
          {status === "authenticated" && user && (
            <>
              <span className="hidden max-w-[8rem] truncate text-sm text-muted sm:inline">
                {user.username}
              </span>
              <Button
                type="button"
                size="sm"
                variant="secondary"
                onClick={async () => {
                  await logout();
                }}
              >
                登出
              </Button>
            </>
          )}
          <Button
            size="sm"
            onClick={() => {
              document.getElementById("form")?.scrollIntoView({ behavior: "smooth" });
            }}
          >
            立即解析
          </Button>
        </div>
      </div>
    </motion.header>
  );
}
