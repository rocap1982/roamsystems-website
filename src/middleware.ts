import { defineMiddleware } from 'astro:middleware';

/**
 * Permanent (301) redirects.
 *
 * 1. Legacy Shopify URLs that Google still indexes — these paths no longer
 *    exist as routes, so they fall through the static file server to this
 *    middleware before Astro's 404 renders.
 * 2. Defence-in-depth non-www → www host redirect. Note: prerendered pages
 *    are served directly by the Node adapter's static file handler, which
 *    bypasses middleware — the authoritative non-www → www redirect must be
 *    configured at the platform level (Cloudflare redirect rule). This only
 *    covers on-demand routes (/api/*, /checkout/success, 404s).
 */
const CANONICAL_HOST = 'www.roamsystems.co.uk';

export const onRequest = defineMiddleware((context, next) => {
  const url = context.url;

  if (url.hostname === 'roamsystems.co.uk') {
    return context.redirect(`https://${CANONICAL_HOST}${url.pathname}${url.search}`, 301);
  }

  const path = url.pathname.toLowerCase();

  if (path === '/products/build-your-dream-campervan' || path === '/products/build-your-dream-campervan/') {
    return context.redirect('/products', 301);
  }
  if (path === '/collections' || path.startsWith('/collections/')) {
    return context.redirect('/products', 301);
  }
  if (path === '/pages' || path.startsWith('/pages/')) {
    return context.redirect('/', 301);
  }

  return next();
});
