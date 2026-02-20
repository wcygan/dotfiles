# TanStack Start — Execution Model

## Core Principle: Isomorphic by Default

Code in TanStack Start runs in **both** server and client bundles unless explicitly constrained. This is the most important concept to understand.

```
┌─────────────────────────────────────────────┐
│              Isomorphic Code                │
│  (route components, loaders, utilities)     │
│  ┌──────────┐             ┌──────────────┐  │
│  │  Server  │             │   Client     │  │
│  │  Bundle  │             │   Bundle     │  │
│  └──────────┘             └──────────────┘  │
└─────────────────────────────────────────────┘
```

## Environment Functions

### createServerFn — RPC Pattern

Client makes an HTTP request to the server. Code only runs on server.

```typescript
import { createServerFn } from '@tanstack/react-start'

export const getSecret = createServerFn({ method: 'GET' })
  .handler(async () => {
    return process.env.SECRET_KEY  // Safe: only runs on server
  })
```

### createServerOnlyFn — Throws on Client

```typescript
import { createServerOnlyFn } from '@tanstack/react-start'

// Will throw an error if somehow called from client
export const serverOnlyHelper = createServerOnlyFn()
  .handler(async (data: { id: string }) => {
    return await db.sensitiveTable.findUnique({ where: { id: data.id } })
  })
```

### createClientOnlyFn — Throws on Server

```typescript
import { createClientOnlyFn } from '@tanstack/react-start'

// Will throw if called during SSR
export const getBrowserStorage = createClientOnlyFn()
  .handler(() => {
    return localStorage.getItem('user-preferences')
  })
```

### createIsomorphicFn — Different Per Environment

```typescript
import { createIsomorphicFn } from '@tanstack/react-start'

export const getUser = createIsomorphicFn()
  .server(async () => {
    // Runs on server: direct DB access
    return await db.user.findFirst()
  })
  .client(async () => {
    // Runs on client: API call
    return await fetch('/api/user').then(r => r.json())
  })
```

## Client-Only Components

```typescript
import { ClientOnly } from '@tanstack/react-start'
import { useHydrated } from '@tanstack/react-start'

// Render only on client (after hydration)
function MapWidget() {
  return (
    <ClientOnly fallback={<MapSkeleton />}>
      {() => <InteractiveMap />}
    </ClientOnly>
  )
}

// Hook version
function DateDisplay() {
  const isHydrated = useHydrated()
  if (!isHydrated) return <span>Loading...</span>
  return <span>{new Date().toLocaleString()}</span>  // Locale-dependent, client-only
}
```

## Common Anti-Patterns

### ❌ Exposing server secrets in loaders

```typescript
// WRONG: Loader runs on client too!
export const Route = createFileRoute('/posts')({
  loader: async () => {
    // This code runs on the CLIENT during navigation
    // process.env.DATABASE_URL will be undefined
    const db = new PrismaClient({ datasourceUrl: process.env.DATABASE_URL })
    return db.post.findMany()
  },
})

// CORRECT: Use a server function for DB access
export const getPostsFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const db = new PrismaClient({ datasourceUrl: process.env.DATABASE_URL })
    return db.post.findMany()
  })

export const Route = createFileRoute('/posts')({
  loader: async () => getPostsFn(),
})
```

### ❌ Assuming loaders only run on server

```typescript
// WRONG assumption
export const Route = createFileRoute('/dashboard')({
  loader: async () => {
    // Don't assume server-only environment here
    const headers = getRequestHeaders()  // Only works during SSR!
  },
})
```

### ❌ Using browser APIs in isomorphic code

```typescript
// WRONG: window is undefined on server
const theme = window.localStorage.getItem('theme')

// CORRECT: Guard with typeof check or ClientOnly
const theme = typeof window !== 'undefined'
  ? window.localStorage.getItem('theme')
  : null
```

## Architecture Decision Framework

| Need | Solution |
|------|----------|
| DB access from component | `createServerFn` in loader |
| Secret env var | `process.env.SECRET` in `createServerFn` handler |
| Client-only browser API | `createClientOnlyFn` or `ClientOnly` component |
| Same logic, different impl | `createIsomorphicFn` with `.server()` + `.client()` |
| Always throws if wrong env | `createServerOnlyFn` or `createClientOnlyFn` |
| After-hydration render | `useHydrated()` hook |
| Conditional SSR | Route's `ssr` option (see ssr-modes.md) |

## Build Bundles

TanStack Start creates two bundles:
1. **Server bundle** (`src/ssr.tsx` entry) — handles SSR requests
2. **Client bundle** (`src/client.tsx` entry) — hydrates and handles navigation

Import protection enforces boundaries between them (see import-protection.md).
