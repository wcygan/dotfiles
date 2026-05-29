# React, MDX, Deno, And TanStack Start

Use this reference when embedding a graphics demo in a React/MDX article, especially in a Deno + TanStack Start static/prerendered blog.

Sources:
- TanStack Start static prerendering: https://tanstack.com/start/latest/docs/framework/react/guide/static-prerendering
- Deno web development docs: https://docs.deno.com/runtime/fundamentals/web_dev/
- MDX: https://mdxjs.com/

## Contents

- Prerender Rule
- MDX Shape
- File Layout
- Dynamic Imports
- Styling
- Local Validation

## Prerender Rule

Static prerendering executes route rendering outside the browser. Client APIs must be delayed until mount:

- No `window` at module top level.
- No `document` at module top level.
- No `canvas.getContext()` before mount.
- No WebGL renderer construction before mount.
- No `matchMedia` before mount.

Use a stable shell for server/prerender output and hydrate the demo after mount.

```tsx
export function MechanismDemo() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const engine = createMechanismDemo(canvasRef.current);
    engine.start();
    return () => engine.destroy();
  }, []);

  return (
    <figure className="mechanism-demo">
      <canvas ref={canvasRef} aria-label="Interactive mechanism demo" />
      <figcaption>Drag or scrub to inspect the mechanism.</figcaption>
    </figure>
  );
}
```

## MDX Shape

Import the component from the article:

```mdx
import { MechanismDemo } from "~/components/MechanismDemo";

The pitch circles preserve the speed ratio:

<MechanismDemo />
```

Keep article prose in MDX. Keep demo state and rendering in TypeScript modules.

## File Layout

Recommended:

```text
src/components/MechanismDemo.tsx
src/demos/mechanism/model.ts
src/demos/mechanism/engine.ts
src/demos/mechanism/render-canvas.ts
src/demos/mechanism/viewport.ts
src/demos/mechanism/types.ts
```

For one-off demos, fewer files are fine. Split when the component mixes React lifecycle, math, and drawing in a way that is hard to read.

## Dynamic Imports

Use dynamic import for heavy browser-only dependencies:

```tsx
useEffect(() => {
  let disposed = false;
  let destroy = () => {};

  import("~/demos/gearbox/three-engine").then(({ createGearboxDemo }) => {
    if (disposed || !canvasRef.current) return;
    const engine = createGearboxDemo(canvasRef.current);
    destroy = engine.destroy;
    engine.start();
  });

  return () => {
    disposed = true;
    destroy();
  };
}, []);
```

## Styling

Give canvases stable dimensions:

```css
.mechanism-demo canvas {
  display: block;
  width: 100%;
  aspect-ratio: 16 / 9;
}
```

Avoid layout shifts from labels or controls. Put controls in normal DOM flow below or beside the canvas, or use absolutely positioned overlays inside a fixed-ratio wrapper.

## Local Validation

For Deno/TanStack blogs, prefer:

```sh
deno task typecheck
deno task test
deno task build
deno task preview-static
```

Use the commands actually present in the repo. For the `wcygan.net` blog, `deno task build` exercises MDX and prerendering.
