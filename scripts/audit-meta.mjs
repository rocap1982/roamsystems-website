// One-off audit helper for the audit-fixes branch: walks dist/client HTML,
// extracts <title>, canonical href and meta description, and reports lengths.
import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';

const root = join(process.cwd(), 'dist', 'client');
const pages = [];

function walk(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) walk(p);
    else if (name.endsWith('.html')) pages.push(p);
  }
}
walk(root);

const decode = (s) =>
  s
    .replace(/&amp;/g, '&')
    .replace(/&#39;/g, "'")
    .replace(/&quot;/g, '"')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>');

let badCanonical = 0;
let badTitle = 0;
const rows = [];
for (const p of pages.sort()) {
  const html = readFileSync(p, 'utf8');
  const title = decode(html.match(/<title>([^<]*)<\/title>/)?.[1] ?? '(none)');
  const canonical = html.match(/rel="canonical" href="([^"]*)"/)?.[1] ?? '(none)';
  const desc = decode(html.match(/name="description" content="([^"]*)"/)?.[1] ?? '');
  if (!canonical.startsWith('https://www.roamsystems.co.uk')) badCanonical++;
  if (title.includes('| Campervan Furniture')) badTitle++;
  const url = '/' + relative(root, p).replace(/\\/g, '/').replace(/index\.html$/, '');
  rows.push({ url, title, canonical, len: desc.length, over: desc.length > 160 ? 'OVER' : '', desc });
}

console.log(`pages: ${rows.length}, non-www canonicals: ${badCanonical}, titles with old suffix: ${badTitle}`);
console.log('');
for (const r of rows) {
  console.log(`${r.over ? '!! ' : '   '}${String(r.len).padStart(3)}  ${r.url}`);
  console.log(`        title: ${r.title}`);
  console.log(`        desc:  ${r.desc}`);
}
