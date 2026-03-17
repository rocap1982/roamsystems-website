import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/blog' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    publishedDate: z.date(),
    updatedDate: z.date().optional(),
    author: z.string().default('ROAM Systems'),
    category: z.enum(['guides', 'products', 'lifestyle', 'certification', 'news']),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    draft: z.boolean().default(true),
    keywords: z.array(z.string()).default([]),
  }),
});

export const collections = { blog };
