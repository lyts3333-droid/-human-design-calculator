"use client";

import { motion } from "framer-motion";
import { Card } from "@/components/ui/card";

export function AboutSection() {
  return (
    <section id="about" className="mx-auto max-w-6xl px-5 py-12 md:px-8 md:py-16">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="grid gap-6 md:grid-cols-3"
      >
        {[
          {
            title: "類型與策略",
            desc: "了解你如何與世界互動，以及何時該行動、何時該等待。",
          },
          {
            title: "內在權威",
            desc: "認識真正適合你的決策方式，減少內耗與錯誤選擇。",
          },
          {
            title: "基因天命之路",
            desc: "從陰影到天賦再到神聖才能，看見轉化的完整路徑。",
          },
        ].map((item) => (
          <Card key={item.title} className="p-6">
            <h3 className="text-lg font-medium text-accent-light">{item.title}</h3>
            <p className="mt-3 text-sm leading-7 text-muted">{item.desc}</p>
          </Card>
        ))}
      </motion.div>
    </section>
  );
}
