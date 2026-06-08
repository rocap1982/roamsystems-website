/**
 * Homepage-specific product selection + display config.
 * Pulls real data from src/data/products.json and maps it for the
 * dark-industrial homepage (v2) sections.
 */
import productsJson from '../../data/products.json';

type RawProduct = typeof productsJson[number];

const raw: RawProduct[] = productsJson as RawProduct[];

function byId(id: string): RawProduct {
  const p = raw.find((x) => x.id === id);
  if (!p) throw new Error(`homeData: product "${id}" not found in products.json`);
  return p;
}

// --- Featured: M1 U-shape seating frame ---
const m1 = byId('m1-certified-u-shape-seating-frame');

export const featuredProduct = {
  id: m1.id,
  href: `/products/${m1.id}`,
  name: m1.name,
  tagline: 'The only M1 certified U-shape seating system available',
  description:
    'Engineered for safety with integrated 3-point seatbelts and ISOFIX points. Quick bed conversion. Built in Essex by Romark Engineering.',
  price: m1.price,
  image: m1.images[0],
  // Real cart payload for the basket JS in HomeLayout
  cart: {
    id: m1.id,
    name: m1.name,
    price: m1.price,
    variant: m1.variants[0].title,
    image: m1.images[0],
    stripePriceId: m1.variants[0].stripePriceId ?? null,
  },
  specs: [
    { label: 'Max Width', value: '158cm' },
    { label: 'Sleeping Length', value: '170cm' },
    { label: 'Configuration', value: 'SWB / LWB' },
    { label: 'USB Ports', value: '2 Built In' },
  ],
};

// Hero background image
export const heroImage = m1.images[1] ?? m1.images[0];

// --- Grid: 6 products ---
type CategoryLabel = 'Frames' | 'Upholstery' | 'Kitchens' | 'Storage' | 'Panels';

const gridIds: Array<{ id: string; label: CategoryLabel; blurb: string }> = [
  {
    id: 'central-under-bed-pull-out-drawer-storage',
    label: 'Storage',
    blurb: '220kg capacity runners. Full-extension access under the seating frame.',
  },
  {
    id: 'rear-pull-out-drawer-storage-system',
    label: 'Storage',
    blurb: 'Tailgate-mounted pull-out storage. Powder-coated steel, tamper-proof locks.',
  },
  {
    id: 'rear-pull-out-kitchen-pod',
    label: 'Kitchens',
    blurb: 'Compact kitchen pod with slide-out bay and storage compartments.',
  },
  {
    id: 'powder-coated-aluminium-front-facing-panels',
    label: 'Panels',
    blurb: 'Precision laser-cut panels finished in matte powder coat. SWB & LWB.',
  },
  {
    id: 'full-upholstery-kit-rear-seating-only',
    label: 'Upholstery',
    blurb: '100+ fabric choices. High-density foam, reinforced stitching.',
  },
  {
    id: 'kitchen-pod-campervan-package',
    label: 'Kitchens',
    blurb: 'Full pod bundle — worktop, sink, storage locker and integrated wiring.',
  },
];

export type HomeGridProduct = {
  id: string;
  href: string;
  name: string;
  price: number;
  image: string;
  category: CategoryLabel;
  blurb: string;
  cart: {
    id: string;
    name: string;
    price: number;
    variant: string;
    image: string;
    stripePriceId: string | null;
  };
};

export const gridProducts: HomeGridProduct[] = gridIds.map(({ id, label, blurb }) => {
  const p = byId(id);
  const v = p.variants[0];
  return {
    id: p.id,
    href: `/products/${p.id}`,
    name: p.name,
    price: p.price,
    image: p.images[0],
    category: label,
    blurb,
    cart: {
      id: p.id,
      name: p.name,
      price: p.price,
      variant: v.title,
      image: p.images[0],
      stripePriceId: v.stripePriceId ?? null,
    },
  };
});

// --- Vehicle selector pills ---
export const vehicles = [
  'VW T5',
  'VW T6',
  'VW T6.1',
  'Ford Transit Custom',
  'Renault Trafic',
  'Nissan Primastar',
];

// --- Trust marquee items ---
const minVariantPrice = Math.min(
  ...raw.flatMap((p) => p.variants.map((v) => v.price)),
);
const fromPriceLabel = `From £${minVariantPrice.toLocaleString('en-GB')} + VAT`;

export const trustItems = [
  'M1 Certified Safety',
  '100+ Fabric Choices',
  '220kg Runner Capacity',
  'UK Made & Delivered',
  '17 Approved Installers',
  'EU Registered Design',
  fromPriceLabel,
];

// --- Nav links: full site routes (used by every page) ---
export const navLinks = [
  { label: 'All Furniture', href: '/products' },
  { label: 'Frames', href: '/products?category=Frames' },
  { label: 'Upholstery', href: '/products?category=Upholstery' },
  { label: 'Kitchens', href: '/products?category=Kitchens' },
  { label: 'Vehicles', href: '/vehicles' },
  { label: 'Installers', href: '/installers' },
  { label: 'Blog', href: '/blog' },
  { label: 'Gallery', href: '/gallery' },
  { label: 'Contact', href: '/contact' },
];

// Secondary nav links (mobile drawer + footer only, not in desktop header)
export const navLinksSecondary = [
  { label: 'Delivery', href: '/delivery' },
  { label: 'Certifications', href: '/certifications' },
];

// Declare window.roamCart so TS stops complaining inside island components
declare global {
  interface Window {
    roamCart?: {
      add: (p: {
        id: string;
        name: string;
        price: number;
        variant: string;
        image: string;
        stripePriceId?: string | null;
      }) => void;
    };
  }
}
