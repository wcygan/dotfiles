# Layouts: Grid-Breaking & Anti-SaaS

The default AI output: a `max-w-7xl mx-auto` container, centered headline, three rounded cards in a row, subtle drop shadow. Every page looks the same. This document is about choosing something else.

## Anti-patterns (the statistical center)

- Centered container (`max-w-7xl mx-auto px-6`) as the *only* layout primitive
- Three-column card grid ("Features", "Benefits", "Testimonials")
- Rounded corners (`rounded-xl`) + `shadow-lg` + `border border-gray-100` everywhere
- Hero = centered headline + subhead + two buttons
- Footer = four equal columns of links
- Gradient background on hero, flat white on everything else

## Grid-breaking moves

### 1. Asymmetry
Instead of centering, offset the primary content to ⅔ of the viewport width. Let the other ⅓ hold a large image, negative space, or a single line of oversized type.

### 2. Full-bleed moments
Break out of the container for at least one section — full-viewport image, full-width colored band, or an edge-to-edge type treatment. Signals "we aren't afraid of the page."

### 3. Vertical split
Two columns of equal height, each full-viewport, with a sharp dividing line. Left = title + copy, right = image or form. Works for editorial and brutalist.

### 4. Hanging text
Display headline breaks out of its column: oversized first letter in the margin, drop-cap style, or a word overflowing the grid.

### 5. Strong horizontal rhythm
Use one very tall hero, then a sequence of short horizontal bands with strong color blocks. Each band = one idea.

### 6. Viewport typography
A single phrase scaled to fill the viewport. `text-[12vw]` kind of moment. Use sparingly — once per page maximum.

## Spacing

- Do not default to generous equal padding. Asymmetric margins feel intentional.
- Vertical rhythm: use a fixed "section spacing" token — `py-24` or `py-32` — between major sections.
- Horizontal rhythm: let the container width vary between sections for visual interest.

## Cards (when you *must*)

If cards are unavoidable:
- No drop shadows. Use a border or a background-tint instead.
- Sharp corners for brutalist/editorial; `rounded-sm` or `rounded` at most.
- Break the "three equal cards" pattern — one big hero card + two smaller, or an asymmetric grid.

## Canonical exemplars

- Stripe's long-form marketing (strong horizontal rhythm)
- Apple product pages (staged hero, full-bleed imagery)
- Linear.app (restraint, dark moody, single accent)
- It's Nice That (editorial, hanging type, asymmetry)
