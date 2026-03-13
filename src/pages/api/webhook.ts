export const prerender = false;

import type { APIRoute } from 'astro';
import Stripe from 'stripe';
import { sendConfirmationEmail } from '../../lib/email';

export const POST: APIRoute = async ({ request }) => {
  const stripeKey = process.env.STRIPE_SECRET_KEY;
  const webhookSecret = process.env.STRIPE_WEBHOOK_SECRET;

  if (!stripeKey || !webhookSecret) {
    console.error('STRIPE_SECRET_KEY or STRIPE_WEBHOOK_SECRET is not configured');
    return new Response('Webhook not configured', { status: 500 });
  }

  const stripe = new Stripe(stripeKey);
  const payload = await request.text();
  const sig = request.headers.get('stripe-signature');

  if (!sig) {
    return new Response('Missing stripe-signature header', { status: 400 });
  }

  let event: Stripe.Event;
  try {
    event = stripe.webhooks.constructEvent(payload, sig, webhookSecret);
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    console.error('Webhook signature verification failed:', message);
    return new Response('Invalid signature', { status: 400 });
  }

  if (event.type === 'checkout.session.completed') {
    const session = event.data.object as Stripe.Checkout.Session;

    try {
      const fullSession = await stripe.checkout.sessions.retrieve(session.id, {
        expand: ['line_items', 'shipping_cost'],
      });
      await sendConfirmationEmail(fullSession, event.id);
    } catch (err) {
      console.error('Failed to process checkout.session.completed:', err);
      // Still return 200 to prevent Stripe retries for transient email failures
    }
  }

  return new Response(JSON.stringify({ received: true }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};

export const ALL: APIRoute = async () => {
  return new Response(JSON.stringify({ error: 'Method not allowed' }), {
    status: 405,
    headers: { 'Content-Type': 'application/json', 'Allow': 'POST' },
  });
};
