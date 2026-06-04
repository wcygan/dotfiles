# TylorS/typed Effect Examples

Snapshot: `3b44be752873fb43497539783e47ffc642411182` on the `development` branch, inspected 2026-06-04.

Use these examples for Effect-native library architecture: `Effect<A, E, R>` APIs, `Layer` composition, browser/server runtime differences, HTTP handler boundaries, schedulers, queues, resources, and stream bridges.

## High-Level Read

Typed is the most Effect-native library architecture in this set. It uses `Effect<A, E, R>` and `Layer` to model framework services: routing, navigation, rendering, DOM access, queues, random values, HTTP handlers, schedulers, and stream bridges. The important idea is that framework capabilities become typed requirements rather than globals.

This repo is useful when designing a reusable TypeScript framework or UI/runtime library. It shows how to expose platform-specific implementations as layers, keep APIs polymorphic over `R`, and convert Effect programs back to ordinary framework boundaries such as web handlers.

## Permalinks

- [HTTP API builder imports](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/server/src/HttpApiBuilder.ts#L4-L25) - uses `@effect/platform`, `@effect/schema`, `Effect`, `Context`, `Layer`, `ManagedRuntime`, and route libraries together.
- [HTTP app as an Effect with requirements](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/server/src/HttpApiBuilder.ts#L55-L103) - `serve` unwraps an effect into a layer; `httpApp` requires API/router services and schema-encodes errors.
- [ManagedRuntime to web handler boundary](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/server/src/HttpApiBuilder.ts#L112-L150) - documents runtime composition and converts an Effect HTTP app into a Promise-based web handler.
- [Idle scheduler layer and scoped requestIdleCallback](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/fx/src/Idle.ts#L119-L170) - `Layer.setScheduler`, `Effect.asyncEffect`, finalizers, and idle-loop requirements.
- [Core browser/server service layers](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/core/src/CoreServices.ts#L20-L67) - merges app-wide services for DOM/browser and server environments.
- [Current route browser/server layers and navigation effect](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/router/src/CurrentRoute.ts#L250-L332) - browser `Layer`, server `Layer`, computed refs, and navigation as `Effect` requiring services.
- [Context-backed Queue helper](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/context/src/Queue.ts#L34-L87) - wraps `Queue` operations as required services and provides bounded/dropping/sliding/unbounded layers.
- [Fx to Stream bridge](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/fx/src/Stream.ts#L22-L69) - converts custom Fx values into scoped streams using queues, exits, forked fibers, and `Stream.unwrapScoped`.
- [Scoped render queue layers](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/template/src/RenderQueue.ts#L70-L110) - scoped layers for idle, RAF, microtask, sync, and mixed render queues.
- [Context-backed Resource helper](https://github.com/TylorS/typed/blob/3b44be752873fb43497539783e47ffc642411182/packages/context/src/Resource.ts#L20-L55) - `Layer.scoped` resources with automatic schedule-based refresh or manual acquisition.

## Code Samples

These are distilled pattern sketches from the linked code, not verbatim excerpts.

### Effect HTTP App With Requirements

```ts
const httpApp: Effect.Effect<
  HttpApp.Default<never, HttpRouter.DefaultServices>,
  never,
  HttpApi.Service | HttpApiRouter
> = Effect.gen(function* () {
  const api = yield* HttpApi.Service
  const router = yield* HttpApiRouter.router
  const encodeError = Schema.encodeUnknown(makeErrorSchema(api))

  return router.pipe(
    Effect.catchAll((error) =>
      Effect.matchEffect(encodeError(error), {
        onFailure: () => Effect.die(error),
        onSuccess: Effect.succeed,
      })
    )
  )
})
```

### Managed Runtime At The Web Boundary

```ts
const runtime = ManagedRuntime.make(
  Layer.mergeAll(ApiLive, RouterLive, PlatformLive).pipe(
    Layer.provideMerge(NodeContext.layer)
  )
)

export const handler = (request: Request): Promise<Response> =>
  httpApp.pipe(
    Effect.map((app) => HttpApp.toWebHandlerRuntime(runtime)(app)(request)),
    runtime.runPromise
  )
```

### Browser And Server Services As Layers

```ts
export function fromWindow(window: Window & GlobalThis): Layer.Layer<CoreDomServices> {
  return Layer.mergeAll(
    GetRandomValues.implement((length) =>
      Effect.succeed(window.crypto.getRandomValues(new Uint8Array(length)))
    ),
    Navigation.fromWindow,
    CurrentRoute.browser
  ).pipe(Layer.provideMerge(renderLayer(window)))
}

export const server = Layer.mergeAll(
  getRandomValues,
  CurrentRoute.server("/"),
  RenderQueue.sync
)
```

### Scoped Idle Scheduler

```ts
const whenIdle = (options?: IdleRequestOptions) =>
  Effect.asyncEffect<IdleDeadline, never, Scope.Scope>((resume) => {
    const id = requestIdleCallback((deadline) => resume(Effect.succeed(deadline)), options)
    return Effect.addFinalizer(() => Effect.sync(() => cancelIdleCallback(id)))
  })

const whileIdle = (body: Effect.Effect<void>) =>
  Effect.gen(function* () {
    while (true) {
      const deadline = yield* whenIdle()
      while (deadline.didTimeout || deadline.timeRemaining() > 0) {
        yield* body
      }
    }
  })
```

### Context-Backed Queue Helper

```ts
function QueueService<A>() {
  const tag = Context.GenericTag<Queue.Queue<A>>("Queue")

  return Object.assign(tag, {
    take: Effect.flatMap(tag, Queue.take),
    offer: (value: A) => Effect.flatMap(tag, Queue.offer(value)),
    bounded: (capacity: number) => Layer.effect(tag, Queue.bounded<A>(capacity)),
    unbounded: Layer.effect(tag, Queue.unbounded<A>()),
  })
}
```
