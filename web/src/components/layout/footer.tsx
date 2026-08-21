import Link from "next/link";

export function Footer() {
  const year = new Date().getFullYear();
  return (
    <footer className="mt-24 border-t border-white/8 bg-black/20">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-14 md:grid-cols-[1.2fr_1fr] md:px-8">
        <div>
          <div className="text-xl font-semibold tracking-[0.16em] text-accent-light">
            玩轉人生
          </div>
          <div className="mt-1 text-xs uppercase tracking-[0.28em] text-muted">
            Life Design Lab
          </div>
          <p className="mt-4 max-w-md text-sm leading-relaxed text-muted">
            以人類圖與基因天命為鏡，幫助你看清天賦、決策模式與人生方向，活出真正適合自己的節奏。
          </p>
        </div>

        <div className="grid grid-cols-2 gap-6 text-sm text-muted">
          <div className="space-y-3">
            <div className="text-foreground">探索</div>
            <a href="#form" className="block hover:text-accent-light">
              免費人生圖
            </a>
            <a href="#about" className="block hover:text-accent-light">
              認識人類圖
            </a>
            <a href="#faq" className="block hover:text-accent-light">
              常見問題
            </a>
          </div>
          <div className="space-y-3">
            <div className="text-foreground">支援</div>
            <Link href="#contact" className="block hover:text-accent-light">
              聯絡我們
            </Link>
            <Link href="#privacy" className="block hover:text-accent-light">
              隱私政策
            </Link>
            <Link href="#terms" className="block hover:text-accent-light">
              服務條款
            </Link>
          </div>
        </div>
      </div>
      <div className="border-t border-white/8 py-5 text-center text-xs text-muted">
        © {year} 玩轉人生 Life Design Lab. All rights reserved.
      </div>
    </footer>
  );
}
