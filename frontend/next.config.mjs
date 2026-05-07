/** @type {import('next').NextConfig} */
const nextConfig = {
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "/api",
    NEXT_PUBLIC_API_BASE: process.env.NEXT_PUBLIC_API_BASE || "/api",
    NEXT_PUBLIC_OFF_API_BASE_URL:
      process.env.NEXT_PUBLIC_OFF_API_BASE_URL || "https://world.openfoodfacts.org",
  },
};

export default nextConfig;
