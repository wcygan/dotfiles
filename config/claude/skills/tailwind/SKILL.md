---
name: tailwind
description: Tailwind CSS v4 expert. Auto-loads when working with Tailwind CSS, utility classes, responsive design, dark mode, shadcn/ui, CSS variables, @theme directive, custom variants, component styling, clsx, cn helper, color palette, spacing, typography utilities, hover/focus/group/peer states, container queries, and @apply patterns.
allowed-tools: Read, Grep, Glob, WebFetch
---

# Tailwind CSS v4

Tailwind CSS is a utility-first CSS framework. v4 is a ground-up rewrite: configuration is CSS-first (`@theme` replaces `tailwind.config.js`), all colors use OKLCH, and the Vite plugin replaces PostCSS.

## Install (v4)

```bash
npm install tailwindcss @tailwindcss/vite
```

```css
/* app.css */
@import "tailwindcss";
```

```typescript
// vite.config.ts
import tailwindcss from '@tailwindcss/vite'
export default { plugins: [tailwindcss()] }
```

## Core Concept: Utility-First

Style elements by combining small, single-purpose classes directly in markup. No custom class names, no context switching.

```html
<div class="mx-auto flex max-w-sm items-center gap-4 rounded-xl bg-white p-6 shadow-lg">
  <img class="size-12 shrink-0 rounded-full" src="..." />
  <div>
    <p class="text-xl font-semibold text-gray-900">Title</p>
    <p class="text-sm text-gray-500">Subtitle</p>
  </div>
</div>
```

## Variant Syntax

Variants prefix any utility: `{variant}:{utility}`

```html
hover:bg-blue-600        focus:ring-2          active:scale-95
dark:bg-gray-900         sm:flex-row           lg:grid-cols-3
disabled:opacity-50      group-hover:text-white peer-invalid:visible
aria-checked:bg-sky-700  data-active:border-2  md:max-lg:hidden
```

Variants stack: `dark:md:hover:bg-fuchsia-600`

## @theme — Design Tokens

Replace `tailwind.config.js` with CSS variables:

```css
@import "tailwindcss";

@theme {
  --color-brand-500: oklch(0.65 0.2 240);
  --font-display: "Inter", sans-serif;
  --radius-card: 0.75rem;
  --breakpoint-xs: 30rem;
  --animate-fade-in: fade-in 0.3s ease-out;
}
```

Generates: `bg-brand-500`, `font-display`, `rounded-card`, `xs:*`, `animate-fade-in`

## Key Directives

| Directive | Purpose |
|-----------|---------|
| `@theme { }` | Define design tokens → generates utility classes |
| `@layer base/components/utilities { }` | Add custom CSS to cascade layers |
| `@utility name { }` | Add custom utility (works with all variants) |
| `@custom-variant name (...) ;` | Add reusable custom variant |
| `@apply util1 util2;` | Inline utilities into custom CSS |
| `@source "../path"` | Explicitly add source files for class detection |
| `@reference "app.css";` | Import theme vars without duplicating CSS |

## Arbitrary Values

```html
bg-[#1da1f2]          text-[22px]         grid-cols-[1fr_500px_2fr]
top-[117px]           w-[calc(100%-2rem)]  fill-(--brand-color)
```

## Responsive Breakpoints (mobile-first)

| Prefix | Min-width |
|--------|-----------|
| `sm:` | 40rem (640px) |
| `md:` | 48rem (768px) |
| `lg:` | 64rem (1024px) |
| `xl:` | 80rem (1280px) |
| `2xl:` | 96rem (1536px) |

```html
<!-- Stack on mobile, row on md+ -->
<div class="flex flex-col md:flex-row">
```

## Common Patterns

```typescript
// cn() helper — combine + deduplicate classes
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'
export function cn(...inputs: ClassValue[]) { return twMerge(clsx(inputs)) }
```

```html
<!-- Dark mode -->
<div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">

<!-- Group: style children based on parent state -->
<a class="group"><span class="text-gray-500 group-hover:text-white">Link</span></a>

<!-- Peer: style siblings based on sibling state -->
<input class="peer" /><p class="hidden peer-invalid:block text-red-500">Invalid</p>
```

## References

- [Utility Classes](references/utility-classes.md) — core concepts, arbitrary values, important modifier
- [States & Variants](references/states-and-variants.md) — hover, focus, group, peer, ARIA, data, dark
- [Responsive Design](references/responsive-design.md) — breakpoints, mobile-first, container queries
- [Theme & Design Tokens](references/theme.md) — @theme, namespaces, CSS variables, customization
- [Colors](references/colors.md) — palette, OKLCH, opacity modifiers, dark mode
- [Custom Styles](references/custom-styles.md) — @layer, @apply, @utility, @custom-variant
- [Directives & Functions](references/directives-and-functions.md) — complete directive/function reference
- [shadcn/ui](references/shadcn.md) — installation, Tailwind v4 setup, theming, components
