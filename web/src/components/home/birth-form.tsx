"use client";

import { useEffect, useMemo, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { MapPin, UserRound, Loader2, History, Trash2, X } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FieldLabel, Input, Select } from "@/components/ui/input";
import { chinaLocations, taiwanLocations } from "@/data/locations";
import type { BirthFormValues, HumanDesignResult } from "@/types/hd";
import { calculateHumanDesign } from "@/lib/api";
import {
  clearSearchHistory,
  historyLabel,
  loadSearchHistory,
  removeSearchHistory,
  upsertSearchHistory,
  type SearchHistoryItem,
} from "@/lib/search-history";

type Props = {
  onResult: (result: HumanDesignResult, form: BirthFormValues) => void;
};

function hourLabel(h: number) {
  if (h === 0) return "00 · 午夜";
  if (h === 12) return "12 · 中午";
  if (h < 12) return `${String(h).padStart(2, "0")} · 上午 ${h} 時`;
  return `${String(h).padStart(2, "0")} · 下午 ${h - 12} 時`;
}

const DEFAULT_FORM: BirthFormValues = {
  name: "",
  year: 1990,
  month: 9,
  day: 21,
  time: "12:00",
  region: "taiwan",
  county: "",
  district: "",
  timezone: "Asia/Taipei",
  longitude: 121.5,
  latitude: 25.0,
};

export function BirthForm({ onResult }: Props) {
  const [form, setForm] = useState<BirthFormValues>(DEFAULT_FORM);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "ok" | "err"; text: string } | null>(null);
  const [saveHistory, setSaveHistory] = useState(false);
  const [history, setHistory] = useState<SearchHistoryItem[]>([]);

  useEffect(() => {
    setHistory(loadSearchHistory());
  }, []);

  const regionMap = form.region === "china" ? chinaLocations : taiwanLocations;
  const counties = useMemo(() => Object.keys(regionMap), [regionMap]);
  const districts = useMemo(
    () => (form.county ? Object.keys(regionMap[form.county] || {}) : []),
    [form.county, regionMap]
  );

  const years = useMemo(() => {
    const current = new Date().getFullYear();
    return Array.from({ length: current - 1900 + 1 }, (_, i) => current - i);
  }, []);

  const months = useMemo(() => Array.from({ length: 12 }, (_, i) => i + 1), []);

  const daysInMonth = useMemo(
    () => new Date(form.year, form.month, 0).getDate(),
    [form.year, form.month]
  );

  const days = useMemo(
    () => Array.from({ length: daysInMonth }, (_, i) => i + 1),
    [daysInMonth]
  );

  const { hour, minute } = useMemo(() => {
    const [h = "12", m = "00"] = (form.time || "12:00").split(":");
    return { hour: Number(h), minute: Number(m) };
  }, [form.time]);

  const hours = useMemo(
    () =>
      Array.from({ length: 24 }, (_, h) => ({
        value: h,
        label: hourLabel(h),
      })),
    []
  );

  const minutes = useMemo(
    () => Array.from({ length: 60 }, (_, m) => m),
    []
  );

  const update = <K extends keyof BirthFormValues>(key: K, value: BirthFormValues[K]) => {
    setForm((prev) => ({ ...prev, [key]: value }));
  };

  const updateDate = (key: "year" | "month" | "day", value: number) => {
    setForm((prev) => {
      const next = { ...prev, [key]: value };
      const maxDay = new Date(next.year, next.month, 0).getDate();
      if (next.day > maxDay) next.day = maxDay;
      return next;
    });
  };

  const updateTime = (nextHour: number, nextMinute: number) => {
    update(
      "time",
      `${String(nextHour).padStart(2, "0")}:${String(nextMinute).padStart(2, "0")}`
    );
  };

  const onRegionChange = (region: "taiwan" | "china") => {
    setForm((prev) => ({
      ...prev,
      region,
      county: "",
      district: "",
      timezone: region === "taiwan" ? "Asia/Taipei" : "Asia/Shanghai",
      longitude: region === "taiwan" ? 121.5 : 116.4,
      latitude: region === "taiwan" ? 25.0 : 39.9,
    }));
  };

  const onCountyChange = (county: string) => {
    setForm((prev) => ({ ...prev, county, district: "" }));
  };

  const onDistrictChange = (district: string) => {
    const loc = regionMap[form.county]?.[district];
    setForm((prev) => ({
      ...prev,
      district,
      longitude: loc?.longitude ?? prev.longitude,
      latitude: loc?.latitude ?? prev.latitude,
    }));
  };

  const applyResult = (data: HumanDesignResult, values: BirthFormValues, saved: boolean) => {
    setMessage({
      type: "ok",
      text: saved ? "解析完成，已儲存至搜尋紀錄" : "解析完成，你的人生圖已就緒",
    });
    onResult(data, values);
    setTimeout(() => {
      document.getElementById("results")?.scrollIntoView({ behavior: "smooth" });
    }, 120);
  };

  const runCalculate = async (values: BirthFormValues, shouldSave: boolean) => {
    setLoading(true);
    setMessage(null);
    try {
      const res = await calculateHumanDesign(values);
      if (res.status === "success" && res.data) {
        if (shouldSave) {
          setHistory(upsertSearchHistory(values, res.data));
        }
        applyResult(res.data, values, shouldSave);
      } else {
        setMessage({ type: "err", text: res.error || "計算失敗，請檢查輸入資料" });
      }
    } catch {
      setMessage({
        type: "err",
        text: "無法連接到伺服器。請確認後端 API 正在運行。",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.county || !form.district) {
      setMessage({ type: "err", text: "請選擇出生地點的縣市與區域" });
      return;
    }
    await runCalculate(form, saveHistory);
  };

  const handleLoadHistory = async (item: SearchHistoryItem) => {
    setForm({ ...item.form });
    setSaveHistory(true);
    if (item.result) {
      applyResult(item.result, item.form, false);
      setHistory(upsertSearchHistory(item.form, item.result));
      return;
    }
    await runCalculate(item.form, true);
  };

  const handleClearHistory = () => {
    clearSearchHistory();
    setHistory([]);
  };

  return (
    <section id="form" className="mx-auto max-w-2xl px-5 py-10 md:px-8 md:py-16">
      <motion.div
        initial={{ opacity: 0, y: 24 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true, amount: 0.3 }}
        transition={{ duration: 0.6 }}
      >
        <div className="mb-8 text-center">
          <p className="text-xs uppercase tracking-[0.28em] text-accent-light">
            Free Profile
          </p>
          <h2 className="mt-2 text-3xl font-semibold tracking-wide text-foreground">
            輸入出生資訊
          </h2>
          <p className="mt-3 text-sm leading-7 text-muted">
            填寫出生日期、時間與地點，立即取得人類圖與基因天命黃金之路預覽。
          </p>
        </div>

        <Card hover={false} className="p-6 md:p-8">
          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <FieldLabel htmlFor="name">姓名（選填）</FieldLabel>
              <div className="relative">
                <UserRound className="pointer-events-none absolute left-3.5 top-1/2 h-4 w-4 -translate-y-1/2 text-muted" />
                <Input
                  id="name"
                  className="pl-10"
                  placeholder="例如：小明"
                  value={form.name}
                  onChange={(e) => update("name", e.target.value)}
                />
              </div>
            </div>

            <div>
              <FieldLabel>出生日期</FieldLabel>
              <div className="grid grid-cols-3 gap-3">
                <Select
                  required
                  aria-label="出生年"
                  value={form.year}
                  onChange={(e) => updateDate("year", Number(e.target.value))}
                >
                  {years.map((y) => (
                    <option key={y} value={y}>
                      {y} 年
                    </option>
                  ))}
                </Select>
                <Select
                  required
                  aria-label="出生月"
                  value={form.month}
                  onChange={(e) => updateDate("month", Number(e.target.value))}
                >
                  {months.map((m) => (
                    <option key={m} value={m}>
                      {m} 月
                    </option>
                  ))}
                </Select>
                <Select
                  required
                  aria-label="出生日"
                  value={form.day}
                  onChange={(e) => updateDate("day", Number(e.target.value))}
                >
                  {days.map((d) => (
                    <option key={d} value={d}>
                      {d} 日
                    </option>
                  ))}
                </Select>
              </div>
            </div>

            <div>
              <FieldLabel>
                出生時間
                <span className="ml-1 font-normal tracking-normal text-muted/80">
                  （不確定出生時間？可先輸入 12:00 試算）
                </span>
              </FieldLabel>
              <div className="grid grid-cols-[1fr_auto_1fr] items-center gap-2">
                <Select
                  required
                  aria-label="時"
                  value={hour}
                  onChange={(e) => updateTime(Number(e.target.value), minute)}
                >
                  {hours.map((h) => (
                    <option key={h.value} value={h.value}>
                      {h.label}
                    </option>
                  ))}
                </Select>
                <span className="text-center text-lg text-muted">:</span>
                <Select
                  required
                  aria-label="分"
                  value={minute}
                  onChange={(e) => updateTime(hour, Number(e.target.value))}
                >
                  {minutes.map((m) => (
                    <option key={m} value={m}>
                      {String(m).padStart(2, "0")} 分
                    </option>
                  ))}
                </Select>
              </div>
            </div>

            <div>
              <FieldLabel>
                出生地點
                <span className="ml-1 font-normal tracking-normal text-muted/80">
                  （找不到城市時，請選同一時區的鄰近主要城市）
                </span>
              </FieldLabel>
              <div className="grid gap-3 md:grid-cols-3">
                <div className="relative">
                  <MapPin className="pointer-events-none absolute left-3.5 top-1/2 z-10 h-4 w-4 -translate-y-1/2 text-muted" />
                  <Select
                    required
                    className="pl-10"
                    value={form.region}
                    onChange={(e) =>
                      onRegionChange(e.target.value as "taiwan" | "china")
                    }
                  >
                    <option value="taiwan">台灣</option>
                    <option value="china">中國大陸</option>
                  </Select>
                </div>
                <Select
                  required
                  value={form.county}
                  onChange={(e) => onCountyChange(e.target.value)}
                >
                  <option value="">選擇縣市</option>
                  {counties.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </Select>
                <Select
                  required
                  value={form.district}
                  onChange={(e) => onDistrictChange(e.target.value)}
                >
                  <option value="">選擇區域</option>
                  {districts.map((d) => (
                    <option key={d} value={d}>
                      {d}
                    </option>
                  ))}
                </Select>
              </div>
            </div>

            <label className="flex cursor-pointer items-start gap-3 rounded-2xl border border-white/10 bg-white/[0.03] px-4 py-3 transition hover:border-primary/30 hover:bg-primary/5">
              <input
                type="checkbox"
                checked={saveHistory}
                onChange={(e) => setSaveHistory(e.target.checked)}
                className="mt-0.5 h-4 w-4 shrink-0 rounded border-white/20 bg-transparent accent-primary"
              />
              <span className="text-sm leading-6 text-muted">
                <span className="font-medium text-foreground">儲存這次搜尋紀錄</span>
                <span className="mt-0.5 block text-xs">
                  僅保存在此裝置瀏覽器，方便下次直接點選查看。可隨時刪除。
                </span>
              </span>
            </label>

            {message && (
              <div
                className={`rounded-2xl px-4 py-3 text-sm ${
                  message.type === "ok"
                    ? "border border-secondary/30 bg-secondary/10 text-secondary"
                    : "border border-red-400/30 bg-red-500/10 text-red-200"
                }`}
              >
                {message.text}
              </div>
            )}

            <Button type="submit" size="lg" className="w-full" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  解析中…
                </>
              ) : (
                "立即解析"
              )}
            </Button>
          </form>

          <AnimatePresence>
            {history.length > 0 && (
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -8 }}
                className="mt-6 border-t border-white/10 pt-6"
              >
                <div className="mb-3 flex items-center justify-between gap-3">
                  <div className="flex flex-wrap items-center gap-2 text-sm text-accent-light">
                    <History className="h-4 w-4" />
                    <span className="font-medium tracking-wide">搜尋紀錄</span>
                    <span className="text-xs text-muted">點一下即可帶入並查看</span>
                  </div>
                  <button
                    type="button"
                    onClick={handleClearHistory}
                    className="inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs text-muted transition hover:bg-white/5 hover:text-foreground"
                  >
                    <Trash2 className="h-3.5 w-3.5" />
                    全部清除
                  </button>
                </div>
                <ul className="flex flex-col gap-2">
                  {history.map((item) => (
                    <li
                      key={item.id}
                      className="flex items-stretch gap-1 rounded-2xl border border-white/10 bg-white/[0.03] transition hover:border-primary/40 hover:bg-primary/10"
                    >
                      <button
                        type="button"
                        onClick={() => handleLoadHistory(item)}
                        disabled={loading}
                        className="min-w-0 flex-1 px-3.5 py-3 text-left disabled:opacity-60"
                      >
                        <div className="truncate text-sm font-medium text-foreground">
                          {historyLabel(item)}
                        </div>
                        <div className="mt-0.5 truncate text-xs text-muted">
                          {item.form.time}
                          {item.form.county
                            ? ` · ${item.form.county}${item.form.district ? ` ${item.form.district}` : ""}`
                            : ""}
                        </div>
                      </button>
                      <button
                        type="button"
                        aria-label="刪除此紀錄"
                        onClick={() => setHistory(removeSearchHistory(item.id))}
                        className="shrink-0 self-center rounded-full p-2 text-muted transition hover:bg-white/10 hover:text-red-300"
                      >
                        <X className="h-3.5 w-3.5" />
                      </button>
                    </li>
                  ))}
                </ul>
              </motion.div>
            )}
          </AnimatePresence>
        </Card>
      </motion.div>
    </section>
  );
}
