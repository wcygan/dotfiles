# Anti-patterns (the Statistical Center)

These are the defaults Claude reaches for without guidance — the visual equivalent of "write a React component." Avoid them deliberately.

## Typography

- **Inter everywhere.** The clearest signal of unguided AI output.
- **Roboto / Open Sans / Lato / Arial / system-ui for display.** Same problem.
- **Space Grotesk display + Inter body.** The "I've seen a Dribbble post" default.
- **Display and body in the same family, just different weights.** Weak contrast, no voice.
- **`text-4xl` as the biggest thing on the page.** Fear of scale. Push to `text-6xl`+ for landing pages.
- **Default tracking on display text.** Tighten display aggressively (`tracking-tight` / `tracking-tighter`).

## Color

- **Purple-to-blue gradient on white.** The single most common AI default.
- **Any gradient across three or more hues.** Reads as "designed in 2021 Figma."
- **`bg-gradient-to-br from-purple-500 to-blue-500`.** Delete on sight.
- **Raw `bg-blue-500` / `text-gray-600`.** Bypasses the token system. See `tailwind-v4-tokens`.
- **"Safe" palettes: slate + indigo + white.** The stock-photo version of a color system.

## Layout

- **`max-w-7xl mx-auto` as the only container.** Learn `max-w-prose`, `max-w-screen-sm`, full-bleed.
- **Three-column card grid labeled "Features" / "Benefits" / "Why choose us".** The stock SaaS pattern.
- **Hero = centered headline + subhead + two buttons.** Boring.
- **Rounded-xl + shadow-lg + border-gray-100 everywhere.** The SaaS dashboard uniform.
- **Footer with four equal columns.** Varies little between different companies.

## Motion

- **Every card bounces on hover.** Scattered micro-animations feel chaotic.
- **Icons that independently pulse or spin.** Motion without meaning.
- **Default `ease` easing curves.** No personality.
- **Scroll-hijacking.** Users hate it.
- **Blur-on-scroll backgrounds that kill performance.** Be careful on low-end devices.

## Copy & Content

- **"Build faster. Scale smarter."** Generic landing-page slop.
- **Hero copy that explains what the product does before selling a feeling.**
- **"Trusted by thousands of teams worldwide."** If you have to say it, you aren't.

## Composition

- **Dashboard screenshot in a browser-chrome mockup.** The MacOS window frame + screenshot combo.
- **Testimonial carousel with avatar circles.** Cliché.
- **"Get started" as the primary CTA label.** Pick a verb that matches the product.
- **Gradient borders on cards.** 2022 called.

## Contradictions to avoid

Do not take this document as "always do the opposite." Some of these patterns (cards, centered containers, testimonials) work in context — the issue is using them *by default* without a reason. Every choice should be defensible against: "why not something more distinct?"

## The Claude-specific trap

The bundled `frontend-design` skill says "NEVER converge on common choices across generations" — but Claude has no cross-session memory, so this is unactionable advice. Ignore it. The real rule: **within this project, pick a direction and commit to it.** Drift happens inside a project, not across sessions.
