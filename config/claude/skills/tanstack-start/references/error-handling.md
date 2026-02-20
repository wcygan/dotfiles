# TanStack Start — Error Handling

## Route Error Components

```typescript
import { createFileRoute, ErrorComponentProps } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await getPostFn({ data: { id: params.postId } })
    if (!post) throw notFound()
    return { post }
  },
  component: PostPage,
  errorComponent: PostError,
  pendingComponent: PostSkeleton,
  notFoundComponent: PostNotFound,
})

function PostError({ error, reset }: ErrorComponentProps) {
  return (
    <div>
      <h2>Something went wrong</h2>
      <p>{error.message}</p>
      <button onClick={reset}>Try again</button>
    </div>
  )
}

function PostNotFound() {
  return (
    <div>
      <h2>Post not found</h2>
      <Link to="/posts">Back to posts</Link>
    </div>
  )
}
```

## Default Error Component (Global)

```typescript
// router.tsx
const router = createRouter({
  routeTree,
  defaultErrorComponent: ({ error }) => (
    <div>
      <h1>Error</h1>
      <pre>{error.message}</pre>
    </div>
  ),
  defaultNotFoundComponent: () => (
    <div>
      <h1>404 - Not Found</h1>
      <Link to="/">Go home</Link>
    </div>
  ),
})
```

## notFound() — 404 Responses

```typescript
import { notFound, createServerFn } from '@tanstack/react-start'
import { notFound as routerNotFound } from '@tanstack/react-router'

// In a server function
export const getPostFn = createServerFn({ method: 'GET' })
  .handler(async ({ data }) => {
    const post = await db.post.findUnique({ where: { id: data.id } })
    if (!post) throw notFound()
    return post
  })

// In a route loader
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await getPostFn({ data: { id: params.postId } })
    // notFound() from server function propagates automatically
    return { post }
  },
})
```

## redirect() — Navigation from Loaders

```typescript
import { redirect } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard')({
  loader: async ({ context }) => {
    if (!context.user) {
      throw redirect({ to: '/login', search: { returnTo: '/dashboard' } })
    }
  },
})

// In server functions
export const protectedActionFn = createServerFn({ method: 'POST' })
  .handler(async () => {
    const session = await getSession()
    if (!session.user) throw redirect({ to: '/login' })
    return performAction()
  })
```

## Hydration Errors

Hydration errors occur when server-rendered HTML doesn't match client render.

### Strategy 1: Make server and client match

```typescript
// WRONG: Date varies between server render and client hydration
function Timestamp() {
  return <span>{new Date().toLocaleString()}</span>
}

// CORRECT: Use a stable value from loader
function Timestamp({ serverTime }: { serverTime: string }) {
  return <span>{serverTime}</span>
}
```

### Strategy 2: Locale/Timezone Middleware

```typescript
// Middleware to set deterministic locale from cookies
const localeMiddleware = createMiddleware()
  .server(async ({ next, request }) => {
    const locale = getCookie('locale') ?? 'en-US'
    const timezone = getCookie('timezone') ?? 'UTC'
    return next({ context: { locale, timezone }, sendContext: { locale, timezone } })
  })
  .client(async ({ next, context }) => {
    // Apply locale from server context to client
    Intl.NumberFormat = // patch if needed
    return next()
  })
```

### Strategy 3: ClientOnly Component

```typescript
import { ClientOnly } from '@tanstack/react-start'

function LocalTime() {
  return (
    <ClientOnly fallback={<span>Loading time...</span>}>
      {() => <span>{new Date().toLocaleString()}</span>}
    </ClientOnly>
  )
}
```

### Strategy 4: Selective SSR

```typescript
// Disable SSR for problematic routes
export const Route = createFileRoute('/dashboard/analytics')({
  ssr: false,
  component: AnalyticsDashboard,
})
```

### Strategy 5: suppressHydrationWarning

```typescript
// For elements that intentionally differ (e.g., timestamps)
<time
  dateTime={serverIsoDate}
  suppressHydrationWarning
>
  {clientLocalDate}
</time>
```

## Error Boundaries in Components

```typescript
import { ErrorBoundary } from 'react-error-boundary'

function App() {
  return (
    <ErrorBoundary
      fallback={<div>Something went wrong</div>}
      onError={(error, info) => logError(error, info)}
    >
      <FeatureComponent />
    </ErrorBoundary>
  )
}
```

## Error Logging

```typescript
// router.tsx — log all unhandled errors
const router = createRouter({
  routeTree,
  onError: (error) => {
    console.error('Router error:', error)
    // Send to Sentry, LogRocket, etc.
    Sentry.captureException(error)
  },
})
```

## HTTP Status Codes

```typescript
// Set status from server function
export const getProtectedDataFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const session = await getSession()
    if (!session.user) {
      setResponseStatus(401)
      throw new Error('Unauthorized')
    }
    if (!session.user.isAdmin) {
      setResponseStatus(403)
      throw new Error('Forbidden')
    }
    return sensitiveData
  })
```
