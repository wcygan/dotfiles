# Tailwind CSS — Custom Styles

## @layer Directive

Tailwind uses three cascade layers. Add custom CSS to any layer:

```css
@import "tailwindcss";

/* Base: element defaults, CSS resets */
@layer base {
  h1 { font-size: var(--text-2xl); font-weight: var(--font-weight-bold); }
  h2 { font-size: var(--text-xl); font-weight: var(--font-weight-semibold); }
  a { color: var(--color-blue-600); text-decoration: underline; }
  *, *::before, *::after { box-sizing: border-box; }
}

/* Components: reusable component classes */
@layer components {
  .card {
    background-color: var(--color-white);
    border-radius: var(--radius-lg);
    padding: --spacing(6);
    box-shadow: var(--shadow-md);
    border: 1px solid var(--color-gray-200);
  }

  .btn {
    display: inline-flex;
    align-items: center;
    padding: --spacing(2) --spacing(4);
    border-radius: var(--radius-md);
    font-weight: var(--font-weight-semibold);
    font-size: var(--text-sm);
    transition: colors 150ms;
    cursor: pointer;
  }

  .btn-primary {
    background-color: var(--color-blue-600);
    color: var(--color-white);
    &:hover { background-color: var(--color-blue-700); }
  }
}

/* Utilities: single-purpose, works with all variants */
@utility content-auto { content-visibility: auto; }
```

**Layer priority:** `base` < `components` < `utilities`

Utilities always win over components — by design. `@utility` classes work with all variants (`hover:`, `md:`, etc.); `@layer components` classes don't get variant support automatically.

## @apply Directive

Inline utility classes into custom CSS. Useful for third-party component libraries or legacy HTML:

```css
/* Good use: styling externally-controlled HTML */
.prose h1 { @apply text-3xl font-bold mb-4; }
.prose p { @apply text-gray-700 leading-relaxed mb-4; }
.prose a { @apply text-blue-600 hover:text-blue-800 underline; }

/* Good use: third-party component overrides */
.select2-container { @apply w-full; }
.select2-selection { @apply rounded-md border border-gray-300 bg-white; }
```

**When NOT to use @apply:** Don't use it just to avoid "repeating" utilities in HTML. Components (React/Vue/Svelte) already solve that.

## @utility Directive

Define custom utilities that work with ALL variants (hover, dark, md, etc.):

```css
/* Simple utility */
@utility content-auto {
  content-visibility: auto;
}

/* With pseudo-elements */
@utility scrollbar-hidden {
  &::-webkit-scrollbar { display: none; }
  -ms-overflow-style: none;
  scrollbar-width: none;
}

/* Functional utility matching theme values */
@theme {
  --tab-size-2: 2;
  --tab-size-4: 4;
  --tab-size-8: 8;
}

@utility tab-* {
  tab-size: --value(--tab-size-*);  /* matches tab-2, tab-4, tab-8 */
}

/* Bare integer values */
@utility columns-* {
  columns: --value(integer);        /* matches columns-1, columns-76, etc. */
}

/* Arbitrary values */
@utility opacity-* {
  opacity: --value([percentage]);   /* matches opacity-[71.37%] */
}

/* Combined: theme + bare + arbitrary */
@utility text-* {
  font-size: --value(--text-*, [length], [percentage]);
}
```

Usage in HTML (these work with all variants):
```html
<div class="content-auto hover:scrollbar-hidden md:tab-4">
```

## @custom-variant Directive

Create reusable variants for complex selectors:

```css
/* Simple selector variant */
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));

/* Arbitrary class variant */
@custom-variant card-hover (&:where(.card:hover *));

/* Media query variant */
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover { @slot; }
  }
}

/* Print variant */
@custom-variant print {
  @media print { @slot; }
}

/* Multi-rule variant */
@custom-variant hocus {
  &:hover { @slot; }
  &:focus { @slot; }
}
```

```html
<html data-theme="midnight">
  <button class="bg-white theme-midnight:bg-black theme-midnight:text-white">
  <button class="hocus:underline hocus:text-blue-600">
  <p class="print:text-black print:text-sm">
```

## @variant Directive (in CSS)

Apply a Tailwind variant to styles inside CSS (not markup):

```css
.my-card {
  background: white;
  @variant dark {
    background: var(--color-gray-900);
    color: var(--color-gray-100);
  }
  @variant hover {
    box-shadow: var(--shadow-lg);
  }
  @variant md {
    padding: --spacing(8);
  }
}
```

## Nesting in Custom CSS

Tailwind v4 supports modern CSS nesting:

```css
@layer components {
  .dropdown {
    position: relative;

    &:hover .dropdown-menu,
    &:focus-within .dropdown-menu {
      display: block;
    }

    .dropdown-menu {
      position: absolute;
      display: none;
      background: var(--color-white);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-lg);
    }
  }
}
```

## @source — Class Detection

Tell Tailwind where to scan for classes:

```css
@import "tailwindcss";

/* Scan library in node_modules (normally excluded) */
@source "../node_modules/@acmecorp/ui-lib";

/* Set base scanning directory */
@import "tailwindcss" source("../src");

/* Disable auto-detection, be explicit */
@import "tailwindcss" source(none);
@source "../src";
@source "../components";
```

## @reference — Avoid CSS Duplication

Import theme variables without duplicating CSS output (for Vue SFCs, Svelte, CSS Modules):

```css
/* In a Vue <style> block or CSS module */
@reference "../../app.css";

h1 {
  @apply text-2xl font-bold text-red-500;
  /* uses theme variables from app.css without re-emitting them */
}
```

Or reference Tailwind directly:
```css
@reference "tailwindcss";
```

## Common Patterns

### Typography prose

```css
@layer components {
  .prose {
    max-width: 65ch;
    color: var(--color-gray-800);

    p { @apply mb-4 leading-relaxed; }
    h1 { @apply text-3xl font-bold mb-6 text-gray-900; }
    h2 { @apply text-2xl font-semibold mb-4 mt-8 text-gray-900; }
    h3 { @apply text-xl font-semibold mb-3 mt-6 text-gray-900; }
    a { @apply text-blue-600 hover:text-blue-800 underline; }
    code { @apply bg-gray-100 rounded px-1 py-0.5 text-sm font-mono; }
    pre { @apply bg-gray-900 text-gray-100 rounded-lg p-4 overflow-x-auto mb-4; }
    ul { @apply list-disc list-inside mb-4 space-y-1; }
    ol { @apply list-decimal list-inside mb-4 space-y-1; }
    blockquote { @apply border-l-4 border-gray-300 pl-4 italic text-gray-600 mb-4; }
  }
}
```

### Focus ring

```css
@layer base {
  :focus-visible {
    @apply outline-2 outline-offset-2 outline-blue-500;
  }
}
```
