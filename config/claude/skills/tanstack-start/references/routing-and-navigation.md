# TanStack Start — Routing & Navigation

TanStack Start uses TanStack Router's file-based routing. Routes are defined in `src/routes/`.

## File Naming Conventions

| Pattern | URL | Description |
|---------|-----|-------------|
| `__root.tsx` | (all routes) | Root layout, wraps all routes |
| `index.tsx` | `/` | Index of current directory |
| `about.tsx` | `/about` | Static segment |
| `posts.tsx` | `/posts` | Layout for posts/* routes |
| `posts.index.tsx` | `/posts/` | Index of posts |
| `posts.$postId.tsx` | `/posts/:postId` | Dynamic segment |
| `posts_.$postId.edit.tsx` | `/posts/:postId/edit` | Flat file, path separator |
| `_authed.tsx` | (pathless) | Pathless layout (no URL segment added) |
| `_authed.dashboard.tsx` | `/dashboard` | Child of pathless layout |
| `(marketing).tsx` | (group) | Route group, no URL impact |
| `files.$.tsx` | `/files/*` | Splat/wildcard (catch-all) |
| `about.lazy.tsx` | `/about` | Code-split lazy route |
| `[.]well-known.tsx` | `/.well-known` | Literal dot in segment |

## createFileRoute

```typescript
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/posts/$postId')({
  // Type-safe params
  params: {
    parse: (params) => ({ postId: Number(params.postId) }),
    stringify: ({ postId }) => ({ postId: String(postId) }),
  },

  // Validate/parse search params
  validateSearch: (search) => ({
    page: Number(search.page ?? 1),
    filter: String(search.filter ?? ''),
  }),

  // Load data (isomorphic — runs on server AND client)
  loader: async ({ params, context }) => {
    const post = await fetchPost(params.postId)
    return { post }
  },

  // Head tags
  head: ({ loaderData }) => ({
    meta: [{ title: loaderData?.post.title }],
  }),

  // Components
  component: PostPage,
  errorComponent: PostErrorPage,
  pendingComponent: PostSkeleton,
  notFoundComponent: PostNotFound,
})

function PostPage() {
  const { post } = Route.useLoaderData()
  const { postId } = Route.useParams()
  const { page } = Route.useSearch()
  return <div>{post.title}</div>
}
```

## Link Component

```typescript
import { Link } from '@tanstack/react-router'

// Basic navigation
<Link to="/posts/$postId" params={{ postId: post.id }}>
  {post.title}
</Link>

// With search params
<Link to="/posts" search={{ page: 2, filter: 'react' }}>
  Next page
</Link>

// Active styling
<Link
  to="/dashboard"
  activeProps={{ className: 'font-bold text-blue-500' }}
  inactiveProps={{ className: 'text-gray-600' }}
>
  Dashboard
</Link>

// Preload on hover/focus
<Link to="/about" preload="intent">About</Link>
<Link to="/about" preload="viewport">About</Link>

// External link
<Link href="https://example.com" target="_blank">External</Link>
```

## Navigation Hooks

```typescript
import { useNavigate, useRouter, useParams, useSearch, useLocation } from '@tanstack/react-router'

// Programmatic navigation
function Component() {
  const navigate = useNavigate()

  const handleClick = () => {
    navigate({ to: '/posts/$postId', params: { postId: '123' } })
    // With search params
    navigate({ to: '/search', search: { q: 'tanstack' } })
    // Replace history entry
    navigate({ to: '/login', replace: true })
  }
}

// Access route params
function Post() {
  const { postId } = useParams({ from: '/posts/$postId' })
}

// Access search params
function SearchPage() {
  const search = useSearch({ from: '/search' })
}

// Full router access
function Component() {
  const router = useRouter()
  router.invalidate() // Reload all loaders
}

// Current location
function Component() {
  const location = useLocation()
  console.log(location.pathname) // "/posts/123"
}
```

## Pathless Layouts (Route Groups)

Pathless layouts let you share UI and logic without adding URL segments.

```
src/routes/
  _authed.tsx           # Pathless layout: checks auth in beforeLoad
  _authed.dashboard.tsx # /dashboard (protected)
  _authed.profile.tsx   # /profile (protected)
  login.tsx             # /login (public)
```

```typescript
// _authed.tsx
export const Route = createFileRoute('/_authed')({
  beforeLoad: async ({ context }) => {
    if (!context.user) {
      throw redirect({ to: '/login' })
    }
  },
  component: Outlet, // Just pass through
})
```

## beforeLoad

Runs before the route loads. Use for auth checks, redirects, context setup.

```typescript
export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context, params, search }) => {
    // Throw redirects
    if (!context.user) throw redirect({ to: '/login' })

    // Return additional context for this route
    return { isAdmin: context.user.role === 'admin' }
  },
})
```

## Route Context

Pass data from `createRouter` context down through routes.

```typescript
// router.tsx
createRouter({ routeTree, context: { user: null, queryClient } })

// Any route
export const Route = createFileRoute('/dashboard')({
  beforeLoad: ({ context }) => {
    context.user    // typed from Register
    context.queryClient
  },
})
```
