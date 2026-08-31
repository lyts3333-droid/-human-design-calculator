import type { SequenceFilter } from "@/lib/gene-keys";

export type GeneKeyPathInfo = {
  id: string;
  title: string;
  subtitle: string;
  tagline: string;
  sequence: SequenceFilter;
  fromLabel: string;
  toLabel: string;
  paragraphs: string[];
};

export const GENE_KEY_PATHS: Record<string, GeneKeyPathInfo> = {
  challenge: {
    id: "challenge",
    title: "挑戰之路",
    subtitle: "路徑 · 挑戰",
    tagline: "透過覺察和勇氣，將內心的緊張感轉化為力量。",
    sequence: "genius",
    fromLabel: "人生事業（黑太陽）",
    toLabel: "進化（黑地球）",
    paragraphs: [
      "這條路徑是「黃金之路」啟動序列的第一步，連結你的生命使命領域（你的天賦所在）與進化領域（你此生注定要面對的挑戰）。",
      "當你願意直面進化領域的陰影，而不是逃避或壓抑，生命真正的考驗往往會在意想不到的地方轉化為成長的契機。這是一段在冒險中展現的靈性旅程。",
      "挑戰之路提醒你：天賦與陰影是一體兩面。越是能誠實面對自己的課題，你的生命使命就越能清晰而穩定地展現。",
    ],
  },
  breakthrough: {
    id: "breakthrough",
    title: "突破之路",
    subtitle: "路徑 · 突破",
    tagline: "當你學會從生命課題中汲取智慧，光芒便會自然綻放。",
    sequence: "genius",
    fromLabel: "進化（黑地球）",
    toLabel: "光芒（紅太陽）",
    paragraphs: [
      "突破之路橫跨啟動序列的中軸，連結你的進化領域與光芒領域，並經過穩定頻率（SQ）這個內在樞紐。",
      "當你整合進化領域的課題，身體、情緒與心智會逐漸恢復活力。這條路徑象徵生命中那些「突然想通」的時刻——舊模式鬆動，新的可能性得以進入。",
      "越能從日常經驗中學習，你的光芒就越明亮；光芒越穩定，也越能支持你在進化中保持耐心與信任。",
    ],
  },
  "core-stability": {
    id: "core-stability",
    title: "核心穩定之路",
    subtitle: "路徑 · 核心穩定",
    tagline: "在光芒與人生目的之間，建立能承載夢想的根基。",
    sequence: "genius",
    fromLabel: "光芒（紅太陽）",
    toLabel: "人生目的（紅地球）",
    paragraphs: [
      "核心穩定之路連結你的光芒與人生目的，是啟動序列中滋養內在根基的路徑。",
      "光芒關乎你的身心健康與生命力；人生目的則藏在你最深的夢想與內在尊嚴之中。當兩者透過這條路徑對話，你會更清楚什麼樣的生活方式能長期支撐你。",
      "這條路徑邀請你把高遠的理想落實到日常——不是退縮，而是找到能持續滋養你的節奏與環境。",
    ],
  },
  dharma: {
    id: "dharma",
    title: "正法之路",
    subtitle: "路徑 · 正法",
    tagline: "以寬容與覺察，接納生命為你安排的節奏與際遇。",
    sequence: "love",
    fromLabel: "吸引力（紅月亮）",
    toLabel: "人生目的（紅地球）",
    paragraphs: [
      "正法之路是金星序列的起點之一，連結吸引力與人生目的，探問「為什麼生命會以這樣的方式來到我面前」。",
      "這條路徑不是要你接受一切，而是培養一種對命運的優雅——在關係與際遇中，看見背後更深層的學習與邀請。",
      "當你能以更從容的態度面對生命中的際遇，心會逐漸鬆開，為後續的情感轉化創造空間。",
    ],
  },
  karma: {
    id: "karma",
    title: "業力之路",
    subtitle: "路徑 · 業力",
    tagline: "在吸引力與智商之間，看見你一再重複的關係模式。",
    sequence: "love",
    fromLabel: "吸引力（紅月亮）",
    toLabel: "智商（黑金星）",
    paragraphs: [
      "業力之路連結吸引力與智商，揭示你容易被什麼樣的人與情境吸引，以及心智如何試圖控制情緒。",
      "這條路徑常指向童年以來形成的思維習慣——用理性壓過直覺、用辯論取代感受。覺察這些模式，是鬆開情緒觸發點的第一步。",
      "當業力被看見而非否認，關係中的重複劇本才有機會鬆動，讓更真實的連結得以發生。",
    ],
  },
  intelligence: {
    id: "intelligence",
    title: "智慧之路",
    subtitle: "路徑 · 智慧",
    tagline: "讓心智從控制走向包容，擴展你理解自己與他人的能力。",
    sequence: "love",
    fromLabel: "智商（黑金星）",
    toLabel: "情商（黑火星）",
    paragraphs: [
      "智慧之路連結智商與情商，是金星序列中從「想明白」走向「感受得到」的橋樑。",
      "當你不再用狹隘的觀點評判情緒，心智會變得更開闊，能同時容納矛盾與不確定。這讓你在關係中更少防衛、更少挑釁。",
      "這條路徑支持你把情緒視為訊息而非敵人，從而恢復內在的流動與真誠。",
    ],
  },
  love: {
    id: "love",
    title: "愛之路",
    subtitle: "路徑 · 愛",
    tagline: "從情商走向穩定頻率，讓心再次向生命敞開。",
    sequence: "love",
    fromLabel: "情商（黑火星）",
    toLabel: "穩定頻率（紅金星）",
    paragraphs: [
      "愛之路連結情商與穩定頻率（SQ），是金星序列中通往心靈敞開的關鍵通道。",
      "當童年的情緒防衛被鬆開，你會更容易與自己的感受共處，也更容易在關係中保持真實與溫柔。",
      "這條路徑指向一種持久的敞開——不是沒有界限，而是帶著覺察去愛，讓關係成為彼此成長的場域。",
    ],
  },
  realisation: {
    id: "realisation",
    title: "覺悟之路",
    subtitle: "路徑 · 覺悟",
    tagline: "從穩定頻率回到核心，觸及最深處的傷口與天賦。",
    sequence: "love",
    fromLabel: "穩定頻率（紅金星）",
    toLabel: "核心（紅火星）",
    paragraphs: [
      "覺悟之路連結穩定頻率與核心，是金星序列的深化階段，引向最內層的情感印記與生命天職。",
      "核心承載著古老的傷口，也藏著你最高的天職。當覺察能溫柔地觸及這裡，苦難與神性往往在同一處被轉化。",
      "走完這條路徑，你會更理解自己為何如此反應、如此渴望，並在關係中帶著更多的慈悲與清明。",
    ],
  },
  initiative: {
    id: "initiative",
    title: "啟動之路",
    subtitle: "路徑 · 啟動",
    tagline: "從人生事業出發，啟動你服務世界的核心力量。",
    sequence: "prosperity",
    fromLabel: "人生事業（黑太陽）",
    toLabel: "核心（紅火星）",
    paragraphs: [
      "啟動之路是珍珠序列的第一步，從你的人生事業（外在表達）連向核心（內在天職），開啟豐盛與服務的旅程。",
      "這條路徑問的是：你如何把天賦帶進世界，同時觸及內心真正願意奉獻的方向？當外在與內在對齊，行動會更有力量。",
      "啟動不是匆忙行動，而是找到那個讓你願意長期投入的焦點，並從那裡開始創造價值。",
    ],
  },
  growth: {
    id: "growth",
    title: "成長之路",
    subtitle: "路徑 · 成長",
    tagline: "從核心走向文化，在對的環境中擴展你的影響力。",
    sequence: "prosperity",
    fromLabel: "核心（紅火星）",
    toLabel: "文化（紅木星）",
    paragraphs: [
      "成長之路連結核心與文化，探討你如何融入更大的社群與集體，並在其中繁榮。",
      "文化領域顯示你適合怎樣的環境與合作方式。當核心的陰影被轉化，這條路徑會吸引對的盟友與機會進入你的生命。",
      "真正的成長往往來自於與他人共創，而非獨自奮鬥。這條路徑邀請你找到能放大你天賦的集體節奏。",
    ],
  },
  service: {
    id: "service",
    title: "服務之路",
    subtitle: "路徑 · 服務",
    tagline: "透過服務與給予，讓豐盛在生命中自然流動。",
    sequence: "prosperity",
    fromLabel: "珍珠（黑木星）",
    toLabel: "人生事業（黑太陽）",
    paragraphs: [
      "服務之路連結珍珠與人生事業，是珍珠序列中將內在收穫化為外在貢獻的路徑。",
      "珍珠象徵生命的豐收與恩典；當你願意以服務的心態分享天賦，資源與機會往往會以意想不到的方式回流。",
      "豐盛不是囤積，而是讓能量在給予與接收之間保持流動。這條路徑提醒你：最持久的繁榮，來自於對世界的真誠貢獻。",
    ],
  },
};

export function getGeneKeyPath(pathId: string | undefined): GeneKeyPathInfo | null {
  if (!pathId) return null;
  return GENE_KEY_PATHS[pathId] ?? null;
}
