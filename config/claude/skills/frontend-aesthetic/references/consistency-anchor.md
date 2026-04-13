# Consistency Anchor (chrome vs content)

Even while taking an extreme aesthetic position on a landing page, site chrome must stay consistent across routes. The user should always know where they are.

## The rule

- **Chrome** (top nav, footer, global header, `<html>`/`<body>` setup, providers) = single source of truth in `src/routes/__root.tsx`.
- **Content** (hero, sections, page-specific layout) = per-route, free to be extreme.

**Never regenerate nav/header/footer in a child route.** Render inside `<Outlet />`.

## How this skill and `bun-tanstack-start` cooperate

| Responsibility | Owner |
|---|---|
| File-based router mechanics | `bun-tanstack-start` |
| `__root.tsx` canonical shape | `bun-tanstack-start` — see its [routing](../../bun-tanstack-start/references/routing.md) |
| Nav / footer design decisions | `frontend-aesthetic` (this skill) |
| Tokenizing those decisions | `tailwind-v4-tokens` |

## Checking for drift

If someone adds a second `<nav>` inside a route file, that is a consistency break. Grep:

```sh
rg "^\s*<nav" src/routes/ --type tsx -g '!__root.tsx'
```

Any hit outside `__root.tsx` is a drift signal. Either:
- Move the nav markup up to `__root.tsx` and conditionally render per route, OR
- Keep the per-route element, but rename it (e.g., `<aside>`) if it's truly not site-level navigation.

## The `design-loop` rule, in one sentence

When adding the second, third, or Nth landing page, **copy the top nav and footer verbatim** from the most recent route — do not regenerate from scratch. The `__root.tsx` structure makes this automatic; the rule exists for the cases where someone breaks the automation.

## What can vary per-route

- Hero styling, color, type scale (it's a landing page; be bold)
- Page-specific background treatments
- Transitions between sections
- CTA button style (as long as the token set is respected)

## What must not vary per-route

- Logo mark and placement
- Primary nav items and their labels
- Footer columns and links
- Global font stack (`font-display`, `font-sans`, `font-mono` tokens)
- Semantic color tokens (`bg-background`, `text-foreground`, etc.)
