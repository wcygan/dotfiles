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
- `references/react-mdx-deno-tanstack.md`: prerender-safe React/MDX embedding for Deno and TanStack Start blogs.
- `references/overlays-controls-accessibility.md`: labels, sliders, scrubbers, DOM/SVG overlays, keyboard support, reduced motion, and semantics.
- `references/performance-testing.md`: resize, device pixels, profiling, browser verification, screenshots, and visual regressions.
- `references/creator-patterns.md`: creator examples and what to study without copying source or prose.
- `examples/gear-ratio-canvas.html`: standalone Canvas 2D gear-ratio demo with inline CSS and JavaScript.

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
6. Verify the runtime lifecycle: resize, pause, cleanup, reduced motion, mobile pointer input, and prerender/static build behavior.

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

Keep time-driven animation optional. Sliders and scroll/scrub state should be able to set the model directly so the article remains inspectable frame by frame.

## Examples

Use `examples/*.html` as runnable teaching artifacts. They are intentionally standalone HTML files with inline CSS and JavaScript so they can be opened directly, inspected without a build step, and adapted into React/MDX components later.

## First Demo Ladder

For mechanical or spatial posts, build in this order:

1. Draw a static diagram with correct world coordinates.
2. Add one slider mapped to one model parameter.
3. Add derived labels that update from the same model.
4. Add play/pause with `requestAnimationFrame`.
5. Add scrub mode so prose can point at exact states.
6. Add force vectors, traces, ghost positions, or overlays only after the core motion is correct.
7. Verify desktop and mobile layout, reduced motion, and static build output.

## Quality Bar

- Do not fake physics with arbitrary easing when the article claims a mechanical or physical relationship. Use formulas, constraints, or clearly labeled illustrative motion.
- Prefer readable math and named intermediate values over compressed vector cleverness.
- Keep controls close to the visual they affect.
- Make default states useful: the first frame should explain something even before interaction.
- Use color semantically and consistently; include labels or legends for non-obvious mappings.
- Do not copy large source files, article prose, or distinctive visual assets from example creators. Study patterns, summarize, and link.

## Validation

Use the narrowest checks available:

- Type/model changes: run the repo's typecheck or tests.
- Deno/TanStack blog posts: default to `deno task build`; use `deno task preview-static` or the app's preview command for rendered verification.
- Visual work: inspect in browser at desktop and mobile widths; check canvas is nonblank, correctly sized, and interactive.
- Three.js/WebGL: verify the canvas has nonzero pixels, camera framing is correct, resize works, and no console WebGL errors appear.
