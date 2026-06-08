#!/usr/bin/env node
// Verifies that every stripePriceId in src/data/products.json matches the live
// Stripe price: amount, currency, active state, and tax_behavior=exclusive.
// Read-only — only calls stripe.prices.retrieve. Run with a (read-only) key:
//   node --env-file=.env scripts/verify-stripe-prices.mjs
import { readFile } from 'node:fs/promises';
import Stripe from 'stripe';

const key = process.env.STRIPE_SECRET_KEY;
if (!key) {
  console.error('STRIPE_SECRET_KEY not set. Put it in .env and run: node --env-file=.env scripts/verify-stripe-prices.mjs');
  process.exit(2);
}
const stripe = new Stripe(key);
const products = JSON.parse(await readFile('src/data/products.json', 'utf8'));

const rows = [];
for (const p of products) {
  for (const v of p.variants) {
    if (!v.stripePriceId) {
      rows.push({ ok: null, id: '(none)', label: `${p.id} / ${v.title}`, json: v.price, note: 'made-to-order (no Stripe price)' });
      continue;
    }
    try {
      const price = await stripe.prices.retrieve(v.stripePriceId);
      const stripeAmount = price.unit_amount != null ? price.unit_amount / 100 : null;
      const amountOk = stripeAmount === v.price;
      const currencyOk = price.currency === 'gbp';
      const taxOk = price.tax_behavior === 'exclusive';
      const activeOk = price.active === true;
      const ok = amountOk && currencyOk && taxOk && activeOk;
      const notes = [];
      if (!amountOk) notes.push(`AMOUNT json=£${v.price} stripe=£${stripeAmount}`);
      if (!currencyOk) notes.push(`CURRENCY=${price.currency}`);
      if (!taxOk) notes.push(`TAX_BEHAVIOR=${price.tax_behavior}`);
      if (!activeOk) notes.push('INACTIVE');
      rows.push({ ok, id: v.stripePriceId, label: `${p.id} / ${v.title}`, json: v.price, note: notes.join('; ') || 'match' });
    } catch (err) {
      rows.push({ ok: false, id: v.stripePriceId, label: `${p.id} / ${v.title}`, json: v.price, note: `RETRIEVE FAILED: ${err.message}` });
    }
  }
}

console.log('\nStripe price verification (products.json vs live Stripe)\n');
for (const r of rows) {
  const mark = r.ok === null ? '–' : r.ok ? 'OK ' : 'XX ';
  console.log(`${mark} £${String(r.json).padEnd(5)} ${r.label.padEnd(60)} ${r.note}`);
}
const fails = rows.filter((r) => r.ok === false);
console.log(`\n${rows.length} variants checked, ${fails.length} problem(s).`);
process.exit(fails.length ? 1 : 0);
