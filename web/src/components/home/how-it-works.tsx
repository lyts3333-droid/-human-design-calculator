"use client";

import { motion } from "framer-motion";
import { CalendarDays, Compass, Sparkles, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

type StepTone = "purple" | "blue" | "green";

type Step = {
  id: number;
  tone: StepTone;
  title: string;
  body: string;
  cta: string;
  target: string;
  visual: "chart" | "decode" | "live";
};

const STEPS: Step[] = [
  {
    id: 1,
    tone: "purple",
    title: "建立你的免費人生圖",
    body: "輸入出生日期、出生時間與出生地點，即可立即產生專屬的人類圖與人生藍圖，快速了解你的天賦與人生方向。",
    cta: "立即建立人生圖",
    target: "form",
    visual: "chart",
  },
  {
    id: 2,
    tone: "blue",
    title: "解讀你的核心設計",
    body: "深入了解你的類型、策略、內在權威、人生角色、九大能量中心與人生使命，幫助你做出更適合自己的選擇。",
    cta: "開始閱讀解析",
    target: "results",
    visual: "decode",
  },
  {
    id: 3,
    tone: "green",
    title: "開始玩轉人生",
    body: "將人類圖的洞察應用到工作、關係、決策與個人成長，活出真正符合自己設計的人生。",
    cta: "開始探索人生藍圖",
    target: "form",
    visual: "live",
  },
];

const TONE = {
  purple: {
    accent: "#6F6CFF",
    soft: "rgba(111,108,255,0.18)",
    glow: "rgba(111,108,255,0.45)",
    border: "border-primary/35",
    text: "text-primary",
    btn: "border-primary/50 text-primary hover:bg-primary/10 hover:border-primary hover:shadow-[0_0_28px_rgba(111,108,255,0.35)]",
    badge: "bg-primary/15 text-primary",
  },
  blue: {
    accent: "#4EC5FF",
    soft: "rgba(78,197,255,0.16)",
    glow: "rgba(78,197,255,0.4)",
    border: "border-secondary/35",
    text: "text-secondary",
    btn: "border-secondary/50 text-secondary hover:bg-secondary/10 hover:border-secondary hover:shadow-[0_0_28px_rgba(78,197,255,0.35)]",
    badge: "bg-secondary/15 text-secondary",
  },
  green: {
    accent: "#3DDB9A",
    soft: "rgba(61,219,154,0.14)",
    glow: "rgba(61,219,154,0.38)",
    border: "border-success/35",
    text: "text-success",
    btn: "border-success/50 text-success hover:bg-success/10 hover:border-success hover:shadow-[0_0_28px_rgba(61,219,154,0.35)]",
    badge: "bg-success/15 text-success",
  },
} as const;

function scrollToId(id: string) {
  const el = document.getElementById(id);
  if (el) {
    el.scrollIntoView({ behavior: "smooth", block: "start" });
    return;
  }
  if (id === "results") {
    document.getElementById("about")?.scrollIntoView({ behavior: "smooth" });
    return;
  }
  document.getElementById("form")?.scrollIntoView({ behavior: "smooth" });
}

function StepVisual({ kind, tone }: { kind: Step["visual"]; tone: StepTone }) {
  const t = TONE[tone];
  return (
    <div className="relative mx-auto aspect-square w-full max-w-[340px]">
      <div
        className="absolute inset-6 rounded-full blur-3xl transition-opacity duration-500 group-hover:opacity-100"
        style={{ background: t.soft, opacity: 0.85 }}
      />
      <motion.div
        whileHover={{ y: -6 }}
        transition={{ type: "spring", stiffness: 260, damping: 22 }}
        className={cn(
          "relative flex h-full flex-col justify-between overflow-hidden rounded-[1.75rem] border bg-white/[0.06] p-7 shadow-[0_24px_80px_rgba(0,0,0,0.35)] backdrop-blur-2xl",
          t.border
        )}
        style={{ boxShadow: `0 0 0 1px ${t.soft}, 0 24px 80px rgba(0,0,0,0.35), 0 0 60px ${t.soft}` }}
      >
        <div
          className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full blur-2xl"
          style={{ background: t.soft }}
        />
        <div className={cn("inline-flex w-fit items-center gap-2 rounded-full px-3 py-1 text-[11px] tracking-[0.2em]", t.badge)}>
          {kind === "chart" && <CalendarDays className="h-3.5 w-3.5" />}
          {kind === "decode" && <Sparkles className="h-3.5 w-3.5" />}
          {kind === "live" && <Compass className="h-3.5 w-3.5" />}
          {kind === "chart" ? "BIRTH DATA" : kind === "decode" ? "CORE DESIGN" : "LIFE PATH"}
        </div>

        {kind === "chart" && <ChartIllustration color={t.accent} />}
        {kind === "decode" && <DecodeIllustration color={t.accent} />}
        {kind === "live" && <LiveIllustration color={t.accent} />}

        <div className="relative z-10 space-y-1">
          <div className="h-1.5 w-16 rounded-full" style={{ background: t.accent, opacity: 0.7 }} />
          <div className="h-1.5 w-24 rounded-full bg-white/10" />
          <div className="h-1.5 w-12 rounded-full bg-white/10" />
        </div>
      </motion.div>
    </div>
  );
}

function ChartIllustration({ color }: { color: string }) {
  return (
    <svg viewBox="0 0 220 140" className="relative z-10 my-4 w-full" aria-hidden>
      <circle cx="110" cy="70" r="52" fill="none" stroke={color} strokeOpacity="0.25" strokeWidth="1.5" />
      <circle cx="110" cy="70" r="34" fill="none" stroke={color} strokeOpacity="0.45" strokeWidth="1.5" />
      <circle cx="110" cy="70" r="8" fill={color} fillOpacity="0.9" />
      {[0, 60, 120, 180, 240, 300].map((deg) => {
        const a = ((deg - 90) * Math.PI) / 180;
        const x = 110 + Math.cos(a) * 34;
        const y = 70 + Math.sin(a) * 34;
        return <circle key={deg} cx={x} cy={y} r="5" fill={color} fillOpacity="0.75" />;
      })}
      <rect x="24" y="28" width="48" height="10" rx="5" fill={color} fillOpacity="0.2" />
      <rect x="24" y="46" width="36" height="8" rx="4" fill="white" fillOpacity="0.12" />
      <rect x="148" y="88" width="48" height="10" rx="5" fill={color} fillOpacity="0.2" />
      <rect x="156" y="106" width="36" height="8" rx="4" fill="white" fillOpacity="0.12" />
    </svg>
  );
}

function DecodeIllustration({ color }: { color: string }) {
  const centers = [
    [110, 18],
    [78, 42],
    [142, 42],
    [110, 66],
    [78, 90],
    [142, 90],
    [110, 114],
  ];
  return (
    <svg viewBox="0 0 220 140" className="relative z-10 my-4 w-full" aria-hidden>
      <path
        d="M110 18 L78 42 L110 66 L142 42 Z M110 66 L78 90 L110 114 L142 90 Z"
        fill="none"
        stroke={color}
        strokeOpacity="0.35"
        strokeWidth="1.5"
      />
      {centers.map(([x, y], i) => (
        <circle
          key={i}
          cx={x}
          cy={y}
          r={i === 3 ? 9 : 7}
          fill={i % 2 === 0 ? color : "transparent"}
          fillOpacity={i % 2 === 0 ? 0.85 : 0}
          stroke={color}
          strokeWidth="1.5"
          strokeOpacity="0.8"
        />
      ))}
    </svg>
  );
}

function LiveIllustration({ color }: { color: string }) {
  return (
    <svg viewBox="0 0 220 140" className="relative z-10 my-4 w-full" aria-hidden>
      <circle cx="110" cy="72" r="46" fill="none" stroke={color} strokeOpacity="0.25" strokeWidth="1.5" />
      <circle cx="110" cy="72" r="28" fill="none" stroke={color} strokeOpacity="0.4" strokeWidth="1.5" strokeDasharray="4 6" />
      <path
        d="M110 36 L118 68 L150 72 L118 80 L110 112 L102 80 L70 72 L102 68 Z"
        fill={color}
        fillOpacity="0.2"
        stroke={color}
        strokeWidth="1.5"
      />
      <circle cx="110" cy="72" r="4" fill={color} />
      <path d="M42 108 C70 92, 150 92, 178 108" fill="none" stroke={color} strokeOpacity="0.35" strokeWidth="2" />
    </svg>
  );
}

function CurvedArrow({ flip, tone }: { flip?: boolean; tone: StepTone }) {
  const color = TONE[tone].accent;
  const gradId = `journey-arrow-${tone}`;
  return (
    <div className="pointer-events-none relative mx-auto hidden h-24 w-full max-w-3xl md:block" aria-hidden>
      <svg
        viewBox="0 0 640 96"
        className={cn("h-full w-full", flip && "scale-x-[-1]")}
        fill="none"
      >
        <defs>
          <linearGradient id={gradId} x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor={color} stopOpacity="0" />
            <stop offset="40%" stopColor={color} stopOpacity="0.55" />
            <stop offset="100%" stopColor={color} stopOpacity="0.15" />
          </linearGradient>
        </defs>
        <path
          d="M40 20 C180 20, 220 76, 320 76 C420 76, 460 20, 600 20"
          stroke={`url(#${gradId})`}
          strokeWidth="2"
          strokeLinecap="round"
        />
        <path
          d="M582 10 L600 20 L582 30"
          stroke={color}
          strokeOpacity="0.55"
          strokeWidth="2"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
      </svg>
    </div>
  );
}

export function HowItWorks() {
  return (
    <section
      id="how-it-works"
      className="relative mx-auto max-w-6xl px-5 py-20 md:px-8 md:py-28"
    >
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, margin: "-80px" }}
        transition={{ duration: 0.7 }}
        className="mx-auto mb-16 max-w-2xl text-center md:mb-24"
      >
        <p className="text-xs tracking-[0.28em] text-muted">YOUR JOURNEY</p>
        <h2 className="mt-4 text-3xl font-semibold tracking-wide text-accent-light md:text-4xl">
          三個步驟，開始玩轉人生
        </h2>
        <p className="mt-4 text-base leading-8 text-muted">
          從建立人生圖，到理解核心設計，再到把洞察帶進日常——用屬於你的節奏前進。
        </p>
      </motion.div>

      <div className="space-y-16 md:space-y-0">
        {STEPS.map((step, index) => {
          const t = TONE[step.tone];
          const imageLeft = index % 2 === 0;
          const fromX = imageLeft ? -36 : 36;

          return (
            <div key={step.id}>
              <motion.article
                initial={{ opacity: 0, y: 36, x: fromX }}
                whileInView={{ opacity: 1, y: 0, x: 0 }}
                viewport={{ once: true, margin: "-100px" }}
                transition={{ duration: 0.75, ease: [0.22, 1, 0.36, 1] }}
                className={cn(
                  "group grid items-center gap-10 md:gap-16 lg:gap-20",
                  "md:grid-cols-2"
                )}
              >
                <div className={cn(imageLeft ? "md:order-1" : "md:order-2")}>
                  <StepVisual kind={step.visual} tone={step.tone} />
                </div>

                <div
                  className={cn(
                    "relative rounded-[1.75rem] border border-white/10 bg-white/[0.045] p-8 backdrop-blur-2xl md:p-10",
                    "shadow-[inset_0_1px_0_rgba(255,255,255,0.06)]",
                    "transition duration-500 hover:border-white/20 hover:bg-white/[0.07]",
                    imageLeft ? "md:order-2" : "md:order-1"
                  )}
                  style={{
                    boxShadow: `inset 0 1px 0 rgba(255,255,255,0.06), 0 0 80px ${t.soft}`,
                  }}
                >
                  <div
                    className="pointer-events-none absolute -left-6 top-10 h-24 w-24 rounded-full blur-3xl"
                    style={{ background: t.soft }}
                  />

                  <div className={cn("mb-5 inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-medium tracking-[0.18em]", t.badge)}>
                    STEP {String(step.id).padStart(2, "0")}
                  </div>

                  <h3 className="text-2xl font-semibold leading-snug tracking-wide text-foreground md:text-[1.75rem]">
                    {step.title}
                  </h3>
                  <p className="mt-5 max-w-md text-base leading-8 text-muted">
                    {step.body}
                  </p>

                  <Button
                    variant="outline"
                    className={cn("mt-8 rounded-full", t.btn)}
                    onClick={() => scrollToId(step.target)}
                  >
                    {step.cta}
                    <ArrowRight className="h-4 w-4" />
                  </Button>
                </div>
              </motion.article>

              {index < STEPS.length - 1 && (
                <CurvedArrow
                  flip={index % 2 === 1}
                  tone={STEPS[index + 1].tone}
                />
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}
