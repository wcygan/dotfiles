---
name: frontend-aesthetic
description: Opinionated aesthetic direction for frontend work. Forks Anthropic's bundled `frontend-design` with NEVER/INSTEAD directives, expanded aesthetic territories (editorial, brutalist, swiss, dark-moody, handcrafted, lo-fi-zine), explicit typography pairings, and a single motion-library choice. Use when the user says "design", "landing", "hero", "make it beautiful", "style this", or when creating a new marketing/landing route. Complements `tailwind-v4-tokens` (which owns consistency) and `bun-tanstack-start` (which owns wiring). Keywords aesthetic, design, taste, landing page, hero, typography, motion, visual direction, frontend design.
---

# Frontend Aesthetic (Taste & Direction)

The *taste* skill. Its job is to push Claude away from the statistical center of its training data — Inter + purple gradient + centered cards — and commit to a distinct aesthetic direction *before* writing any code.

**High-freedom**: pick an aesthetic, declare it, then let the details follow. Lean on `tailwind-v4-tokens` for how to encode the decision.

## When to use this skill

| Signal | Action |
|---|---|
| User says "design", "make it beautiful", "landing page", "hero", "style this" | Apply this skill |
| New marketing route or landing page | Apply this skill |
| Refining visual polish on existing UI | Apply this skill — pick or confirm the direction first |
| CRUD / internal tool work | **Do not** use this skill — stay consistent, don't reinvent |

The trigger is deliberate. Internal dashboards get `tailwind-v4-tokens` for consistency; *visible surfaces* get this skill for direction.

## Rule zero: commit to a direction before coding

Before writing a single JSX tag, pick **one** aesthetic from [aesthetics](references/aesthetics.md) and *state it*. Every subsequent typography, color, spacing, and motion choice follows from that commitment.

Never produce a "good default" hoping the user notices. Pick an extreme point and defend it.

## NEVER / INSTEAD (typography)

- **NEVER** use Inter, Roboto, Arial, system-ui, or Space Grotesk for display text.
- **NEVER** use the same font family for display and body — pair distinct voices.
- **INSTEAD** pick a display + body pairing from [typography](references/typography.md). Examples:
  - Editorial: Fraunces (display) + Inter Tight (body)
  - Swiss: Söhne (display) + Söhne Mono for accents
  - Brutalist: Neue Haas Grotesk Display (display) + JetBrains Mono (body)
  - Handcrafted: Canela (display) + Söhne (body)
  - Lo-fi zine: VT323 / Departure Mono (display) + Inter Tight (body)

## NEVER / INSTEAD (color)

- **NEVER** a purple-to-blue gradient on white.
- **NEVER** a gradient across more than two hues.
- **NEVER** raw hex literals — use tokens from `tailwind-v4-tokens`.
- **INSTEAD** pick a dominant color + one sharp accent. Let the accent appear ≤20% of the surface.

## NEVER / INSTEAD (motion)

- **NEVER** scatter micro-animations across the page (individual card hover bounces, each icon pulsing).
- **NEVER** mix two motion libraries.
- **INSTEAD** pick **one** orchestrated entrance (page-load cascade, scroll-driven reveal, or staged hero) and let the rest of the page be still. See [motion](references/motion.md).
- **INSTEAD** pick **one** animation library for the project. This codebase defaults to **Motion** (`motion` npm package). Do not add Framer Motion or GSAP alongside.

## NEVER / INSTEAD (layout)

- **NEVER** center everything in a 1200px container with stacked cards.
- **NEVER** rounded cards + drop shadow + subtle border (the "SaaS dashboard" default).
- **INSTEAD** break the grid deliberately — asymmetry, full-bleed imagery, hanging text, or a strong vertical split. See [layouts](references/layouts.md).

## Consistency guard

Even while being extreme on a landing page, the **chrome** (nav, footer, global frame) stays consistent across routes. Load the `bun-tanstack-start` skill's [routing](../../bun-tanstack-start/references/routing.md) rule: `__root.tsx` is the single source of truth. See [consistency-anchor](references/consistency-anchor.md).

## Check before you commit

- [ ] One aesthetic direction stated explicitly
- [ ] Display font and body font named — not Inter
- [ ] One dominant color + one accent — no purple-to-blue gradient
- [ ] Motion orchestrated, not scattered; single library
- [ ] Layout is not "centered container of cards"
- [ ] Tokens declared via `tailwind-v4-tokens` skill, not hex
- [ ] `__root.tsx` chrome untouched (unless this *is* the root)

## References

- [aesthetics](references/aesthetics.md) — **18 committed directions** with traits; pick one per page
- [domain-matching](references/domain-matching.md) — narrow the 18 to a domain-appropriate pool of 4–6 before picking
- [typography](references/typography.md) — approved font pairings, anti-patterns
- [motion](references/motion.md) — Motion library patterns, orchestration rules
- [layouts](references/layouts.md) — grid-breaking, asymmetry, anti-SaaS patterns
- [consistency-anchor](references/consistency-anchor.md) — chrome vs content, `__root.tsx` rule
- [anti-patterns](references/anti-patterns.md) — the statistical center to avoid

## External canonical sources

- Anthropic bundled skill (forked from): https://github.com/anthropics/claude-code/blob/main/plugins/frontend-design/skills/frontend-design/SKILL.md
- "Teaching Claude to Design Better" (methodology source): https://www.justinwetch.com/blog/improvingclaudefrontend
- Anthropic blog on the skill: https://claude.com/blog/improving-frontend-design-through-skills
- Motion library: https://motion.dev/

## Complements

- `tailwind-v4-tokens` — encodes the decisions made here as CSS variables
- `bun-tanstack-start` — owns routing, wiring, server code
- `tailwind` / `tanstack-start` — general framework reference
