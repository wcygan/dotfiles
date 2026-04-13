# Routing & Consistency Anchor

## File-based router

Routes live in `src/routes/` and are discovered automatically. The generator writes `src/routeTree.gen.ts` — never edit it by hand; re-run the dev server.

## `__root.tsx` is the consistency anchor

Every page is rendered inside `__root.tsx`'s `<Outlet />`. **Treat `__root.tsx` as the single source of truth for site chrome**:

- Top nav
- Global header
- Footer
- `<html>` / `<body>` attributes
- Global stylesheet injection (`app.css?url`)
- Providers (React Query, theme, auth)

When adding a new route, **never** paste a new nav or footer into the route file. If the chrome needs to change per-route (e.g., landing-only), do it with conditional logic in `__root.tsx`, not by duplicating.

## `createFileRoute`

```tsx
// src/routes/dashboard.tsx
import { createFileRoute } from '@tanstack/react-router'

export const Route = createFileRoute('/dashboard')({
  component: DashboardPage,
  loader: async () => ({ stats: await fetchStats() }),
})

function DashboardPage() {
  const { stats } = Route.useLoaderData()
  return <div>{stats.count}</div>
}
```

## Loaders vs server functions

- **Loader**: data needed to render the route. Runs on the server for SSR, on the client for client-side nav.
- **Server function**: explicit RPC, called from handlers/mutations. Always server-side.

Prefer loaders for read-on-render; prefer `createServerFn` for mutations or data that shouldn't block navigation.

## Route context

Pass shared context (auth, query client) via `createRootRouteWithContext`:

```tsx
export const Route = createRootRouteWithContext<{
  queryClient: QueryClient
  user: User | null
}>()({ component: () => <Outlet /> })
```

Access downstream via `Route.useRouteContext()`.
