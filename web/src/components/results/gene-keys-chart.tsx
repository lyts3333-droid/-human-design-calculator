"use client";

import { useMemo, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { fetchGeneKey } from "@/lib/api";
import {
  buildGeneKeyNodes,
  CHART_CENTER,
  CONNECTION_STROKE,
  GENE_KEY_CONNECTIONS,
  getSequenceViewBox,
  NODE_POSITIONS,
  type SequenceFilter,
  type SphereColor,
} from "@/lib/gene-keys";
import type { GeneKeyDetail, PlanetInfo } from "@/types/hd";
import { IChingWheel } from "@/components/results/iching-wheel";
import { cn } from "@/lib/utils";

const FILTERS: { id: SequenceFilter; label: string }[] = [
  { id: "all", label: "全部" },
  { id: "genius", label: "天賦" },
  { id: "love", label: "關係" },
  { id: "prosperity", label: "服務" },
];

const TABS: { key: keyof GeneKeyDetail; label: string }[] = [
  { key: "meaning", label: "意義" },
  { key: "shadow", label: "陰影" },
  { key: "manifestation", label: "表現形式" },
  { key: "gift", label: "天賦" },
  { key: "transformation", label: "轉化過程" },
  { key: "siddhi", label: "神聖才能" },
  { key: "finalState", label: "最終狀態" },
  { key: "synthesis", label: "綜合意義" },
];

function sphereGradient(color: SphereColor) {
  if (color === "green") return "radial-gradient(circle at 30% 30%, #5a8a60, #1e3a24)";
  if (color === "blue") return "radial-gradient(circle at 30% 30%, #2874a6, #1a3a52)";
  return "radial-gradient(circle at 30% 30%, #a03030, #5a1818)";
}

export function GeneKeysChart({
  personalityList,
  designList,
}: {
  personalityList?: PlanetInfo[];
  designList?: PlanetInfo[];
}) {
  const [filter, setFilter] = useState<SequenceFilter>("all");
  const [detail, setDetail] = useState<GeneKeyDetail | null>(null);
  const [activeTab, setActiveTab] = useState<keyof GeneKeyDetail>("meaning");
  const [loadingGate, setLoadingGate] = useState<number | null>(null);
  const [title, setTitle] = useState("基因天命");
  const [hoverId, setHoverId] = useState<string | null>(null);

  const nodes = useMemo(
    () => buildGeneKeyNodes(personalityList, designList),
    [personalityList, designList]
  );

  const positions = useMemo(() => {
    const map: Record<string, { x: number; y: number }> = { ...NODE_POSITIONS };
    nodes.forEach((n) => {
      if (!map[n.id] && NODE_POSITIONS[n.id]) {
        map[n.id] = NODE_POSITIONS[n.id];
      }
    });
    return map;
  }, [nodes]);

  const viewBox = useMemo(
    () => getSequenceViewBox(filter, nodes, positions),
    [filter, nodes, positions]
  );

  const isZoomed = filter !== "all";

  const openDetail = async (gate: number | undefined, label: string) => {
    if (!gate) return;
    setLoadingGate(gate);
    setTitle(label);
    try {
      const data = await fetchGeneKey(gate);
      setDetail(data);
      setActiveTab("meaning");
    } catch (err) {
      setDetail({
        name: label,
        meaning: err instanceof Error ? err.message : "載入失敗",
      });
    } finally {
      setLoadingGate(null);
    }
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-2xl font-semibold tracking-wide text-accent-light">
          基因天命 · 黃金之路
        </h3>
        <p className="mt-2 text-sm text-muted">
          點擊每個球體，深入了解陰影、天賦與神聖才能。
        </p>
      </div>

      <div className="flex flex-wrap justify-center gap-2">
        {FILTERS.map((f) => (
          <Button
            key={f.id}
            size="sm"
            variant={filter === f.id ? "primary" : "secondary"}
            onClick={() => setFilter(f.id)}
          >
            {f.label}
          </Button>
        ))}
      </div>

      <div
        className={cn(
          "rounded-3xl border border-white/10 bg-white/[0.03] p-4 backdrop-blur-xl sm:p-6",
          isZoomed ? "overflow-hidden" : "overflow-visible"
        )}
      >
        <motion.svg
          viewBox={viewBox}
          initial={false}
          animate={{ viewBox }}
          transition={{ duration: 0.85, ease: [0.22, 1, 0.36, 1] }}
          className="mx-auto aspect-square h-auto w-full max-w-4xl"
          preserveAspectRatio="xMidYMid meet"
          overflow="hidden"
        >
          {/* 背景易經圓環（不影響中間節點位置） */}
          <IChingWheel cx={CHART_CENTER.x} cy={CHART_CENTER.y} radius={455} />

          {GENE_KEY_CONNECTIONS.map((c, idx) => {
            const from = positions[c.from];
            const to = positions[c.to];
            if (!from || !to) return null;
            const visible = filter === "all" || filter === c.sequence;
            return (
              <line
                key={`${c.from}-${c.to}-${idx}`}
                x1={from.x}
                y1={from.y}
                x2={to.x}
                y2={to.y}
                stroke={CONNECTION_STROKE[c.color]}
                strokeWidth={isZoomed && visible ? 5 : 4}
                strokeOpacity={visible ? 0.55 : 0.08}
              />
            );
          })}

          {nodes.map((node) => {
            const pos = positions[node.id];
            if (!pos) return null;
            const sequences = node.sequences || [node.sequence];
            const visible = filter === "all" || sequences.includes(filter);
            let color = node.color;
            if (filter === "love" && node.loveColor) color = node.loveColor;
            if (filter === "prosperity" && node.prosperityColor)
              color = node.prosperityColor;
            const hovered = hoverId === node.id;

            return (
              <g
                key={node.id}
                opacity={visible ? 1 : 0.12}
                style={{
                  cursor: visible ? "pointer" : "default",
                  pointerEvents: visible ? "auto" : "none",
                }}
                onClick={() =>
                  visible && openDetail(node.gate, `${node.label} · ${node.value}`)
                }
                onMouseEnter={() => visible && setHoverId(node.id)}
                onMouseLeave={() => setHoverId(null)}
                transform={`translate(${pos.x} ${pos.y}) scale(${hovered ? 1.1 : 1}) translate(${-pos.x} ${-pos.y})`}
              >
                <circle
                  cx={pos.x}
                  cy={pos.y}
                  r={hovered ? 56 : 48}
                  fill="url(#glow)"
                  opacity={hovered ? 0.5 : 0.35}
                />
                <foreignObject
                  x={pos.x - 72}
                  y={pos.y - 56}
                  width={144}
                  height={148}
                  overflow="visible"
                >
                  <div className="flex h-full flex-col items-center overflow-visible">
                    <div
                      className={`flex h-[96px] w-[96px] flex-col items-center justify-center gap-0.5 rounded-full border-2 border-accent/40 px-1 text-white shadow-[0_0_28px_rgba(199,168,111,0.25)] transition-[box-shadow] duration-200 ${
                        hovered ? "shadow-[0_0_36px_rgba(199,168,111,0.45)]" : ""
                      }`}
                      style={{ background: sphereGradient(color) }}
                    >
                      <div className="text-[11px] font-medium leading-tight tracking-wide opacity-95">
                        {node.description}
                      </div>
                      <div className="font-mono text-xl font-bold leading-none tracking-tight md:text-2xl">
                        {node.value && node.value !== "—" ? node.value : "—"}
                      </div>
                      {loadingGate === node.gate && (
                        <div className="text-[10px] opacity-80">載入中</div>
                      )}
                    </div>
                    <div className="mt-2 whitespace-nowrap rounded-full border border-white/15 bg-black/40 px-2.5 py-0.5 text-[14px] font-semibold leading-tight text-accent-light">
                      {node.label}
                    </div>
                  </div>
                </foreignObject>
              </g>
            );
          })}

          <defs>
            <radialGradient id="glow">
              <stop offset="0%" stopColor="#C7A86F" stopOpacity="0.8" />
              <stop offset="100%" stopColor="#C7A86F" stopOpacity="0" />
            </radialGradient>
          </defs>
        </motion.svg>
      </div>

      <AnimatePresence>
        {detail && (
          <motion.div
            className="fixed inset-0 z-[100] flex items-center justify-center p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div
              className="absolute inset-0 bg-black/70 backdrop-blur-sm"
              onClick={() => setDetail(null)}
            />
            <motion.div
              initial={{ opacity: 0, y: 24, scale: 0.96 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 16, scale: 0.96 }}
              className="relative z-10 flex max-h-[85vh] w-full max-w-2xl flex-col overflow-hidden rounded-3xl border border-white/15 bg-[#0d1228]/95 shadow-[0_30px_80px_rgba(0,0,0,0.55)]"
            >
              <div className="flex items-start justify-between border-b border-white/10 px-6 py-5">
                <div>
                  <div className="text-xs tracking-[0.2em] text-muted">{title}</div>
                  <h4 className="mt-1 text-xl font-semibold text-accent-light">
                    {detail.name}
                  </h4>
                </div>
                <button
                  onClick={() => setDetail(null)}
                  className="rounded-full border border-white/10 p-2 text-muted hover:text-foreground"
                >
                  <X className="h-4 w-4" />
                </button>
              </div>
              <div className="flex flex-wrap gap-2 border-b border-white/10 px-6 py-3">
                {TABS.map((tab) => (
                  <button
                    key={tab.key}
                    onClick={() => setActiveTab(tab.key)}
                    className={`rounded-full px-3 py-1.5 text-xs transition ${
                      activeTab === tab.key
                        ? "bg-primary/30 text-accent-light"
                        : "text-muted hover:bg-white/5"
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
              <div className="overflow-y-auto px-6 py-5 text-sm leading-7 text-muted">
                {String(detail[activeTab] || "尚無內容")}
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
