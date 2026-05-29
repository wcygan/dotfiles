# Performance And Testing

Graphics demos need browser verification. Type checks do not prove the canvas is nonblank, correctly sized, or interactive.

Sources:
- WebGL Fundamentals canvas resizing: https://webglfundamentals.org/webgl/lessons/webgl-resizing-the-canvas.html
- MDN ResizeObserver: https://developer.mozilla.org/en-US/docs/Web/API/ResizeObserver
- MDN Performance API: https://developer.mozilla.org/en-US/docs/Web/API/Performance_API

## Performance Defaults

- Render only while playing, dragging, resizing, or after state changes.
- Pause offscreen demos when many appear in one article.
- Cap device pixel ratio, commonly at 2.
- Avoid allocating large arrays every frame.
- Precompute static geometry.
- Cache text measurements if drawing many labels.
- Use `transform` for DOM overlays that move every frame.
- Avoid expensive filters and shadows inside tight loops.

## Resize Checklist

For Canvas 2D:
- CSS controls the displayed size.
- Drawing buffer matches displayed size times capped DPR.
- Context transform is reset before drawing.
- World viewport recomputes after size change.

For WebGL/Three.js:
- Renderer size matches canvas display size.
- Viewport updates after buffer resize.
- Camera aspect and projection update.
- Pixel ratio is capped.

## Browser Verification

Before final handoff:

1. Open the article route in a browser.
2. Check desktop and mobile widths.
3. Confirm the first frame is useful.
4. Use play, pause, step, reset, sliders, and drag handles.
5. Resize the viewport.
6. Check browser console errors.
7. For WebGL, confirm context creation succeeds and the canvas is nonblank.
8. Test reduced motion when relevant.

## Pixel Checks

For automated smoke tests, a basic canvas pixel check can catch blank renderers:

```ts
const image = ctx.getImageData(0, 0, canvas.width, canvas.height);
const hasInk = image.data.some((value, index) => index % 4 !== 3 && value !== 0);
```

Use this only as a smoke check. Visual correctness still needs screenshots or human review.

## Layout Risk

Watch for:
- canvas height collapsing to 0
- blurry output from CSS size/drawing-buffer mismatch
- labels leaving the viewport
- controls wrapping badly on mobile
- overlay labels intercepting pointer input
- fixed-size canvases causing horizontal overflow
- autoplay continuing after unmount

## Validation Commands

Use project-local commands. Common web checks:

```sh
deno task typecheck
deno task test
deno task build
deno task preview-static
npm run build
pnpm test
```

For visual work, add browser screenshots when the user needs evidence or when the change is layout-heavy.
