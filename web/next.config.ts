import type { NextConfig } from "next";

const flaskOrigin = process.env.FLASK_ORIGIN || "http://127.0.0.1:5000";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      { source: "/calculate_hd", destination: `${flaskOrigin}/calculate_hd` },
      { source: "/api/:path*", destination: `${flaskOrigin}/api/:path*` },
      { source: "/health", destination: `${flaskOrigin}/health` },
      { source: "/callback", destination: `${flaskOrigin}/callback` },
      {
        source: "/api/line/callback",
        destination: `${flaskOrigin}/api/line/callback`,
      },
    ];
  },
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
