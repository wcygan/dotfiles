---
name: tanstack-start
description: TanStack Start full-stack React framework expert. Auto-loads when working on TanStack Start projects, TanStack Router, Vite+Nitro full-stack apps, createServerFn, createFileRoute, file-based routing, SSR/SPA mode, server functions, middleware, React Query integration, tRPC, Cloudflare/Netlify/Vercel deployment, isomorphic code patterns, route loaders, useSession authentication, and Tailwind v4 setup.
allowed-tools: Read, Grep, Glob, Bash, WebFetch, Write, Edit
---

# TanStack Start

TanStack Start is a full-stack React framework built on TanStack Router + Vite + Nitro. It provides file-based routing, server functions (RPC), SSR/SPA/static modes, and deploys anywhere (Cloudflare, Netlify, Vercel, Node, Bun).

## Core API Quick Reference

| API | Purpose |
|-----|---------|
| `createFileRoute('/path')` | Define a route with loader, component, head |
| `createRootRoute()` / `createRootRouteWithContext()` | Root layout route |
| `createRouter({ routeTree, context })` | App router instance |
| `createServerFn({ method: 'GET'\|'POST' })` | Server-only RPC function |
| `createMiddleware()` | Request or function middleware |
| `useSession()` | Cookie-based server session |
| `Route.useLoaderData()` | Access route loader return value |
| `useNavigate()` | Programmatic navigation |
| `<Link to="/path">` | Type-safe navigation link |
| `redirect({ to, throw: true })` | Redirect (throw inside loader/beforeLoad) |
| `notFound({ throw: true })` | Trigger 404 boundary |

## Minimal Project Structure

```
src/
  routes/
    __root.tsx          # Root layout (shellComponent when SSR disabled)
    index.tsx           # /
    about.tsx           # /about
    posts/
      $postId.tsx       # /posts/:postId
  routeTree.gen.ts      # Auto-generated (never edit)
  router.tsx            # createRouter() entry
  client.tsx            # Client entry (StartClient)
  ssr.tsx               # SSR handler
app.config.ts           # tanstackStart() vite plugin config
```

## File-Based Routing Key Conventions

- `.` in filename → `/` path separator (e.g., `posts.index.tsx` → `/posts/`)
- `$param` → dynamic segment
- `_layout` → pathless layout (no URL segment)
- `(group)` → route group (no URL impact)
- `index.tsx` → index route for a directory
- `*.lazy.tsx` → code-split lazy route

## Core Dependencies

```json
{
  "@tanstack/react-start": "latest",
  "@tanstack/react-router": "latest",
  "react": "^19.0.0",
  "vite": "^6.0.0",
  "vinxi": "latest"
}
```

## References

- [Documentation URL Map](references/documentation-map.md) — fetch live docs via WebFetch
- [Project Setup](references/project-setup.md) — scaffold, vite.config, tsconfig, router.tsx
- [Routing & Navigation](references/routing-and-navigation.md) — file conventions, Link, hooks
- [Data Loading](references/data-loading.md) — loaders, preloading, staleTime
- [Server Functions](references/server-functions.md) — createServerFn, validation, errors
- [Middleware](references/middleware.md) — request/function middleware, context, global
- [Server Routes](references/server-routes.md) — API routes, HTTP handlers, dynamic params
- [Execution Model](references/execution-model.md) — isomorphic code, server/client boundaries
- [SSR Modes](references/ssr-modes.md) — selective SSR, SPA, static prerendering, ISR
- [Authentication](references/authentication.md) — sessions, route protection, OAuth
- [Environment Variables](references/environment-variables.md) — VITE_ prefix, .env, type safety
- [Import Protection](references/import-protection.md) — server/client enforcement, markers
- [Tailwind & Styling](references/tailwind-and-styling.md) — v4 setup, CSS imports
- [SEO & Head](references/seo-and-head.md) — meta, OG, structured data, sitemaps
- [Hosting & Deployment](references/hosting-and-deployment.md) — Cloudflare, Netlify, Vercel
- [Error Handling](references/error-handling.md) — boundaries, notFound, hydration errors
- [React Query & tRPC](references/react-query-and-trpc.md) — integration patterns
- [Database Patterns](references/database-patterns.md) — DB access, recommended providers
