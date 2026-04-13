# Typography

Font choice does more than any other single decision. Inter is the statistical center; avoid it for display.

## NEVER

- Inter, Roboto, Open Sans, Arial, Helvetica, Lato, system-ui — all signal "generic AI output"
- Space Grotesk — over-used as the "design-conscious default"
- The same family for display and body — always pair two distinct voices
- More than three families on a page (display, body, mono at most)

## INSTEAD — approved pairings

| Aesthetic | Display | Body | Mono/accent |
|---|---|---|---|
| **Editorial** | Fraunces, Canela, Tiempos Headline | Inter Tight, Söhne | JetBrains Mono |
| **Swiss / modernist** | Söhne, Neue Haas Grotesk Display | Söhne | Söhne Mono |
| **Brutalist** | Neue Haas Grotesk Display, Druk | JetBrains Mono | — |
| **Handcrafted / warm** | Canela, Tiempos, Loos | Söhne, Reckless | — |
| **Dark / moody** | Reckless Neue, Signifier | Söhne Breit | IBM Plex Mono |
| **Lo-fi zine / retro** | VT323, Departure Mono, PP Mondwest | Inter Tight, JetBrains Mono | — |
| **Serif-forward tech** | GT Super, Söhne Breit | Söhne | JetBrains Mono |

## How to load

Declare once in `@theme` (see `tailwind-v4-tokens` skill):

```css
@theme {
  --font-display: 'Fraunces', 'Times New Roman', serif;
  --font-sans:    'Inter Tight', system-ui, sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
}
```

Then use `font-display`, `font-sans`, `font-mono` everywhere. **Never** inline `font-['Inter']` arbitrary values.

## Size and rhythm

- Display text: at least one headline ≥ `text-6xl` (60px) on landing pages — fear of large type is the default failure.
- Body: `text-base` to `text-lg`, line-height `1.5`–`1.65`.
- Tracking: tighten display (`tracking-tight`, `tracking-tighter`), leave body at default.
- Weight contrast: pair ultra-light display (200–300) with medium body (400–500), or black display (800–900) with regular body. Avoid "mid on mid."

## Self-host via Fontsource or native @font-face

For production, prefer Fontsource packages (`@fontsource-variable/fraunces`) or `@font-face` with `display: swap`. Do not rely on Google Fonts CDN in high-performance builds.
