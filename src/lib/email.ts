import type Stripe from 'stripe';

const RESEND_API_URL = 'https://api.resend.com/emails';

function escapeHtml(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

interface ResendPayload {
  from: string;
  to: string | string[];
  subject: string;
  html: string;
  reply_to?: string;
  bcc?: string | string[];
  headers?: Record<string, string>;
  tags?: Array<{ name: string; value: string }>;
}

interface ResendResponse {
  id?: string;
  statusCode?: number;
  message?: string;
  name?: string;
}

async function sendViaResend(payload: ResendPayload): Promise<string> {
  const apiKey = process.env.RESEND_API_KEY;
  if (!apiKey) {
    throw new Error('RESEND_API_KEY is not set');
  }

  const res = await fetch(RESEND_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  });

  const data: ResendResponse = await res.json();

  if (!res.ok) {
    throw new Error(`Resend API ${res.status}: ${data.message ?? JSON.stringify(data)}`);
  }

  return data.id ?? 'unknown';
}

function formatCurrency(amount: number | null | undefined): string {
  if (amount == null) return '£0.00';
  return `£${(amount / 100).toFixed(2)}`;
}

function buildEmailHtml(session: Stripe.Checkout.Session): string {
  const lineItems = session.line_items?.data ?? [];
  const shipping = session.shipping_details;
  const orderRef = session.payment_intent
    ? String(session.payment_intent).slice(-8).toUpperCase()
    : session.id?.slice(-8).toUpperCase() ?? 'N/A';

  const itemRows = lineItems
    .map(
      (item) => `
      <tr>
        <td style="padding:8px 0;border-bottom:1px solid #eee;">${item.description ?? 'Item'}</td>
        <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:center;">${item.quantity ?? 1}</td>
        <td style="padding:8px 0;border-bottom:1px solid #eee;text-align:right;">${formatCurrency(item.amount_total)}</td>
      </tr>`
    )
    .join('');

  const shippingAddress = shipping?.address
    ? [
        shipping.name,
        shipping.address.line1,
        shipping.address.line2,
        shipping.address.city,
        shipping.address.state,
        shipping.address.postal_code,
        shipping.address.country,
      ]
        .filter(Boolean)
        .join('<br>')
    : '';

  const taxAmount = session.total_details?.amount_tax;
  const shippingCost = session.shipping_cost?.amount_total;

  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:0 auto;background:#ffffff;">
    <!-- Header -->
    <div style="background:#1a1a1a;padding:24px;text-align:center;">
      <h1 style="color:#f47d23;margin:0;font-size:24px;letter-spacing:1px;">ROAM SYSTEMS</h1>
    </div>

    <!-- Content -->
    <div style="padding:32px 24px;">
      <h2 style="margin:0 0 8px;color:#1a1a1a;font-size:20px;">Order Confirmed</h2>
      <p style="margin:0 0 24px;color:#666;font-size:14px;">Reference: ${orderRef}</p>

      <!-- Line items -->
      <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:24px;">
        <thead>
          <tr style="border-bottom:2px solid #1a1a1a;">
            <th style="padding:8px 0;text-align:left;font-weight:600;">Item</th>
            <th style="padding:8px 0;text-align:center;font-weight:600;">Qty</th>
            <th style="padding:8px 0;text-align:right;font-weight:600;">Price</th>
          </tr>
        </thead>
        <tbody>
          ${itemRows}
        </tbody>
      </table>

      <!-- Totals -->
      <table style="width:100%;font-size:14px;margin-bottom:24px;">
        <tr>
          <td style="padding:4px 0;color:#666;">Subtotal</td>
          <td style="padding:4px 0;text-align:right;">${formatCurrency(session.amount_subtotal)}</td>
        </tr>
        ${taxAmount != null && taxAmount > 0 ? `
        <tr>
          <td style="padding:4px 0;color:#666;">VAT (20%)</td>
          <td style="padding:4px 0;text-align:right;">${formatCurrency(taxAmount)}</td>
        </tr>` : ''}
        ${shippingCost != null ? `
        <tr>
          <td style="padding:4px 0;color:#666;">Shipping</td>
          <td style="padding:4px 0;text-align:right;">${formatCurrency(shippingCost)}</td>
        </tr>` : ''}
        <tr style="border-top:2px solid #1a1a1a;">
          <td style="padding:12px 0 0;font-weight:700;font-size:16px;">Total</td>
          <td style="padding:12px 0 0;text-align:right;font-weight:700;font-size:16px;">${formatCurrency(session.amount_total)}</td>
        </tr>
      </table>

      ${shippingAddress ? `
      <!-- Shipping -->
      <div style="background:#f9f9f9;padding:16px;border-radius:8px;margin-bottom:24px;">
        <h3 style="margin:0 0 8px;font-size:14px;color:#666;font-weight:600;">Shipping Address</h3>
        <p style="margin:0;font-size:14px;line-height:1.6;">${shippingAddress}</p>
      </div>` : ''}

      <p style="font-size:14px;color:#666;line-height:1.6;">
        We'll be in touch with delivery details. For more information about our delivery process, visit our
        <a href="https://roamsystems.co.uk/delivery" style="color:#f47d23;">delivery information page</a>.
      </p>
    </div>

    <!-- Footer -->
    <div style="background:#1a1a1a;padding:24px;text-align:center;">
      <p style="margin:0 0 8px;color:#999;font-size:12px;">Roam Systems — Premium M1-Certified Campervan Furniture</p>
      <p style="margin:0;color:#999;font-size:12px;">
        <a href="mailto:sales@roamsystems.co.uk" style="color:#f47d23;">sales@roamsystems.co.uk</a>
      </p>
    </div>
  </div>
</body>
</html>`;
}

export async function sendConfirmationEmail(
  session: Stripe.Checkout.Session,
  eventId: string
): Promise<void> {
  const customerEmail = session.customer_details?.email;
  if (!customerEmail) {
    console.error('No customer email found on session — skipping confirmation email');
    return;
  }

  const orderRef = session.payment_intent
    ? String(session.payment_intent).slice(-8).toUpperCase()
    : session.id?.slice(-8).toUpperCase() ?? 'N/A';

  const emailId = await sendViaResend({
    from: 'Roam Systems <orders@roamsystems.co.uk>',
    reply_to: 'sales@roamsystems.co.uk',
    to: customerEmail,
    bcc: 'rob@romarkengineering.com',
    subject: `Order Confirmed — Roam Systems ${orderRef}`,
    html: buildEmailHtml(session),
    headers: { 'X-Entity-Ref-ID': eventId },
    tags: [{ name: 'category', value: 'order-confirmation' }],
  });

  console.log(`Confirmation email sent for session ${session.id} (event: ${eventId}, id: ${emailId})`);
}

// --- Form submission emails ---

export interface FormEmailData {
  type: 'contact' | 'enquiry';
  name: string;
  email: string;
  phone?: string;
  subject?: string;
  message?: string;
  basketItems?: string;
  basketTotal?: string;
}

function buildFormEmailHtml(data: FormEmailData): string {
  const isEnquiry = data.type === 'enquiry';

  const detailRows = [
    `<tr><td style="padding:8px 12px;font-weight:600;color:#666;border-bottom:1px solid #eee;width:140px;">Name</td><td style="padding:8px 12px;border-bottom:1px solid #eee;">${escapeHtml(data.name)}</td></tr>`,
    `<tr><td style="padding:8px 12px;font-weight:600;color:#666;border-bottom:1px solid #eee;">Email</td><td style="padding:8px 12px;border-bottom:1px solid #eee;"><a href="mailto:${escapeHtml(data.email)}" style="color:#f47d23;">${escapeHtml(data.email)}</a></td></tr>`,
    data.phone ? `<tr><td style="padding:8px 12px;font-weight:600;color:#666;border-bottom:1px solid #eee;">Phone</td><td style="padding:8px 12px;border-bottom:1px solid #eee;">${escapeHtml(data.phone)}</td></tr>` : '',
    data.subject ? `<tr><td style="padding:8px 12px;font-weight:600;color:#666;border-bottom:1px solid #eee;">Subject</td><td style="padding:8px 12px;border-bottom:1px solid #eee;">${escapeHtml(data.subject)}</td></tr>` : '',
  ].filter(Boolean).join('');

  const messageSection = data.message
    ? `<div style="background:#f9f9f9;padding:16px;border-radius:8px;margin-bottom:24px;">
        <h3 style="margin:0 0 8px;font-size:14px;color:#666;font-weight:600;">Message</h3>
        <p style="margin:0;font-size:14px;line-height:1.6;white-space:pre-wrap;">${escapeHtml(data.message)}</p>
      </div>`
    : '';

  const basketSection = isEnquiry && data.basketItems
    ? `<div style="background:#f9f9f9;padding:16px;border-radius:8px;margin-bottom:24px;">
        <h3 style="margin:0 0 8px;font-size:14px;color:#666;font-weight:600;">Basket Items</h3>
        <p style="margin:0;font-size:14px;line-height:1.6;white-space:pre-wrap;">${escapeHtml(data.basketItems)}</p>
        ${data.basketTotal ? `<p style="margin:12px 0 0;font-size:16px;font-weight:700;">Total: ${escapeHtml(data.basketTotal)}</p>` : ''}
      </div>`
    : '';

  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:0 auto;background:#ffffff;">
    <div style="background:#1a1a1a;padding:24px;text-align:center;">
      <h1 style="color:#f47d23;margin:0;font-size:24px;letter-spacing:1px;">ROAM SYSTEMS</h1>
    </div>
    <div style="padding:32px 24px;">
      <h2 style="margin:0 0 24px;color:#1a1a1a;font-size:20px;">${isEnquiry ? 'New Basket Enquiry' : 'New Contact Form Submission'}</h2>
      <table style="width:100%;border-collapse:collapse;font-size:14px;margin-bottom:24px;">
        ${detailRows}
      </table>
      ${messageSection}
      ${basketSection}
    </div>
    <div style="background:#1a1a1a;padding:24px;text-align:center;">
      <p style="margin:0 0 8px;color:#999;font-size:12px;">Roam Systems — Premium M1-Certified Campervan Furniture</p>
      <p style="margin:0;color:#999;font-size:12px;">
        <a href="mailto:sales@roamsystems.co.uk" style="color:#f47d23;">sales@roamsystems.co.uk</a>
      </p>
    </div>
  </div>
</body>
</html>`;
}

export async function sendFormEmail(data: FormEmailData): Promise<void> {
  const isEnquiry = data.type === 'enquiry';
  const subject = isEnquiry
    ? 'New Basket Enquiry from ROAM Systems Website'
    : `New Contact from ROAM Systems Website — ${data.subject ?? 'General'}`;

  console.log(`[contact] Sending ${data.type} email from ${data.email}`);

  const emailId = await sendViaResend({
    from: 'Roam Systems <website@roamsystems.co.uk>',
    reply_to: data.email,
    to: 'sales@roamsystems.co.uk',
    subject,
    html: buildFormEmailHtml(data),
    tags: [{ name: 'category', value: isEnquiry ? 'basket-enquiry' : 'contact-form' }],
  });

  console.log(`[contact] Email sent successfully, id: ${emailId}`);
}

// --- Marketing draft emails ---

export interface MarketingDraftData {
  blogDraft: {
    title: string;
    markdown: string;
    keywords: string[];
  };
  socialPosts: Array<{
    day: string;
    caption: string;
    hashtags: string[];
    imageSource: string;
    link: string;
  }>;
}

function buildMarketingDraftHtml(data: MarketingDraftData): string {
  const socialPostRows = data.socialPosts
    .map(
      (post) => `
      <div style="background:#f9f9f9;padding:16px;border-radius:8px;margin-bottom:16px;">
        <h3 style="margin:0 0 8px;font-size:14px;color:#f47d23;font-weight:600;">${escapeHtml(post.day)}</h3>
        <p style="margin:0 0 8px;font-size:14px;line-height:1.6;white-space:pre-wrap;">${escapeHtml(post.caption)}</p>
        <p style="margin:0 0 4px;font-size:12px;color:#666;">Hashtags: ${post.hashtags.map(h => escapeHtml(h)).join(' ')}</p>
        <p style="margin:0 0 4px;font-size:12px;color:#666;">Image: ${escapeHtml(post.imageSource)}</p>
        <p style="margin:0;font-size:12px;color:#666;">Link: <a href="${escapeHtml(post.link)}" style="color:#f47d23;">${escapeHtml(post.link)}</a></p>
      </div>`
    )
    .join('');

  return `<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head>
<body style="margin:0;padding:0;background:#f5f5f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;">
  <div style="max-width:600px;margin:0 auto;background:#ffffff;">
    <div style="background:#1a1a1a;padding:24px;text-align:center;">
      <h1 style="color:#f47d23;margin:0;font-size:24px;letter-spacing:1px;">ROAM SYSTEMS</h1>
      <p style="color:#999;margin:8px 0 0;font-size:14px;">Weekly Marketing Drafts</p>
    </div>
    <div style="padding:32px 24px;">
      <h2 style="margin:0 0 16px;color:#1a1a1a;font-size:20px;">Blog Draft: ${escapeHtml(data.blogDraft.title)}</h2>
      <p style="margin:0 0 8px;font-size:12px;color:#666;">Target keywords: ${data.blogDraft.keywords.map(k => escapeHtml(k)).join(', ')}</p>
      <div style="background:#f9f9f9;padding:16px;border-radius:8px;margin-bottom:24px;font-size:14px;line-height:1.6;white-space:pre-wrap;">${escapeHtml(data.blogDraft.markdown)}</div>

      <h2 style="margin:0 0 16px;color:#1a1a1a;font-size:20px;">Social Media Posts</h2>
      ${socialPostRows}
    </div>
    <div style="background:#1a1a1a;padding:24px;text-align:center;">
      <p style="margin:0;color:#999;font-size:12px;">Reply to approve or request changes. Start a Claude session to publish.</p>
    </div>
  </div>
</body>
</html>`;
}

export async function sendMarketingDrafts(data: MarketingDraftData): Promise<void> {
  console.log(`[marketing] Sending draft email: ${data.blogDraft.title}`);

  const emailId = await sendViaResend({
    from: 'Roam Systems <website@roamsystems.co.uk>',
    reply_to: 'sales@roamsystems.co.uk',
    to: 'sales@roamsystems.co.uk',
    bcc: 'rob@romarkengineering.com',
    subject: `Weekly Marketing Drafts — ${data.blogDraft.title}`,
    html: buildMarketingDraftHtml(data),
    tags: [{ name: 'category', value: 'marketing-draft' }],
  });

  console.log(`[marketing] Draft email sent, id: ${emailId}`);
}
