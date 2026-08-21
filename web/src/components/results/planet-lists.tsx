"use client";

import { Card } from "@/components/ui/card";
import { PLANET_LABELS } from "@/lib/gene-keys";
import type { PlanetInfo } from "@/types/hd";

function PlanetColumn({
  title,
  tone,
  list,
}: {
  title: string;
  tone: "design" | "personality";
  list?: PlanetInfo[];
}) {
  return (
    <Card hover={false} className="p-5">
      <h3
        className={`mb-4 text-center text-sm font-semibold tracking-[0.16em] ${
          tone === "design" ? "text-[#FF9AA2]" : "text-[#F8F5EE]"
        }`}
      >
        {title}
      </h3>
      <div className="space-y-2">
        {(list || []).map((p) => (
          <div
            key={`${tone}-${p.planet}`}
            className="flex items-center justify-between rounded-2xl border border-white/10 bg-[#0B1020]/70 px-3 py-2.5"
          >
            <div className="flex items-center gap-2 text-sm font-medium text-[#F8F5EE]">
              <span className="text-[#4EC5FF]">{p.constellation_symbol || ""}</span>
              <span>{PLANET_LABELS[p.planet] || p.planet}</span>
            </div>
            <div
              className={`font-mono text-sm font-bold ${
                tone === "design" ? "text-[#FFB4BA]" : "text-[#F0D78C]"
              }`}
            >
              {p.gate_line}
              {p.arrow_direction ? (
                <span className="ml-1 text-xs text-[#F8F5EE]">{p.arrow_direction}</span>
              ) : null}
            </div>
          </div>
        ))}
        {!list?.length && (
          <div className="py-8 text-center text-sm text-[#C8C0D8]">等待資料…</div>
        )}
      </div>
    </Card>
  );
}

export function PlanetLists({
  designList,
  personalityList,
}: {
  designList?: PlanetInfo[];
  personalityList?: PlanetInfo[];
}) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <PlanetColumn title="潛意識（Design）" tone="design" list={designList} />
      <PlanetColumn
        title="意識（Personality）"
        tone="personality"
        list={personalityList}
      />
    </div>
  );
}
