# TanStack Start — Middleware

TanStack Start has two types of middleware that serve different purposes.

## Middleware Types

| Type | Scope | Use For |
|------|-------|---------|
| Request middleware | HTTP requests | Auth, logging, headers, CORS |
| Function middleware | Server functions | Shared logic, context injection |

## Request Middleware

Runs for every HTTP request to the server.

```typescript
import { createMiddleware } from '@tanstack/react-start'

// src/middleware/auth.ts
export const authMiddleware = createMiddleware()
  .server(async ({ next, request }) => {
    const token = request.headers.get('Authorization')?.replace('Bearer ', '')
    const user = token ? await verifyToken(token) : null

    return next({
      context: { user },
      // Optionally send context to client
      sendContext: { isAuthenticated: !!user },
    })
  })
  .client(async ({ next, context }) => {
    // context.isAuthenticated is available on client
    return next()
  })
```

## Function Middleware

Runs around specific server functions.

```typescript
// type: 'function' targets server functions, not all requests
export const loggingMiddleware = createMiddleware({ type: 'function' })
  .server(async ({ next, context }) => {
    console.log('Server function called')
    const result = await next()
    console.log('Server function complete')
    return result
  })
  .client(async ({ next }) => {
    console.log('Client calling server function')
    const result = await next()
    console.log('Server function returned')
    return result
  })
```

## Middleware Composition

```typescript
const withAuth = createMiddleware()
  .server(async ({ next }) => {
    const session = await getSession()
    if (!session.user) throw redirect({ to: '/login' })
    return next({ context: { user: session.user } })
  })

const withRateLimit = createMiddleware()
  .server(async ({ next, request }) => {
    await checkRateLimit(request.ip)
    return next()
  })

// Apply multiple to a server function
export const sensitiveAction = createServerFn({ method: 'POST' })
  .middleware([withAuth, withRateLimit])
  .handler(async ({ context }) => {
    // context.user from withAuth
    return performAction(context.user)
  })
```

## Context Passing

```typescript
// Middleware can add to context for downstream handlers
const dbMiddleware = createMiddleware()
  .server(async ({ next }) => {
    const db = createDbClient()
    try {
      return await next({ context: { db } })
    } finally {
      await db.disconnect()
    }
  })

export const getUsers = createServerFn({ method: 'GET' })
  .middleware([dbMiddleware])
  .handler(async ({ context }) => {
    return await context.db.user.findMany()
  })
```

## sendContext (Server → Client)

```typescript
const themeMiddleware = createMiddleware()
  .server(async ({ next, request }) => {
    const theme = getCookie(request, 'theme') ?? 'light'
    return next({ sendContext: { theme } })
  })
  .client(async ({ next, context }) => {
    // context.theme available on client
    applyTheme(context.theme)
    return next()
  })
```

## Global Middleware

Apply middleware to all requests via `src/start.ts`:

```typescript
// src/start.ts
import { createStart } from '@tanstack/react-start/server'
import { authMiddleware, loggingMiddleware } from './middleware'

export default createStart({
  middleware: [loggingMiddleware, authMiddleware],
})
```

Register in app.config.ts:

```typescript
export default defineConfig({
  routers: {
    ssr: {
      middleware: ['./src/start.ts'],
    },
  },
})
```

## Custom Headers / Fetch Override

```typescript
// Override fetch for all server function calls from this middleware context
const corsMiddleware = createMiddleware()
  .client(async ({ next, fetchFn }) => {
    return next({
      fetchFn: async (url, options) => {
        return fetchFn(url, {
          ...options,
          headers: {
            ...options?.headers,
            'X-Client-Version': APP_VERSION,
          },
        })
      },
    })
  })
```

## Execution Order

1. Global middleware (in order registered)
2. Route-level request middleware
3. Server function middleware (innermost)
4. Handler

Middleware wraps like onion layers — each `next()` call goes deeper.

```typescript
// Middleware A wraps Middleware B wraps Handler
// A.before → B.before → Handler → B.after → A.after
```
