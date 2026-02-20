# TanStack Start — SEO & Head Management

## Route head() Property

```typescript
export const Route = createFileRoute('/about')({
  head: () => ({
    meta: [
      { title: 'About Us | My App' },
      { name: 'description', content: 'Learn about our mission and team' },
    ],
    links: [
      { rel: 'canonical', href: 'https://myapp.com/about' },
    ],
  }),
  component: AboutPage,
})
```

## Dynamic Meta from Loader Data

```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await getPostFn({ data: { id: params.postId } })
    return { post }
  },
  head: ({ loaderData }) => ({
    meta: [
      { title: loaderData?.post.title ?? 'Post Not Found' },
      { name: 'description', content: loaderData?.post.excerpt },
      { name: 'author', content: loaderData?.post.author.name },
    ],
  }),
  component: PostPage,
})
```

## Open Graph Tags

```typescript
head: ({ loaderData }) => ({
  meta: [
    { title: loaderData?.post.title },
    { property: 'og:title', content: loaderData?.post.title },
    { property: 'og:description', content: loaderData?.post.excerpt },
    { property: 'og:image', content: loaderData?.post.coverImage },
    { property: 'og:url', content: `https://myapp.com/posts/${loaderData?.post.slug}` },
    { property: 'og:type', content: 'article' },
    { property: 'og:site_name', content: 'My App' },
    // Twitter Card
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: loaderData?.post.title },
    { name: 'twitter:description', content: loaderData?.post.excerpt },
    { name: 'twitter:image', content: loaderData?.post.coverImage },
  ],
}),
```

## Root Route Meta (Defaults)

```typescript
// __root.tsx
export const Route = createRootRoute({
  head: () => ({
    meta: [
      { charSet: 'utf-8' },
      { name: 'viewport', content: 'width=device-width, initial-scale=1' },
      { title: 'My App' },
      { name: 'description', content: 'Default description for all pages' },
    ],
    links: [
      { rel: 'icon', href: '/favicon.ico' },
      { rel: 'apple-touch-icon', href: '/apple-touch-icon.png' },
    ],
  }),
})
```

## Structured Data (JSON-LD)

```typescript
head: ({ loaderData }) => ({
  scripts: [
    {
      type: 'application/ld+json',
      children: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'Article',
        headline: loaderData?.post.title,
        author: {
          '@type': 'Person',
          name: loaderData?.post.author.name,
        },
        datePublished: loaderData?.post.publishedAt,
        image: loaderData?.post.coverImage,
      }),
    },
  ],
}),
```

## Sitemaps

### Static sitemap.xml

```
public/sitemap.xml
```

### Dynamic sitemap via server route

```typescript
// src/routes/sitemap[.]xml.tsx
export const Route = createFileRoute('/sitemap[.]xml')({})

export const server = {
  GET: async () => {
    const posts = await getAllPostsFn()

    const urls = [
      { loc: 'https://myapp.com/', priority: '1.0', changefreq: 'weekly' },
      { loc: 'https://myapp.com/about', priority: '0.8', changefreq: 'monthly' },
      ...posts.map(post => ({
        loc: `https://myapp.com/posts/${post.slug}`,
        priority: '0.7',
        changefreq: 'weekly',
        lastmod: post.updatedAt.toISOString().split('T')[0],
      })),
    ]

    const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${urls.map(url => `  <url>
    <loc>${url.loc}</loc>
    <priority>${url.priority}</priority>
    <changefreq>${url.changefreq}</changefreq>
    ${url.lastmod ? `<lastmod>${url.lastmod}</lastmod>` : ''}
  </url>`).join('\n')}
</urlset>`

    return new Response(xml, {
      headers: { 'Content-Type': 'application/xml' },
    })
  },
}
```

## robots.txt

### Static

```
public/robots.txt
```

```
User-agent: *
Allow: /
Sitemap: https://myapp.com/sitemap.xml
Disallow: /admin/
Disallow: /api/
```

### Dynamic via server route

```typescript
// src/routes/robots[.]txt.tsx
export const Route = createFileRoute('/robots[.]txt')({})

export const server = {
  GET: async () => {
    const content = `User-agent: *
Allow: /
Sitemap: ${process.env.APP_URL}/sitemap.xml
Disallow: /admin/
Disallow: /api/
`
    return new Response(content, {
      headers: { 'Content-Type': 'text/plain' },
    })
  },
}
```

## Canonical URLs

```typescript
// In root route — set base canonical
head: () => ({
  links: [
    { rel: 'canonical', href: `https://myapp.com${useLocation().pathname}` },
  ],
}),

// In specific routes — override
head: ({ loaderData }) => ({
  links: [
    { rel: 'canonical', href: `https://myapp.com/posts/${loaderData?.post.slug}` },
  ],
}),
```

## Preconnect / DNS Prefetch

```typescript
// __root.tsx head
links: [
  { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
  { rel: 'dns-prefetch', href: 'https://cdn.example.com' },
  { rel: 'preload', href: '/fonts/inter.woff2', as: 'font', type: 'font/woff2', crossOrigin: 'anonymous' },
],
```
