# Tailwind CSS — Utility Classes

## Philosophy

Style elements by composing many small, single-purpose utilities directly in markup. Each utility maps to a specific CSS property/value pair.

```html
<!-- Traditional CSS: invent class names, write CSS, switch files -->
<div class="chat-notification">...</div>

<!-- Utility-first: compose in-place, no class names to invent -->
<div class="mx-auto flex max-w-sm items-center gap-4 rounded-xl bg-white p-6 shadow-lg">
```

## Why Not Inline Styles?

| Feature | Utility Classes | Inline Styles |
|---------|----------------|---------------|
| Hover / focus states | ✅ `hover:bg-blue-700` | ❌ |
| Responsive design | ✅ `md:flex-row` | ❌ |
| Design constraints | ✅ pick from theme values | ❌ magic numbers |
| Dark mode | ✅ `dark:bg-gray-900` | ❌ |
| Consistent spacing | ✅ spacing scale | ❌ |

Use inline styles only for truly dynamic values (from DB/API) not known at build time.

## Arbitrary Values

Square brackets let you use any value without adding to your theme:

```html
<!-- Colors -->
<div class="bg-[#1da1f2] text-[oklch(0.7_0.2_240)]">

<!-- Sizes -->
<div class="w-[117px] h-[calc(100vh-4rem)] mt-[--spacing(4)]">

<!-- Grid -->
<div class="grid grid-cols-[24rem_2.5rem_minmax(0,1fr)]">

<!-- Strings (pseudo-elements) -->
<div class="before:content-['Open']">

<!-- CSS variables -->
<div class="fill-(--brand-color) text-(--color-primary)">

<!-- Complex values -->
<div class="max-h-[calc(100dvh-(--spacing(6)))]">
```

Use `_` for spaces inside arbitrary values — Tailwind converts them automatically:
```html
<div class="grid-cols-[1fr_500px_2fr]">    <!-- 1fr 500px 2fr -->
<div class="bg-[url('/my_photo.jpg')]">    <!-- preserves underscore in URL -->
```

## Arbitrary Properties

For CSS properties Tailwind doesn't have utilities for:

```html
<div class="[mask-type:luminance]">
<div class="[scrollbar-width:none]">
<div class="hover:[mask-type:alpha]">
<!-- Set CSS variables with variants -->
<div class="[--scroll-offset:56px] lg:[--scroll-offset:44px]">
```

## Important Modifier

Force a utility to win over conflicting styles with `!`:

```html
<div class="bg-teal-500 bg-red-500!">  <!-- red wins -->
```

## Prefix Option

Avoid conflicts with existing CSS by adding a prefix:

```css
@import "tailwindcss" prefix(tw);
```

```html
<div class="tw-flex tw-items-center tw-bg-white">
```

## Managing Duplication

**Use loops** for repeated elements — same utility string, rendered N times:
```jsx
{items.map(item => (
  <div key={item.id} className="rounded-lg p-4 shadow">
    {item.name}
  </div>
))}
```

**Extract components** for reusable UI — don't extract just to avoid repeating utilities:
```jsx
function Card({ title, body }) {
  return (
    <div className="rounded-xl bg-white p-6 shadow-lg">
      <h2 className="text-lg font-semibold">{title}</h2>
      <p className="mt-2 text-gray-600">{body}</p>
    </div>
  )
}
```

**Use `@layer components`** when you genuinely need a class name (third-party HTML, etc.):
```css
@layer components {
  .btn-primary {
    background-color: var(--color-blue-500);
    color: white;
    padding: --spacing(2) --spacing(4);
    border-radius: var(--radius-md);
    &:hover { background-color: var(--color-blue-600); }
  }
}
```

## Handling Style Conflicts

When two utilities target the same property, the one defined later in the stylesheet wins (not the one appearing later in the class list):

```html
<!-- grid wins (defined after flex in Tailwind's output) -->
<div class="flex grid">
```

Use the `!` modifier or restructure to avoid relying on order.

## Class Detection (Build Time)

Tailwind scans source files as plain text — it needs complete class names:

```jsx
// ❌ Won't be detected
<div className={`text-${color}-500`}>

// ✅ Always use complete class names
<div className={color === 'red' ? 'text-red-500' : 'text-blue-500'}>
```

Add external libraries to scanning:
```css
@source "../node_modules/@acmecorp/ui-lib";
```

Safelist specific classes (force generation):
```css
@source inline("underline");
@source inline("{hover:,focus:,}text-red-{500,600,700}");
```
