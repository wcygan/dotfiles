# Services and Layers

Use this when defining services, wiring dependencies, composing layers, reading config, creating test doubles, or deciding where an application runtime should live. Verify exact APIs in the official docs or installed package exports before editing.

Official docs to check first:
- https://effect.website/docs/requirements-management/services/
- https://effect.website/docs/requirements-management/layers/
- https://effect.website/docs/requirements-management/default-services/
- https://effect.website/docs/requirements-management/layer-memoization/
- https://effect.website/docs/configuration/
- https://effect.website/docs/runtime/

## Service Shape

A service is a typed interface stored in the Effect context. `R` records which service tags are still required.

Common pattern:

```ts
class Users extends Context.Tag("@app/Users")<
  Users,
  {
    readonly findById: (id: UserId) => Effect.Effect<User, UserNotFound>
  }
>() {}
```

Use a stable tag name scoped to the app or package. Keep service methods small and domain-oriented; do not expose entire third-party clients unless the codebase already follows that style.

## Layer Construction

Layers are recipes for building services. Use them to:

- Build real implementations from config and resources.
- Swap test implementations without a mock framework.
- Scope resources so finalizers run on shutdown.
- Memoize shared services when the runtime is reused.

Practical composition rules:

- Define one live layer per service.
- A layer should provide its own transitive dependencies when that keeps consumers simple.
- Compose app-level layers once near startup or the boundary.
- Avoid rebuilding expensive layers per request.

## Config

Use Effect config when the app already uses Effect for startup or service wiring:

- Model required env vars as typed config.
- Use defaults only where the default is a real product decision.
- Use redacted values for secrets so logs do not expose them.
- Keep config parsing at startup when failures should prevent the app from serving traffic.

For small scripts or mixed codebases, plain environment parsing may be acceptable. Do not introduce Layer/Config if the task only needs a narrow Schema or tagged-error improvement.

## Runtime Placement

For long-running servers, prefer building the runtime/layers once and reusing them at request boundaries. This keeps resource lifetimes clear and prevents DB pools, clients, or telemetry exporters from being recreated repeatedly.

For short CLIs or tests, providing a layer directly at the program edge can be enough.

## Testing

Use layers as the swap point:

- Keep domain functions typed against service requirements.
- Provide a test layer with deterministic implementations.
- Avoid mocking internals when replacing the service contract is clearer.
- Use time/test-clock tools for schedules, retry, and timeout logic when the project has Effect testing support.

## Code Review Checks

- Does `R` accurately describe missing services?
- Are services domain-shaped rather than leaking framework or vendor details?
- Are expensive resources scoped and reused appropriately?
- Are test doubles provided by layers or an equivalent project pattern?
- Is runtime construction placed at startup or an edge, not inside hot domain functions?
