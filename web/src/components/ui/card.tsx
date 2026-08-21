"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

type CardProps = {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
};

export function Card({ children, className, hover = true }: CardProps) {
  return (
    <motion.div
      whileHover={hover ? { y: -4, scale: 1.01 } : undefined}
      transition={{ type: "spring", stiffness: 260, damping: 22 }}
      className={cn(
        "rounded-3xl border border-white/15 bg-[#141B33]/92 p-6 text-[#F5F0E8] shadow-[0_20px_60px_rgba(0,0,0,0.45)] backdrop-blur-2xl",
        "hover:border-primary/40 hover:shadow-[0_0_40px_rgba(111,108,255,0.22)]",
        className
      )}
    >
      {children}
    </motion.div>
  );
}
