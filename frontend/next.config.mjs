///** @type {import('next').NextConfig} */
//const nextConfig = {};
//
//export default nextConfig;
//

/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    domains: ["localhost", "api-gateway"],
    remotePatterns: [
      {
        protocol: "http",
        hostname: "localhost",
        port: "8000",
        pathname: "/images/**",
      },
    ],
  },

  async headers() {
    return [
      {
        source: "/api/(.*)", // Apply to all API routes
        headers: [
          { key: "Access-Control-Allow-Origin", value: "*" }, // Adjust based on your CORS policy
          { key: "Access-Control-Allow-Methods", value: "GET,POST,PUT,DELETE" },
          {
            key: "Access-Control-Allow-Headers",
            value: "Content-Type, Authorization",
          },
        ],
      },
    ];
  },
};

export default nextConfig;
