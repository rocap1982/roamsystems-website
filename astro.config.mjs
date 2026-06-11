// @ts-check
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';
import react from '@astrojs/react';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.roamsystems.co.uk',
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
