# Overlays, Controls, And Accessibility

Interactive graphics should be operable, readable, and understandable without guessing.

## Controls

Use native controls where possible:
- `input type="range"` for continuous parameters.
- Segmented controls or radio buttons for modes.
- Buttons for play, pause, step, reset, and view presets.
- Checkboxes or switches for visibility toggles.

Keep controls near the thing they affect. Label them with the model parameter, not implementation language.

Good:
- "Pressure angle"
- "Input gear teeth"
- "Show force normals"

Weak:
- "progress"
- "debug"
- "mode 2"

## Scrubbers

Scrubbers should set model state directly:

```ts
function setScrub(progress: number) {
  state.inputAngle = progress * Math.PI * 2;
  engine.render();
}
```

Do not make scrubbers fight autoplay. When the user drags, pause playback until they restart it.

## Labels

Prefer DOM or SVG overlays for text that must stay sharp, wrap, or be accessible. Use Canvas text for compact inline labels that are part of the drawing.

For overlay labels pinned to world positions:
1. Compute world position from the model.
2. Project to screen coordinates.
3. Position the DOM label with transform.
4. Hide or clamp labels that leave the viewport.

## Pointer Input

Use Pointer Events where possible:
- `pointerdown`
- `pointermove`
- `pointerup`
- `pointercancel`
- `setPointerCapture`

Always convert screen coordinates through the viewport before model hit testing. Use larger hit targets than the visible point.

## Keyboard

Support keyboard interaction for controls:
- range inputs already provide keyboard behavior
- buttons need clear text or `aria-label`
- custom draggable points should have a keyboard alternative when they are essential

For diagrams where full keyboard manipulation is not feasible, provide equivalent controls below the canvas.

## Reduced Motion

Respect `prefers-reduced-motion`:
- start paused
- show a meaningful static frame
- keep step/scrub controls available
- avoid continuous autoplay until the user requests it

Do not remove all visual change; reduce automatic motion and large position changes first.

## Semantic Wrapper

Wrap demos as figures when they explain article content:

```tsx
<figure className="interactive-demo">
  <canvas aria-label="Interactive ray optics demo" />
  <figcaption>Drag the lens to see how focal distance changes.</figcaption>
</figure>
```

Use `aria-live` sparingly for status text. Do not announce every animation frame.

## Color

Use color as a redundant signal:
- pair color with labels, icons, line styles, or legends
- keep contrast readable over the canvas
- avoid relying on red/green alone for state

Use a small, stable palette across demos in the same article so readers learn the visual language.
