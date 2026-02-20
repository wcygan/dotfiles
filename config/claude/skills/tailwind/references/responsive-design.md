# Tailwind CSS — Responsive Design

## Default Breakpoints (mobile-first)

| Prefix | Min-width | CSS |
|--------|-----------|-----|
| `sm:` | 40rem (640px) | `@media (width >= 40rem)` |
| `md:` | 48rem (768px) | `@media (width >= 48rem)` |
| `lg:` | 64rem (1024px) | `@media (width >= 64rem)` |
| `xl:` | 80rem (1280px) | `@media (width >= 80rem)` |
| `2xl:` | 96rem (1536px) | `@media (width >= 96rem)` |

## Mobile-First Approach

Unprefixed utilities apply to **all screen sizes**. Prefixed utilities apply **at that breakpoint and above**.

```html
<!-- ✅ Correct: base (mobile) → enhanced (larger screens) -->
<div class="text-center sm:text-left">

<!-- ❌ Wrong: only applies at sm+, nothing on mobile -->
<div class="sm:text-center">
```

## Common Patterns

```html
<!-- Responsive columns -->
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">

<!-- Responsive flex direction -->
<div class="flex flex-col md:flex-row items-start md:items-center gap-4">

<!-- Responsive sizing -->
<img class="w-full sm:w-64 lg:w-96" />

<!-- Show/hide at breakpoints -->
<nav class="hidden lg:flex">           <!-- hidden on mobile, flex on lg+ -->
<button class="lg:hidden">Menu</button> <!-- only on mobile/tablet -->

<!-- Responsive text -->
<h1 class="text-2xl sm:text-3xl lg:text-4xl xl:text-5xl font-bold">

<!-- Responsive padding -->
<section class="px-4 sm:px-6 lg:px-8 py-12 lg:py-24">
```

## Breakpoint Ranges (max-* variants)

Target a specific range — only apply between two breakpoints:

```html
<!-- Only on medium screens (md to lg) -->
<div class="md:max-lg:flex">

<!-- Only on small screens (below md) -->
<div class="max-md:hidden">
```

Available max variants:
- `max-sm` — `width < 40rem`
- `max-md` — `width < 48rem`
- `max-lg` — `width < 64rem`
- `max-xl` — `width < 80rem`
- `max-2xl` — `width < 96rem`

## Custom Breakpoints

```css
@import "tailwindcss";

@theme {
  --breakpoint-xs: 30rem;     /* adds xs: variant */
  --breakpoint-3xl: 120rem;   /* adds 3xl: variant */
  --breakpoint-2xl: initial;  /* removes 2xl: */
}
```

```html
<div class="xs:flex 3xl:grid-cols-6">
```

## Arbitrary Breakpoints

One-off breakpoints without adding to theme:

```html
<div class="min-[320px]:text-center max-[600px]:bg-sky-300">
```

## Container Queries

Style elements based on their **parent container's size**, not the viewport.

```html
<div class="@container">
  <div class="flex flex-col @md:flex-row @lg:gap-8">
    <img class="w-full @md:w-48" />
    <div class="@md:text-lg">Content</div>
  </div>
</div>
```

### Container Query Breakpoints

| Prefix | Container min-width |
|--------|-------------------|
| `@3xs:` | 16rem (256px) |
| `@2xs:` | 18rem (288px) |
| `@xs:` | 20rem (320px) |
| `@sm:` | 24rem (384px) |
| `@md:` | 28rem (448px) |
| `@lg:` | 32rem (512px) |
| `@xl:` | 36rem (576px) |
| `@2xl:` | 42rem (672px) |
| `@3xl:` | 48rem (768px) |
| `@4xl:` | 56rem (896px) |
| `@5xl:` | 64rem (1024px) |
| `@6xl:` | 72rem (1152px) |
| `@7xl:` | 80rem (1280px) |

### Max-width Container Queries

```html
<div class="@container">
  <div class="@max-md:flex-col @md:flex-row">
```

### Named Containers (nested)

```html
<div class="@container/sidebar">
  <div class="@container/main">
    <!-- Target a specific ancestor -->
    <div class="@sm/sidebar:hidden @lg/main:grid-cols-2">
```

### Arbitrary Container Queries

```html
<div class="@container">
  <div class="@min-[475px]:flex @max-[960px]:flex-col">
```

### Container Query Units

```html
<div class="@container">
  <!-- 50% of container width -->
  <div class="w-[50cqw]">
  <!-- 25% of container height -->
  <div class="h-[25cqh]">
```

## Print Variant

```html
<button class="print:hidden">Not printed</button>
<div class="hidden print:block">Print only</div>
<article class="print:text-black print:text-sm">
```

## Motion / Color Scheme Variants

```html
<!-- Respect user's motion preference -->
<div class="motion-safe:transition-all motion-reduce:transition-none">

<!-- System color scheme (not user toggle) -->
<div class="dark:bg-gray-900">      <!-- prefers-color-scheme: dark -->
```
