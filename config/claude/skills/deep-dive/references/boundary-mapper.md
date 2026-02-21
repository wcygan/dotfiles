# Boundary Mapper (Optional)

The Boundary Mapper identifies **where modules meet** — API surfaces, integration points, and the seams between subsystems. Spawn when the query involves connections or interfaces.

## Mission

Answer: "What connects to what, and where are the boundaries?"

## When to Spawn

- User asks "what connects to X?"
- User asks "how do X and Y interact?"
- User asks about API surfaces, contracts, or integration points
- Understanding the topic requires knowing the module boundaries

## Strategy

### Phase 1: Import/Export Analysis

For the target area, trace imports and exports:

```
Grep: import/require/use statements in the target module
      → what does this module depend on?

Grep: references to the target module from elsewhere
      → what depends on this module?
```

### Phase 2: Interface Identification

Find the public API surface:
- **Exported functions/types** — what the module exposes
- **Configuration** — what knobs exist (env vars, config files, CLI args)
- **Events/signals** — does it emit or listen to events
- **Data contracts** — what shapes of data cross the boundary (types, schemas, protocols)

### Phase 3: Boundary Map

Build a connection diagram:

```
[Module A] ──imports──→ [Target Module] ──imports──→ [Module C]
                              │
                              ├── exports: function_x, type_y
                              ├── config: ENV_VAR_Z
                              └── events: on_complete

[Module D] ──calls──→ function_x
[Module E] ──uses──→ type_y
```

### Phase 4: Coupling Assessment

For each boundary, assess:
- **Coupling strength**: Tight (shared state, direct calls) vs. Loose (events, interfaces)
- **Data flow direction**: One-way vs. bidirectional
- **Change risk**: Would modifying this boundary break other modules?

## What to Report Back

1. **Dependency graph** — what the target imports and what imports it
2. **Public API surface** — exported functions, types, and their signatures
3. **Integration points** — concrete file:line where modules connect
4. **Coupling assessment** — how tightly bound the modules are
5. **Change impact radius** — what would break if this module's API changed

## What NOT to Do

- Don't read internal implementation — focus on boundaries only
- Don't trace call chains — the Tracer handles that
- Don't catalog every import — focus on significant dependencies
- Don't analyze boundaries unrelated to the query
