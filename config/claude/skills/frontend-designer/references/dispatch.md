# Dispatch Pattern

The subagent call is the whole point of this skill. Get it right.

## The call

Use the `Agent` tool with:

- `subagent_type: "frontend-design-agent"`
- `description: "Frontend design: <short subject>"` (3-5 words)
- `prompt:` self-contained — see template below

The subagent does **not** see this session's history. Its prompt must carry every relevant fact.

## Prompt template

```
## Task
<one paragraph: the surface, the route path, the audience, the desired feeling>

## Constraints
- Stack: Bun + TanStack Start + Tailwind v4 (+ shadcn/ui if installed)
- Preloaded skills: bun-tanstack-start, tailwind-v4-tokens, frontend-aesthetic
- Copy: <verbatim hero copy if user provided, otherwise "write yours, keep it tight">
- Assets: <image paths, or "none — propose placeholders">
- Brand: <tone, hue, or "pick one and justify it">

## Expectations
1. Declare aesthetic direction + type pairing + color + motion + layout move in one paragraph before writing JSX.
2. Enforce tokens — no hex, no raw color scales.
3. Use `<Outlet />` chrome from `__root.tsx`; do not regenerate nav/footer.
4. Install shadcn components via `bunx shadcn@latest add` rather than hand-rolling.
5. Run the validation greps from `tailwind-v4-tokens/references/validation.md` before reporting done.
6. Report in the agent's standard output format (Built / Aesthetic Choices / Validation Run / Verified / Follow-ups).

## Files Likely To Change
- src/routes/<route>.tsx
- src/styles/app.css (only if tokens need to be added/extended)
- src/routes/__root.tsx (only if chrome genuinely needs to change)
- components.json / src/components/ui/* (if shadcn primitives get added)
```

## Example invocation

For "build a hero for /routes/index.tsx pitching a productivity app called Cove":

```
subagent_type: frontend-design-agent
description: Hero for Cove landing
prompt: |
  ## Task
  Build a hero section at `src/routes/index.tsx` for a productivity app called Cove.
  Audience: individual knowledge workers frustrated with tool sprawl.
  Desired feeling: calm, focused, premium — not another "10x your workflow" SaaS.

  ## Constraints
  - Stack: Bun + TanStack Start + Tailwind v4 + shadcn/ui (components.json present)
  - Preloaded skills: bun-tanstack-start, tailwind-v4-tokens, frontend-aesthetic
  - Copy: "Quiet software for loud workdays." — plus a one-sentence subhead of your choosing
  - Assets: none — propose a placeholder treatment
  - Brand: pick a hue and justify it

  ## Expectations
  (standard — as above)
```

## After the subagent returns

Relay the agent's output verbatim, then offer 2-3 concrete follow-ups:

- "Add a second route with the same chrome — <route path>"
- "Dark-mode token pass"
- "Extract <component> into `src/components/`"
- "Wire up form submission via `createServerFn`"

Do not silently do the follow-ups. Offer, wait.

## What not to do in the main thread

- Do not write JSX/CSS inline after the agent returns. If a tweak is needed, call the agent again.
- Do not hold two design conversations in parallel (main + agent). Pick the agent, stay with it.
- Do not strip the agent's "Aesthetic Choices" paragraph when relaying — it's the evidence of commitment.
