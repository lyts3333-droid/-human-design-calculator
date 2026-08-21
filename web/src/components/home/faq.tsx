"use client";

import { motion } from "framer-motion";

const faqs = [
  {
    q: "不知道確切出生時間怎麼辦？",
    a: "可先輸入 12:00 試算。若大致知道時段（上午、下午、夜間），可各試一次比對差異。月亮相關資訊對時間較敏感，太陽閘門通常較穩定。",
  },
  {
    q: "找不到我的出生城市？",
    a: "請選同一時區內最接近的主要城市。只要時區正確，人類圖與基因天命的核心計算即具參考價值。",
  },
  {
    q: "會保留哪些資料？",
    a: "所有分析結果（類型、人生角色、策略、內在權威、行星閘門、基因天命圖）都會完整顯示於頁面。我們重視資料安全，僅用於為你產生人生圖。",
  },
];

export function FaqSection() {
  return (
    <section id="faq" className="mx-auto max-w-2xl px-5 py-16 md:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="mb-8 text-center"
      >
        <h2 className="text-3xl font-semibold text-foreground">常見問題</h2>
        <p className="mt-2 text-sm text-muted">開始探索前，這些資訊或許對你有幫助</p>
      </motion.div>

      <div className="space-y-3">
        {faqs.map((item) => (
          <details
            key={item.q}
            className="group overflow-hidden rounded-3xl border border-white/20 bg-[#2A3358] shadow-[0_8px_28px_rgba(0,0,0,0.28)] open:border-primary/45"
          >
            <summary className="cursor-pointer list-none px-5 py-4 text-sm font-semibold tracking-wide text-foreground marker:content-none hover:bg-[#343F68]">
              <span className="flex items-center justify-between gap-4">
                {item.q}
                <span className="text-accent-light transition group-open:rotate-45">+</span>
              </span>
            </summary>
            <div className="border-t border-white/15 bg-[#12182E] px-5 py-4">
              <p className="text-sm leading-7 text-[#EDE8F8]">{item.a}</p>
            </div>
          </details>
        ))}
      </div>
    </section>
  );
}
