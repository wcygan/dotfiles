# TanStack Start — React Query, tRPC & Zod

## React Query Integration

### Install

```bash
npm install @tanstack/react-query @tanstack/react-router-with-query
```

### router.tsx

```typescript
import { createRouter as createTanStackRouter } from '@tanstack/react-router'
import { routerWithQueryClient } from '@tanstack/react-router-with-query'
import { QueryClient } from '@tanstack/react-query'
import { routeTree } from './routeTree.gen'

export function createRouter() {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { staleTime: 5 * 60 * 1000 } },
  })

  const router = createTanStackRouter({
    routeTree,
    context: { queryClient },
    defaultPreload: 'intent',
  })

  return routerWithQueryClient(router, queryClient)
}

declare module '@tanstack/react-router' {
  interface Register { router: ReturnType<typeof createRouter> }
}
```

### Root route context type

```typescript
// __root.tsx
import { createRootRouteWithContext } from '@tanstack/react-router'
import type { QueryClient } from '@tanstack/react-query'

export const Route = createRootRouteWithContext<{ queryClient: QueryClient }>()({
  component: RootComponent,
})
```

### Prefetch in loader → read in component

```typescript
export const Route = createFileRoute('/posts')({
  loader: async ({ context: { queryClient } }) => {
    await queryClient.ensureQueryData({
      queryKey: ['posts'],
      queryFn: () => getPostsFn(),
    })
  },
  component: PostsPage,
})

function PostsPage() {
  const { data: posts } = useQuery({
    queryKey: ['posts'],
    queryFn: () => getPostsFn(),
  })
  return <ul>{posts?.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

### Mutations with invalidation

```typescript
function CreatePost() {
  const queryClient = useQueryClient()
  const router = useRouter()

  const mutation = useMutation({
    mutationFn: (data: CreatePostInput) => createPostFn({ data }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] })
      router.invalidate()  // also refresh route loaders
    },
  })
}
```

---

## tRPC Integration (current API: `@trpc/tanstack-react-query`)

> **Note**: The old `@trpc/react-query` package is deprecated. Use `@trpc/tanstack-react-query` for new projects.

### Install

```bash
npm install @trpc/server @trpc/client @trpc/tanstack-react-query @tanstack/react-query
```

### 1. Define the tRPC router (server)

```typescript
// src/trpc/router.ts
import { initTRPC } from '@trpc/server'
import { z } from 'zod'

const t = initTRPC.create()
export const router = t.router
export const publicProcedure = t.procedure

export const appRouter = router({
  posts: router({
    list: publicProcedure.query(async () => {
      return await db.post.findMany()
    }),
    byId: publicProcedure
      .input(z.object({ id: z.string() }))
      .query(async ({ input }) => {
        return await db.post.findUnique({ where: { id: input.id } })
      }),
    create: publicProcedure
      .input(z.object({ title: z.string().min(1), content: z.string() }))
      .mutation(async ({ input }) => {
        return await db.post.create({ data: input })
      }),
  }),
})

export type AppRouter = typeof appRouter
```

### 2. Create the tRPC context (client)

```typescript
// src/trpc/client.ts
import { createTRPCContext } from '@trpc/tanstack-react-query'
import { createTRPCClient, httpBatchLink } from '@trpc/client'
import type { AppRouter } from './router'

// Generates TRPCProvider, useTRPC, useTRPCClient
export const { TRPCProvider, useTRPC, useTRPCClient } =
  createTRPCContext<AppRouter>()

export const trpcClient = createTRPCClient<AppRouter>({
  links: [httpBatchLink({ url: '/api/trpc' })],
})
```

### 3. Wrap providers in root component

```typescript
// __root.tsx
import { TRPCProvider, trpcClient } from '../trpc/client'
import { QueryClientProvider } from '@tanstack/react-query'

function RootComponent() {
  return (
    <QueryClientProvider client={queryClient}>
      <TRPCProvider trpcClient={trpcClient} queryClient={queryClient}>
        <Outlet />
      </TRPCProvider>
    </QueryClientProvider>
  )
}
```

### 4. Mount the tRPC HTTP handler (server route)

```typescript
// src/routes/api/trpc.$.tsx
import { createFileRoute } from '@tanstack/react-router'
import { fetchRequestHandler } from '@trpc/server/adapters/fetch'
import { appRouter } from '../../trpc/router'

export const Route = createFileRoute('/api/trpc/$')({})

export const server = {
  GET: handleTRPC,
  POST: handleTRPC,
}

async function handleTRPC({ request }: { request: Request }) {
  return fetchRequestHandler({
    endpoint: '/api/trpc',
    req: request,
    router: appRouter,
    createContext: () => ({}),
  })
}
```

### 5. Use in components

```typescript
import { useQuery, useMutation } from '@tanstack/react-query'
import { useTRPC } from '../trpc/client'

function PostsList() {
  const trpc = useTRPC()

  // queryOptions() / mutationOptions() integrate with standard React Query hooks
  const { data: posts } = useQuery(trpc.posts.list.queryOptions())
  const createPost = useMutation(trpc.posts.create.mutationOptions())

  return (
    <div>
      {posts?.map(p => <div key={p.id}>{p.title}</div>)}
      <button onClick={() => createPost.mutate({ title: 'New', content: '...' })}>
        Add Post
      </button>
    </div>
  )
}

function PostDetail({ id }: { id: string }) {
  const trpc = useTRPC()
  const { data } = useQuery(trpc.posts.byId.queryOptions({ id }))
  return <div>{data?.title}</div>
}
```

### 6. Prefetch tRPC in route loaders

```typescript
import { createTRPCOptionsProxy } from '@trpc/tanstack-react-query'
import { createTRPCClient, httpBatchLink } from '@trpc/client'
import type { AppRouter } from '../trpc/router'

// Create a server-side options proxy for prefetching
function getServerTRPC(queryClient: QueryClient) {
  const client = createTRPCClient<AppRouter>({
    links: [httpBatchLink({ url: 'http://localhost:3000/api/trpc' })],
  })
  return createTRPCOptionsProxy<AppRouter>({ client, queryClient })
}

export const Route = createFileRoute('/posts')({
  loader: async ({ context: { queryClient } }) => {
    const trpc = getServerTRPC(queryClient)
    await queryClient.prefetchQuery(trpc.posts.list.queryOptions())
  },
  component: PostsPage,
})
```

---

## Zod — Schema Validation

Zod is used throughout TanStack Start for server function validation, search params, and tRPC inputs.

### Install

```bash
npm install zod
```

### Core Primitives

```typescript
import { z } from 'zod'

z.string()
z.number()
z.boolean()
z.date()
z.undefined()
z.null()
z.any()
z.unknown()
z.literal('admin')
```

### Objects & Arrays

```typescript
const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(2).max(100),
  email: z.string().email(),
  age: z.number().int().min(0).max(150),
  role: z.enum(['user', 'admin', 'moderator']),
  createdAt: z.date(),
})

// Type inference — no duplicate types!
type User = z.infer<typeof UserSchema>

const TagsSchema = z.array(z.string()).min(1).max(10)
```

### Optional, Nullable, Default

```typescript
z.string().optional()              // string | undefined
z.string().nullable()              // string | null
z.string().nullish()               // string | null | undefined
z.string().default('anonymous')    // undefined → 'anonymous'
z.string().catch('fallback')       // invalid → 'fallback'
```

### Union & Intersection

```typescript
const IdSchema = z.union([z.string(), z.number()])

const AdminSchema = z.intersection(
  UserSchema,
  z.object({ permissions: z.array(z.string()) })
)

// Discriminated union (faster, better errors)
const ResultSchema = z.discriminatedUnion('status', [
  z.object({ status: z.literal('ok'), data: z.string() }),
  z.object({ status: z.literal('error'), message: z.string() }),
])
```

### Transform & Refine

```typescript
// Transform: modify value after validation
const TrimmedString = z.string().transform(s => s.trim())
const StringToNumber = z.string().transform(Number)

// Refine: custom validation with message
const StrongPassword = z.string()
  .min(8)
  .refine(s => /[A-Z]/.test(s), { message: 'Needs uppercase' })
  .refine(s => /[0-9]/.test(s), { message: 'Needs number' })

// SuperRefine: multiple issues at once
const ConfirmPassword = z.object({
  password: z.string(),
  confirm: z.string(),
}).superRefine(({ password, confirm }, ctx) => {
  if (password !== confirm) {
    ctx.addIssue({ code: 'custom', path: ['confirm'], message: 'Passwords must match' })
  }
})
```

### Parsing

```typescript
// throws ZodError on failure
const user = UserSchema.parse(rawInput)

// returns { success, data } or { success, error }
const result = UserSchema.safeParse(rawInput)
if (result.success) {
  result.data  // typed
} else {
  result.error.issues  // array of ZodIssue
}

// async parsing (for async refinements)
const user = await UserSchema.parseAsync(rawInput)
```

### Zod + tRPC

```typescript
// tRPC uses Zod for input validation — fully type-safe end-to-end
const createPost = publicProcedure
  .input(z.object({
    title: z.string().min(1).max(200),
    content: z.string(),
    tags: z.array(z.string()).default([]),
  }))
  .mutation(async ({ input }) => {
    // input is { title: string, content: string, tags: string[] }
    return db.post.create({ data: input })
  })
```

### Zod + TanStack Router Search Params

```typescript
import { zodSearchValidator } from '@tanstack/router-zod-adapter'

const searchSchema = z.object({
  q: z.string().default(''),
  page: z.number().int().min(1).default(1),
  sort: z.enum(['latest', 'popular', 'oldest']).default('latest'),
  tags: z.array(z.string()).default([]),
})

export const Route = createFileRoute('/search')({
  validateSearch: zodSearchValidator(searchSchema),
  loaderDeps: ({ search }) => search,
  loader: async ({ deps, context: { queryClient } }) => {
    await queryClient.ensureQueryData({
      queryKey: ['search', deps],
      queryFn: () => searchFn({ data: deps }),
    })
  },
})
```

### Zod + Server Function Validation

```typescript
import { zodValidator } from '@tanstack/zod-adapter'

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
})

export const createPostFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(CreatePostSchema))
  .handler(async ({ data }) => {
    // data: { title: string, content: string }
    return db.post.create({ data })
  })
```
