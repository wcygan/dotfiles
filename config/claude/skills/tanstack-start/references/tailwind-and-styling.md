# TanStack Start — Tailwind & Styling

## Tailwind v4 Setup (Recommended)

### Install packages

```bash
npm install tailwindcss @tailwindcss/vite
```

### app.config.ts

```typescript
import { defineConfig } from '@tanstack/react-start/config'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  vite: {
    plugins: [
      tailwindcss(),
    ],
  },
})
```

### src/styles/app.css

```css
@import 'tailwindcss' source('../');
```

The `source('../')` tells Tailwind where to scan for class usage. Adjust the path as needed relative to your CSS file.

### Import in root route

```typescript
// src/routes/__root.tsx
/// <reference types="vite/client" />
import appCss from '../styles/app.css?url'
import { createRootRoute, HeadContent, Outlet, Scripts } from '@tanstack/react-router'

export const Route = createRootRoute({
  head: () => ({
    links: [{ rel: 'stylesheet', href: appCss }],
  }),
  component: RootComponent,
})
```

> **Critical**: The `/// <reference types="vite/client" />` triple-slash directive is required to resolve the `?url` import type.

### Using Tailwind Classes

```tsx
function Button({ children }: { children: React.ReactNode }) {
  return (
    <button className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors">
      {children}
    </button>
  )
}
```

## Tailwind v4 CSS Variables

Tailwind v4 uses CSS variables for theming:

```css
@import 'tailwindcss' source('../');

@theme {
  --color-brand-500: #6366f1;
  --color-brand-600: #4f46e5;
  --font-family-sans: 'Inter', sans-serif;
  --radius-card: 0.75rem;
}
```

```tsx
<div className="bg-brand-500 font-sans rounded-card">...</div>
```

## Tailwind v3 Fallback

If you need Tailwind v3:

### Install packages

```bash
npm install tailwindcss@3 autoprefixer postcss
```

### tailwind.config.ts

```typescript
import type { Config } from 'tailwindcss'

export default {
  content: ['./src/**/*.{ts,tsx}'],
  theme: {
    extend: {},
  },
  plugins: [],
} satisfies Config
```

### postcss.config.js

```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

### src/styles/app.css (v3)

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### app.config.ts (v3 — no @tailwindcss/vite)

```typescript
import { defineConfig } from '@tanstack/react-start/config'

export default defineConfig({
  // Vite handles PostCSS automatically via postcss.config.js
})
```

## CSS Modules

```typescript
// Button.module.css
.button {
  padding: 0.5rem 1rem;
  background: var(--color-brand-500);
}

// Button.tsx
import styles from './Button.module.css'

function Button() {
  return <button className={styles.button}>Click me</button>
}
```

## Global Styles + CSS Variables

```css
/* src/styles/app.css */
@import 'tailwindcss' source('../');

:root {
  --sidebar-width: 240px;
  --header-height: 64px;
}

body {
  font-family: system-ui, sans-serif;
  -webkit-font-smoothing: antialiased;
}
```

## clsx / cn Pattern

```bash
npm install clsx tailwind-merge
```

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
<div className={cn('base-class', isActive && 'active-class', className)}>
```
