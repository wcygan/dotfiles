# Spatial Math

Mechanical and spatial demos live or die on coordinate clarity. Name spaces, units, and transforms explicitly.

## Core Types

Use small plain types unless the project already has a math library:

```ts
type Vec2 = { x: number; y: number };
type Segment = { a: Vec2; b: Vec2 };
type Circle = { center: Vec2; radius: number };
```

Use radians internally. Convert to degrees only for labels.

## Vector Helpers

Useful helpers:
- `add`, `sub`, `scale`
- `dot`, `cross2`
- `length`, `normalize`
- `perp`
- `lerp`
- `rotate`
- `projectPointToLine`
- `distancePointToSegment`

Keep degenerate cases explicit. For example, `normalize({ x: 0, y: 0 })` should return a fallback or signal failure, not `NaN`.

## Viewport

Define viewport transforms once:

```ts
type Viewport = {
  worldCenter: Vec2;
  worldUnitsPerCssPx: number;
  cssWidth: number;
  cssHeight: number;
};

function worldToScreen(p: Vec2, v: Viewport): Vec2 {
  return {
    x: (p.x - v.worldCenter.x) / v.worldUnitsPerCssPx + v.cssWidth / 2,
    y: v.cssHeight / 2 - (p.y - v.worldCenter.y) / v.worldUnitsPerCssPx,
  };
}
```

The flipped y-axis belongs in the viewport layer. The model should not know that screen y grows downward.

## Curves

Parametric curves are natural for explainers:
- Circle: position from angle.
- Involute: gear tooth construction.
- Bezier: paths, easing illustrations, curve normals.
- Cycloid: rolling wheel path.
- Sine/cosine: oscillator, pendulum approximation, waves.

Sample curves into points for drawing and hit testing. Keep the original formula available for exact labels and derived values.

## Mechanical Relationships

Common relationships:
- Angular velocity: `linearVelocity = angularVelocity * radius`.
- Meshed gear ratio: `outputAngle = -inputAngle * inputTeeth / outputTeeth`.
- Torque ratio for ideal gears: `outputTorque = inputTorque * outputTeeth / inputTeeth`.
- Spring force: `force = -stiffness * displacement - damping * velocity`.
- Pendulum small angle: `angle = amplitude * cos(sqrt(g / length) * time)`.

Label simplifications. If you use a small-angle pendulum, say so in the article or UI when precision matters.

## Constraints

For linkages and mechanisms:
- Solve geometry first, render second.
- Prefer closed-form intersections for simple two-bar/four-bar setups.
- Use iterative solvers only when needed, and cap iteration counts.
- Visualize invalid states instead of letting geometry explode.

## 3D Basics

For Three.js:
- Keep model units meaningful.
- Separate object local transforms from world transforms.
- Use groups for mechanisms with nested rotations.
- Use a stable camera and explicit framing before adding controls.
- Put labels in DOM or CSS2D-style overlays when readability matters.
