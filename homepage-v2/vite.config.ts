import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';
import path from 'node:path';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  // Serve the parent Astro project's public/ dir so real product images
  // (public/images/products/*.jpg) are available under /images/... in homepage-v2.
  publicDir: path.resolve(__dirname, '../public'),
  server: {
    port: 5174,
  },
});
