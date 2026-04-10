export type Product = {
  id: string;
  name: string;
  price: number; // GBP, ex VAT
  category: 'Frames' | 'Upholstery' | 'Kitchens' | 'Storage' | 'Panels';
  blurb: string;
  image: string;
};

export const featuredProduct = {
  id: 'm1-certified-u-shape-seating-frame',
  name: 'M1 Certified U-Shape Seating Frame',
  tagline: 'The only M1 certified U-shape seating system available',
  description:
    'Engineered for safety with integrated 3-point seatbelts and ISOFIX points. Quick bed conversion. Built in Essex by Romark Engineering.',
  price: 1999,
  image: '/images/products/m1-certified-u-shape-seating-frame-5.jpg',
  specs: [
    { label: 'Max Width', value: '158cm' },
    { label: 'Sleeping Length', value: '170cm' },
    { label: 'Configuration', value: 'SWB / LWB' },
    { label: 'USB Ports', value: '2 Built In' },
  ],
};

// Hero background uses one of the M1 frame shots for atmosphere
export const heroImage = '/images/products/m1-certified-u-shape-seating-frame-8.jpg';

export const products: Product[] = [
  {
    id: 'central-under-bed-pull-out-drawer',
    name: 'Central Under Bed Pull-Out Drawer',
    price: 399,
    category: 'Storage',
    blurb: '220kg capacity runners. Full-extension access under the seating frame.',
    image: '/images/products/central-under-bed-pull-out-drawer-storage-10.jpg',
  },
  {
    id: 'rear-pull-out-drawer-storage-system',
    name: 'Rear Pull-Out Drawer Storage System',
    price: 449,
    category: 'Storage',
    blurb: 'Tailgate-mounted pull-out storage. Powder-coated steel, tamper-proof locks.',
    image: '/images/products/rear-pull-out-drawer-storage-system-3.jpg',
  },
  {
    id: 'rear-pull-out-kitchen-pod',
    name: 'Rear Pull-Out Kitchen Pod',
    price: 649,
    category: 'Kitchens',
    blurb: 'Compact kitchen pod with slide-out sink bay and storage compartments.',
    image: '/images/products/rear-pull-out-kitchen-pod-4.jpg',
  },
  {
    id: 'powder-coated-aluminium-panels',
    name: 'Powder Coated Aluminium Panels',
    price: 379,
    category: 'Panels',
    blurb: 'Precision laser-cut panels finished in matte powder coat. SWB & LWB.',
    image: '/images/products/powder-coated-aluminium-front-facing-panels-1.jpg',
  },
  {
    id: 'full-upholstery-kit-rear-seating',
    name: 'Full Upholstery Kit – Rear Seating',
    price: 1099,
    category: 'Upholstery',
    blurb: '100+ fabric choices. High-density foam, reinforced stitching.',
    image: '/images/products/full-upholstery-kit-rear-seating-only-5.jpg',
  },
  {
    id: 'kitchen-pod-package',
    name: 'Kitchen Pod Package',
    price: 1249,
    category: 'Kitchens',
    blurb: 'Full pod bundle — worktop, sink, storage locker and integrated wiring.',
    image: '/images/products/kitchen-pod-campervan-package-1.jpg',
  },
];

export const vehicles = [
  'VW T5',
  'VW T6',
  'VW T6.1',
  'Ford Transit Custom',
  'Renault Trafic',
  'Nissan Primastar',
];

export const trustItems = [
  'M1 Certified Safety',
  '100+ Fabric Choices',
  '220kg Runner Capacity',
  'UK Made & Delivered',
  '17 Approved Installers',
  'EU Registered Design',
  'From £1,850 + VAT',
];
