import type { BirthFormValues, CalculateResponse, GeneKeyDetail } from "@/types/hd";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE ?? "";

export async function calculateHumanDesign(
  form: BirthFormValues
): Promise<CalculateResponse> {
  const response = await fetch(`${API_BASE}/calculate_hd`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      year: form.year,
      month: form.month,
      day: form.day,
      time: form.time,
      timezone: form.timezone,
      longitude: form.longitude,
      latitude: form.latitude,
      name: form.name,
    }),
  });

  if (!response.ok) {
    let error = `伺服器錯誤 (${response.status})`;
    try {
      const payload = await response.json();
      error = payload.error || error;
    } catch {
      /* ignore */
    }
    return { status: "error", error };
  }

  return response.json();
}

export async function fetchGeneKey(gate: number): Promise<GeneKeyDetail> {
  const response = await fetch(`${API_BASE}/api/gene_key/${gate}`);
  if (!response.ok) {
    throw new Error(response.status === 404 ? "找不到該基因天命資料" : "載入失敗");
  }
  return response.json();
}
