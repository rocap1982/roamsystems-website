// Verifies the Stripe account has a Terms of Service URL set (required for
// consent_collection.terms_of_service='required'). Creates a checkout session
// with the same consent params as /api/checkout, reports, then expires it.
// Usage: node --env-file=.env scripts/verify-tos-consent.mjs
import Stripe from 'stripe';

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
const origin = 'https://www.roamsystems.co.uk';

try {
  const session = await stripe.checkout.sessions.create({
    mode: 'payment',
    line_items: [{ price: 'price_1TVugcP8jCOedj2eUbpmfjaR', quantity: 1 }],
    consent_collection: { terms_of_service: 'required' },
    custom_text: {
      terms_of_service_acceptance: {
        message: `I agree to the [Terms of Service](${origin}/policies/terms), including the intellectual property and design rights provisions.`,
      },
    },
    success_url: `${origin}/checkout/success?session_id={CHECKOUT_SESSION_ID}`,
    cancel_url: `${origin}/checkout/cancel`,
  });
  console.log('PASS: session created with required ToS consent:', session.id);
  console.log('consent_collection:', JSON.stringify(session.consent_collection));
  await stripe.checkout.sessions.expire(session.id);
  console.log('Cleanup: session expired.');
} catch (err) {
  console.error('FAIL:', err.message);
  process.exit(1);
}
