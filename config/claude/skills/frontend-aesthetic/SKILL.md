---
name: frontend-aesthetic
description: Opinionated aesthetic direction for frontend work. Research-first — study 3–5 credible reference sites in the user's space, identify the patterns they share, build to that consensus rather than inventing distinctive aesthetics. Use when the user says "design", "landing", "hero", "make it beautiful", "style this", or when creating a new marketing/landing route. Complements `tailwind-v4-tokens` (which owns consistency) and `bun-tanstack-start` (which owns wiring). Keywords aesthetic, design, taste, landing page, hero, typography, motion, visual direction, frontend design.
---

# Frontend Aesthetic (Research & Direction)

The *taste* skill. Its job is to ground design decisions in **what already works in the user's space**, not in invented aesthetic territories. Before writing any code, identify 3–5 credible reference sites — competitors, peers, well-regarded products in the same domain — and synthesize the patterns they share.

The failure mode this skill prevents is twofold:

1. **AI defaults** — Inter + purple gradient + three centered cards.
2. **Cosplay extremes** — picking "brutalist" or "lo-fi zine" because they sound distinctive, not because they fit the product.

The cure for both is the same: study the neighborhood first, then design to fit it (with one deliberate signature, not four).

## When to use this skill

| Signal | Action |
|---|---|
| User says "design", "make it beautiful", "landing page", "hero", "style this" | Apply this skill |
| New marketing route or landing page | Apply this skill |
| Refining visual polish on existing UI | Apply this skill — confirm references first |
| User says "I don't like how this looks" | Apply this skill — disagreement usually means the references were wrong |
| CRUD / internal tool work | **Do not** use this skill — stay consistent with the rest of the app |

The trigger is deliberate. Internal dashboards get `tailwind-v4-tokens` for consistency; *visible surfaces* get this skill for direction.

## Rule zero: study before designing

Before writing a single JSX tag:

1. **Identify the domain** — fintech, dev tools, consumer SaaS, agency portfolio, e-commerce, etc. See [domain-matching](references/domain-matching.md) for canonical reference sites per domain.
2. **Pick 3–5 reference sites** — preferably ones the user named, plus 1–2 from the canonical list. If the user says "I don't have references," use the domain-matching defaults and tell them which ones you used.
3. **Study each one** along the axes in [reference-research](references/reference-research.md): typography, palette, layout rhythm, motion, copy voice, signature elements.
4. **Synthesize the consensus** — what do most of them do? That's your direction. Note the *one or two* places they meaningfully differ — those are spots where you can place a deliberate signature.
5. **State the synthesis back** in one short paragraph before coding. Get the user's nod or correction.

If the user explicitly wants something distinctive ("I want this to feel different from Linear/Vercel"), still do the research — you need to know what you're departing from, and how far.

## Building from the consensus

Once the synthesis is stated, every downstream decision follows from the references:

- **Typography**: use the same family or close substitutes to what the references use. Don't pick a "more interesting" font to differentiate. See [typography](references/typography.md).
- **Color**: match the dominant base + accent pattern your references use. If they're all near-monochrome with one accent, do that.
- **Layout**: respect the rhythm and density of the references. If they all use a contained text column, don't go full-bleed.
- **Motion**: one orchestrated pattern, single library — see [motion](references/motion.md). If the references are mostly still, be still.
- **Tokens**: declare via `tailwind-v4-tokens`. No raw hex.

## Signature: one deliberate departure

After matching the consensus on most axes, pick **one** axis where you go slightly further than the references — a more confident type scale, a single saturated accent your peers don't have, a particular layout move. This is what keeps the result from feeling like a copy.

Don't pick four signatures. One. Defend it in your synthesis paragraph.

## NEVER (the unconditional AI tells)

These have nothing to do with aesthetic direction — they are the giveaways that a page was generated without supervision. Avoid regardless of references:

- **Purple-to-blue gradient on white** — the single most common AI default.
- **Three-card grid with `rounded-xl shadow-lg border-gray-100`** — the SaaS dashboard uniform.
- **`max-w-7xl mx-auto` as the only container primitive** — learn `max-w-prose`, `max-w-screen-sm`, full-bleed.
- **Default `ease` easing curves** — pick a custom cubic-bezier with character.
- **Hero copy that explains what the product does before selling a feeling.**
- **Hex literals or `bg-blue-500` in components** — use semantic tokens (`tailwind-v4-tokens`).
- **Same family for display and body with no weight contrast** — at minimum, pair voices via weight.

Inter is fine when your references use it; the tell is using it lazily without contrast or scale. See [anti-patterns](references/anti-patterns.md) for the full list.

## Consistency guard

Even on a landing page, the **chrome** (nav, footer, global frame) stays consistent across routes. `__root.tsx` is the single source of truth. See [consistency-anchor](references/consistency-anchor.md).

## Check before you commit

- [ ] 3–5 reference sites named (or the user explicitly waived)
- [ ] Synthesis paragraph stated and acknowledged
- [ ] Typography choice grounded in references — not a "more interesting" font picked in isolation
- [ ] Color: dominant + accent pattern matches the references
- [ ] One deliberate signature departure, not four
- [ ] Tokens declared via `tailwind-v4-tokens`, no raw hex
- [ ] Motion: one library, one orchestrated pattern, `prefers-reduced-motion` respected
- [ ] `__root.tsx` chrome untouched (unless this *is* the root)

## References

- [reference-research](references/reference-research.md) — how to study a site, what to extract, how to synthesize
- [domain-matching](references/domain-matching.md) — canonical reference sites per domain
- [typography](references/typography.md) — practical pairings and rhythm; reference-driven
- [motion](references/motion.md) — single library, orchestration, reduced-motion
- [layouts](references/layouts.md) — common patterns and the AI defaults to avoid
- [anti-patterns](references/anti-patterns.md) — the AI tells to avoid regardless of direction
- [consistency-anchor](references/consistency-anchor.md) — chrome vs content boundary

## Complements

- `tailwind-v4-tokens` — encodes the decisions made here as CSS variables
- `bun-tanstack-start` — owns routing, wiring, server code
- `tailwind` / `tanstack-start` — general framework reference
