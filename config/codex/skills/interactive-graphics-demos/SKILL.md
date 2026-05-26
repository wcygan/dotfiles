---
name: interactive-graphics-demos
description: "Design, build, review, or debug article-embedded interactive graphics demos: Canvas 2D, SVG, WebGL/Three.js, mechanical/spatial simulations, physics explainers, sliders, scrubbers, requestAnimationFrame loops, React/MDX embeds, and Deno/TanStack Start prerender-safe blog integrations. Use when Codex needs to create Bartosz Ciechanowski-style visual explanations, live model-driven diagrams, or custom graphics engines for blog posts."
---

# Interactive Graphics Demos

Build model-driven visual explanations for articles. Treat each demo as a small graphics system: domain model, renderer, controls, lifecycle, and article integration.

Success means the demo explains one concept clearly, runs as a live model rather than a video, respects the host page's render/runtime constraints, and has a narrow validation path.

## Reference Map

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
3. Choose the renderer:
   - Canvas 2D for most mechanical, geometric, ray, chart-like, and annotated 2D systems.
   - SVG for mostly static vector diagrams, selectable labels, and low-element-count state diagrams.
   - Canvas or WebGL plus DOM/SVG overlays for dense visuals with readable labels and controls.
   - Three.js for 3D objects, cameras, lighting, depth, rotations, spatial mechanisms, or many mesh instances.
   - A physics library only when the simulation needs collisions, rigid bodies, joints, or constraint solving beyond a few formulas.
4. Design the model before drawing. Keep parameters, derived values, and simulation state separate from rendering details.
5. Build a tiny vertical slice: static render, then one controlled parameter, then animation, then labels and polish.
6. For software diagrams, identify the invariant and keep ownership, quorum, message, or commit truth in derived model state before styling it.
7. Verify the runtime lifecycle: resize, pause, cleanup, reduced motion, mobile pointer input, and prerender/static build behavior.

## Implementation Shape

Prefer a React shell plus plain TypeScript engine for blog embeds:

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

## Visual Design System

Use the example demos as the default visual system for new standalone artifacts and website embeds:

- Start from the shared palette: ink `#172033`, muted text `#5c667a`, line `#d9deea`, page background `#eef1f7`, canvas/panel white `#ffffff`, primary blue `#2f69f0`, semantic red `#d24a44`, probe/highlight gold `#d59b24`, and success/available green `#1d8b65`.
- Map colors semantically and consistently: blue for primary action, selected state, positive direction, or source A; red for negative direction, conflict, failure, or source B; gold for probes, highlighted paths, moving handles, or active focus; green for healthy, available, committed, or successful state. Add a legend when color carries meaning.
- Use the common page shell for standalone examples: Inter/system font stack, constrained `main` width around `min(1100px, calc(100vw - 32px))`, compact headings, muted explanatory copy, and a reusable demo nav with the active page in ink.
- Frame demos with the established panel treatment: 1px `--line` border, radius up to 8px, white surfaces, subtle shadows such as `0 12px 34px rgb(23 32 51 / 8%)`, and single-level cards reserved for metric tiles, controls, modals, or repeated items.
- Keep the default layout pattern: a responsive two-column demo area with `minmax(0, 1fr)` stage plus roughly `310px` controls, `16px` gaps, one-column layout below tablet widths, and stable min heights for canvas stages.
- Style controls like the examples: primary buttons in blue, secondary buttons on white, range and checkbox accents in blue, focus rings using translucent blue, and short transform/color transitions using `--ease-out-ui: cubic-bezier(0.23, 1, 0.32, 1)`.
- Render metrics and legends as quiet supporting UI: translucent white metric overlays with compact labels, muted legends with circular swatches, and labels placed near the marks they explain.
- When adapting a standalone demo into the website, map these values onto the site tokens and component primitives while preserving the same visual hierarchy, semantic color roles, spacing rhythm, and control behavior.

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
- Prefer readable math and named intermediate values over compressed vector cleverness.
- Keep controls close to the visual they affect.
- Make default states useful: the first frame should explain something even before interaction.
- Live demos should start playing by default, with pause, step, scrub, and reset controls available.
- Use color semantically and consistently; include labels or legends for non-obvious mappings.
- Connectors, arrows, and selected paths must be built from shared geometry or named ports, not eyeballed offsets.
- Do not copy large source files, article prose, or distinctive visual assets from example creators. Study patterns, summarize, and link.

## Validation

Use the narrowest checks available:

- Type/model changes: run the repo's typecheck or tests.
- Deno/TanStack blog posts: default to `deno task build`; use `deno task preview-static` or the app's preview command for rendered verification.
- Visual work: inspect in browser at desktop and mobile widths; check canvas is nonblank, correctly sized, and interactive.
- Three.js/WebGL: verify the canvas has nonzero pixels, camera framing is correct, resize works, and no console WebGL errors appear.
