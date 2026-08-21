import type { Metadata } from "next";
import { Inter, Noto_Sans_TC } from "next/font/google";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const notoSansTC = Noto_Sans_TC({
  subsets: ["latin"],
  weight: ["300", "400", "500", "700"],
  variable: "--font-noto",
  display: "swap",
});

export const metadata: Metadata = {
  title: "玩轉人生｜Human Design 人類圖免費解析",
  description:
    "免費的人類圖分析平台，快速了解你的類型、策略、權威、人生角色與能量中心。",
  icons: {
    icon: "/logo.png",
  },
  openGraph: {
    title: "玩轉人生｜Human Design 人類圖免費解析",
    description:
      "免費的人類圖分析平台，快速了解你的類型、策略、權威、人生角色與能量中心。",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="zh-Hant">
      <body className={`${inter.variable} ${notoSansTC.variable} antialiased`}>
        {children}
      </body>
    </html>
  );
}
