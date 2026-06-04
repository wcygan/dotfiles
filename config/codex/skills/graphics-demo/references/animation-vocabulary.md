# Animation Vocabulary For LLM Prompts

Source: https://animations.dev/vocabulary

Use this reference when a graphics demo includes motion, animated state changes, interactive feedback, scroll-linked effects, or animation review. The source page's practical lesson is that LLMs produce better animation work when the prompt uses specific motion vocabulary instead of vague requests such as "make it smooth" or "add animation."

## Default Motion Spec

Before implementation, translate the request into a compact motion spec:

- Purpose: orient the reader, show causality, preserve spatial continuity, confirm input, reveal hidden structure, or improve perceived performance.
- Pattern: name the animation family, such as reveal, stagger, continuity transition, shared element transition, stepped animation, drag, hold to confirm, number ticker, line drawing, pulse, orbit, or idle animation.
- Timing: specify duration, delay, stagger, fill mode, keyframes, and whether playback is continuous, scrubbed, stepped, or tied to scroll.
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

## Demo-Specific Guidance

- For article explainers, prefer motion that exposes the model: stepped animation, scrubbed time, line drawing, continuity transition, number ticker, or state-table updates usually beat decorative entrances.
- For protocol, storage, or distributed-system diagrams, connect packets, arrows, progress bars, logs, and counters to model state. Do not animate approximate motion that contradicts ownership, quorum, message, or commit truth.
- For mechanical or spatial demos, make the transformation vocabulary match the claimed physics. If a spring, collision, orbit, or momentum is part of the explanation, model it or label it as illustrative.
- For timelines and state machines, use orchestration deliberately: name the sequence, the active state, what waits, and what updates together.
- For live loops, specify whether the loop is linear, yoyo, orbiting, pulsing, floating, or idle. Ambient loops should be subtle and must not compete with the teaching invariant.

## Prompt Shapes

Use prompts like:

```text
Animate this as a continuity transition: the selected replica keeps its identity while moving from the ring to the detail panel. Use 220ms ease-in-out, preserve its color and label, and disable transform motion under prefers-reduced-motion.
```

```text
Use a stepped animation for the write path: client request, leader append, follower acks, quorum reached, commit index advances. Each step should update the log table and connector highlight from the same model state.
```

```text
Add press feedback to the filter buttons: 120ms ease-out scale to 0.97 on active, hover lift only on fine pointers, and no transition: all.
```

## Anti-Patterns

- Do not accept "make it more animated" as the final spec. Restate it with purpose, pattern, timing, easing or physics, and validation.
- Do not add scroll reveal, parallax, pop-in, or ambient motion when the demo's job is dense comparison or repeated operation.
- Do not animate width, height, top, or left every frame unless layout animation is the actual lesson and performance has been checked.
- Do not let transitions hide state truth. Motion should make the model easier to inspect, not smooth over missing states.
- Do not forget reduced motion. Preserve essential orientation with simpler opacity, color, or instant state changes when needed.
