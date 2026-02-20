# TanStack Start — Server Routes

Server routes let you define HTTP API endpoints using the file-based routing system.

## Basic Server Route

```typescript
// src/routes/api/health.tsx
import { createFileRoute } from '@tanstack/react-router'
import { json } from '@tanstack/react-start'

export const Route = createFileRoute('/api/health')({
  // No component — this is a pure API route
})

export const server = {
  GET: async () => {
    return json({ status: 'ok', timestamp: new Date().toISOString() })
  },
}
```

## HTTP Methods

```typescript
// src/routes/api/posts.tsx
export const Route = createFileRoute('/api/posts')({})

export const server = {
  GET: async ({ request, context }) => {
    const posts = await db.post.findMany()
    return json(posts)
  },

  POST: async ({ request }) => {
    const body = await request.json()
    const post = await db.post.create({ data: body })
    return json(post, { status: 201 })
  },
}
```

## Dynamic Params

```typescript
// src/routes/api/posts.$postId.tsx
export const Route = createFileRoute('/api/posts/$postId')({})

export const server = {
  GET: async ({ params }) => {
    const post = await db.post.findUnique({ where: { id: params.postId } })
    if (!post) return json({ error: 'Not found' }, { status: 404 })
    return json(post)
  },

  PUT: async ({ params, request }) => {
    const body = await request.json()
    const post = await db.post.update({ where: { id: params.postId }, data: body })
    return json(post)
  },

  DELETE: async ({ params }) => {
    await db.post.delete({ where: { id: params.postId } })
    return json({ success: true })
  },

  PATCH: async ({ params, request }) => {
    const body = await request.json()
    const post = await db.post.update({ where: { id: params.postId }, data: body })
    return json(post)
  },
}
```

## Wildcard / Splat Routes

```typescript
// src/routes/api/files.$.tsx  (catches /api/files/*)
export const Route = createFileRoute('/api/files/$')({})

export const server = {
  GET: async ({ params }) => {
    const filePath = params['*']  // Everything after /api/files/
    const file = await readFile(filePath)
    return new Response(file, {
      headers: { 'Content-Type': getContentType(filePath) },
    })
  },
}
```

## Handler Context

```typescript
export const server = {
  GET: async ({ request, params, context }) => {
    // request: Request object
    request.headers.get('Authorization')
    await request.json()
    await request.formData()
    new URL(request.url).searchParams.get('filter')

    // params: URL params
    params.postId

    // context: from request middleware
    context.user
    context.db
  },
}
```

## Per-Method Middleware

```typescript
import { createHandlers } from '@tanstack/react-start'

export const server = createHandlers({
  GET: {
    middleware: [publicMiddleware],
    handler: async ({ params }) => {
      return json(await getPublicData())
    },
  },
  POST: {
    middleware: [authMiddleware, rateLimitMiddleware],
    handler: async ({ params, context }) => {
      return json(await createResource(context.user, params))
    },
  },
})
```

## Response Helpers

```typescript
import { json, redirect } from '@tanstack/react-start'

// JSON response
return json({ data: result })
return json({ error: 'Forbidden' }, { status: 403 })

// Redirect
return redirect('/login', { status: 302 })

// Custom response
return new Response('Plain text', {
  status: 200,
  headers: { 'Content-Type': 'text/plain' },
})

// Stream
return new Response(
  new ReadableStream({
    start(controller) {
      controller.enqueue('data: hello\n\n')
      controller.close()
    },
  }),
  { headers: { 'Content-Type': 'text/event-stream' } }
)
```

## Escaped File Routes (Literal Dots)

```typescript
// src/routes/[.]well-known.health.tsx → /.well-known/health
// src/routes/sitemap[.]xml.tsx → /sitemap.xml
// src/routes/robots[.]txt.tsx → /robots.txt

export const Route = createFileRoute('/sitemap[.]xml')({})

export const server = {
  GET: async () => {
    const xml = generateSitemapXml()
    return new Response(xml, {
      headers: { 'Content-Type': 'application/xml' },
    })
  },
}
```

## Colocating with App Routes

Server routes can be colocated with their app routes:

```typescript
// src/routes/posts/$postId.tsx
// This file handles BOTH the React component route AND API requests

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => getPosts(params.postId),
  component: PostPage,
})

// API handler — same file, different export
export const server = {
  DELETE: async ({ params, context }) => {
    if (!context.user) return json({ error: 'Unauthorized' }, { status: 401 })
    await db.post.delete({ where: { id: params.postId } })
    return json({ success: true })
  },
}
```

## CORS Setup

```typescript
// src/routes/api/$.tsx — catch-all for CORS preflight
export const server = {
  OPTIONS: async ({ request }) => {
    return new Response(null, {
      status: 204,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, PATCH',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    })
  },
}
```
