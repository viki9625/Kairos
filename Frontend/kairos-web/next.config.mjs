/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  
  // --- THIS IS THE FIX ---
  // This section tells Next.js that it's safe to load images
  // from Google's user content domain.
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'lh3.googleusercontent.com',
        port: '',
        pathname: '/**',
      },
    ],
  },
  // -------------------------
};

export default nextConfig;

