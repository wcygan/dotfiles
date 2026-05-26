# Canvas 2D

Use Canvas 2D for most article demos that are fundamentally planar: gears, linkages, springs, ray optics, coordinate transforms, traces, plots, force arrows, and annotated mechanical diagrams.

Sources:
- MDN Canvas API: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API
- MDN Canvas tutorial: https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial
- WebGL Fundamentals canvas resizing guidance, useful for Canvas too: https://webglfundamentals.org/webgl/lessons/webgl-resizing-the-canvas.html

## Contents

- Renderer Shape
- Coordinate Spaces
- Drawing Order
- Canvas Size
- Hit Testing
- Common Primitives

## Renderer Shape

Keep drawing deterministic:

```ts
function draw(ctx: CanvasRenderingContext2D, state: DemoState, viewport: Viewport) {
  clearCanvas(ctx);
  drawBackground(ctx, viewport);
  drawMechanism(ctx, state, viewport);
  drawForces(ctx, state, viewport);
  drawLabels(ctx, state, viewport);
}
```

Prefer pure helpers for geometry:

```ts
type Point = { x: number; y: number };

function rotate(point: Point, angle: number): Point {
  const c = Math.cos(angle);
  const s = Math.sin(angle);
  return { x: point.x * c - point.y * s, y: point.x * s + point.y * c };
}
```

## Coordinate Spaces

Use a world coordinate system for the model, then transform to screen coordinates in one place. Avoid scattering `canvas.width / 2` and pixel constants through the model.

Good split:
- World space: meters, radians, teeth count, normalized units, or concept-specific units.
- View space: pan, zoom, aspect ratio, visible bounds.
- Screen space: CSS pixels and device pixels.

## Drawing Order

Use a stable order so visual hierarchy stays readable:

1. Background grid or construction guides.
2. Passive geometry, ghost states, traces.
3. Main mechanism or moving bodies.
4. Vectors, contact points, selected paths.
5. Labels, callouts, legends.
6. Interaction affordances such as drag handles.

## Canvas Size

The canvas has a CSS display size and a drawing-buffer size. Resize the drawing buffer from the displayed size, then scale drawing so coordinates remain stable.

```ts
function resizeCanvas(canvas: HTMLCanvasElement, maxDpr = 2) {
  const rect = canvas.getBoundingClientRect();
  const dpr = Math.min(window.devicePixelRatio || 1, maxDpr);
  const width = Math.max(1, Math.round(rect.width * dpr));
  const height = Math.max(1, Math.round(rect.height * dpr));
  const changed = canvas.width !== width || canvas.height !== height;

  if (changed) {
    canvas.width = width;
    canvas.height = height;
  }

  return { dpr, width, height, changed };
}
```

Use `ctx.setTransform(dpr, 0, 0, dpr, 0, 0)` when drawing in CSS-pixel units. Use world transforms separately.

## Hit Testing

Convert pointer coordinates into world coordinates before testing.

```ts
function pointerPoint(event: PointerEvent, canvas: HTMLCanvasElement) {
  const rect = canvas.getBoundingClientRect();
  return { x: event.clientX - rect.left, y: event.clientY - rect.top };
}
```

Use generous hit radii for mobile. Make drag handles stable dimensions so hover or active states do not shift the drawing.

## Common Primitives

Build small helpers instead of retyping drawing code:
- `drawArrow(start, end, options)`
- `drawArc(center, radius, startAngle, endAngle, options)`
- `drawRotatedLabel(text, position, angle)`
- `drawGearPitchCircle(gear)`
- `drawTrace(points)`
- `drawPointHandle(point, state)`

Prefer labels in DOM or SVG overlays when text needs to wrap, be selectable, or stay sharp across device scale. Canvas text is fine for compact in-diagram labels.
