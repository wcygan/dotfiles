# Motion

One library. One orchestration. Stillness is a design choice.

## Library choice

**Use Motion** (`motion` npm package, the successor to Framer Motion that works in more frameworks). Do not install Framer Motion (`framer-motion`) or GSAP alongside — pick one, commit.

```sh
bun add motion
```

```tsx
import { motion } from 'motion/react'

<motion.h1
  initial={{ opacity: 0, y: 24 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.8, ease: [0.16, 1, 0.3, 1] }}
>
  Something bold
</motion.h1>
```

## Orchestration patterns

Pick **one** per page. Do not combine.

### 1. Page-load cascade
Elements enter in sequence on mount: headline → subhead → CTA → hero image. Stagger by ~80–120ms. After the cascade, the page is still.

```tsx
const container = { animate: { transition: { staggerChildren: 0.1 } } }
const item = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0, transition: { duration: 0.6 } },
}
```

### 2. Scroll-driven reveal
Sections fade/slide in as they enter the viewport. Use `whileInView` with `viewport={{ once: true, amount: 0.3 }}`.

### 3. Staged hero
One commanding element (headline, image, or a piece of type) animates dramatically on load; the rest is static. Good for editorial and brutalist aesthetics.

## Anti-patterns

- **Every card bounces on hover.** Scattered micro-animations feel chaotic. Pick 2–3 interactive surfaces and leave the rest still.
- **Icons that independently pulse or spin for no reason.** Reserve motion for meaning.
- **Scroll-jacking** (custom scroll speed, snap-to-section on marketing pages). Users hate it.
- **Durations under 200ms or over 1200ms.** The former feels twitchy, the latter feels broken.
- **Default easing (`ease`, `ease-in-out`).** Use custom cubic-bezier for character: `[0.16, 1, 0.3, 1]` (a nice overshoot-less settle) or `[0.87, 0, 0.13, 1]` (snappy).

## Accessibility

Respect `prefers-reduced-motion`:

```tsx
import { useReducedMotion } from 'motion/react'

const reduced = useReducedMotion()
const variants = reduced
  ? { initial: { opacity: 0 }, animate: { opacity: 1 } }
  : { initial: { opacity: 0, y: 24 }, animate: { opacity: 1, y: 0 } }
```

## Canonical source

https://motion.dev/docs/react
