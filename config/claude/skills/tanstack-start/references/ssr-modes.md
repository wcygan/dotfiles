# TanStack Start — SSR Modes

## Selective SSR

Control SSR on a per-route basis using the `ssr` option.

```typescript
export const Route = createFileRoute('/dashboard')({
  // Default: SSR enabled
  ssr: true,

  // Disable SSR for this route (client-side only)
  ssr: false,

  // SSR for rendering, skip for data loading (loader runs client-side)
  ssr: 'data-only',

  // Dynamic SSR based on route params/search
  ssr: ({ params, search }) => {
    // Disable SSR for authenticated content
    return !search.skipSSR
  },
})
```

### SSR Inheritance Rules

- Child routes can only be **more restrictive** than parent (not less)
- `ssr: false` propagates to all children
- If any ancestor has `ssr: false`, children cannot enable SSR

### shellComponent Required

When a route has `ssr: false`, the root must provide a `shellComponent` for the HTML shell:

```typescript
// __root.tsx
export const Route = createRootRoute({
  component: RootComponent,
  shellComponent: ShellComponent,  // Rendered without React during SSR
})

function ShellComponent() {
  return (
    <html lang="en">
      <head>
        <HeadContent />
      </head>
      <body>
        <div id="root" />
        <Scripts />
      </body>
    </html>
  )
}
```

## SPA Mode

Turn TanStack Start into a pure SPA (no SSR at all).

### app.config.ts

```typescript
import { defineConfig } from '@tanstack/react-start/config'

export default defineConfig({
  routers: {
    ssr: false,  // or use tanstackStart({ spa: { enabled: true } })
  },
})
```

### SPA Config (alternative)

```typescript
import tanstackStart from '@tanstack/react-start/plugin'

export default defineConfig({
  plugins: [
    tanstackStart({
      spa: {
        enabled: true,
      },
    }),
  ],
})
```

### SPA Redirect Config

For hosting (Cloudflare, Netlify, etc.) in SPA mode, configure redirects:

```
# _redirects (Netlify)
/*    /index.html   200

# Cloudflare Pages (_redirects)
/*    /index.html   200
```

## Static Prerendering

Pre-render routes at build time.

```typescript
// app.config.ts
export default defineConfig({
  prerender: {
    // Automatically find routes by crawling links
    crawlLinks: true,

    // Starting paths for crawling
    routes: ['/', '/about', '/blog'],

    // Filter which routes to prerender
    filter: (path) => !path.startsWith('/admin'),

    // Concurrency for parallel prerendering
    concurrency: 4,

    // Retry failed routes
    retryCount: 3,
    retryDelay: 1000,

    // Failover behavior
    failOnError: false,
  },
})
```

### Manual Route List

```typescript
export default defineConfig({
  prerender: {
    routes: async () => {
      const posts = await fetchAllPosts()
      return [
        '/',
        '/about',
        ...posts.map(p => `/posts/${p.slug}`),
      ]
    },
  },
})
```

## Incremental Static Regeneration (ISR)

ISR serves stale content while revalidating in background.

### Cache-Control Headers

```typescript
// In a server function or route
setResponseHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=3600')
```

### Cloudflare ISR

```typescript
// wrangler.jsonc
{
  "cache_rules": [
    {
      "expression": "http.request.uri.path matches \"^/blog\"",
      "action_parameters": { "cache": true, "edge_ttl": { "value": 60 } }
    }
  ]
}
```

### Netlify ISR

```typescript
// In route loader
export const server = {
  GET: async () => {
    return json(data, {
      headers: {
        'Netlify-CDN-Cache-Control': 'public, max-age=0, stale-while-revalidate=31536000',
        'Cache-Tag': 'blog-posts',
      },
    })
  },
}
```

### On-Demand Revalidation

```typescript
// Revalidate specific tags
export const revalidatePost = createServerFn({ method: 'POST' })
  .handler(async ({ data: { tag } }) => {
    // Platform-specific revalidation
    // Netlify: purge by cache tag
    await fetch('https://api.netlify.com/api/v1/purge', {
      method: 'POST',
      headers: { Authorization: `Bearer ${process.env.NETLIFY_TOKEN}` },
      body: JSON.stringify({ site_id: SITE_ID, cache_tags: [tag] }),
    })
  })
```

## Multi-Tier Caching

```typescript
// CDN caching (server response)
setResponseHeader('Cache-Control', 's-maxage=300')

// Client caching (TanStack Router)
export const Route = createFileRoute('/posts')({
  staleTime: 5 * 60 * 1000,    // Fresh for 5 minutes on client
  gcTime: 10 * 60 * 1000,      // Keep in memory for 10 minutes
  loader: async () => getPosts(),
})

// React Query caching (for mutations pattern)
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000,
    },
  },
})
```
