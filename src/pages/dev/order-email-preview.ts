export const prerender = false;

// TEMPORARY dev-only preview route — renders the order confirmation email with
// mock data so the layout can be eyeballed without a live Stripe checkout.
// Safe to delete; not part of the production contract.

import type { APIRoute } from 'astro';
import type Stripe from 'stripe';
import { buildEmailHtml } from '../../lib/email';

const mockSession = {
  id: 'cs_test_a1b2c3d4e5f6',
  payment_intent: 'pi_3ABCDxyz1234A1B2C3D4',
  amount_subtotal: 184900,
  amount_total: 224880,
  customer_details: {
    name: 'Jane Smith',
    email: 'jane.smith@example.com',
    phone: '+447700900123',
  },
  shipping_details: {
    name: 'Jane Smith',
    address: {
      line1: '12 High Street',
      line2: 'Flat 2',
      city: 'Colchester',
      state: 'Essex',
      postal_code: 'CO1 1AA',
      country: 'GB',
    },
  },
  total_details: {
    amount_tax: 36980,
  },
  shipping_cost: {
    amount_total: 2900,
  },
  custom_fields: [
    {
      key: 'vehicle',
      type: 'dropdown',
      dropdown: { value: 'vwT61' },
    },
    {
      key: 'vehicleYearReg',
      type: 'text',
      text: { value: '2021 / AB21 XYZ' },
    },
  ],
  line_items: {
    data: [
      { description: 'M1-Certified U-Shape Seating Frame', quantity: 1, amount_total: 149900 },
      { description: 'Aluminium Overhead Locker', quantity: 1, amount_total: 35000 },
    ],
  },
} as unknown as Stripe.Checkout.Session;

export const GET: APIRoute = async () => {
  return new Response(buildEmailHtml(mockSession), {
    status: 200,
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
  });
};
