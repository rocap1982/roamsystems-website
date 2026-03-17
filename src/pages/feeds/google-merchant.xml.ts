import type { APIRoute } from 'astro';
import products from '../../data/products.json';

export const prerender = true;

const SITE_URL = 'https://roamsystems.co.uk';
const BRAND = 'ROAM Systems';
const VAT_RATE = 1.2;
const SHIPPING_PRICE = '130.00 GBP';
const SHIPPING_COUNTRY = 'UK';
const PRODUCT_TYPE =
  'Vehicles & Parts > Vehicle Parts & Accessories > Motor Vehicle Interior Fittings';

const VEHICLE_LABEL_MAP: Record<string, string> = {
  'vw-transporter-t5': 'VW T5',
  'vw-transporter-t6': 'VW T6',
  'vw-transporter-t6-1': 'VW T6.1',
  'ford-transit-custom': 'Transit Custom',
};

function escapeXml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function formatPrice(priceExVat: number): string {
  return `${(priceExVat * VAT_RATE).toFixed(2)} GBP`;
}

function buildItem(product: (typeof products)[number]): string {
  const description = escapeXml(product.description.slice(0, 5000));
  const title = escapeXml(product.name);
  const link = `${SITE_URL}/products/${product.id}`;
  const availability = product.madeToOrder ? 'preorder' : 'in_stock';

  const compatibleVehicles = product.compatibleVehicles
    .map((v) => VEHICLE_LABEL_MAP[v] || v)
    .join(', ');

  const [firstImage, ...additionalImages] = product.images;

  const additionalImageTags = additionalImages
    .slice(0, 10)
    .map((img) => `      <g:additional_image_link>${escapeXml(img)}</g:additional_image_link>`)
    .join('\n');

  return `    <item>
      <g:id>${escapeXml(product.id)}</g:id>
      <g:title>${title}</g:title>
      <g:description>${description}</g:description>
      <g:link>${link}</g:link>
      <g:image_link>${escapeXml(firstImage)}</g:image_link>
${additionalImageTags}
      <g:price>${formatPrice(product.price)}</g:price>
      <g:availability>${availability}</g:availability>
      <g:condition>new</g:condition>
      <g:brand>${BRAND}</g:brand>
      <g:mpn>${escapeXml(product.mpn)}</g:mpn>
      <g:product_type>${escapeXml(PRODUCT_TYPE)}</g:product_type>
      <g:shipping>
        <g:country>${SHIPPING_COUNTRY}</g:country>
        <g:price>${SHIPPING_PRICE}</g:price>
      </g:shipping>
      <g:custom_label_0>${escapeXml(compatibleVehicles)}</g:custom_label_0>
      <g:identifier_exists>false</g:identifier_exists>
    </item>`;
}

export const GET: APIRoute = () => {
  const items = products.map(buildItem).join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss xmlns:g="http://base.google.com/ns/1.0" version="2.0">
  <channel>
    <title>ROAM Systems</title>
    <link>${SITE_URL}</link>
    <description>Premium M1 Certified Campervan Furniture</description>
${items}
  </channel>
</rss>`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/xml',
    },
  });
};
