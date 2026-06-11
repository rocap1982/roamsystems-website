// @ts-check
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.roamsystems.co.uk',
  security: {
    // Required for Astro to trust Host / X-Forwarded-Host behind Railway's
    // proxy. Without this, on-demand request URLs (middleware host checks,
    // the Stripe success/cancel URLs built from request.url in
    // /api/checkout) resolve to localhost.
    allowedDomains: [
      { hostname: 'roamsystems.co.uk' },
      { hostname: 'www.roamsystems.co.uk' },
    ],
  },
  integrations: [
    react(),
    sitemap({
      filter: (page) => !page.includes('/checkout/') && !page.includes('/basket/'),
    }),
  ],
  adapter: node({ mode: 'standalone' }),
  vite: {
    plugins: [tailwindcss()]
  }
});
