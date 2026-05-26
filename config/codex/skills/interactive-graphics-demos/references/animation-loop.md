# Animation Loop

Use `requestAnimationFrame` for live rendering and keep the loop lifecycle explicit. The callback receives a high-resolution timestamp; use it for time-based motion instead of assuming a fixed frame rate.

Sources:
- MDN requestAnimationFrame: https://developer.mozilla.org/en-US/docs/Web/API/Window/requestAnimationFrame
- MDN cancelAnimationFrame: https://developer.mozilla.org/en-US/docs/Web/API/Window/cancelAnimationFrame

## Contents

- Loop Contract
- Variable vs Fixed Timestep
- Play, Pause, Scrub
- Reduced Motion
- Visibility

## Loop Contract

Expose start/stop/destroy from the engine:

```ts
type DemoEngine = {
  start(): void;
  stop(): void;
  destroy(): void;
  setState(patch: Partial<DemoState>): void;
};
```

Keep one outstanding animation frame request at a time.

```ts
function createLoop(update: (dt: number) => void, render: () => void) {
  let frameId = 0;
  let last = 0;
  let running = false;

  function frame(now: number) {
    if (!running) return;
    const dt = last === 0 ? 0 : Math.min(now - last, 50);
    last = now;
    update(dt);
    render();
    frameId = requestAnimationFrame(frame);
  }

  return {
    start() {
      if (running) return;
      running = true;
      last = 0;
      frameId = requestAnimationFrame(frame);
    },
    stop() {
      running = false;
      cancelAnimationFrame(frameId);
    },
  };
}
```

## Variable vs Fixed Timestep

Use variable timestep for explanatory mechanisms where formulas map directly from time to state:

```ts
state.angle += dtMs * state.angularVelocity;
```

Use fixed timestep for numerical physics when stability matters:

```ts
accumulator += dtMs;
while (accumulator >= fixedStepMs) {
  integrate(state, fixedStepMs / 1000);
  accumulator -= fixedStepMs;
}
render(interpolate(state, accumulator / fixedStepMs));
```

Clamp large `dt` values after hidden tabs or debugger pauses. A max of 50-100ms usually prevents explosive catch-up in article demos.

## Play, Pause, Scrub

Every good explainer should be inspectable:
- Play advances time.
- Pause freezes the state.
- Scrub sets the parameter directly.
- Reset returns to a meaningful first frame.

If a demo has a time dimension, start it playing by default. The first view
should feel alive without the reader discovering a play button. Pause
automatically for reduced motion, hidden/offscreen demos, or after the user
grabs a scrubber.

Do not bind explanation solely to elapsed wall-clock time. Article prose often needs exact states such as "contact begins", "normal crosses the pitch point", or "output gear completes one turn".

## Reduced Motion

Read `prefers-reduced-motion` in the client lifecycle. If reduced motion is requested:
- Start paused.
- Render a useful static state.
- Keep sliders and step buttons usable.
- Avoid automatic looping unless the user explicitly starts it.

## Visibility

Pause or reduce work when the demo is offscreen or the document is hidden. Use `IntersectionObserver` when many demos appear in one article.

```ts
document.addEventListener("visibilitychange", () => {
  if (document.hidden) engine.stop();
});
```

Resume only if the user had the demo playing before it was paused.
