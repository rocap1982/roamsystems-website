import type { APIRoute } from 'astro';
import { sendMarketingDrafts, type MarketingDraftData } from '../../../lib/email';

export const prerender = false;

export const POST: APIRoute = async ({ request }) => {
  try {
    const authToken = process.env.MARKETING_API_TOKEN;
    if (!authToken) {
      console.error('[marketing] MARKETING_API_TOKEN not configured');
      return new Response(JSON.stringify({ error: 'Service not configured' }), {
        status: 503,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const authHeader = request.headers.get('Authorization');
    if (!authHeader?.startsWith('Bearer ') || authHeader.slice(7) !== authToken) {
      return new Response(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    const body = await request.json() as MarketingDraftData;

    if (!body.blogDraft?.title || typeof body.blogDraft.title !== 'string' || !body.blogDraft.title.trim()) {
      return new Response(JSON.stringify({ error: 'blogDraft.title is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!body.blogDraft?.markdown || typeof body.blogDraft.markdown !== 'string' || !body.blogDraft.markdown.trim()) {
      return new Response(JSON.stringify({ error: 'blogDraft.markdown is required' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!Array.isArray(body.socialPosts) || body.socialPosts.length === 0) {
      return new Response(JSON.stringify({ error: 'socialPosts array is required and must not be empty' }), {
        status: 400,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    for (const post of body.socialPosts) {
      if (!post.day || typeof post.day !== 'string' ||
          !post.caption || typeof post.caption !== 'string' ||
          !Array.isArray(post.hashtags) ||
          !post.imageSource || typeof post.imageSource !== 'string' ||
          !post.link || typeof post.link !== 'string') {
        return new Response(JSON.stringify({ error: 'Each socialPost must have day, caption, hashtags[], imageSource, and link' }), {
          status: 400,
          headers: { 'Content-Type': 'application/json' },
        });
      }
    }

    await sendMarketingDrafts(body);

    return new Response(JSON.stringify({ success: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Unknown error';
    console.error('[marketing] Error sending drafts:', message);
    return new Response(JSON.stringify({ error: 'Failed to send drafts' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};
