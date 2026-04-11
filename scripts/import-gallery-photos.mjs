#!/usr/bin/env node
/**
 * One-shot importer: copies photos from George's WeTransfer folder into
 * public/images/gallery/{category}/, resizing to max 2000px wide @ 80% JPEG.
 *
 * Also moves existing flat gallery images into public/images/gallery/builds/.
 *
 * Run once:  node scripts/import-gallery-photos.mjs
 */
import { promises as fs } from 'fs';
import path from 'path';
import sharp from 'sharp';

const SOURCE_ROOT = 'C:/Users/robertdicapite/Documents/Georges Photos/wetransfer_romark-engineering-photography-video-assets_2026-04-03_1400/Romark Engineering/Photography_Finals';
const DEST_ROOT = path.resolve('public/images/gallery');

// Map source folder name -> { category, prefix }
const MAPPING = {
  'U-Shape Frame':     { category: 'frames',     prefix: 'u-shape-frame' },
  'Underbed Storage':  { category: 'frames',     prefix: 'underbed-storage' },
  'Overhead Lockers':  { category: 'frames',     prefix: 'overhead-lockers' },
  'Aluminium Panels':  { category: 'frames',     prefix: 'aluminium-panels' },
  'Cushion Boards':    { category: 'frames',     prefix: 'cushion-boards' },
  'Rear Panel':        { category: 'frames',     prefix: 'rear-panel' },
  'Kitchen Pods':      { category: 'kitchens',   prefix: 'kitchen-pod' },
  'Rear CookerUnit':   { category: 'kitchens',   prefix: 'rear-cooker-unit' },
  'Upholstery Kit':    { category: 'upholstery', prefix: 'upholstery-kit' },
  // Excluded: 'Logo', '_GENERALWarehouse' (welding shots), 'Surface Finish' — not a fit for the public gallery
};

const MAX_WIDTH = 2000;
const JPEG_QUALITY = 80;

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function resizeAndWrite(srcPath, destPath) {
  const img = sharp(srcPath);
  const meta = await img.metadata();
  const pipeline = meta.width && meta.width > MAX_WIDTH
    ? img.resize({ width: MAX_WIDTH })
    : img;
  await pipeline
    .jpeg({ quality: JPEG_QUALITY, mozjpeg: true })
    .toFile(destPath);
  const { size } = await fs.stat(destPath);
  return size;
}

async function importNewPhotos() {
  let imported = 0;
  let totalBytes = 0;
  for (const [folder, { category, prefix }] of Object.entries(MAPPING)) {
    const srcDir = path.join(SOURCE_ROOT, folder);
    let entries;
    try {
      entries = await fs.readdir(srcDir);
    } catch {
      console.warn(`  ! skipping missing folder: ${folder}`);
      continue;
    }
    const images = entries
      .filter(f => /\.(jpe?g|png|webp)$/i.test(f))
      .sort();
    if (images.length === 0) continue;

    const destDir = path.join(DEST_ROOT, category);
    await ensureDir(destDir);

    let n = 1;
    for (const filename of images) {
      const padded = String(n).padStart(2, '0');
      const destName = `${prefix}-${padded}.jpg`;
      const destPath = path.join(destDir, destName);
      const srcPath = path.join(srcDir, filename);
      try {
        const size = await resizeAndWrite(srcPath, destPath);
        totalBytes += size;
        imported++;
        console.log(`  ${category}/${destName}  (${(size / 1024).toFixed(0)} KB)`);
      } catch (err) {
        console.error(`  ! failed: ${filename} -> ${destName}: ${err.message}`);
      }
      n++;
    }
  }
  console.log(`\n  imported: ${imported} photos, ${(totalBytes / 1024 / 1024).toFixed(1)} MB total`);
}

async function moveExistingToBuilds() {
  const buildsDir = path.join(DEST_ROOT, 'builds');
  await ensureDir(buildsDir);
  const entries = await fs.readdir(DEST_ROOT, { withFileTypes: true });
  let moved = 0;
  for (const entry of entries) {
    if (!entry.isFile()) continue;
    if (!/\.(jpe?g|png|webp|gif|avif)$/i.test(entry.name)) continue;
    const src = path.join(DEST_ROOT, entry.name);
    const dest = path.join(buildsDir, entry.name);
    await fs.rename(src, dest);
    moved++;
  }
  console.log(`  moved ${moved} existing images into gallery/builds/`);
}

console.log('1. Moving existing flat gallery images -> gallery/builds/');
await moveExistingToBuilds();
console.log('\n2. Importing new photos from George\'s folder...');
await importNewPhotos();
console.log('\ndone.');
