export const prerender = false;

import type { APIRoute } from 'astro';
import Stripe from 'stripe';

const stripeKey = import.meta.env.STRIPE_SECRET_KEY;
if (!stripeKey) {
  console.warn('STRIPE_SECRET_KEY is not set — checkout will fail at runtime');
}

export const POST: APIRoute = async ({ request }) => {
  if (!stripeKey) {
    return new Response(JSON.stringify({ error: 'Stripe is not configured' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const stripe = new Stripe(stripeKey);

  let body: { items: Array<{ stripePriceId: string; qty: number }> };
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  if (!body.items || !Array.isArray(body.items) || body.items.length === 0) {
    return new Response(JSON.stringify({ error: 'No items provided' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const invalidItem = body.items.find(
    (item) => !item.stripePriceId || !item.qty || item.qty < 1
  );
  if (invalidItem) {
    return new Response(
      JSON.stringify({ error: 'Each item must have a valid stripePriceId and qty >= 1' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  const origin = new URL(request.url).origin;

  try {
    const session = await stripe.checkout.sessions.create({
      mode: 'payment',
      line_items: body.items.map((item) => ({
        price: item.stripePriceId,
        quantity: item.qty,
      })),
      success_url: `${origin}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${origin}/checkout/cancel`,
    });

    return new Response(JSON.stringify({ url: session.url }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error creating checkout session';
    return new Response(JSON.stringify({ error: message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};

export const ALL: APIRoute = async () => {
  return new Response(JSON.stringify({ error: 'Method not allowed' }), {
    status: 405,
    headers: { 'Content-Type': 'application/json', 'Allow': 'POST' },
  });
};
