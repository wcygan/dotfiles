---
name: graphics-demo
description: "Design, build, review, or debug article and web demos across the full range from static to live: semantic HTML/CSS layouts, responsive components, design systems, Grid/Flexbox, accessibility AND interactive Canvas 2D, SVG, WebGL/Three.js, physics/mechanical simulations, sliders, scrubbers, requestAnimationFrame loops, React/MDX/Deno/TanStack embeds. Use when building a non-interactive figure or page layout, a live model-driven explainer (Bartosz Ciechanowski style), or anything between. Keywords: demo, graphics, canvas, WebGL, Three.js, animation, simulation, HTML, CSS, layout, Grid, Flexbox, semantic markup, responsive, accessibility, interactive explainer."
---

# Graphics Demo

Build demos that explain one idea clearly, from a static semantic figure to a live model-driven simulation. Treat markup, layout, model, rendering, and interaction states as separate decisions, and reach for the simplest tier that makes the concept inspectable.

Success means:
- The concept is named in one sentence before any layout, markup, or renderer is chosen.
- The demo uses the lowest-complexity tier that still conveys the idea (static HTML/CSS before canvas, canvas before WebGL).
- Motion requests use explicit vocabulary from `references/animation-vocabulary.md`: purpose, pattern, timing, easing or physics, spatial rules, interaction feedback, performance, and reduced-motion constraints.
- HTML expresses meaning before visual structure; interactive demos keep model state separate from rendering.
- Components own their internal styling; parents own placement.
- The work respects the host page's render/runtime constraints (especially prerender-safe React) and has a narrow validation path.

## Pick the Tier First

Choose the lowest tier that conveys the concept. Most "demos" only need the first one.

- **Non-interactive (static)** — semantic HTML + CSS: documents, navigation, forms, card lists, dashboards, data tables, component libraries, annotated figures, and any layout the reader does not manipulate. Start here unless the concept genuinely requires motion or direct manipulation.
- **Lightly interactive** — HTML/CSS with native controls and state (`details`/`summary`, hover/focus, `:checked` toggles) before reaching for scripting.
- **Interactive (model-driven)** — Canvas 2D, SVG, WebGL/Three.js, or a simulation when the reader needs to drive a live model: drag, slider, scrub, play/pause, or watch a system evolve over time.

When a concept spans tiers, split it: a static figure to frame the idea, then a live demo for the part that benefits from manipulation.

## Reference Map

### Motion vocabulary
- `references/animation-vocabulary.md`: prompt-ready vocabulary for animation patterns, timing, easing, springs, interaction feedback, performance, and reduced-motion constraints. Read this before adding or reviewing motion; use its terms to restate vague animation asks into a concrete motion spec.
- For UI motion implementation examples, see the sibling `ui-motion-polish` skill's `examples/animation-showcase-*.html` files. Use those for staggered entrances, continuity transitions, scroll-driven reveal, spring drag/rubber-banding, and line drawing/number ticker patterns before inventing a fresh animation surface.

### Non-interactive: HTML & CSS layout
- `references/semantic-html.md`: document structure, sectioning, landmarks, native controls, and when `div` is acceptable.
- `references/layout-grid-flex.md`: choosing normal flow, Grid, Flexbox, alignment, gaps, nesting, and page/component layout split.
- `references/responsive-design.md`: intrinsic responsive layout, media queries, container queries, fluid sizing, and reduced motion.
- `references/css-architecture.md`: cascade, specificity, layers, custom properties, naming, resets, and keeping component CSS maintainable.
- `references/visual-design.md`: spacing, typography, hierarchy, color, density, shadows, borders, and clean design constraints.
- `references/accessibility-states.md`: keyboard paths, focus, labels, forms, landmarks, contrast, target size, and ARIA fallback.
- `references/media-images.md`: images, figures, aspect ratios, object fit, responsive media, and layout stability.
- `references/forms-validation.md`: form structure, labels, field groups, client validation, errors, and submission states.
- `references/tables-data.md`: tabular semantics, captions, header scope, responsive table containers, and data density.
- `references/navigation-disclosure.md`: nav patterns, skip links, details/summary, dialogs, popovers, tabs, and disclosure behavior.
- `references/motion-interaction.md`: CSS transitions, animations, interaction feedback, view transitions, and reduced-motion safeguards.
- `references/debugging-validation.md`: DevTools workflows, layout overlays, computed styles, browser support checks, and validation passes.

### Interactive: model-driven graphics
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

## Examples

Use `examples/*` as runnable teaching artifacts. Each is standalone — open it directly, inspect it without a build step, and adapt it into a component later.

### Non-interactive (HTML/CSS only, shared nav bar)
- `examples/semantic-document.html`: semantic page shell with landmarks, article cards, aside, and footer.
- `examples/grid-dashboard.html`: responsive dashboard shell using CSS Grid, named sections, and stable cards.
- `examples/flex-toolbar.html`: Flexbox toolbar, grouped controls, wrapping filters, and aligned media rows.
- `examples/responsive-cards.html`: intrinsic card gallery with `auto-fit`, `minmax()`, `aspect-ratio`, and readable metadata.
- `examples/form-accessibility.html`: accessible form layout with labels, help text, fieldsets, focus states, and error copy.
- `examples/cascade-tokens.html`: cascade layers, tokens, component variants, and theme-like overrides without specificity fights.
- `examples/media-objects.html`: stable media cards with figures, captions, aspect ratios, and `object-fit`.
- `examples/data-table.html`: accessible table with caption, scoped headers, status chips, and a responsive overflow wrapper.
- `examples/disclosure-navigation.html`: native details/summary disclosure groups, skip link, and section navigation.
- `examples/page-shell.html`: responsive app shell with header, sidebar navigation, main content, and aside regions.
- `examples/motion-states.html`: visible component states, transition tokens, and reduced-motion fallback.
- `examples/debugging-checklist.html`: inspectable layout debugging checklist for overflow, box model, cascade, and responsive checks.
- `examples/demo-styles.css`: shared stylesheet used by the static demos above.

### Interactive (standalone Canvas 2D, inline CSS + JS)
- `examples/gear-ratio-canvas.html`: gear-ratio demo with derived output angle and ratio.
- `examples/optics-pinhole-camera-canvas.html`: pinhole camera ray diagram with aperture, projection, and magnification controls.
- `examples/orbital-transfer-canvas.html`: orbital transfer diagram with circular orbits, transfer ellipse, scrubber, and velocity vector.
- `examples/wave-interference-canvas.html`: two-source wave interference field with wavelength, phase, spacing, and probe controls.
- `examples/consistent-hashing-ring-canvas.html`: partitioning demo with virtual node tokens, key ownership, load skew, and key movement.
- `examples/quorum-replication-canvas.html`: tunable quorum demo showing write acks, read responses, failures, and quorum intersection.
- `examples/raft-log-replication-canvas.html`: replicated log demo showing leader append, follower match indexes, majority, and commit advancement.

## Workflow

1. Inspect the article/repo context first: framework, MDX or build pipeline, CSS strategy, design tokens, existing components, accessibility helpers, and browser verification path.
2. Name the concept in one sentence. If it cannot be stated narrowly, split it into smaller demos.
3. **Pick the tier** (above). Default to non-interactive; only escalate to a live model when manipulation or motion is essential.
4. If motion is involved, read `references/animation-vocabulary.md` and name the animation vocabulary before coding: purpose, pattern, timing, easing or physics, spatial rules, feedback behavior, performance constraints, and reduced-motion fallback. Do not proceed from "make it smooth" or "make it animated" without translating it into a motion spec.
5. Choose the representation before the renderer: the visual form that makes the concept easiest to inspect — annotated figure, timeline, log, ring, map, field, small multiples, state table, direct-manipulation scene, instrument panel, or another concept-specific shape.
6. For static work, choose layout by dimensionality: Flexbox for one-dimensional rows/toolbars/wrapping chips, Grid for two-dimensional shells/dashboards/galleries, normal flow when it already reads correctly. Prefer native semantics over ARIA.
7. For interactive work, choose the renderer:
   - Canvas 2D for most mechanical, geometric, ray, chart-like, and annotated 2D systems.
   - SVG for mostly static vector diagrams, selectable labels, and low-element-count state diagrams.
   - Canvas/WebGL plus DOM/SVG overlays for dense visuals with readable labels and controls.
   - Three.js for 3D objects, cameras, lighting, depth, rotations, spatial mechanisms, or many mesh instances.
   - A physics library only when the simulation needs collisions, rigid bodies, joints, or constraint solving beyond a few formulas.
8. Design the model before drawing. Keep parameters, derived values, and simulation state separate from rendering.
9. Build a tiny vertical slice: static render, then one controlled parameter, then animation, then labels and polish.
10. Verify the runtime lifecycle: resize, pause, cleanup, reduced motion, mobile pointer input, and prerender/static build behavior.

## Implementation Shape

### Static HTML/CSS
- Start from semantic markup, then add class names for styling hooks.
- Keep reading order and visual order aligned unless there is a strong, tested accessibility reason.
- Prefer `gap` over margin choreography in Grid and Flexbox.
- Prefer `max-width`, `minmax()`, `clamp()` for dimensions; reach for container/media queries only when intrinsic layout is insufficient.
- Use logical properties (`margin-inline`, `padding-block`, `inset-inline`) when the component does not depend on physical direction.
- Use CSS custom properties for design tokens and component-local knobs.
- Prefer one or two class selectors. Avoid IDs in CSS, deep ancestry, and `!important` unless overriding third-party CSS with a documented reason.
- Keep component states explicit: hover, active, focus-visible, disabled, selected, expanded, invalid, loading, and empty.
- Never hide important text or controls behind hover-only interactions.

### Interactive embeds (React shell + plain TS engine)
For blog embeds with real behavior, prefer a React shell plus a plain TypeScript engine:

```text
src/components/GearTrainDemo.tsx
src/demos/gears/model.ts
src/demos/gears/render-canvas.ts
src/demos/gears/viewport.ts
src/demos/gears/input.ts
```

Boundary:
- React owns markup, controls, article layout, accessibility text, and lifecycle.
- The engine owns state, math, rendering, pointer mapping, and animation timing.
- The model is deterministic and testable without a canvas when practical.
- The renderer reads state; it is not the source of truth.

Scale this to the demo. Keep a small static SVG or single-state figure in one component when the boundary would add ceremony. Split into `model`, `render`, `viewport`, and `input` only when the demo has animation, pointer input, reusable math, or meaningful state transitions.

For prerendered React sites, never touch `window`, `document`, canvas/WebGL contexts, or `matchMedia` at module top level. Start them inside an effect and clean them up.

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

### Model pattern
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

Keep time-driven animation optional. When a demo includes playback, run it by default so the reader immediately sees it is live. Sliders and scrub state should set the model directly so the article stays inspectable frame by frame.

## Visual Direction

Give each concept the visual form that makes its model easiest to inspect. Name the representation before layout or styling starts; let existing examples supply reusable vocabulary (palette, control feel, label density, model/render boundaries).

For interactive demos, start from the shared palette when it fits and map color semantically: ink `#172033`, muted text `#5c667a`, line `#d9deea`, page background `#eef1f7`, panel white `#ffffff`, primary blue `#2f69f0`, semantic red `#d24a44`, probe/highlight gold `#d59b24`, success/available green `#1d8b65`. Blue for primary action/selected/source A; red for negative/conflict/failure/source B; gold for probes and active focus; green for healthy/committed/available. Add a legend when color carries meaning. Style controls like the examples when the site has no stronger local primitive (primary buttons blue, secondary on white, translucent blue focus rings, short transitions with `--ease-out-ui: cubic-bezier(0.23, 1, 0.32, 1)`).

When adapting a standalone demo into a website, map these values onto the site's tokens and primitives while preserving semantic color roles, readable spacing, and the chosen composition.

## Quality Bar

- The first viewport shows the actual product, document, or demo — not a marketing wrapper.
- The layout stays stable when labels wrap, cards have uneven content, or controls enter focus; text fits its parent on mobile and desktop.
- Color carries meaning and maintains WCAG contrast.
- Styling stays boring where the product is operational; be expressive only when the domain warrants it.
- Do not fake physics with arbitrary easing when the article claims a mechanical or physical relationship — use formulas, constraints, or clearly labeled illustrative motion.
- Use animation vocabulary as an implementation contract: state the purpose, named pattern, timing/orchestration, easing or physics, spatial continuity rule, interaction feedback, performance target, and reduced-motion behavior.
- Prefer readable math and named intermediate values over compressed vector cleverness.
- Keep controls close to the visual they affect; make default states useful (the first frame should explain something before interaction).
- Live demos start playing by default, with pause, step, scrub, and reset available.
- Connectors, arrows, and selected paths are built from shared geometry or named ports, not eyeballed offsets.
- Begin new demos and meaningful revisions with a short representation note: concept, invariant, visual form, tier/renderer, controls, layout, and validation path.
- Official docs are the source of truth for HTML/CSS/ARIA syntax, semantics, and support; bundled references route, they do not freeze the platform. Study creator patterns, summarize what you use, and write original code.

## Validation

Use the narrowest check that proves the work:

- Static demos: open the HTML file or run a static server; verify desktop and narrow widths.
- Component work: run the project typecheck/tests and inspect the changed UI in a browser.
- Accessibility-sensitive work: tab through controls, inspect labels and names, check contrast against WCAG.
- Responsive work: test narrow mobile, mid tablet, and desktop ranges.
- Type/model changes in interactive demos: run the repo's typecheck or tests.
- Deno/TanStack blog posts: default to `deno task build`; use `deno task preview-static` or the app's preview command for rendered verification.
- Canvas/WebGL: confirm the canvas has nonzero pixels, is correctly sized and interactive, resize works, camera framing is correct, and no console WebGL errors appear.
- CSS architecture changes: search for overly broad selectors, duplicated tokens, unnecessary `!important`, and layout rules leaking across components.
