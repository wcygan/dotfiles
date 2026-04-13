# Pre-flight Checks

Run these before delegating. They are fast reads, not a full audit. If a check fails, fix or flag *before* spawning the subagent — the agent assumes the stack is wired correctly.

## Stack

- [ ] `package.json` contains `@tanstack/react-start`
- [ ] `package.json` contains `tailwindcss` v4 (check `^4` or `^4.0`)
- [ ] `bun.lockb` exists (Bun is the runtime, not npm)
- [ ] Scripts in `package.json` use `bun --bun vite …` (forces Bun end-to-end)

## Tailwind v4 shape

- [ ] Exactly one CSS entry with `@import 'tailwindcss'` (not `@tailwind base/components/utilities`)
- [ ] No `tailwind.config.js` or `.ts` file
- [ ] `@theme` block present (if starting fresh, agent will add it)

## TanStack Start shape

- [ ] `src/routes/__root.tsx` exists — it's the chrome anchor
- [ ] Vite plugins ordered: `tsConfigPaths → tanstackStart → viteReact → tailwindcss`
- [ ] Stylesheet imported via `?url` + `head.links` in `__root.tsx`

## shadcn/ui (optional)

- [ ] If `components.json` exists, note the base color / style so the agent respects it
- [ ] If not, ask the user whether to install shadcn before delegating (one question, one answer)

## What to do if checks fail

Do **not** run the subagent blind. Either:
- Fix the stack first (often the `bun-tanstack-start` skill has the exact snippet), or
- Surface the gap to the user and ask how to proceed.

Blind delegation on a broken stack produces code that can't run.

## Quick grep recipes

```sh
# Confirm v4 + shape
rg "@tailwind (base|components|utilities)" src/   # should be 0 hits
fd -t f "tailwind\.config\.(js|ts|cjs|mjs)"       # should be 0 files
rg "^\s*\"dev\":\s*\".*bun --bun" package.json    # should hit
rg "@import ['\"]tailwindcss" src/                 # should hit
```

If any of these surprise you, surface to the user.
