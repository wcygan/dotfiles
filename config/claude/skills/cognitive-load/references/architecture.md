# Architectural Cognitive Load Patterns

Anti-patterns at the system/architecture level that inflate cognitive load across teams.

---

## 1. Premature Microservices

**Cognitive cost**: Every service boundary is a chunk. Developers must hold service topology, inter-service contracts, network failure modes, and deployment dependencies in working memory simultaneously.

### The pattern
A startup with 5 engineers splits their product into 17 microservices. Every feature change touches 4+ services. Releases take coordination across teams. What was a function call is now a network hop with failure modes, retries, and eventual consistency.

### The reality
> "A well-crafted monolith with isolated modules is often more flexible than microservices."

**When microservices make sense**: When you have multiple teams that need to deploy independently at different cadences. The benefit is organizational, not technical.

**When they don't**: When a single team owns the entire system. You're adding network complexity without gaining deployment independence.

### Decision framework
1. Start with a monolith with well-defined module boundaries
2. Measure: Is deployment coupling actually blocking team velocity?
3. Extract services only at proven pain points
4. Each extraction should reduce total cognitive load, not increase it

### Historical evidence
- **Linux vs Hurd**: Monolithic Linux defeated the theoretically superior microkernel Hurd
- **Instagram**: Monolithic Python app served 14M users with 3 engineers
- The Tanenbaum-Torvalds debate settled in practice: simpler architecture won

---

## 2. Shallow Abstraction Layers (Hexagonal/Onion/Clean Architecture)

**Cognitive cost**: Each layer is an indirection. To trace a request, the reader must jump through Controller → Service → Repository → Adapter → Port → Implementation. Each jump consumes a working memory slot.

### The promise
"Swap your database by changing one adapter!"

### The reality
- **Hyrum's Law**: Every observable behavior becomes a dependency. Changing storage means handling implicit contracts across the entire system, not just swapping an adapter.
- Real database migrations take months due to data migration, query semantics differences, and behavioral contracts — not because of missing abstractions.
- Teams report spending more time navigating layers than solving business problems.

### The fix
Follow the principles directly without the pattern:
- **Dependency inversion**: Depend on abstractions, not concretions (doesn't require 6 layers)
- **Information hiding**: Hide implementation details (doesn't require ports and adapters)
- **Cognitive load reduction**: Each abstraction must reduce total mental effort, not just add indirection

**Test**: If removing a layer would make the code easier to trace with no functional loss, the layer is extraneous.

---

## 3. Framework Tight Coupling

**Cognitive cost**: Framework "magic" creates an implicit mental model that all developers must learn before being productive. The framework becomes a prerequisite, not a tool.

### Signs
- New developers spend weeks learning the framework before writing business logic
- Business logic is tangled with framework decorators, annotations, and conventions
- Testing requires the framework to be running
- "That's just how the framework does it" is a common answer to "why?"

### The fix
- Write business logic framework-agnostically as plain functions/classes
- Use the framework as a library at the edges (HTTP handling, DI wiring, etc.)
- New contributors should be able to read and modify business logic without framework knowledge

**Rule**: If your business logic can't run in a unit test without the framework, you're coupled.

---

## 4. DDD Misapplication (Solution-Space DDD)

**Cognitive cost**: When DDD is applied to solution architecture (folder structure, repository patterns, value objects everywhere), it creates subjective mental models. Ten developers reading the same DDD codebase build 10 different mental models.

### Problem-space DDD (valuable)
- Ubiquitous language: shared vocabulary between developers and domain experts
- Bounded contexts: clear boundaries between subdomains
- Strategic design: understanding where to invest engineering effort

### Solution-space DDD (cognitive load trap)
- Aggregate roots, value objects, domain events as mandatory patterns
- Repository pattern for every entity regardless of complexity
- Folder structures mirroring DDD tactical patterns

### The fix
Use DDD's strategic patterns (ubiquitous language, bounded contexts) for understanding the problem. For solution architecture, apply cognitive load principles directly:
- Does this pattern reduce or increase mental effort?
- Can a new developer understand this without DDD training?

**Alternative**: Team Topologies provides clearer organizational boundaries with less subjective interpretation.

---

## 5. Over-Applied DRY

**Cognitive cost**: Shared abstractions create coupling between unrelated components. Changing the shared code requires understanding all consumers. Each consumer is a chunk the modifier must hold in memory.

### The trap
Two services both format dates. A developer extracts a shared `DateFormatter` utility. Six months later:
- Service A needs timezone support, Service B doesn't
- The shared utility grows options, flags, and conditional paths
- Changing it requires testing both services
- The "simple" utility is now a complex, coupled dependency

### The principle
> "A little copying is better than a little dependency." — Rob Pike

### When DRY applies
- Within a single module/service where shared code has one owner
- For genuine business rules that MUST be consistent (e.g., tax calculation)

### When DRY hurts
- Across service boundaries (creates coupling)
- For incidental similarity (two things that happen to look alike today)
- For utility code that's trivial to re-implement (3-5 lines)

**Rule**: Before extracting shared code, ask: "If these two uses diverge, will this abstraction become a constraint?" If yes, copy instead.

---

## 6. Distributed Monolith

**Cognitive cost**: Combines the worst of both worlds — the operational complexity of microservices with the coupling of a monolith.

### Signs
- Deploying one service requires deploying 3 others simultaneously
- A single feature requires changes across 4+ repositories
- Services share a database
- Circular dependencies between services
- "We can't deploy on Friday" despite having microservices

### The fix
Either:
1. **Re-consolidate** into a well-structured monolith (usually the right answer)
2. **Properly decouple** with async messaging, separate data stores, and independent deployment

**Test**: Can each service be deployed independently with zero coordination? If not, you have a distributed monolith.

---

## Decision Framework: When to Add Architectural Complexity

Before adding any architectural pattern, layer, or boundary:

1. **What working memory slots does this consume?** (layers, concepts, conventions)
2. **What working memory slots does this free?** (hidden complexity, simpler interfaces)
3. **Net effect**: If consumed >= freed, don't add it
4. **The newcomer test**: Can someone unfamiliar with this pattern understand the system in < 40 minutes?
5. **The boring test**: Would a "boring" alternative (plain functions, simple modules) achieve the same goal?

> "Layers of abstraction aren't free; they're held in limited working memory."
