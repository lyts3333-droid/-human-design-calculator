"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";
import type { HumanDesignResult } from "@/types/hd";

const items = [
  { key: "input_date", label: "輸入時間", render: (d: HumanDesignResult) => d.input_date || "—" },
  { key: "profile", label: "人生角色", render: (d: HumanDesignResult) => d.profile || "—" },
  {
    key: "type",
    label: "類型",
    render: (d: HumanDesignResult) => d.type || d.type_name || "—",
  },
  { key: "strategy", label: "策略", render: (d: HumanDesignResult) => d.strategy || "—" },
  {
    key: "decision_mode",
    label: "定義",
    render: (d: HumanDesignResult) => d.decision_mode || "—",
  },
  { key: "authority", label: "內在權威", render: (d: HumanDesignResult) => d.authority || "—" },
  {
    key: "not_self_theme",
    label: "非自己主題",
    render: (d: HumanDesignResult) => d.not_self_theme || "—",
  },
] as const;

export function AnalysisCards({ data }: { data: HumanDesignResult }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((item, i) => (
        <motion.div
          key={item.key}
          initial={{ opacity: 0, y: 16 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ delay: i * 0.05 }}
        >
          <Card className="h-full p-5">
            <div className="text-xs font-medium tracking-[0.14em] text-[#C8C0D8]">
              {item.label}
            </div>
            <div
              className={`mt-3 text-lg font-semibold ${
                item.key === "profile"
                  ? "text-2xl text-[#F0D78C]"
                  : "text-[#F8F5EE]"
              }`}
            >
              {item.key === "type" ||
              item.key === "strategy" ||
              item.key === "authority" ||
              item.key === "decision_mode" ||
              item.key === "not_self_theme" ? (
                <span className="inline-flex rounded-full border border-[#8B7CFF]/50 bg-gradient-to-r from-[#6F6CFF]/90 to-[#4EC5FF]/80 px-3.5 py-1.5 text-base font-semibold text-white shadow-[0_0_16px_rgba(111,108,255,0.35)]">
                  {item.render(data)}
                </span>
              ) : (
                item.render(data)
              )}
            </div>
          </Card>
        </motion.div>
      ))}
    </div>
  );
}
