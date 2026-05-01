# Anti-patterns (the AI tells)

These are the defaults Claude reaches for without guidance — the visual equivalent of "write a React component." They are the giveaway that a page was generated without supervision. Avoid them regardless of the design direction you're heading.

This file is short on purpose. It used to ban specific aesthetic territories ("never X aesthetic"). That was wrong — most "extreme" aesthetics are perfectly fine when the references support them. The real anti-patterns are the *unguided defaults*.

## Typography tells

- **Inter (or any sans) used with no weight contrast and no scale.** The fix isn't a different font — it's a heavier display, a tighter tracking, a larger size.
- **Display and body in the same family at the same weight, just different sizes.** No voice contrast.
- **`text-4xl` as the largest thing on the page.** Fear of scale. Marketing landing pages typically push to `text-6xl`+.
- **Default tracking on display.** Tighten — `tracking-tight` or `tracking-tighter`.
- **Inline arbitrary values like `font-['Inter']` in components.** Bypasses tokens. Declare in `@theme`.

## Color tells

- **Purple-to-blue gradient on white.** The single most common AI default. Delete on sight.
- **Gradient across three or more hues.** Reads as "designed in 2021 Figma."
- **Raw `bg-blue-500` / `text-gray-600` / hex literals in components.** Bypasses the token system. See `tailwind-v4-tokens`.
- **"Safe" Tailwind palette: slate + indigo + white.** The stock-photo version of a color system.
- **Two accent colors with no hierarchy.** Pick one accent, make it appear ≤20% of the surface.

## Layout tells

- **`max-w-7xl mx-auto` as the only container.** Learn `max-w-prose`, `max-w-screen-sm`, full-bleed for variety.
- **Three-column card grid labeled "Features" / "Benefits" / "Why choose us."** The stock SaaS pattern. If you must use a 3-card grid, give it a real reason and break the visual symmetry slightly.
- **Hero = centered headline + subhead + two buttons of equal weight.** Pick a primary CTA; vary the layout.
- **`rounded-xl` + `shadow-lg` + `border-gray-100` on every card.** The SaaS dashboard uniform.
- **Footer with four equal columns of links.** Varies almost zero between companies.

## Motion tells

- **Every card and icon animates on hover.** Scattered micro-animations feel chaotic. Pick 2–3 interactive surfaces; keep the rest still.
- **Default `ease` / `ease-in-out` curves.** No personality. Use `[0.16, 1, 0.3, 1]` or similar custom curves.
- **Scroll-jacking** (custom scroll speed, snap-to-section). Users hate it.
- **Durations under 200ms or over 1200ms.** Twitchy or broken-feeling.
- **Multiple motion libraries.** Pick one — Motion (`motion` npm package).

## Copy tells

- **"Build faster. Scale smarter."** Generic landing-page slop.
- **Hero copy that explains what the product does before selling a feeling.**
- **"Trusted by thousands of teams worldwide."** If you have to say it, you aren't.
- **"Get started" as the primary CTA.** Pick a verb that matches the product.

## Composition tells

- **Dashboard screenshot in a fake browser-chrome / macOS window mockup.** Cliché.
- **Testimonial carousel with avatar circles.** Cliché.
- **Gradient borders on cards.** 2022 called.

## When the references actually do these things

If your reference sites use a centered three-card grid, or Inter with no contrast, that's a signal that those patterns are *consensus in your domain*, not anti-patterns. Match the consensus — but on the axes where you have freedom (scale, weight, accent placement, copy voice), avoid the AI tells listed here.

The rule: do what your references do, but better than a default-Claude-output version of the same thing.
