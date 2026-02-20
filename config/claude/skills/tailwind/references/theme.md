# Tailwind CSS — Theme & Design Tokens

## @theme Directive

`@theme` replaces `tailwind.config.js` in v4. CSS variables defined here generate utility classes.

```css
@import "tailwindcss";

@theme {
  --color-brand-primary: oklch(0.65 0.2 240);
  --font-display: "Satoshi", "Inter", sans-serif;
  --radius-card: 0.75rem;
  --breakpoint-xs: 30rem;
  --animate-fade-in: fade-in 0.3s ease-out;
}
```

This generates: `bg-brand-primary`, `text-brand-primary`, `font-display`, `rounded-card`, `xs:*`, `animate-fade-in`

## Why @theme Instead of :root?

| | `@theme { }` | `:root { }` |
|--|--|--|
| Generates utility classes | ✅ | ❌ |
| Available in CSS as vars | ✅ | ✅ |
| Must be top-level | ✅ | ✅ |
| For design tokens | ✅ | ❌ |
| For app-level vars | ❌ | ✅ |

## Theme Variable Namespaces

| CSS variable prefix | Utilities generated |
|---------------------|---------------------|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `ring-*`, `fill-*`, `stroke-*`, `shadow-*`, etc. |
| `--font-*` | `font-*` (font-family) |
| `--text-*` | `text-*` (font-size + line-height) |
| `--font-weight-*` | `font-*` (font-weight) |
| `--tracking-*` | `tracking-*` (letter-spacing) |
| `--leading-*` | `leading-*` (line-height) |
| `--breakpoint-*` | `sm:`, `md:`, `lg:`, etc. |
| `--spacing` | `p-*`, `m-*`, `w-*`, `h-*`, `gap-*`, etc. (multiplied by value) |
| `--spacing-*` | Named spacing values |
| `--radius-*` | `rounded-*` |
| `--shadow-*` | `shadow-*` |
| `--inset-shadow-*` | `inset-shadow-*` |
| `--drop-shadow-*` | `drop-shadow-*` |
| `--blur-*` | `blur-*` |
| `--perspective-*` | `perspective-*` |
| `--aspect-*` | `aspect-*` |
| `--ease-*` | `ease-*` (transition-timing-function) |
| `--animate-*` | `animate-*` (animation shorthand) |
| `--z-*` | `z-*` |
| `--opacity-*` | `opacity-*` |
| `--width-*` | Named width values |

## Customization Patterns

### Extend (add without removing defaults)

```css
@theme {
  --color-brand-500: oklch(0.65 0.2 240);
  --color-brand-600: oklch(0.55 0.22 240);
  --font-display: "Inter Variable", sans-serif;
  --radius-2xl: 1rem;
  --spacing-18: 4.5rem;
}
```

### Override specific defaults

```css
@theme {
  --breakpoint-sm: 30rem;       /* sm: now triggers at 30rem instead of 40rem */
  --font-sans: "Inter", sans-serif;  /* change default sans font */
}
```

### Replace entire namespace

```css
@theme {
  --color-*: initial;           /* removes ALL default colors */
  --color-white: #fff;
  --color-black: #000;
  --color-brand: oklch(0.65 0.2 240);
  --color-accent: oklch(0.75 0.15 45);
}
```

### Complete custom theme (start from scratch)

```css
@theme {
  --*: initial;                 /* removes ALL defaults */
  --spacing: 4px;
  --font-body: "Inter", sans-serif;
  --color-background: oklch(0.99 0 0);
  --color-foreground: oklch(0.1 0 0);
  --radius-base: 0.5rem;
}
```

## Animations

Define custom animations directly in @theme:

```css
@theme {
  --animate-fade-in-scale: fade-in-scale 0.3s ease-out;
  --animate-slide-up: slide-up 0.4s cubic-bezier(0.16, 1, 0.3, 1);

  @keyframes fade-in-scale {
    0% { opacity: 0; transform: scale(0.95); }
    100% { opacity: 1; transform: scale(1); }
  }

  @keyframes slide-up {
    0% { opacity: 0; transform: translateY(8px); }
    100% { opacity: 1; transform: translateY(0); }
  }
}
```

```html
<div class="animate-fade-in-scale">Animated content</div>
```

## @theme inline — Reference Other Variables

Use when your design tokens reference other CSS variables (e.g., from a design system package):

```css
:root {
  --brand-primary: oklch(0.65 0.2 240);
}

/* inline resolves the variable at compile time */
@theme inline {
  --color-primary: var(--brand-primary);
  --font-sans: var(--font-inter);  /* from next/font or similar */
}
```

## @theme static — Always Emit Variables

Force variables into output even if no utilities use them:

```css
@theme static {
  --color-surface: var(--color-gray-50);
  --color-on-surface: var(--color-gray-900);
}
```

## Using Theme Variables in CSS

All theme variables become CSS custom properties:

```css
@layer components {
  .card {
    background-color: var(--color-white);
    border-radius: var(--radius-lg);
    padding: --spacing(6);                /* convenience function */
    box-shadow: var(--shadow-md);
  }

  .typography {
    color: var(--color-gray-900);
    font-size: var(--text-base);

    h1 { font-size: var(--text-3xl); font-weight: var(--font-weight-bold); }
    h2 { font-size: var(--text-2xl); font-weight: var(--font-weight-semibold); }

    a {
      color: var(--color-blue-600);
      &:hover { color: var(--color-blue-800); }
    }
  }
}
```

## Using Theme Variables in Arbitrary Values

```html
<div class="rounded-[calc(var(--radius-xl)-1px)]">  <!-- Concentric border radius -->
<div class="p-[--spacing(4)]">                       <!-- Spacing function -->
<div class="bg-[--color-brand-500]">                 <!-- Direct variable reference -->
```

## Shared Theme (monorepo / design system)

```css
/* packages/design-system/theme.css */
@theme {
  --color-brand-500: oklch(0.65 0.2 240);
  --font-display: "Brand Font", sans-serif;
}
```

```css
/* apps/web/app.css */
@import "tailwindcss";
@import "@company/design-system/theme.css";
```

## Accessing in JavaScript

```javascript
const styles = getComputedStyle(document.documentElement)
const brandColor = styles.getPropertyValue('--color-brand-500')
const shadowXl = styles.getPropertyValue('--shadow-xl')
```
