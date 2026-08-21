"use client";

import { motion } from "framer-motion";

export function CosmicBackground() {
  return (
    <div className="pointer-events-none fixed inset-0 -z-10 overflow-hidden">
      <div className="absolute inset-0 bg-background" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_80%_50%_at_50%_-10%,rgba(111,108,255,0.28),transparent_55%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_15%_80%,rgba(78,197,255,0.12),transparent_40%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_85%_25%,rgba(199,168,111,0.12),transparent_35%)]" />

      <motion.div
        className="absolute left-1/2 top-24 h-[420px] w-[420px] -translate-x-1/2 rounded-full bg-primary/20 blur-[120px]"
        animate={{ opacity: [0.35, 0.55, 0.35], scale: [1, 1.08, 1] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
      />
      <motion.div
        className="absolute bottom-10 right-10 h-[280px] w-[280px] rounded-full bg-secondary/15 blur-[100px]"
        animate={{ opacity: [0.25, 0.45, 0.25], y: [0, -18, 0] }}
        transition={{ duration: 10, repeat: Infinity, ease: "easeInOut" }}
      />

      <svg
        className="absolute left-1/2 top-1/3 h-[640px] w-[640px] -translate-x-1/2 opacity-[0.07]"
        viewBox="0 0 200 200"
        fill="none"
      >
        <circle cx="100" cy="100" r="90" stroke="#C7A86F" strokeWidth="0.4" />
        <circle cx="100" cy="100" r="60" stroke="#6F6CFF" strokeWidth="0.4" />
        <circle cx="100" cy="100" r="30" stroke="#4EC5FF" strokeWidth="0.4" />
        <path
          d="M100 10 L160 145 L40 145 Z"
          stroke="#C7A86F"
          strokeWidth="0.35"
        />
        <path
          d="M100 190 L40 55 L160 55 Z"
          stroke="#6F6CFF"
          strokeWidth="0.35"
        />
      </svg>

      <div
        className="absolute inset-0 opacity-40"
        style={{
          backgroundImage:
            "radial-gradient(1px 1px at 20% 30%, rgba(255,255,255,0.35), transparent), radial-gradient(1px 1px at 70% 60%, rgba(255,255,255,0.25), transparent), radial-gradient(1px 1px at 40% 80%, rgba(255,255,255,0.2), transparent)",
        }}
      />
    </div>
  );
}
