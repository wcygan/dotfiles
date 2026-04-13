# `@theme` Block (CSS-first config)

Tailwind v4 removes `tailwind.config.js`. All customization lives in a `@theme` block inside your CSS entry.

## Minimal app.css

```css
@import 'tailwindcss' source('../');

@theme {
  /* Brand */
  --brand-hue: 265;

  /* Semantic colors — reference via bg-primary, text-foreground, etc. */
  --color-background:         oklch(98% 0.005 var(--brand-hue));
  --color-foreground:         oklch(18% 0.02 var(--brand-hue));
  --color-primary:            oklch(62% 0.18 var(--brand-hue));
  --color-primary-foreground: oklch(98% 0.02 var(--brand-hue));
  --color-muted:              oklch(94% 0.01 var(--brand-hue));
  --color-muted-foreground:   oklch(45% 0.03 var(--brand-hue));
  --color-border:             oklch(90% 0.01 var(--brand-hue));

  /* Typography */
  --font-display: 'Fraunces', serif;
  --font-sans:    'Inter Tight', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;

  /* Radius */
  --radius-sm: 0.25rem;
  --radius:    0.5rem;
  --radius-lg: 0.75rem;
  --radius-xl: 1rem;
}
```

## Naming convention

Prefix determines how Tailwind exposes the token:

| Prefix | Generates utility | Example |
|---|---|---|
| `--color-*` | `bg-*`, `text-*`, `border-*`, `ring-*` | `bg-primary` |
| `--font-*` | `font-*` | `font-display` |
| `--radius-*` | `rounded-*` | `rounded-lg` |
| `--spacing-*` | `p-*`, `m-*`, etc. | `p-md` |
| `--breakpoint-*` | responsive prefixes | `xl:...` |
| `--text-*` | `text-*` for sizes | `text-display` |

Follow this naming strictly — utilities only appear for tokens that use the right prefix.

## What NOT to do

- Do not create `tailwind.config.js` or `tailwind.config.ts`.
- Do not import theme tokens from a JS module.
- Do not define raw colors outside `@theme` unless they are truly one-off (and even then, question whether they should be a token).
