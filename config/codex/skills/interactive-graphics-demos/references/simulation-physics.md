# Simulation And Physics

Most explanatory demos should be deterministic models, not full physics engines. Use real equations where the article makes a physical claim, and use illustrative motion only when it is labeled as illustrative.

Useful libraries:
- Matter.js docs: https://brm.io/matter-js/docs/
- Rapier JavaScript: https://rapier.rs/docs/user_guides/javascript/getting_started_js
- MyPhysicsLab examples: https://www.myphysicslab.com/
- Falstad math and physics applets: https://www.falstad.com/mathphysics.html

## Choose The Model

Use closed-form or direct parameter mapping when possible:
- Gear ratio from teeth counts.
- Ray optics from intersection/refraction formulas.
- Pendulum approximation from time and length.
- Camera projection from matrices.
- Linkage positions from circle intersections.

Use numerical integration when state evolves from forces:
- springs
- damped oscillators
- particles
- fluid-like fields
- chaotic systems

Use a physics engine when you need:
- collision detection
- rigid-body dynamics
- joints and constraints
- stacking or contact resolution
- many objects interacting

## Integration

Simple semi-implicit Euler is often enough for article demos:

```ts
velocity += acceleration * dt;
position += velocity * dt;
```

For stiffer systems or precision-sensitive demos, use smaller fixed steps or a better integrator. Cap accumulated steps so hidden-tab resumes do not run hundreds of updates.

## Constraint Solving

For mechanisms, prefer solving constraints directly:

```ts
const joint = intersectCircles(crankEnd, couplerLength, rockerPivot, rockerLength);
```

If no valid solution exists, render the nearest valid state or show the invalid configuration as a teaching point.

## Determinism

Article demos should be replayable:
- Keep random seeds explicit.
- Let sliders set state directly.
- Store presets as data.
- Make reset return to the same first frame.
- Avoid frame-rate-dependent integration.

## Truthfulness

Do not overclaim. If the model ignores friction, backlash, turbulence, nonlinearities, relativistic effects, or manufacturing tolerances, either omit the claim or label the simplification.

Good explanatory copy:
- "Idealized, no slip"
- "Small-angle approximation"
- "Not to scale"
- "Contact forces simplified"
- "Qualitative field view"

## Debug Views

Add temporary debug overlays while building:
- centers, pivots, joints
- bounding boxes
- constraint residuals
- normals and tangents
- velocity and acceleration vectors
- current timestep and FPS

Remove or hide debug controls before publication unless they help the reader.
