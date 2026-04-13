---
name: tailwind-v4-tokens
description: Opinionated design-token system for Tailwind v4 projects. Enforces semantic tokens over raw colors, single-source brand hue via OKLCH, CSS-first `@theme` configuration, and shadcn/ui composition rules. Auto-loads when CSS contains `@theme` or `@import 'tailwindcss'`, or when `components.json` exists. Rejects hex literals, arbitrary `bg-*-500` Tailwind classes, and duplicate dark-mode definitions. Complements the general `tailwind` skill (which covers v4 basics) and the `bun-tanstack-start` skill (which owns wiring). Keywords design tokens, OKLCH, @theme, brand hue, shadcn, semantic colors, consistency, dark mode.
allowed-tools: Read, Grep, Glob, Write, Edit, WebFetch
---

# Tailwind v4 Design Tokens (Consistency Layer)

The *consistency* skill. Its job is to make sure every color, radius, font, and spacing decision flows from a small set of named tokens — so visual drift across routes and components is structurally impossible.

This skill is **medium-freedom**: tokens are prescriptive, but how you compose them is up to the design. Pair with `frontend-aesthetic` for direction and `bun-tanstack-start` for wiring.

## When to use this skill

| Signal | Action |
|---|---|
| CSS file contains `@theme` or `@import 'tailwindcss'` | Apply this skill's rules |
| `components.json` in repo root (shadcn/ui) | Enforce [shadcn-integration](references/shadcn-integration.md) |
| User writes a hex literal or `bg-red-500`-style class | Flag and replace with a semantic token |
| User adds dark-mode styling | Use [dark-mode](references/dark-mode.md) CSS-var pattern, not `dark:` duplication |
| New component or page | Validate against [validation](references/validation.md) checklist |

## Core rules (NEVER / INSTEAD)

- **NEVER** use hex literals anywhere in components (`#3b82f6`, `#fff`).
  **INSTEAD** reference a semantic token: `bg-primary`, `text-foreground`.
- **NEVER** use raw Tailwind color scales in component code (`bg-blue-500`, `text-gray-600`).
  **INSTEAD** define a semantic token in `@theme` and use it: `bg-primary`, `text-muted-foreground`.
- **NEVER** maintain a separate `tailwind.config.js` / `.ts`.
  **INSTEAD** put all config in a `@theme` block inside the CSS entry.
- **NEVER** duplicate colors for dark mode with `dark:bg-slate-900` per-utility.
  **INSTEAD** redefine CSS variables under `@media (prefers-color-scheme: dark)` or a `.dark` class — see [dark-mode](references/dark-mode.md).
- **NEVER** add a new color without declaring it in `@theme`.
  **INSTEAD** add it once as a semantic token and reference it everywhere.

## The brand-hue pattern (single source of truth)

One CSS variable drives the entire accent palette:

```css
@theme {
  --brand-hue: 265;             /* change this, everything shifts */
  --color-primary:        oklch(62% 0.18 var(--brand-hue));
  --color-primary-fg:     oklch(98% 0.02 var(--brand-hue));
  --color-primary-muted:  oklch(94% 0.03 var(--brand-hue));
}
```

This is the lynchpin of consistency — see [oklch-palette](references/oklch-palette.md) for the full pattern.

## Semantic token vocabulary (recommended minimum)

| Token | Purpose |
|---|---|
| `background` / `foreground` | Page bg + default text |
| `primary` / `primary-foreground` | Brand accent + text on it |
| `secondary` / `secondary-foreground` | Alternate accent |
| `muted` / `muted-foreground` | Low-emphasis surfaces + text |
| `accent` / `accent-foreground` | Highlights, hover states |
| `destructive` / `destructive-foreground` | Errors, deletions |
| `border` / `input` / `ring` | Structural UI |
| `card` / `card-foreground` | Elevated surfaces |
| `popover` / `popover-foreground` | Overlays |

This matches shadcn/ui's vocabulary — reuse it even if not using shadcn components.

## Validation checklist

Before calling a task done:

- [ ] No hex literals in `src/` except inside `@theme`
- [ ] No raw Tailwind color-scale classes (`bg-{color}-{shade}`) in components
- [ ] Every new color added once in `@theme`, referenced by name elsewhere
- [ ] `dark` styling uses CSS-var redefinition, not per-utility `dark:` duplicates
- [ ] No `tailwind.config.js` / `.ts` file in repo
- [ ] Spacing, radius, and font tokens also declared in `@theme` (not hardcoded)

## References

- [theme-block](references/theme-block.md) — `@theme` CSS-first config, variable naming
- [oklch-palette](references/oklch-palette.md) — `--brand-hue` + OKLCH math for the scale
- [semantic-tokens](references/semantic-tokens.md) — the NEVER/INSTEAD catalog
- [shadcn-integration](references/shadcn-integration.md) — `components.json`, `data-slot`, composition rules
- [dark-mode](references/dark-mode.md) — CSS-var redefinition strategy
- [validation](references/validation.md) — grep recipes to enforce rules

## External canonical docs

- Tailwind v4 `@theme`: https://tailwindcss.com/docs/functions-and-directives#theme-directive
- Tailwind v4 installation: https://tailwindcss.com/docs/installation/using-vite
- OKLCH color: https://developer.mozilla.org/en-US/docs/Web/CSS/color_value/oklch
- shadcn/ui skills: https://ui.shadcn.com/docs/skills
- shadcn/ui theming: https://ui.shadcn.com/docs/theming

## Complements

- `tailwind` skill — general v4 utility reference
- `bun-tanstack-start` skill — how the CSS gets imported
- `frontend-aesthetic` skill — what direction the tokens should express
