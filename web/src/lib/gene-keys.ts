import type { PlanetInfo } from "@/types/hd";

export type SequenceFilter = "all" | "genius" | "love" | "prosperity";
export type SphereColor = "green" | "orange" | "blue";

export type GeneKeyNode = {
  id: string;
  label: string;
  value: string;
  color: SphereColor;
  gridRow: number;
  gridCol: number;
  description: string;
  sequence: SequenceFilter;
  sequences?: SequenceFilter[];
  loveColor?: SphereColor;
  prosperityColor?: SphereColor;
  gate?: number;
};

export type GeneKeyConnection = {
  from: string;
  to: string;
  color: "green" | "red" | "blue";
  sequence: SequenceFilter;
  /** 黃金之路路徑 ID，對應 gene-key-paths.ts */
  pathId?: string;
};

/**
 * 菱形黃金之路座標（viewBox 1000×1000，置中正圓結構）
 *
 *              黑太陽
 *              黑木星
 *        紅火星      紅木星
 * 紅太陽      紅金星      黑地球
 *        黑金星      黑火星
 *              紅月亮
 *              紅地球
 */
export const CHART_CENTER = { x: 500, y: 500 };
/** 外圈半徑：紅太陽、黑地球的中心點落在此圓上 */
export const CHART_RING_R = 400;

export const NODE_POSITIONS: Record<string, { x: number; y: number }> = {
  "personality-sun": { x: 500, y: 120 }, // 黑太陽（頂）
  // 黑木星在上；紅火星在其左下、紅木星在其右下
  "personality-jupiter": { x: 500, y: 270 }, // 黑木星（珍珠）
  "design-mars": { x: 340, y: 390 }, // 紅火星（核心）— 黑木星左下
  "design-jupiter": { x: 660, y: 390 }, // 紅木星（文化）— 黑木星右下
  // 紅太陽、黑地球：貼在外圈左右（水平直徑端點）
  "design-sun": {
    x: CHART_CENTER.x - CHART_RING_R,
    y: CHART_CENTER.y,
  }, // 紅太陽（光芒）
  "design-venus": { x: 500, y: 500 }, // 紅金星（SQ）
  "personality-earth": {
    x: CHART_CENTER.x + CHART_RING_R,
    y: CHART_CENTER.y,
  }, // 黑地球（進化）
  // 黑金星／黑火星在紅月亮左上、右上；紅月亮居中偏下（整體略上移）
  "personality-venus": { x: 340, y: 630 }, // 黑金星（智商）— 紅月亮左上
  "personality-mars": { x: 660, y: 630 }, // 黑火星（情商）— 紅月亮右上
  "design-moon": { x: 500, y: 740 }, // 紅月亮（吸引力）
  "design-earth": { x: 500, y: 900 }, // 紅地球（使命）
};

function findPlanet(list: PlanetInfo[] | undefined, planet: string) {
  return list?.find((p) => p.planet === planet);
}

export function buildGeneKeyNodes(
  personalityList?: PlanetInfo[],
  designList?: PlanetInfo[]
): GeneKeyNode[] {
  const pSun = findPlanet(personalityList, "Sun");
  const pEarth = findPlanet(personalityList, "Earth");
  const pVenus = findPlanet(personalityList, "Venus");
  const pMars = findPlanet(personalityList, "Mars");
  const pJupiter = findPlanet(personalityList, "Jupiter");
  const dSun = findPlanet(designList, "Sun");
  const dEarth = findPlanet(designList, "Earth");
  const dMoon = findPlanet(designList, "Moon");
  const dVenus = findPlanet(designList, "Venus");
  const dMars = findPlanet(designList, "Mars");
  const dJupiter = findPlanet(designList, "Jupiter");

  return [
    {
      id: "personality-sun",
      label: "黑太陽",
      value: pSun?.gate_line || "—",
      color: "green",
      gridRow: 1,
      gridCol: 3,
      description: "人生事業",
      sequence: "genius",
      sequences: ["genius", "prosperity"],
      prosperityColor: "blue",
      gate: pSun?.gate,
    },
    {
      id: "design-mars",
      label: "紅火星",
      value: dMars?.gate_line || "—",
      color: "blue",
      gridRow: 2,
      gridCol: 2,
      description: "核心",
      sequence: "prosperity",
      sequences: ["prosperity", "love"],
      loveColor: "orange",
      gate: dMars?.gate,
    },
    {
      id: "personality-jupiter",
      label: "黑木星",
      value: pJupiter?.gate_line || "—",
      color: "blue",
      gridRow: 2,
      gridCol: 3,
      description: "珍珠",
      sequence: "prosperity",
      gate: pJupiter?.gate,
    },
    {
      id: "design-jupiter",
      label: "紅木星",
      value: dJupiter?.gate_line || "—",
      color: "blue",
      gridRow: 2,
      gridCol: 4,
      description: "文化",
      sequence: "prosperity",
      gate: dJupiter?.gate,
    },
    {
      id: "design-sun",
      label: "紅太陽",
      value: dSun?.gate_line || "—",
      color: "green",
      gridRow: 3,
      gridCol: 1,
      description: "光芒",
      sequence: "genius",
      gate: dSun?.gate,
    },
    {
      id: "design-venus",
      label: "紅金星",
      value: dVenus?.gate_line || "—",
      color: "orange",
      gridRow: 3,
      gridCol: 3,
      description: "穩定頻率",
      sequence: "love",
      gate: dVenus?.gate,
    },
    {
      id: "personality-earth",
      label: "黑地球",
      value: pEarth?.gate_line || "—",
      color: "green",
      gridRow: 3,
      gridCol: 5,
      description: "進化",
      sequence: "genius",
      gate: pEarth?.gate,
    },
    {
      id: "personality-venus",
      label: "黑金星",
      value: pVenus?.gate_line || "—",
      color: "orange",
      gridRow: 4,
      gridCol: 2,
      description: "智商",
      sequence: "love",
      gate: pVenus?.gate,
    },
    {
      id: "design-moon",
      label: "紅月亮",
      value: dMoon?.gate_line || "—",
      color: "orange",
      gridRow: 4,
      gridCol: 3,
      description: "吸引力",
      sequence: "love",
      gate: dMoon?.gate,
    },
    {
      id: "personality-mars",
      label: "黑火星",
      value: pMars?.gate_line || "—",
      color: "orange",
      gridRow: 4,
      gridCol: 4,
      description: "情商",
      sequence: "love",
      gate: pMars?.gate,
    },
    {
      id: "design-earth",
      label: "紅地球",
      value: dEarth?.gate_line || "—",
      color: "green",
      gridRow: 5,
      gridCol: 3,
      description: "人生目的",
      sequence: "genius",
      sequences: ["genius", "love"],
      loveColor: "orange",
      gate: dEarth?.gate,
    },
  ];
}

/** 連線依 NODE_POSITIONS 自動取端點，勿寫死像素 */
export const GENE_KEY_CONNECTIONS: GeneKeyConnection[] = [
  // 藍色：珍珠序列
  { from: "personality-sun", to: "design-mars", color: "blue", sequence: "prosperity", pathId: "initiative" },
  { from: "personality-sun", to: "design-jupiter", color: "blue", sequence: "prosperity", pathId: "initiative" },
  { from: "design-mars", to: "design-jupiter", color: "blue", sequence: "prosperity", pathId: "growth" },
  { from: "personality-jupiter", to: "personality-sun", color: "blue", sequence: "prosperity", pathId: "service" },
  { from: "personality-jupiter", to: "design-mars", color: "blue", sequence: "prosperity", pathId: "service" },
  { from: "personality-jupiter", to: "design-jupiter", color: "blue", sequence: "prosperity", pathId: "service" },

  // 綠色：啟動序列
  { from: "personality-sun", to: "personality-earth", color: "green", sequence: "genius", pathId: "challenge" },
  { from: "design-sun", to: "design-earth", color: "green", sequence: "genius", pathId: "core-stability" },
  { from: "design-sun", to: "design-venus", color: "green", sequence: "genius", pathId: "breakthrough" },
  { from: "design-venus", to: "personality-earth", color: "green", sequence: "genius", pathId: "breakthrough" },

  // 紅色：金星序列
  { from: "design-mars", to: "design-venus", color: "red", sequence: "love", pathId: "realisation" },
  { from: "design-venus", to: "personality-mars", color: "red", sequence: "love", pathId: "love" },
  { from: "personality-venus", to: "personality-mars", color: "red", sequence: "love", pathId: "intelligence" },
  { from: "personality-venus", to: "design-moon", color: "red", sequence: "love", pathId: "karma" },
  { from: "design-moon", to: "design-earth", color: "red", sequence: "love", pathId: "dharma" },
];

export function getNodePosition(id: string): { x: number; y: number } | undefined {
  return NODE_POSITIONS[id];
}

/** 依序列計算放大用 viewBox（正方形，置中該區節點） */
export function getSequenceViewBox(
  filter: SequenceFilter,
  nodes: GeneKeyNode[],
  positions: Record<string, { x: number; y: number }> = NODE_POSITIONS
): string {
  const FULL = "0 0 1000 1000";
  if (filter === "all") return FULL;

  const ids = nodes
    .filter((n) => (n.sequences || [n.sequence]).includes(filter))
    .map((n) => n.id);

  if (!ids.length) return FULL;

  const EXT = 100; // 球體 + 標籤緩衝
  let minX = Infinity;
  let minY = Infinity;
  let maxX = -Infinity;
  let maxY = -Infinity;

  for (const id of ids) {
    const p = positions[id];
    if (!p) continue;
    minX = Math.min(minX, p.x - EXT);
    maxX = Math.max(maxX, p.x + EXT);
    minY = Math.min(minY, p.y - EXT);
    maxY = Math.max(maxY, p.y + EXT + 36);
  }

  if (!Number.isFinite(minX)) return FULL;

  const width = maxX - minX;
  const height = maxY - minY;
  // 略留邊，並維持正方形以配合 aspect-square
  const pad = filter === "prosperity" ? 72 : 36;
  const size = Math.max(width, height) + pad * 2;
  // 關係／服務：數值越大＝放大越少（viewBox 越大）
  const zoom = filter === "love" ? 0.92 : filter === "prosperity" ? 1.05 : 0.95;
  const viewSize = Math.min(1000, Math.max(420, size * zoom));
  const cx = (minX + maxX) / 2;
  const cy = (minY + maxY) / 2;

  let x = cx - viewSize / 2;
  let y = cy - viewSize / 2;
  // 避免過度超出畫布（允許些微溢出以利構圖）
  x = Math.max(-40, Math.min(x, 1000 - viewSize + 40));
  y = Math.max(-40, Math.min(y, 1000 - viewSize + 40));

  return `${x.toFixed(1)} ${y.toFixed(1)} ${viewSize.toFixed(1)} ${viewSize.toFixed(1)}`;
}

/** @deprecated 改用 NODE_POSITIONS */
export function getCenterPoint(gridRow: number, gridCol: number) {
  const minX = 180;
  const maxX = 820;
  const minY = 120;
  const maxY = 880;
  const cellWidth = (maxX - minX) / 4;
  const cellHeight = (maxY - minY) / 4;
  return {
    x: minX + (gridCol - 1) * cellWidth,
    y: minY + (gridRow - 1) * cellHeight,
  };
}

export const CONNECTION_STROKE: Record<string, string> = {
  green: "#76a07b",
  red: "#c0392b",
  blue: "#3498db",
};

export const PLANET_LABELS: Record<string, string> = {
  Sun: "太陽",
  Earth: "地球",
  Moon: "月亮",
  "North Node": "北交點",
  "South Node": "南交點",
  Mercury: "水星",
  Venus: "金星",
  Mars: "火星",
  Jupiter: "木星",
  Saturn: "土星",
  Uranus: "天王星",
  Neptune: "海王星",
  Pluto: "冥王星",
};
