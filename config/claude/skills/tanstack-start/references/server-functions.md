# TanStack Start — Server Functions

Server functions (`createServerFn`) are the primary way to run server-only code. They create RPC-style endpoints that clients call via HTTP.

## Basic Usage

```typescript
import { createServerFn } from '@tanstack/react-start'

// GET server function (safe to call from loaders)
export const getUser = createServerFn({ method: 'GET' })
  .handler(async () => {
    const users = await db.user.findMany()
    return users
  })

// POST server function (mutations)
export const createUser = createServerFn({ method: 'POST' })
  .validator((data: { name: string; email: string }) => data)
  .handler(async ({ data }) => {
    const user = await db.user.create({ data })
    return user
  })
```

## Input Validation

### Inline validator (TypeScript type checking)

```typescript
export const updatePost = createServerFn({ method: 'POST' })
  .validator((data: unknown) => {
    if (typeof data !== 'object' || !data) throw new Error('Invalid data')
    const d = data as any
    if (!d.id || !d.title) throw new Error('Missing required fields')
    return d as { id: string; title: string }
  })
  .handler(async ({ data }) => {
    return await db.post.update({ where: { id: data.id }, data: { title: data.title } })
  })
```

### Zod validation

```typescript
import { zodValidator } from '@tanstack/zod-adapter'
import { z } from 'zod'

const CreatePostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  published: z.boolean().default(false),
})

export const createPost = createServerFn({ method: 'POST' })
  .validator(zodValidator(CreatePostSchema))
  .handler(async ({ data }) => {
    // data is fully typed: { title: string, content: string, published: boolean }
    return await db.post.create({ data })
  })
```

## Calling from Components and Loaders

```typescript
// In a route loader
export const Route = createFileRoute('/posts')({
  loader: async () => {
    return await getPosts()  // GET server fn — called directly
  },
})

// In a component (mutation)
function CreatePostForm() {
  const [isPending, startTransition] = useTransition()

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)

    startTransition(async () => {
      await createPost({
        data: {
          title: formData.get('title') as string,
          content: formData.get('content') as string,
        },
      })
    })
  }
}

// With useServerFn hook
import { useServerFn } from '@tanstack/react-start'

function DeleteButton({ postId }: { postId: string }) {
  const deletePost = useServerFn(deletePostFn)
  return <button onClick={() => deletePost({ data: { id: postId } })}>Delete</button>
}
```

## Error Handling

```typescript
export const getPost = createServerFn({ method: 'GET' })
  .validator((data: { id: string }) => data)
  .handler(async ({ data }) => {
    const post = await db.post.findUnique({ where: { id: data.id } })

    if (!post) {
      throw notFound()
    }

    if (!currentUser?.canRead(post)) {
      throw redirect({ to: '/login' })
    }

    // Throw regular errors for error boundaries
    if (post.deleted) {
      throw new Error('Post has been deleted')
    }

    return post
  })
```

## Server Context (Request/Response)

```typescript
import {
  getRequest,
  getRequestHeader,
  setResponseHeader,
  setResponseStatus,
  getCookie,
  setCookie,
} from '@tanstack/react-start/server'

export const authenticatedAction = createServerFn({ method: 'POST' })
  .handler(async () => {
    const request = getRequest()
    const authHeader = getRequestHeader('Authorization')
    const sessionCookie = getCookie('session')

    // Set response headers
    setResponseHeader('X-Custom-Header', 'value')
    setResponseStatus(201)

    return { success: true }
  })
```

## File Organization

```
src/
  functions/
    posts.functions.ts    # Server functions for posts domain
    users.functions.ts    # Server functions for users domain
  server/
    db.server.ts          # Database client (server-only)
    auth.server.ts        # Auth utilities (server-only)
  schemas/
    posts.schema.ts       # Shared Zod schemas (isomorphic)
```

### Naming convention

```typescript
// posts.functions.ts
export const getPostsFn = createServerFn({ method: 'GET' }).handler(...)
export const createPostFn = createServerFn({ method: 'POST' }).handler(...)
export const updatePostFn = createServerFn({ method: 'POST' }).handler(...)
export const deletePostFn = createServerFn({ method: 'POST' }).handler(...)
```

## FormData Handling

```typescript
export const uploadFile = createServerFn({ method: 'POST' })
  .handler(async ({ request }) => {
    const formData = await request.formData()
    const file = formData.get('file') as File
    const title = formData.get('title') as string

    // Process file...
    return { success: true }
  })

// In component
<form
  onSubmit={(e) => {
    e.preventDefault()
    const formData = new FormData(e.currentTarget)
    uploadFile({ data: formData })
  }}
>
  <input type="file" name="file" />
  <input type="text" name="title" />
  <button type="submit">Upload</button>
</form>
```

## Middleware on Server Functions

```typescript
import { createMiddleware } from '@tanstack/react-start'

const authMiddleware = createMiddleware({ type: 'function' })
  .server(async ({ next }) => {
    const session = await getSession()
    if (!session.user) throw redirect({ to: '/login' })
    return next({ context: { user: session.user } })
  })

export const protectedAction = createServerFn({ method: 'POST' })
  .middleware([authMiddleware])
  .handler(async ({ context, data }) => {
    // context.user is available and typed
    return await doSomethingAs(context.user)
  })
```
