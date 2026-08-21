/** 命盤底圖 Sacred Mandala（純裝飾，不影響節點座標） */

type Props = {
  cx: number;
  cy: number;
  /** 卦象環中心半徑 */
  radius?: number;
};

const GOLD = "#C6A96A";
const BRONZE = "#9E8353";
const GOLD_SOFT = "rgba(198,169,106,0.25)";

/** 伏羲先天：0–63 二進位六爻（底爻為最低位） */
function hexagramLines(index: number): number[] {
  return [0, 1, 2, 3, 4, 5].map((bit) => (index >> bit) & 1);
}

function polar(cx: number, cy: number, r: number, angle: number) {
  return {
    x: cx + Math.cos(angle) * r,
    y: cy + Math.sin(angle) * r,
  };
}

function HexagramMark({
  x,
  y,
  angle,
  lines,
  scale = 1,
}: {
  x: number;
  y: number;
  angle: number;
  lines: number[];
  scale?: number;
}) {
  const w = 10 * scale;
  const gap = 2.05 * scale;
  const stroke = 0.95 * scale;
  const breakGap = 2.2 * scale;
  const ordered = [...lines].reverse();

  return (
    <g transform={`translate(${x} ${y}) rotate(${(angle * 180) / Math.PI + 90})`}>
      {ordered.map((yang, i) => {
        const ly = -5.2 * scale + i * gap;
        if (yang) {
          return (
            <line
              key={i}
              x1={-w / 2}
              y1={ly}
              x2={w / 2}
              y2={ly}
              stroke={GOLD}
              strokeOpacity={0.42}
              strokeWidth={stroke}
              strokeLinecap="round"
            />
          );
        }
        return (
          <g key={i}>
            <line
              x1={-w / 2}
              y1={ly}
              x2={-breakGap / 2}
              y2={ly}
              stroke={GOLD}
              strokeOpacity={0.42}
              strokeWidth={stroke}
              strokeLinecap="round"
            />
            <line
              x1={breakGap / 2}
              y1={ly}
              x2={w / 2}
              y2={ly}
              stroke={GOLD}
              strokeOpacity={0.42}
              strokeWidth={stroke}
              strokeLinecap="round"
            />
          </g>
        );
      })}
    </g>
  );
}

/** Seed of Life：中心 + 六圍 */
function SeedOfLife({ cx, cy, r }: { cx: number; cy: number; r: number }) {
  const centers = [
    { x: cx, y: cy },
    ...Array.from({ length: 6 }, (_, i) => {
      const a = (i / 6) * Math.PI * 2 - Math.PI / 2;
      return polar(cx, cy, r, a);
    }),
  ];
  return (
    <g opacity={0.055}>
      {centers.map((c, i) => (
        <circle
          key={i}
          cx={c.x}
          cy={c.y}
          r={r}
          fill="none"
          stroke={GOLD}
          strokeWidth={0.9}
        />
      ))}
    </g>
  );
}

/** Flower of Life（兩環花瓣） */
function FlowerOfLife({ cx, cy, r }: { cx: number; cy: number; r: number }) {
  const centers: { x: number; y: number }[] = [{ x: cx, y: cy }];
  for (let ring = 1; ring <= 2; ring++) {
    const count = ring * 6;
    for (let i = 0; i < count; i++) {
      const a = (i / count) * Math.PI * 2 - Math.PI / 2;
      centers.push(polar(cx, cy, r * ring, a));
    }
  }
  return (
    <g opacity={0.04}>
      <circle
        cx={cx}
        cy={cy}
        r={r * 3}
        fill="none"
        stroke={BRONZE}
        strokeWidth={0.7}
      />
      {centers.map((c, i) => (
        <circle
          key={i}
          cx={c.x}
          cy={c.y}
          r={r}
          fill="none"
          stroke={GOLD}
          strokeWidth={0.75}
        />
      ))}
    </g>
  );
}

/** Metatron's Cube：13 圓心連線 */
function MetatronCube({ cx, cy, r }: { cx: number; cy: number; r: number }) {
  const pts: { x: number; y: number }[] = [{ x: cx, y: cy }];
  for (let ring = 1; ring <= 2; ring++) {
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2 - Math.PI / 2;
      pts.push(polar(cx, cy, r * ring, a));
    }
  }
  const lines: [number, number][] = [];
  for (let i = 0; i < pts.length; i++) {
    for (let j = i + 1; j < pts.length; j++) {
      lines.push([i, j]);
    }
  }
  return (
    <g opacity={0.035}>
      {pts.map((p, i) => (
        <circle
          key={`m-c-${i}`}
          cx={p.x}
          cy={p.y}
          r={r * 0.22}
          fill="none"
          stroke={GOLD}
          strokeWidth={0.6}
        />
      ))}
      {lines.map(([i, j]) => (
        <line
          key={`m-l-${i}-${j}`}
          x1={pts[i].x}
          y1={pts[i].y}
          x2={pts[j].x}
          y2={pts[j].y}
          stroke={BRONZE}
          strokeWidth={0.35}
        />
      ))}
    </g>
  );
}

/** 黃金比例弧 */
function GoldenRatioArcs({ cx, cy }: { cx: number; cy: number }) {
  const phi = 1.618;
  const base = 55;
  const arcs = [0, 1, 2, 3, 4].map((i) => base * Math.pow(phi, i));
  return (
    <g opacity={0.05}>
      {arcs.map((r, i) => (
        <path
          key={i}
          d={`M ${cx + r} ${cy} A ${r} ${r} 0 0 1 ${cx} ${cy + r}`}
          fill="none"
          stroke={GOLD}
          strokeWidth={0.8}
          strokeLinecap="round"
        />
      ))}
      {arcs.map((r, i) => (
        <path
          key={`m-${i}`}
          d={`M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx} ${cy - r}`}
          fill="none"
          stroke={BRONZE}
          strokeWidth={0.6}
        />
      ))}
    </g>
  );
}

function CompassMarker({
  cx,
  cy,
  angle,
  r,
}: {
  cx: number;
  cy: number;
  angle: number;
  r: number;
}) {
  const tip = polar(cx, cy, r + 14, angle);
  const baseL = polar(cx, cy, r + 2, angle - 0.035);
  const baseR = polar(cx, cy, r + 2, angle + 0.035);
  const diamond = polar(cx, cy, r - 8, angle);
  const cross = polar(cx, cy, r + 22, angle);

  return (
    <g opacity={0.55}>
      <polygon
        points={`${tip.x},${tip.y} ${baseL.x},${baseL.y} ${baseR.x},${baseR.y}`}
        fill={GOLD}
        fillOpacity={0.55}
      />
      <rect
        x={diamond.x - 3}
        y={diamond.y - 3}
        width={6}
        height={6}
        fill="none"
        stroke={GOLD}
        strokeOpacity={0.65}
        strokeWidth={0.8}
        transform={`rotate(45 ${diamond.x} ${diamond.y})`}
      />
      <line
        x1={cross.x - 4}
        y1={cross.y}
        x2={cross.x + 4}
        y2={cross.y}
        stroke={BRONZE}
        strokeWidth={0.8}
        strokeOpacity={0.7}
      />
      <line
        x1={cross.x}
        y1={cross.y - 4}
        x2={cross.x}
        y2={cross.y + 4}
        stroke={BRONZE}
        strokeWidth={0.8}
        strokeOpacity={0.7}
      />
    </g>
  );
}

function MiniDiamond({
  cx,
  cy,
  angle,
  r,
}: {
  cx: number;
  cy: number;
  angle: number;
  r: number;
}) {
  const p = polar(cx, cy, r, angle);
  return (
    <rect
      x={p.x - 2.2}
      y={p.y - 2.2}
      width={4.4}
      height={4.4}
      fill="none"
      stroke={GOLD}
      strokeOpacity={0.35}
      strokeWidth={0.7}
      transform={`rotate(45 ${p.x} ${p.y})`}
    />
  );
}

function MiniTriangle({
  cx,
  cy,
  angle,
  r,
  outward,
}: {
  cx: number;
  cy: number;
  angle: number;
  r: number;
  outward?: boolean;
}) {
  const tip = polar(cx, cy, outward ? r + 6 : r - 6, angle);
  const a = polar(cx, cy, r, angle - 0.028);
  const b = polar(cx, cy, r, angle + 0.028);
  return (
    <polygon
      points={`${tip.x},${tip.y} ${a.x},${a.y} ${b.x},${b.y}`}
      fill="none"
      stroke={BRONZE}
      strokeOpacity={0.4}
      strokeWidth={0.7}
    />
  );
}

export function IChingWheel({ cx, cy, radius = 455 }: Props) {
  // 多層同心圓半徑（由外到內）
  const R = {
    bloom: radius + 42,
    outerFine: radius + 34,
    tickOuter: radius + 26,
    tickInner: radius + 18,
    hex: radius,
    hexBandOuter: radius + 12,
    hexBandInner: radius - 14,
    midA: radius - 36,
    midB: radius - 72,
    midC: radius - 118,
    sacred: 168,
    seed: 92,
    innerGlow: 70,
    core: 28,
  };

  const ticks360 = Array.from({ length: 360 }, (_, i) => {
    const a = (i / 360) * Math.PI * 2 - Math.PI / 2;
    const major = i % 30 === 0;
    const mid = i % 10 === 0;
    const len = major ? 11 : mid ? 7 : 4;
    return {
      a,
      r0: R.tickOuter - len,
      r1: R.tickOuter,
      major,
      mid,
    };
  });

  const cardinals = [-Math.PI / 2, 0, Math.PI / 2, Math.PI];
  const interCardinals = cardinals.map((a) => a + Math.PI / 4);

  return (
    <g className="pointer-events-none" aria-hidden>
      <defs>
        <radialGradient id="mandala-outer-glow" cx="50%" cy="50%" r="50%">
          <stop offset="72%" stopColor={GOLD} stopOpacity="0" />
          <stop offset="88%" stopColor={GOLD} stopOpacity="0.05" />
          <stop offset="100%" stopColor={GOLD} stopOpacity="0.11" />
        </radialGradient>
        <radialGradient id="mandala-soft-bloom" cx="50%" cy="48%" r="52%">
          <stop offset="0%" stopColor={GOLD} stopOpacity="0.04" />
          <stop offset="45%" stopColor={BRONZE} stopOpacity="0.02" />
          <stop offset="100%" stopColor="#050816" stopOpacity="0" />
        </radialGradient>
        <filter id="mandala-blur" x="-20%" y="-20%" width="140%" height="140%">
          <feGaussianBlur stdDeviation="1.2" />
        </filter>
      </defs>

      {/* —— 後景：柔光與神聖幾何 —— */}
      <circle cx={cx} cy={cy} r={R.bloom} fill="url(#mandala-outer-glow)" />
      <circle cx={cx} cy={cy} r={R.hexBandInner} fill="url(#mandala-soft-bloom)" />

      <FlowerOfLife cx={cx} cy={cy} r={R.sacred / 2.15} />
      <MetatronCube cx={cx} cy={cy} r={R.sacred / 2.4} />
      <SeedOfLife cx={cx} cy={cy} r={R.seed} />
      <GoldenRatioArcs cx={cx} cy={cy} />

      {/* 極淡內六芒星（非雷達放射線） */}
      <g opacity={0.045}>
        {[0, 1].map((k) => (
          <polygon
            key={k}
            points={Array.from({ length: 6 }, (_, i) => {
              const a = (i / 6) * Math.PI * 2 - Math.PI / 2 + (k * Math.PI) / 6;
              const p = polar(cx, cy, R.sacred * 0.95, a);
              return `${p.x},${p.y}`;
            }).join(" ")}
            fill="none"
            stroke={GOLD}
            strokeWidth={0.9}
          />
        ))}
      </g>

      {/* —— 中景：多層同心圓 —— */}
      {(
        [
          [R.outerFine, 0.9, 0.28],
          [R.tickOuter, 0.7, 0.18],
          [R.hexBandOuter, 1.1, 0.22],
          [R.hexBandInner, 1.0, 0.2],
          [R.midA, 0.75, 0.16],
          [R.midB, 0.65, 0.13],
          [R.midC, 0.55, 0.1],
          [R.sacred, 0.7, 0.12],
          [R.seed, 0.6, 0.1],
          [R.innerGlow, 0.5, 0.08],
        ] as const
      ).map(([r, w, op]) => (
        <circle
          key={`ring-${r}`}
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={GOLD}
          strokeOpacity={op}
          strokeWidth={w}
        />
      ))}

      {/* 卦帶微光底 */}
      <circle
        cx={cx}
        cy={cy}
        r={(R.hexBandOuter + R.hexBandInner) / 2}
        fill="none"
        stroke={GOLD_SOFT}
        strokeWidth={R.hexBandOuter - R.hexBandInner}
        opacity={0.35}
      />

      {/* 分段弧（HUD 感，非完整雷達） */}
      <g filter="url(#mandala-blur)" opacity={0.35}>
        {[0, 1, 2, 3].map((i) => {
          const start = -Math.PI / 2 + (i * Math.PI) / 2 + 0.18;
          const end = start + Math.PI / 2 - 0.36;
          const r = R.midA - 10;
          const s = polar(cx, cy, r, start);
          const e = polar(cx, cy, r, end);
          return (
            <path
              key={`arc-${i}`}
              d={`M ${s.x} ${s.y} A ${r} ${r} 0 0 1 ${e.x} ${e.y}`}
              fill="none"
              stroke={BRONZE}
              strokeWidth={1.2}
              strokeOpacity={0.5}
              strokeLinecap="round"
            />
          );
        })}
      </g>

      {/* —— 前景外圈：360° 細刻度（圓周刻度，非放射網格） —— */}
      {ticks360.map((t, i) => (
        <line
          key={`tick-${i}`}
          x1={cx + Math.cos(t.a) * t.r0}
          y1={cy + Math.sin(t.a) * t.r0}
          x2={cx + Math.cos(t.a) * t.r1}
          y2={cy + Math.sin(t.a) * t.r1}
          stroke={t.major ? GOLD : BRONZE}
          strokeOpacity={t.major ? 0.48 : t.mid ? 0.28 : 0.14}
          strokeWidth={t.major ? 1.05 : 0.65}
        />
      ))}

      {/* 六十四卦 */}
      {Array.from({ length: 64 }, (_, i) => {
        const a = (i / 64) * Math.PI * 2 - Math.PI / 2;
        const p = polar(cx, cy, R.hex, a);
        return (
          <HexagramMark
            key={`hx-${i}`}
            x={p.x}
            y={p.y}
            angle={a}
            lines={hexagramLines(i)}
            scale={1}
          />
        );
      })}

      {/* 卦與卦之間的微型分隔短線 */}
      {Array.from({ length: 64 }, (_, i) => {
        const a = ((i + 0.5) / 64) * Math.PI * 2 - Math.PI / 2;
        const inner = polar(cx, cy, R.hexBandInner + 2, a);
        const outer = polar(cx, cy, R.hexBandOuter - 2, a);
        return (
          <line
            key={`sep-${i}`}
            x1={inner.x}
            y1={inner.y}
            x2={outer.x}
            y2={outer.y}
            stroke={BRONZE}
            strokeOpacity={0.18}
            strokeWidth={0.6}
          />
        );
      })}

      {/* 四方位 compass + 交方位菱形／三角 */}
      {cardinals.map((a, i) => (
        <CompassMarker key={`card-${i}`} cx={cx} cy={cy} angle={a} r={R.outerFine} />
      ))}
      {interCardinals.map((a, i) => (
        <g key={`inter-${i}`}>
          <MiniDiamond cx={cx} cy={cy} angle={a} r={R.outerFine + 6} />
          <MiniTriangle cx={cx} cy={cy} angle={a} r={R.tickInner} outward />
        </g>
      ))}

      {/* 環上微型裝飾菱形（每 22.5°） */}
      {Array.from({ length: 16 }, (_, i) => {
        const a = (i / 16) * Math.PI * 2 - Math.PI / 2;
        if (i % 4 === 0) return null;
        return (
          <MiniDiamond
            key={`dec-${i}`}
            cx={cx}
            cy={cy}
            angle={a}
            r={R.midB}
          />
        );
      })}

      {/* 最外細金環 + 核心淡環 */}
      <circle
        cx={cx}
        cy={cy}
        r={R.bloom - 4}
        fill="none"
        stroke={GOLD}
        strokeOpacity={0.22}
        strokeWidth={1}
      />
      <circle
        cx={cx}
        cy={cy}
        r={R.core}
        fill="none"
        stroke={GOLD}
        strokeOpacity={0.08}
        strokeWidth={0.8}
      />
    </g>
  );
}
