# Tailwind CSS — Directives & Functions

## Directives

### @import

```css
/* Import Tailwind */
@import "tailwindcss";

/* Tailwind with options */
@import "tailwindcss" source("../src");     /* set base source dir */
@import "tailwindcss" source(none);         /* disable auto-detection */
@import "tailwindcss" important;            /* make all utilities !important */
@import "tailwindcss" prefix(tw);           /* prefix all utilities with tw- */
```

### @theme

Define design tokens that generate utility classes:

```css
@theme {
  --color-brand: oklch(0.65 0.2 240);
  --font-display: "Inter", sans-serif;
  --radius-card: 0.75rem;
  --animate-pop: pop 0.3s ease-out;

  @keyframes pop {
    0%   { transform: scale(0.95); opacity: 0; }
    100% { transform: scale(1);    opacity: 1; }
  }
}

/* inline: resolve variable references at compile time */
@theme inline {
  --font-sans: var(--font-inter);
  --color-primary: var(--brand-primary);
}

/* static: always emit these variables in output */
@theme static {
  --color-surface: var(--color-gray-50);
}
```

### @layer

Add custom CSS to Tailwind's cascade layers:

```css
@layer base {
  /* Element defaults, resets */
  h1 { font-size: var(--text-3xl); }
}

@layer components {
  /* Reusable component classes */
  .card { @apply rounded-lg bg-white shadow-md p-6; }
}

@layer utilities {
  /* Single-purpose utilities (rarely needed — prefer @utility) */
  .scrollbar-none { scrollbar-width: none; }
}
```

### @utility

Define custom utilities that work with ALL variants:

```css
/* Simple */
@utility content-auto { content-visibility: auto; }

/* With nesting */
@utility scrollbar-hidden {
  &::-webkit-scrollbar { display: none; }
  scrollbar-width: none;
}

/* Functional (matches theme values) */
@utility tab-* {
  tab-size: --value(--tab-size-*);
}

/* Bare integer values */
@utility z-* {
  z-index: --value(integer);
}

/* Arbitrary values */
@utility opacity-* {
  opacity: --value([percentage]);
}
```

### @custom-variant

Create reusable variants:

```css
/* Simple (shorthand) */
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));

/* Multi-rule (block form) */
@custom-variant any-hover {
  @media (any-hover: hover) {
    &:hover { @slot; }
  }
}

/* Multiple conditions */
@custom-variant hocus (&:hover, &:focus);
```

### @variant

Apply a variant inside CSS:

```css
.element {
  background: white;

  @variant dark {
    background: var(--color-gray-900);
  }

  @variant hover {
    box-shadow: var(--shadow-lg);
  }

  @variant md {
    max-width: 48rem;
  }
}
```

### @apply

Inline utilities into custom CSS:

```css
.btn-primary {
  @apply inline-flex items-center rounded-md bg-blue-600 px-4 py-2;
  @apply text-sm font-semibold text-white hover:bg-blue-700;
  @apply focus-visible:outline-2 focus-visible:outline-offset-2;
  @apply disabled:opacity-50 disabled:cursor-not-allowed;
}
```

### @source

Tell Tailwind which files to scan:

```css
/* Add external library */
@source "../node_modules/@company/ui-lib";

/* Safelist specific classes */
@source inline("underline");
@source inline("{hover:,focus:,}text-red-{500,600,700}");

/* Exclude paths */
@source not "../src/legacy";
```

### @reference

Import theme without duplicating CSS (for CSS Modules, Vue SFCs, Svelte):

```css
/* In a component's CSS */
@reference "../../app.css";
@reference "tailwindcss";

h1 { @apply text-3xl font-bold; }
```

### @plugin

Load a v3-compatible Tailwind plugin:

```css
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
@plugin "@tailwindcss/aspect-ratio";
```

### @config

Load a v3 `tailwind.config.js` (backwards compatibility):

```css
@import "tailwindcss";
@config "../../tailwind.config.js";
```

---

## CSS Functions

### --spacing()

Generate spacing values based on the spacing scale:

```css
.element {
  margin: --spacing(4);         /* calc(var(--spacing) * 4) */
  padding: --spacing(2) --spacing(6);
  gap: --spacing(3);
}
```

Useful in arbitrary values:
```html
<div class="py-[calc(--spacing(4)-1px)]">
<div class="mt-[--spacing(6)]">
```

### --alpha()

Adjust color opacity in CSS:

```css
.element {
  /* input */
  background: --alpha(var(--color-blue-500) / 10%);

  /* compiled output */
  background: color-mix(in oklab, var(--color-blue-500) 10%, transparent);
}
```

### --value()

Used inside `@utility` to bind to theme values or input types:

```css
@utility text-* {
  /* Match named theme values */
  font-size: --value(--text-*);

  /* Match bare integers */
  font-size: --value(integer);

  /* Match arbitrary length values */
  font-size: --value([length]);

  /* Match multiple */
  font-size: --value(--text-*, [length], [percentage]);
}
```

### theme() (deprecated in v4)

Access theme values with dot notation — replaced by CSS variables in v4:

```css
/* v3 */
.element { margin: theme(spacing.12); }

/* v4 equivalent */
.element { margin: var(--spacing-12); }
/* or */
.element { margin: --spacing(12); }
```

---

## Subpath Imports

Use Node.js subpath imports with directives:

```json
// package.json
{
  "imports": {
    "#styles": "./src/styles/app.css",
    "#theme": "./src/styles/theme.css"
  }
}
```

```css
@reference "#styles";
@import "#theme";
```
