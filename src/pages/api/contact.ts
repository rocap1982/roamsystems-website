export const prerender = false;

import type { APIRoute } from 'astro';
import { sendFormEmail, type FormEmailData } from '../../lib/email';

export const POST: APIRoute = async ({ request }) => {
  let body: Record<string, string>;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: 'Invalid JSON body' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  const { type, name, email, phone, subject, message, basketItems, basketTotal } = body;

  if (!name || !email || !type) {
    return new Response(
      JSON.stringify({ error: 'Name, email, and type are required' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  if (type !== 'contact' && type !== 'enquiry') {
    return new Response(
      JSON.stringify({ error: 'Type must be "contact" or "enquiry"' }),
      { status: 400, headers: { 'Content-Type': 'application/json' } }
    );
  }

  try {
    const data: FormEmailData = {
      type,
      name,
      email,
      phone: phone || undefined,
      subject: subject || undefined,
      message: message || undefined,
      basketItems: basketItems || undefined,
      basketTotal: basketTotal || undefined,
    };

    await sendFormEmail(data);

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'Unknown error';
    console.error('Failed to send form email:', msg);
    return new Response(JSON.stringify({ error: 'Failed to send message' }), {
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
