---
name: interactive-graphics-demos
description: "Design, build, review, or debug article-embedded interactive graphics demos: Canvas 2D, SVG, WebGL/Three.js, mechanical/spatial simulations, physics explainers, sliders, scrubbers, requestAnimationFrame loops, React/MDX embeds, and Deno/TanStack Start prerender-safe blog integrations. Use when Codex needs to create Bartosz Ciechanowski-style visual explanations, live model-driven diagrams, or custom graphics engines for blog posts."
---

# Interactive Graphics Demos

Build model-driven visual explanations for articles. Treat each demo as a small graphics system: domain model, renderer, controls, lifecycle, and article integration.

Success means the demo explains one concept clearly, runs as a live model rather than a video, uses explicit animation vocabulary when motion matters, respects the host page's render/runtime constraints, and has a narrow validation path.

## Reference Map

- `references/animation-vocabulary.md`: prompt-ready vocabulary for animation patterns, timing, easing, springs, interaction feedback, performance, and reduced-motion constraints. Read this before adding or reviewing motion; use its terms to restate vague animation asks into a concrete motion spec.
- `references/canvas-2d.md`: Canvas 2D renderer structure, drawing order, transforms, hit testing, and common primitives.
- `references/animation-loop.md`: `requestAnimationFrame`, fixed/variable timestep choices, play/pause/scrub behavior, and cleanup.
- `references/spatial-math.md`: vectors, coordinate spaces, transforms, curves, projections, and mechanical geometry.
- `references/webgl-threejs.md`: when to use WebGL or Three.js, scene structure, camera controls, labels, and bundle boundaries.
- `references/simulation-physics.md`: deterministic models, constraints, springs, collisions, numerical integration, and library selection.
- `references/software-diagram-demos.md`: distributed systems, protocol, storage, routing, quorum, log, and state-machine diagram patterns.
- `references/react-mdx-deno-tanstack.md`: prerender-safe React/MDX embedding for Deno and TanStack Start blogs.
- `references/overlays-controls-accessibility.md`: labels, sliders, scrubbers, DOM/SVG overlays, keyboard support, reduced motion, and semantics.
- `references/performance-testing.md`: resize, device pixels, profiling, browser verification, screenshots, and visual regressions.
- `references/creator-patterns.md`: creator examples and what to study without copying source or prose.
- `examples/gear-ratio-canvas.html`: standalone Canvas 2D gear-ratio demo with inline CSS and JavaScript.
- `examples/optics-pinhole-camera-canvas.html`: pinhole camera ray diagram with aperture, projection, and magnification controls.
- `examples/orbital-transfer-canvas.html`: orbital transfer diagram with circular orbits, transfer ellipse, scrubber, and velocity vector.
- `examples/wave-interference-canvas.html`: two-source wave interference field with wavelength, phase, spacing, and probe controls.
- `examples/consistent-hashing-ring-canvas.html`: distributed partitioning demo with virtual node tokens, key ownership, load skew, and key movement.
- `examples/quorum-replication-canvas.html`: tunable quorum demo showing write acknowledgments, read responses, failures, and quorum intersection.
- `examples/raft-log-replication-canvas.html`: replicated log demo showing leader append, follower match indexes, majority, and commit advancement.

## Workflow

1. Inspect the article and repo context first: framework, MDX pipeline, existing demo components, CSS constraints, build commands, and browser verification path.
2. Name the concept being explained in one sentence. If the concept cannot be stated narrowly, split it into smaller demos.
3. Choose the representation before the renderer. Name the visual form that makes the concept easiest to inspect: inline annotated figure, timeline, log, ring, map, field, small multiples, state table, direct-manipulation scene, instrument panel, or another concept-specific shape.
4. If motion is involved, read `references/animation-vocabulary.md` and name the animation vocabulary before coding: purpose, pattern, timing, easing or physics, spatial rules, feedback behavior, performance constraints, and reduced-motion fallback. Do not proceed from "make it smooth" or "make it animated" without translating it into a motion spec.
5. Choose the renderer:
   - Canvas 2D for most mechanical, geometric, ray, chart-like, and annotated 2D systems.
   - SVG for mostly static vector diagrams, selectable labels, and low-element-count state diagrams.
   - Canvas or WebGL plus DOM/SVG overlays for dense visuals with readable labels and controls.
   - Three.js for 3D objects, cameras, lighting, depth, rotations, spatial mechanisms, or many mesh instances.
   - A physics library only when the simulation needs collisions, rigid bodies, joints, or constraint solving beyond a few formulas.
6. Design the model before drawing. Keep parameters, derived values, and simulation state separate from rendering details.
7. Build a tiny vertical slice: static render, then one controlled parameter, then animation, then labels and polish.
8. For software diagrams, identify the invariant and keep ownership, quorum, message, or commit truth in derived model state before styling it.
9. Verify the runtime lifecycle: resize, pause, cleanup, reduced motion, mobile pointer input, and prerender/static build behavior.

## Implementation Shape

For blog embeds with real behavior, prefer a React shell plus plain TypeScript engine:

```text
src/components/GearTrainDemo.tsx
src/demos/gears/model.ts
src/demos/gears/render-canvas.ts
src/demos/gears/viewport.ts
src/demos/gears/input.ts
```

Use this boundary:

- React owns markup, controls, article layout, accessibility text, and lifecycle.
- The engine owns state, math, rendering, pointer mapping, and animation timing.
- The model is deterministic and testable without a canvas when practical.
- The renderer reads state; it should not be the source of truth.

Scale this file shape to the demo. Keep a small static SVG or simple single-state figure in one component when the boundary would add ceremony. Split into `model`, `render`, `viewport`, and `input` modules when the demo has animation, pointer input, reusable math, or meaningful state transitions.

For prerendered React sites, never access `window`, `document`, canvas contexts, WebGL contexts, or `matchMedia` at module top level. Start them inside an effect and clean them up.

```tsx
export function GearTrainDemo() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const demo = createGearTrainDemo(canvas);
    demo.start();
    return () => demo.destroy();
  }, []);

  return <canvas ref={canvasRef} aria-label="Interactive gear train demo" />;
}
```

## Model Pattern

Use explicit state and derived values:

```ts
type DemoState = {
  inputAngle: number;
  inputTeeth: number;
  outputTeeth: number;
  playing: boolean;
  showForces: boolean;
};

function deriveGearTrain(state: DemoState) {
  const ratio = state.inputTeeth / state.outputTeeth;
  return {
    ratio,
    outputAngle: -state.inputAngle * ratio,
  };
}
```

Keep time-driven animation optional. When a demo does include playback, it should be running by default so the reader immediately sees that it is live. Sliders and scroll/scrub state should be able to set the model directly so the article remains inspectable frame by frame.

## Examples

Use `examples/*.html` as runnable teaching artifacts. They are intentionally standalone HTML files with inline CSS and JavaScript so they can be opened directly, inspected without a build step, and adapted into React/MDX components later.

## Visual Direction

Goal: Give each concept the visual form that makes its model easiest to inspect.

Success means:

- The representation choice is named before layout or styling starts.
- Existing examples provide reusable vocabulary: palette, control feel, label density, and model/render boundaries.
- The final composition fits the concept, article position, and interaction model.

Stop when the demo's renderer, layout, controls, and framing all follow from the concept sentence and model invariant.

Use the example demos as a pattern library. Select only the pieces that serve the current concept:

- Start from the shared palette when it supports the subject: ink `#172033`, muted text `#5c667a`, line `#d9deea`, page background `#eef1f7`, canvas/panel white `#ffffff`, primary blue `#2f69f0`, semantic red `#d24a44`, probe/highlight gold `#d59b24`, and success/available green `#1d8b65`.
- Map colors semantically and consistently: blue for primary action, selected state, positive direction, or source A; red for negative direction, conflict, failure, or source B; gold for probes, highlighted paths, moving handles, or active focus; green for healthy, available, committed, or successful state. Add a legend when color carries meaning.
- Choose the page shape from the concept: inline figure, narrow annotated sketch, full-width stage, tall mobile-first sequence, small multiples, side-by-side comparison, instrument panel, ring, timeline, log, table, map, or freeform canvas.
- Use a framed panel when the demo reads as a contained instrument or figure. Use an unframed, inline, edge-to-edge, or prose-integrated composition when that makes the relationship clearer.
- Place controls where the reader needs them: beside the stage for parameter-heavy instruments, directly under the mark for scrubbers, inline with prose for sentence-level exploration, or hidden behind presets when interaction would distract from the invariant.
- Style controls like the examples when the site has no stronger local primitive: primary buttons in blue, secondary buttons on white, range and checkbox accents in blue, focus rings using translucent blue, and short transform/color transitions using `--ease-out-ui: cubic-bezier(0.23, 1, 0.32, 1)`.
- Render metrics and legends as quiet supporting UI: translucent white overlays, compact labels, muted legends with circular swatches, and labels placed near the marks they explain.
- When adapting a standalone demo into a website, map these values onto the site tokens and component primitives while preserving semantic color roles, readable spacing, and the chosen concept-specific composition.

## First Demo Ladder

For mechanical or spatial posts, build in this order:

1. Draw a static diagram with correct world coordinates.
2. Add one slider mapped to one model parameter.
3. Add derived labels that update from the same model.
4. Add play/pause with `requestAnimationFrame`.
5. Add scrub mode so prose can point at exact states.
6. Add force vectors, traces, ghost positions, or overlays only after the core motion is correct.
7. Verify desktop and mobile layout, reduced motion, and static build output.

For software protocol or state-machine diagrams, build in this order:

1. State the invariant the frame should teach.
2. Draw the static topology: nodes, rings, replicas, logs, clients, queues, or partitions.
3. Add derived model state: ownership, quorum overlap, message lifecycle, commit index, or failure status.
4. Map semantic color from the model to marks, labels, legends, and metrics.
5. Add ports and named geometry constants before drawing connectors or arrows.
6. Add animation or scrubbed time only after the static states are correct.
7. Verify representative semantic cases, not just the default frame.

## Quality Bar

- Do not fake physics with arbitrary easing when the article claims a mechanical or physical relationship. Use formulas, constraints, or clearly labeled illustrative motion.
- Use animation vocabulary as an implementation contract: state the purpose, named pattern, timing/orchestration, easing or physics, spatial continuity rule, interaction feedback, performance target, and reduced-motion behavior.
- Prefer readable math and named intermediate values over compressed vector cleverness.
- Keep controls close to the visual they affect.
- Make default states useful: the first frame should explain something even before interaction.
- Live demos should start playing by default, with pause, step, scrub, and reset controls available.
- Use color semantically and consistently; include labels or legends for non-obvious mappings.
- Connectors, arrows, and selected paths must be built from shared geometry or named ports, not eyeballed offsets.
- Begin new demos and meaningful revisions with a short representation note: concept, invariant, visual form, renderer, controls, layout, and validation path.
- Study creator patterns, summarize the parts you use, and write original code, prose, and visual assets.

## Validation

Use the narrowest checks available:

- Type/model changes: run the repo's typecheck or tests.
- Deno/TanStack blog posts: default to `deno task build`; use `deno task preview-static` or the app's preview command for rendered verification.
- Visual work: inspect in browser at desktop and mobile widths; check canvas is nonblank, correctly sized, and interactive.
- Three.js/WebGL: verify the canvas has nonzero pixels, camera framing is correct, resize works, and no console WebGL errors appear.
