# TanStack Start — Authentication

## useSession (Cookie-Based Sessions)

```typescript
import { useSession } from '@tanstack/react-start/server'

// Type-safe session
type SessionUser = { id: string; email: string; role: 'user' | 'admin' }

export async function getSession() {
  return useSession<SessionUser>({
    password: process.env.SESSION_SECRET!,  // Min 32 chars for encryption
    cookieName: 'session',
    cookieOptions: {
      secure: process.env.NODE_ENV === 'production',
      httpOnly: true,
      sameSite: 'lax',
      maxAge: 60 * 60 * 24 * 30,  // 30 days
    },
  })
}
```

## Auth Server Functions

```typescript
import { redirect } from '@tanstack/react-start'
import { hashPassword, verifyPassword } from './crypto.server'

// Login
export const loginFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({ email: z.string().email(), password: z.string() })))
  .handler(async ({ data }) => {
    const user = await db.user.findUnique({ where: { email: data.email } })
    if (!user || !await verifyPassword(data.password, user.passwordHash)) {
      throw new Error('Invalid credentials')
    }

    const session = await getSession()
    await session.update({ id: user.id, email: user.email, role: user.role })

    throw redirect({ to: '/dashboard' })
  })

// Logout
export const logoutFn = createServerFn({ method: 'POST' })
  .handler(async () => {
    const session = await getSession()
    await session.clear()
    throw redirect({ to: '/login' })
  })

// Get current user
export const getCurrentUserFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const session = await getSession()
    if (!session.data?.id) return null
    return await db.user.findUnique({ where: { id: session.data.id } })
  })
```

## Route Protection (Pathless Layout)

```typescript
// src/routes/_authed.tsx
import { createFileRoute, redirect, Outlet } from '@tanstack/react-router'

export const Route = createFileRoute('/_authed')({
  beforeLoad: async ({ context }) => {
    const user = await getCurrentUserFn()
    if (!user) {
      throw redirect({
        to: '/login',
        search: { returnTo: window?.location.pathname },
      })
    }
    return { user }
  },
  component: Outlet,
})

// src/routes/_authed.dashboard.tsx — protected route
export const Route = createFileRoute('/_authed/dashboard')({
  component: Dashboard,
})
```

## RBAC (Role-Based Access Control)

```typescript
const roleHierarchy = { user: 1, moderator: 2, admin: 3 } as const

function hasRole(userRole: keyof typeof roleHierarchy, required: keyof typeof roleHierarchy) {
  return roleHierarchy[userRole] >= roleHierarchy[required]
}

// Middleware for RBAC
const requireRole = (role: keyof typeof roleHierarchy) =>
  createMiddleware({ type: 'function' })
    .server(async ({ next, context }) => {
      if (!context.user || !hasRole(context.user.role, role)) {
        throw new Error('Insufficient permissions')
      }
      return next()
    })

// Admin-only server function
export const deleteUserFn = createServerFn({ method: 'POST' })
  .middleware([authMiddleware, requireRole('admin')])
  .validator(zodValidator(z.object({ userId: z.string() })))
  .handler(async ({ data }) => {
    await db.user.delete({ where: { id: data.userId } })
  })
```

## Email/Password Registration

```typescript
import bcrypt from 'bcryptjs'

export const registerFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({
    email: z.string().email(),
    password: z.string().min(8),
    name: z.string().min(2),
  })))
  .handler(async ({ data }) => {
    const existing = await db.user.findUnique({ where: { email: data.email } })
    if (existing) throw new Error('Email already registered')

    const passwordHash = await bcrypt.hash(data.password, 12)
    const user = await db.user.create({
      data: { email: data.email, name: data.name, passwordHash },
    })

    const session = await getSession()
    await session.update({ id: user.id, email: user.email, role: 'user' })

    throw redirect({ to: '/dashboard' })
  })
```

## OAuth / Social Auth

```typescript
// Using arctic or better-auth library

import { GitHub } from 'arctic'

const github = new GitHub(
  process.env.GITHUB_CLIENT_ID!,
  process.env.GITHUB_CLIENT_SECRET!,
  { redirectURI: process.env.APP_URL + '/api/auth/callback/github' }
)

export const githubLoginFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const state = generateState()
    const url = await github.createAuthorizationURL(state, { scopes: ['user:email'] })

    setCookie('oauth_state', state, { httpOnly: true, maxAge: 600 })
    throw redirect({ href: url.toString() })
  })

export const githubCallbackFn = createServerFn({ method: 'GET' })
  .handler(async () => {
    const request = getRequest()
    const url = new URL(request.url)
    const code = url.searchParams.get('code')!
    const state = url.searchParams.get('state')!
    const savedState = getCookie('oauth_state')

    if (state !== savedState) throw new Error('State mismatch')

    const tokens = await github.validateAuthorizationCode(code)
    const githubUser = await fetch('https://api.github.com/user', {
      headers: { Authorization: `Bearer ${tokens.accessToken()}` },
    }).then(r => r.json())

    // Upsert user
    const user = await db.user.upsert({
      where: { githubId: String(githubUser.id) },
      update: { name: githubUser.name },
      create: { githubId: String(githubUser.id), email: githubUser.email, name: githubUser.name },
    })

    const session = await getSession()
    await session.update({ id: user.id, email: user.email, role: user.role })
    throw redirect({ to: '/dashboard' })
  })
```

## Password Reset Flow

```typescript
export const requestPasswordResetFn = createServerFn({ method: 'POST' })
  .validator(zodValidator(z.object({ email: z.string().email() })))
  .handler(async ({ data }) => {
    const user = await db.user.findUnique({ where: { email: data.email } })
    if (!user) return  // Don't reveal if email exists

    const token = crypto.randomBytes(32).toString('hex')
    const expires = new Date(Date.now() + 60 * 60 * 1000)  // 1 hour

    await db.passwordResetToken.create({
      data: { userId: user.id, token, expires },
    })

    await sendEmail({
      to: user.email,
      subject: 'Reset your password',
      html: `<a href="${process.env.APP_URL}/reset-password?token=${token}">Reset password</a>`,
    })
  })
```

## Rate Limiting

```typescript
import { LRUCache } from 'lru-cache'

const loginAttempts = new LRUCache<string, number>({
  max: 10000,
  ttl: 15 * 60 * 1000,  // 15 minutes
})

const rateLimitMiddleware = createMiddleware({ type: 'function' })
  .server(async ({ next, request }) => {
    const ip = getRequestHeader('x-forwarded-for') ?? 'unknown'
    const attempts = loginAttempts.get(ip) ?? 0

    if (attempts >= 5) {
      throw new Error('Too many login attempts. Please try again in 15 minutes.')
    }

    try {
      const result = await next()
      loginAttempts.delete(ip)  // Clear on success
      return result
    } catch (e) {
      loginAttempts.set(ip, attempts + 1)
      throw e
    }
  })
```

## Security Best Practices

- Use `httpOnly: true` cookies to prevent XSS
- Use `sameSite: 'lax'` or `'strict'` for CSRF protection
- Use `secure: true` in production (HTTPS only)
- Use bcrypt with cost factor ≥ 12 for passwords
- Use crypto-random tokens for password resets and OAuth state
- Rotate SESSION_SECRET periodically
- Store SESSION_SECRET in environment variables, never in code
