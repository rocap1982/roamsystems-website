#!/usr/bin/env node
import { readdir, readFile } from 'node:fs/promises';
import { join } from 'node:path';

const BLOG_DIR = 'src/content/blog';
const BAD_PATTERN = /\(£\s?\d/g;

const files = (await readdir(BLOG_DIR)).filter((f) => f.endsWith('.md') || f.endsWith('.mdx'));
const offences = [];

for (const file of files) {
  const path = join(BLOG_DIR, file);
  const content = await readFile(path, 'utf8');
  const lines = content.split(/\r?\n/);
  lines.forEach((line, idx) => {
    if (BAD_PATTERN.test(line)) {
      offences.push({ path, line: idx + 1, text: line.trim() });
    }
    BAD_PATTERN.lastIndex = 0;
  });
}

if (offences.length === 0) {
  console.log('check-blog-prices: clean — no parenthesised £ prices in blog markdown.');
  process.exit(0);
}

console.error('check-blog-prices: hardcoded prices found in blog markdown.');
console.error('Prices belong in src/data/products.json — the source of truth. Remove the parenthesised £NNN and let readers click through to the product page for the live price.\n');
for (const o of offences) {
  console.error(`  ${o.path}:${o.line}  ${o.text}`);
}
process.exit(1);
