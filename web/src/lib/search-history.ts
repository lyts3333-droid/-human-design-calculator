import type { BirthFormValues, HumanDesignResult } from "@/types/hd";

export type SearchHistoryItem = {
  id: string;
  savedAt: number;
  form: BirthFormValues;
  result?: HumanDesignResult;
};

const STORAGE_KEY = "wanjuan-search-history";
const MAX_ITEMS = 12;

function canUseStorage() {
  return typeof window !== "undefined" && typeof localStorage !== "undefined";
}

export function loadSearchHistory(): SearchHistoryItem[] {
  if (!canUseStorage()) return [];
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw) as SearchHistoryItem[];
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

export function saveSearchHistory(items: SearchHistoryItem[]) {
  if (!canUseStorage()) return;
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, MAX_ITEMS)));
}

function sameBirth(a: BirthFormValues, b: BirthFormValues) {
  return (
    a.year === b.year &&
    a.month === b.month &&
    a.day === b.day &&
    a.time === b.time &&
    a.region === b.region &&
    a.county === b.county &&
    a.district === b.district &&
    a.longitude === b.longitude &&
    a.latitude === b.latitude &&
    (a.name || "") === (b.name || "")
  );
}

export function upsertSearchHistory(
  form: BirthFormValues,
  result?: HumanDesignResult
): SearchHistoryItem[] {
  const prev = loadSearchHistory();
  const existing = prev.find((item) => sameBirth(item.form, form));
  const nextItem: SearchHistoryItem = {
    id: existing?.id || `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    savedAt: Date.now(),
    form: { ...form },
    result: result ?? existing?.result,
  };
  const rest = prev.filter((item) => item.id !== nextItem.id);
  const next = [nextItem, ...rest].slice(0, MAX_ITEMS);
  saveSearchHistory(next);
  return next;
}

export function removeSearchHistory(id: string): SearchHistoryItem[] {
  const next = loadSearchHistory().filter((item) => item.id !== id);
  saveSearchHistory(next);
  return next;
}

export function clearSearchHistory() {
  if (!canUseStorage()) return;
  localStorage.removeItem(STORAGE_KEY);
}

export function historyLabel(item: SearchHistoryItem) {
  const name = item.form.name?.trim();
  const date = `${item.form.year}/${String(item.form.month).padStart(2, "0")}/${String(item.form.day).padStart(2, "0")}`;
  const place = [item.form.county, item.form.district].filter(Boolean).join(" ");
  if (name) return `${name} · ${date}`;
  if (place) return `${date} · ${place}`;
  return date;
}
