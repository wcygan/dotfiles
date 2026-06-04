---
name: ui-motion-polish
description: Use when Codex is building, styling, or reviewing frontend UI where motion, micro-interactions, component feel, animation performance, or interaction polish matters. Triggers include animation timing/easing, popovers, dialogs, drawers, toasts, tabs, tooltips, hover/active states, drag or swipe gestures, reduced-motion behavior, Framer Motion or CSS transition choices, and requests to make an interface feel more polished or responsive.
---

# UI Motion Polish

## Purpose

Apply practical design-engineering judgment to make interface motion feel fast, intentional, accessible, and cohesive. This skill is a condensed local guide inspired by Emil Kowalski's public design-engineering writing and skill: https://github.com/emilkowalski/skill.

## Reference Map

- `references/animation-vocabulary.md`: prompt-ready vocabulary from https://animations.dev/vocabulary for animation patterns, timing, easing, springs, interaction feedback, performance, and reduced-motion constraints. Read this before adding, tuning, or reviewing motion; use its terms to turn vague animation asks into a concrete motion spec.
- `examples/animation-showcase-*.html`: standalone, browser-runnable examples for staggered entrance, continuity transition, scroll-driven reveal, spring drag/rubber-banding, and line drawing with number ticker. Open these when the user wants examples, asks for motion inspiration, or needs a concrete implementation pattern to adapt.

## Workflow

1. Inspect the existing UI patterns before changing code: framework, component library, animation library, design tokens, accessibility helpers, and current transition conventions.
2. Decide whether motion should exist before tuning it. Remove or reduce animation for high-frequency actions, keyboard-driven flows, dense work surfaces, or anything that blocks repeated use.
3. Read `references/animation-vocabulary.md` when any animation or motion quality matters. Restate the request with the exact vocabulary: purpose, pattern, timing, easing or spring physics, spatial rules, feedback behavior, performance constraints, and reduced-motion fallback.
4. State the purpose of each animation in implementation terms: spatial continuity, state feedback, explanation, confirmation, or making an otherwise abrupt state change legible.
5. Prefer the project's existing primitives. Use CSS transitions for predictable state changes, CSS animations for predetermined non-interactive motion, spring animation for gesture-driven or interruptible motion, and WAAPI when JavaScript control is needed with browser-native animation behavior.
6. Verify visually after editing. Slow animations down temporarily, test reduced-motion behavior, and check representative desktop and mobile viewports.

## Vocabulary Contract

Do not implement from a vague direction like "make it smoother," "make it pop," or "add some animation." Translate it first:

- Purpose: orientation, feedback, continuity, confirmation, reveal, or perceived performance.
- Pattern: fade, slide, scale, pop, reveal, crossfade, continuity transition, layout animation, origin-aware overlay, direction-aware transition, press feedback, drag, swipe, hold to confirm, number ticker, shimmer, or another named pattern from `references/animation-vocabulary.md`.
- Timing and orchestration: duration, delay, stagger, keyframes, fill mode, interruptibility, loop behavior, or scroll linkage.
- Easing or physics: ease-out, ease-in-out, cubic-bezier token, spring stiffness, damping, mass, velocity, momentum, or bounce.
- Spatial and interaction rules: transform origin, direction, anchor, pointer capture, cancellation, velocity thresholds, focus and keyboard behavior.
- Constraints: transform/opacity preference, no `transition: all`, no layout thrashing unless layout animation is intentional, reduced motion behavior, and browser/device validation.

## Examples

Use `examples/*.html` as compact implementation references. They are standalone files with inline CSS and JavaScript, shared navigation, motion specs embedded in the page, focus states, reduced-motion handling, and desktop/mobile layout checks.

- `examples/animation-showcase-01-staggered-entrance.html`: fade, slide, scale, pop-in, short stagger, replay button, and transform/opacity-only entrance.
- `examples/animation-showcase-02-continuity-layout.html`: continuity transition, shared-element-style traveling mark, layout change, state copy crossfade, and active selection state.
- `examples/animation-showcase-03-scroll-reveal-parallax.html`: scroll-driven animation, parallax, route line drawing, scroll reveal, and `requestAnimationFrame`-throttled scroll updates.
- `examples/animation-showcase-04-spring-drag-rubberband.html`: drag, pointer capture, rubber-banding, momentum, interruptible spring return, and animation-loop cleanup at rest.
- `examples/animation-showcase-05-line-drawing-number-ticker.html`: SVG line drawing, path-synchronized checkpoint reveal, tabular number ticker, replay, and reduced-motion final state.

When adapting an example, keep the motion contract visible in implementation terms: purpose, pattern, timing, easing or physics, spatial rule, feedback behavior, performance constraint, and reduced-motion fallback. Do not copy the styling wholesale when a project has its own design system.

## Motion Decisions

- Do not animate keyboard shortcuts, command palette toggles, or actions users may trigger dozens of times in a session.
- Keep normal UI motion under 300ms. Use roughly 100-160ms for press feedback, 125-200ms for tooltips and compact popovers, 150-250ms for menus/selects, and 200-500ms only for larger surfaces like drawers or dialogs.
- Use easing that responds immediately. Prefer `ease-out` for enter/exit and feedback, `ease-in-out` for movement between visible states, `ease` for subtle color/hover changes, and `linear` for constant motion.
- Avoid `ease-in` for normal UI feedback because the slow start makes the interface feel late.
- Use custom curves when the project already supports tokens. Good defaults:

```css
--ease-out-ui: cubic-bezier(0.23, 1, 0.32, 1);
--ease-in-out-ui: cubic-bezier(0.77, 0, 0.175, 1);
--ease-drawer-ui: cubic-bezier(0.32, 0.72, 0, 1);
```

## Component Rules

- Add subtle press feedback to clickable controls when it fits the design system: `transform: scale(0.97)` with a short transform transition.
- Specify transition properties directly. Avoid `transition: all`.
- Animate transform and opacity by default. Avoid animating layout properties unless the layout change itself is the point and performance is acceptable.
- Do not enter from `scale(0)`. Start around `scale(0.95)` with opacity so the element has visual continuity.
- Make anchored overlays origin-aware. Popovers, menus, and tooltips should scale from the trigger side when the library exposes a transform-origin variable. Keep centered dialogs centered.
- Gate hover-only motion behind `@media (hover: hover) and (pointer: fine)` so touch devices do not get stuck in hover-like states.
- Use short stagger delays, around 30-80ms, only for decorative group entry. Never block interaction until staggered items finish.
- Prefer percentage translates for offscreen entry/exit when movement should be relative to the element's own size.
- For toolbars with adjacent tooltips, preserve the initial delay but make subsequent tooltips instant once the tooltip layer is already active.

## Concrete Patterns

Use these as starting points, then adapt names, tokens, and selectors to the project.

### Pressable Controls

```css
.action-button {
  transition: transform 140ms var(--ease-out-ui), background-color 140ms ease;
}

.action-button:active {
  transform: scale(0.97);
}

@media (hover: hover) and (pointer: fine) {
  .action-button:hover {
    transform: translateY(-1px);
  }

  .action-button:hover:active {
    transform: scale(0.97);
  }
}
```

### Anchored Overlays

```css
.menu-content {
  opacity: 1;
  transform: translateY(0) scale(1);
  transform-origin: var(--radix-dropdown-menu-content-transform-origin, center);
  transition:
    opacity 150ms var(--ease-out-ui),
    transform 150ms var(--ease-out-ui);

  @starting-style {
    opacity: 0;
    transform: translateY(-2px) scale(0.96);
  }
}

@media (prefers-reduced-motion: reduce) {
  .menu-content {
    transform: none;
    transition: opacity 120ms ease;
  }
}
```

Use the component library's transform-origin variable when available. Keep dialogs centered unless they are visually anchored to a trigger.

### Hold-To-Confirm

```css
.danger-action {
  position: relative;
  overflow: hidden;
  transition: transform 140ms var(--ease-out-ui);
}

.danger-action::before {
  content: "";
  position: absolute;
  inset: 0;
  background: color-mix(in srgb, currentColor 16%, transparent);
  clip-path: inset(0 100% 0 0);
  transition: clip-path 180ms var(--ease-out-ui);
}

.danger-action:active {
  transform: scale(0.97);
}

.danger-action:active::before {
  clip-path: inset(0 0 0 0);
  transition: clip-path 1800ms linear;
}
```

Pair this visual progress with real pointer/keyboard logic. Cancel the action on `pointerup`, `pointercancel`, `blur`, or `Escape`; do not make destructive behavior depend on CSS alone.

### Swipe Dismissal

```ts
const elapsedMs = Math.max(performance.now() - dragStartedAt, 1);
const velocityPxPerMs = Math.abs(offsetPx) / elapsedMs;
const passedDistance = Math.abs(offsetPx) > dismissDistancePx;
const flickedFastEnough = velocityPxPerMs > 0.12;

if (passedDistance || flickedFastEnough) {
  dismiss();
} else {
  restore();
}
```

During drag, update the dragged element directly:

```ts
node.style.transform = `translate3d(0, ${offsetPx}px, 0)`;
```

Prefer this over inherited CSS variables on a large parent subtree when the value changes every frame.

### Staggered Entry

```css
.result-row {
  animation: result-enter 220ms var(--ease-out-ui) both;
  animation-delay: calc(var(--row-index) * 45ms);
}

@keyframes result-enter {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@media (prefers-reduced-motion: reduce) {
  .result-row {
    animation: none;
  }
}
```

Use short stagger only for decorative entry. The list should be readable and interactive immediately.

### State Swap Crossfades

```css
.button-label {
  transition: opacity 180ms ease, filter 180ms ease;
}

.button-label[data-swapping="true"] {
  opacity: 0.7;
  filter: blur(1.5px);
}
```

Use blur sparingly to soften state swaps where two labels or icons briefly overlap. Keep the blur small and remove it under reduced motion if the result feels smeared.

## Gestures

- Use pointer capture once dragging starts so the interaction continues even if the pointer leaves the element.
- Protect active drags from extra touch points.
- Use velocity as well as distance for swipe dismissal so a deliberate flick can complete the action.
- Apply damping or friction beyond natural boundaries instead of hard stops.
- Use springs for gestures that can reverse or be interrupted. Keep bounce subtle unless the product is intentionally playful.

## Performance And Accessibility

- Respect `prefers-reduced-motion`. Reduce position and transform motion first; keep brief opacity or color transitions when they aid comprehension.
- Avoid per-frame JavaScript animation for predictable effects during page loads or heavy work. Prefer CSS animation/transition where the target is known.
- Be cautious with inherited CSS variables in large subtrees during drag interactions; direct element transforms are often cheaper.
- Keep blur small and rare. It can smooth crossfades, but heavy filters are expensive, especially in Safari.
- Test touch gestures on a real device when possible. Use a simulator only as a fallback.

## Review Format

When reviewing UI code, lead with concrete findings. If the feedback is about motion or interaction polish, prefer a Markdown table:

| Before | After | Why |
| --- | --- | --- |
| `transition: all 300ms` | `transition: transform 180ms var(--ease-out-ui)` | Limit the animated property and make feedback immediate |

For implementation tasks, make the code change directly and mention the relevant verification. Do not force the table format when a short prose summary is clearer.

## Checklist

- Check for `transition: all`.
- Check for `ease-in` on interactive UI.
- Check for durations over 300ms on routine UI.
- Check for keyboard-triggered animations.
- Check popover/menu/tooltip transform origin.
- Check whether vague animation language has been translated into the vocabulary contract.
- Check hover effects on touch devices.
- Check missing active states on pressable controls.
- Check transform or opacity alternatives before layout animation.
- Check reduced-motion behavior.
- Check destructive hold-to-confirm flows for cancellation and keyboard access.
- Check drag interactions for pointer capture, velocity, damping, and direct transform updates.
- Check whether the motion style matches the product's tone: crisp for work tools, more expressive only where the domain supports it.
