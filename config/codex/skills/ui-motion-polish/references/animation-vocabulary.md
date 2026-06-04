# Animation Vocabulary For LLM Prompts

Source: https://animations.dev/vocabulary

Use this reference when a UI includes motion, animated state changes, interactive feedback, scroll-linked effects, or animation review. The source page's practical lesson is that LLMs produce better animation work when the prompt uses specific motion vocabulary instead of vague requests such as "make it smooth" or "add animation."

## Default Motion Spec

Before implementation, translate the request into a compact motion spec:

- Purpose: orient the user, preserve spatial continuity, confirm input, reveal hidden structure, show relationship, or improve perceived performance.
- Pattern: name the animation family, such as reveal, stagger, continuity transition, shared element transition, layout animation, direction-aware transition, press feedback, drag, swipe to dismiss, hold to confirm, number ticker, pulse, or idle animation.
- Timing: specify duration, delay, stagger, fill mode, keyframes, and whether playback is one-shot, continuous, interruptible, scrubbed, or tied to scroll.
- Easing or physics: choose ease-out for responsive feedback, ease-in-out for visible state-to-state movement, linear only for constant loops, or a spring with stiffness, damping, mass, velocity, and interruptibility when gesture motion needs physics.
- Spatial rules: specify translate, scale, rotate, transform origin, origin-aware growth, direction-aware navigation, perspective, or 3D tilt when position and identity matter.
- Feedback rules: define hover, press, tap, drag, swipe, rubber-banding, shake, ripple, or cancellation behavior in terms of actual user actions.
- Constraints: include reduced motion, transform/opacity first, no layout thrashing, no blocking high-frequency workflows, and the expected browser/mobile validation.

## Vocabulary Buckets

Reach for the smallest vocabulary that describes the intended behavior:

- Entrances and exits: fade, slide, scale, pop, reveal, enter, exit.
- Sequencing and timing: keyframes, interpolation, stagger, orchestration, delay, duration, fill mode, stepped animation.
- Movement and transforms: translate, scale, rotate, skew, 3D tilt, flip, perspective, transform origin, origin-aware animation.
- State transitions: crossfade, continuity transition, morph, shared element transition, layout animation, accordion or collapse, direction-aware transition.
- Scroll and navigation: scroll reveal, scroll-driven animation, parallax, page transition, view transition.
- Feedback and interaction: hover effect, press or tap feedback, hold to confirm, drag, drag to reorder, swipe to dismiss, rubber-banding, shake or wiggle, ripple.
- Easing: ease-out, ease-in, ease-in-out, linear, cubic-bezier, asymmetric easing.
- Springs: stiffness or tension, damping, mass, bounce, perceptual duration, momentum, velocity, interruptible animation.
- Looping and ambient motion: marquee, loop, alternate or yoyo, orbit, pulse, float, idle animation.
- Polish effects: blur, clip-path, mask, before/after slider, line drawing, text morph, skeleton or shimmer, number ticker, tabular numbers, typewriter.
- Performance: frame rate, jank, dropped frames, compositing, will-change, layout thrashing.
- Principles: purposeful animation, anticipation, follow-through, squash and stretch, perceived performance, frequency of use, spatial consistency, hardware acceleration, reduced motion.

## UI-Specific Guidance

- For routine controls, use concrete feedback vocabulary: press feedback, hover effect, focus state, ripple, or hold to confirm. Keep it short and cancellable.
- For overlays, use origin-aware animation so menus, popovers, and tooltips grow from the trigger side when the component library exposes a transform-origin variable.
- For navigation, use direction-aware transitions or shared element transitions only when they preserve orientation. Avoid decorative page motion for high-frequency work surfaces.
- For counters, timers, and values, pair number ticker with tabular numbers so changing digits do not shift layout.
- For drag and swipe, specify momentum, velocity, damping, rubber-banding, and interruptibility. Do not tune only duration.
- For loading UI, skeleton, shimmer, and perceived performance are acceptable when they make waiting legible without pretending work finished earlier.

## Prompt Shapes

Use prompts like:

```text
Make the dropdown origin-aware: 150ms ease-out opacity plus translateY(-2px) and scale(0.96) from the Radix transform-origin variable. Under reduced motion, keep opacity only.
```

```text
Use interruptible spring motion for the drawer drag: preserve velocity on release, add light damping near the boundary, and dismiss on distance or flick velocity.
```

```text
Add press feedback to the filter buttons: 120ms ease-out scale to 0.97 on active, hover lift only on fine pointers, and no transition: all.
```

## Anti-Patterns

- Do not accept "make it more animated" as the final spec. Restate it with purpose, pattern, timing, easing or physics, and validation.
- Do not add scroll reveal, parallax, pop-in, or ambient motion when the interface is a dense work surface or the user repeats the action often.
- Do not animate width, height, top, or left every frame unless layout animation is the actual feature and performance has been checked.
- Do not make destructive confirmation depend on CSS alone. Pair hold-to-confirm visuals with real pointer, keyboard, blur, and cancel logic.
- Do not forget reduced motion. Preserve essential orientation with simpler opacity, color, or instant state changes when needed.
