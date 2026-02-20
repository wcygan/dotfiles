# TanStack Start — Data Loading

## Route Loaders

Loaders run **isomorphically** — on the server during SSR, on the client during navigation.

```typescript
export const Route = createFileRoute('/posts')({
  loader: async ({ params, context, abortController }) => {
    // This runs on BOTH server and client
    const posts = await fetchPosts()
    return { posts }
  },
  component: PostsPage,
})

function PostsPage() {
  const { posts } = Route.useLoaderData()
  return <ul>{posts.map(p => <li key={p.id}>{p.title}</li>)}</ul>
}
```

## beforeLoad vs loader

| | `beforeLoad` | `loader` |
|--|--|--|
| Runs | Before loader | After beforeLoad |
| Can throw redirect | Yes | Yes |
| Return merges into | Route context | Loader data |
| Parallel with parent | No (sequential) | Yes (parallel with siblings) |

```typescript
export const Route = createFileRoute('/dashboard')({
  beforeLoad: async ({ context }) => {
    // Auth check, redirect if needed
    if (!context.user) throw redirect({ to: '/login' })
    return { permissions: await fetchPermissions(context.user.id) }
  },
  loader: async ({ context }) => {
    // context.permissions available from beforeLoad
    const data = await fetchDashboardData()
    return { data }
  },
})
```

## Accessing Loader Data

```typescript
// Inside route component (type-safe)
const { posts } = Route.useLoaderData()

// From parent in child route
import { getRouteApi } from '@tanstack/react-router'
const postsRoute = getRouteApi('/posts')
const { posts } = postsRoute.useLoaderData()

// With React Query (preferred for mutations)
export const Route = createFileRoute('/posts')({
  loader: async ({ context: { queryClient } }) => {
    await queryClient.ensureQueryData({
      queryKey: ['posts'],
      queryFn: fetchPosts,
    })
  },
  component: PostsPage,
})

function PostsPage() {
  const { data: posts } = useQuery({ queryKey: ['posts'], queryFn: fetchPosts })
}
```

## Preloading

Configure how routes preload data on hover/focus.

```typescript
// In createRouter
const router = createRouter({
  routeTree,
  defaultPreload: 'intent',        // Preload on hover/focus
  defaultPreloadStaleTime: 0,      // Always refetch on preload
  defaultPreloadDelay: 50,         // ms before preloading (debounce)
})

// Per-link override
<Link to="/posts" preload="intent">Posts</Link>
<Link to="/posts" preload={false}>No preload</Link>
```

## Staleness & Caching

```typescript
export const Route = createFileRoute('/posts')({
  // How long loader data is considered fresh (ms)
  staleTime: 5 * 60 * 1000,    // 5 minutes

  // How long to keep in cache after route unmounts
  gcTime: 10 * 60 * 1000,      // 10 minutes

  // Custom should-reload logic
  shouldReload: ({ cause }) => cause === 'enter',

  loader: async () => fetchPosts(),
})
```

## Invalidation After Mutations

```typescript
import { useRouter } from '@tanstack/react-router'

function CreatePost() {
  const router = useRouter()

  const handleSubmit = async (data: FormData) => {
    await createPostFn({ data: { title: data.get('title') } })
    // Invalidate all loaders to trigger refetch
    await router.invalidate()
  }
}
```

## Loader Dependencies (Search Params)

```typescript
export const Route = createFileRoute('/search')({
  validateSearch: (search) => ({
    q: String(search.q ?? ''),
    page: Number(search.page ?? 1),
  }),
  // Loader re-runs when search params change
  loaderDeps: ({ search }) => ({ q: search.q, page: search.page }),
  loader: async ({ deps }) => {
    return await searchPosts(deps.q, deps.page)
  },
})
```

## Error Handling in Loaders

```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId)

    if (!post) {
      throw notFound()
    }

    if (!currentUser) {
      throw redirect({ to: '/login', search: { returnTo: location.pathname } })
    }

    return { post }
  },
  notFoundComponent: () => <div>Post not found</div>,
  errorComponent: ({ error }) => <div>Error: {error.message}</div>,
})
```

## Deferred/Streaming Data

```typescript
export const Route = createFileRoute('/posts/$postId')({
  loader: async ({ params }) => {
    const post = await fetchPost(params.postId)

    return {
      post,
      // Deferred — won't block render
      comments: fetchComments(params.postId),
    }
  },
  component: PostPage,
})

function PostPage() {
  const { post, comments } = Route.useLoaderData()

  return (
    <div>
      <h1>{post.title}</h1>
      <Suspense fallback={<CommentsLoader />}>
        <Await promise={comments}>
          {(data) => <CommentsList comments={data} />}
        </Await>
      </Suspense>
    </div>
  )
}
```
