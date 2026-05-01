# Typography

Font choice does more than any other single decision. **Match what your references use** — that is the rule. Don't pick "more interesting" type to differentiate; differentiate via scale, weight contrast, and rhythm instead.

## The principle

Look at what 4–5 credible sites in your domain use. Note their display family, body family, and any mono. The consensus is usually a sans-serif workhorse (Inter, IBM Plex Sans, Geist, Söhne, Söhne Mono, GT America, Suisse Int'l) plus optional accents.

If the references all use Inter, **use Inter**. The "AI default" failure mode is using Inter without weight contrast or scale — not using Inter at all.

## What to look for in references

| Question | Where it shows up |
|---|---|
| One family or two? | Most landing pages use one sans for everything; some pair a serif display with a sans body. |
| Display weight | Often heavy (700–900) for a confident hero, occasionally ultra-light (200–300). Mid-weight display reads as bland. |
| Body weight | Usually 400 regular, sometimes 450/500 medium. |
| Largest headline size | Marketing hero headlines today commonly land at `text-6xl` to `text-8xl`. `text-4xl` as max is a fear-of-scale tell. |
| Tracking on display | Almost always tightened — `tracking-tight` or `tracking-tighter`. |
| Mono usage | Only some sites use mono; if so, it's reserved for code, URLs, status, or version chrome. Not body. |

## Practical defaults when references are vague

If you genuinely can't tell what your references use:

- **Sans-only** is the safe consensus. Pair display + body via weight (e.g. 700 display + 400 body) rather than family.
- Use Inter, Geist, IBM Plex Sans, or whichever sans the project already imports. Don't add a new font for distinctiveness.
- Add mono (JetBrains Mono, IBM Plex Mono, or Geist Mono) **only** if the product is technical and the references use mono.

## How to load

Declare in `@theme` (see `tailwind-v4-tokens` skill) and use the semantic class names:

```css
@theme {
  --font-sans:    'Inter', system-ui, sans-serif;
  --font-display: 'Inter', system-ui, sans-serif;  /* same family, weight does the work */
  --font-mono:    'JetBrains Mono', monospace;
}
```

Use `font-sans`, `font-display`, `font-mono` in classes. **Never** inline `font-['Inter']` arbitrary values.

## Size and rhythm — where to be confident

- **Push the largest headline.** Marketing landing pages commonly hit `text-6xl` to `text-8xl`. Use `clamp()` for responsive scale.
- **Body**: `text-base` to `text-lg`, line-height `1.5`–`1.65`.
- **Tracking**: tighten display (`tracking-tight`, `tracking-tighter`); leave body at default.
- **Weight contrast**: pair heavy display (700–900) with regular body (400), or light display (200–300) with medium body (500). Avoid mid-on-mid — that's the bland zone.
- **Tabular nums** for any numerals you want aligned: `font-feature-settings: 'tnum' 1` or Tailwind's `tabular-nums`.

## When to bring in a serif or distinctive display

Bring in a serif display (Fraunces, Tiempos, GT Super, Reckless, Canela) **only if** your references do, and the product's voice supports it:

- E-commerce / fashion / luxury — a thin serif display is common consensus.
- Editorial / publishing / journalism — almost always serif display.
- Wellness / hospitality — humanist serif fits.
- Dev tools / fintech / consumer SaaS — usually no serif. Don't add one to "feel different."

## Self-host for production

Prefer Fontsource packages (`@fontsource-variable/inter`) or `@font-face` with `display: swap`. Google Fonts CDN is fine for prototypes; ship self-hosted for real.

## What this file replaces

The previous version of this file banned Inter, Roboto, system-ui, and Space Grotesk outright. That rule was wrong — it ignores what credible reference sites in many domains actually use. The replacement: **match references; differentiate via scale, weight, and rhythm, not via picking an unusual font in isolation.**
