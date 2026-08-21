"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { Sparkles, Compass } from "lucide-react";
import { Button } from "@/components/ui/button";

export function Hero() {
  const scrollToForm = () =>
    document.getElementById("form")?.scrollIntoView({ behavior: "smooth" });
  const scrollToAbout = () =>
    document.getElementById("about")?.scrollIntoView({ behavior: "smooth" });

  return (
    <section className="relative mx-auto grid max-w-6xl items-center gap-12 px-5 pb-10 pt-12 md:grid-cols-2 md:gap-16 md:px-8 md:pb-16 md:pt-20">
      <motion.div
        initial={{ opacity: 0, y: 28 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="space-y-7"
      >
        <div className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-3 py-1 text-xs tracking-[0.18em] text-accent-light backdrop-blur">
          <Sparkles className="h-3.5 w-3.5" />
          免費人生圖
        </div>

        <Image
          src="/logo.png"
          alt="玩轉人生"
          width={88}
          height={88}
          className="h-[88px] w-[88px] rounded-full object-contain shadow-[0_0_48px_rgba(199,168,111,0.4)]"
          priority
        />

        <div>
          <h1 className="text-4xl font-semibold tracking-[0.12em] text-accent-light md:text-5xl">
            玩轉人生
          </h1>
          <p className="mt-2 text-sm uppercase tracking-[0.34em] text-muted">
            Life Design Lab
          </p>
        </div>

        <div className="space-y-3">
          <h2 className="max-w-xl text-2xl font-medium leading-snug text-foreground md:text-3xl">
            探索你的 Human Design
          </h2>
          <p className="max-w-lg text-base leading-8 text-muted md:text-lg">
            找到真正適合自己的生活方式，
            <br className="hidden sm:block" />
            了解天賦、決策模式與人生方向。
          </p>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row">
          <Button size="lg" onClick={scrollToForm}>
            立即解析人生圖
          </Button>
          <Button size="lg" variant="secondary" onClick={scrollToAbout}>
            <Compass className="h-4 w-4" />
            了解 Human Design
          </Button>
        </div>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, scale: 0.92 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 1, delay: 0.15 }}
        className="relative mx-auto flex h-[360px] w-full max-w-md items-center justify-center md:h-[460px]"
      >
        <motion.div
          className="absolute inset-8 rounded-full bg-gradient-to-br from-primary/30 via-secondary/20 to-accent/20 blur-3xl"
          animate={{ opacity: [0.45, 0.75, 0.45], rotate: [0, 8, 0] }}
          transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
        />
        <motion.div
          animate={{ y: [0, -14, 0] }}
          transition={{ duration: 5.5, repeat: Infinity, ease: "easeInOut" }}
          className="relative rounded-[2rem] border border-white/15 bg-white/[0.06] p-8 shadow-[0_30px_80px_rgba(0,0,0,0.45)] backdrop-blur-2xl"
        >
          <div className="absolute -inset-px rounded-[2rem] bg-gradient-to-br from-primary/40 via-transparent to-accent/30 opacity-60" />
          <Image
            src="/logo.png"
            alt="Human Design 神秘風格插畫"
            width={280}
            height={280}
            className="relative z-10 mx-auto h-[280px] w-[280px] object-contain"
            priority
          />
          <div className="relative z-10 mt-5 text-center">
            <div className="text-sm tracking-[0.2em] text-accent-light">
              人類圖 × 基因天命
            </div>
            <div className="mt-1 text-xs text-muted">你的獨特能量藍圖</div>
          </div>
        </motion.div>
      </motion.div>
    </section>
  );
}
