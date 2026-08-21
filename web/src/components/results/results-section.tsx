"use client";

import { motion } from "framer-motion";
import { AnalysisCards } from "@/components/results/analysis-cards";
import { PlanetLists } from "@/components/results/planet-lists";
import { GeneKeysChart } from "@/components/results/gene-keys-chart";
import type { BirthFormValues, HumanDesignResult } from "@/types/hd";

export function ResultsSection({
  data,
  form,
}: {
  data: HumanDesignResult;
  form: BirthFormValues | null;
}) {
  return (
    <section id="results" className="mx-auto max-w-6xl space-y-12 px-5 py-12 md:px-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center"
      >
        <p className="text-xs uppercase tracking-[0.28em] text-accent-light">
          Profile Preview
        </p>
        <h2 className="mt-2 text-3xl font-semibold text-foreground">
          {form?.name ? `${form.name} 的人生圖預覽` : "你的人生圖預覽"}
        </h2>
        <p className="mt-3 text-sm text-muted">
          完整保留人類圖分析、行星閘門與基因天命圖，點擊球體即可深入探索。
        </p>
      </motion.div>

      <GeneKeysChart
        designList={data.design_list}
        personalityList={data.personality_list}
      />

      <div className="space-y-4">
        <h3 className="text-lg font-medium tracking-wide text-foreground">
          人類圖摘要
        </h3>
        <AnalysisCards data={data} />
      </div>

      <div className="space-y-4">
        <h3 className="text-lg font-medium tracking-wide text-foreground">
          行星閘門與爻線
        </h3>
        <PlanetLists
          designList={data.design_list}
          personalityList={data.personality_list}
        />
      </div>
    </section>
  );
}
