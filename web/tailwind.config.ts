import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#050816",
        foreground: "#F5F0E8",
        muted: "#A8A0B8",
        primary: "#6F6CFF",
        secondary: "#4EC5FF",
        accent: "#C7A86F",
        "accent-light": "#E6D3A3",
        success: "#3DDB9A",
        card: "rgba(255,255,255,0.06)",
      },
      borderRadius: {
        "3xl": "1.5rem",
      },
      boxShadow: {
        glow: "0 0 40px rgba(111,108,255,0.35)",
      },
      fontFamily: {
        sans: ["var(--font-noto)", "var(--font-inter)", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
