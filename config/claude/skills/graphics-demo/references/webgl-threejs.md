# WebGL And Three.js

Use WebGL or Three.js when Canvas 2D stops being the right abstraction: true 3D, camera movement, lighting, depth ordering, meshes, many particles, shaders, or spatial mechanisms that need perspective.

Sources:
- MDN WebGL API: https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API
- Three.js fundamentals: https://threejs.org/manual/en/fundamentals.html
- Three.js examples: https://threejs.org/examples/
- MathBox: https://mathbox.org/
- Steven Wittens on MathBox: https://acko.net/blog/making-mathbox/

## Contents

- Prefer Three.js First
- Scene Structure
- Labels And Controls
- Resize
- Bundle Boundaries
- Camera Discipline

## Prefer Three.js First

Do not hand-roll raw WebGL for article demos unless shaders, custom pipelines, or learning goals require it. Three.js gives a practical scene graph:

```ts
const renderer = new WebGLRenderer({ canvas, antialias: true });
const scene = new Scene();
const camera = new PerspectiveCamera(35, 1, 0.1, 100);

const gear = new Mesh(gearGeometry, gearMaterial);
scene.add(gear);

function render(state: DemoState) {
  gear.rotation.z = state.inputAngle;
  renderer.render(scene, camera);
}
```

## Scene Structure

Use groups to mirror the mechanism:

```text
scene
  mechanismGroup
    inputShaftGroup
      inputGearMesh
      inputAxisHelper
    outputShaftGroup
      outputGearMesh
  labelLayer
  lights
  camera
```

Keep generated geometry creation separate from per-frame transform updates.

## Labels And Controls

WebGL text is rarely worth it for article explainers. Use DOM/SVG overlays for:
- readable labels
- sliders and toggles
- legends
- equations
- callouts pinned to projected 3D positions

Project world points into screen coordinates when labels must follow objects.

## Resize

On every render or resize event:
- read the canvas display size
- set renderer size without changing CSS layout
- update camera aspect
- update projection matrix

```ts
function resize(renderer: WebGLRenderer, camera: PerspectiveCamera) {
  const canvas = renderer.domElement;
  const rect = canvas.getBoundingClientRect();
  const width = Math.max(1, Math.round(rect.width));
  const height = Math.max(1, Math.round(rect.height));

  renderer.setSize(width, height, false);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}
```

Use a capped pixel ratio. High DPR can multiply GPU work quickly on mobile.

## Bundle Boundaries

For static/prerendered blogs:
- Import Three.js only in client-only code or dynamic imports when possible.
- Do not create renderers at module top level.
- Dispose geometries, materials, textures, controls, and renderer resources in cleanup.
- Avoid adding all Three.js examples to the main article bundle by accident.

## Camera Discipline

Article demos need predictable framing more than free navigation. Start with a fixed camera, then add constrained orbit controls only if changing perspective teaches something.

Good controls:
- reset view
- rotate around one axis
- exploded/assembled mode
- orthographic/perspective toggle

Avoid uncontrolled orbit cameras that make the diagram hard to return to the prose's intended viewpoint.
