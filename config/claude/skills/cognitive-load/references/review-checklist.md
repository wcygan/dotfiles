# Cognitive Load Review Checklist

Use this checklist when reviewing code, PRs, or architecture decisions. Each item maps to a specific principle from the cognitive load framework.

---

## Code-Level Review

### Conditionals & Control Flow
- [ ] **No complex conditionals**: Expressions with 3+ terms use named intermediates
- [ ] **Flat control flow**: Maximum nesting depth of 2; early returns used for preconditions
- [ ] **No ternary chains**: Nested ternaries replaced with if/else or match/switch
- [ ] **Guard clauses first**: Error/edge cases handled at the top, happy path flows linearly

### Naming & Readability
- [ ] **Specific names**: No `data`, `result`, `tmp`, `info`, `manager`, `handler` without qualification
- [ ] **Names reveal intent**: Reader understands purpose without checking surrounding code
- [ ] **No variable reuse**: Each variable has one meaning throughout its scope
- [ ] **Function names are verbs**: Describe WHAT it does, not HOW

### Functions & Methods
- [ ] **Single level of abstraction**: Each function operates at one abstraction level
- [ ] **Short enough to hold in memory**: ~40 lines maximum; describable in one sentence without "and"
- [ ] **No clever code**: Readable equivalent preferred over concise tricks
- [ ] **Explicit side effects**: Side effects visible at the call site, not hidden in helpers

### Types & Interfaces
- [ ] **Self-describing error codes**: Application errors use strings, not opaque numbers
- [ ] **Deep modules**: Interface simpler than implementation
- [ ] **No wrapper-only classes**: Classes that just delegate add indirection without value

---

## Architecture-Level Review

### Module Boundaries
- [ ] **Deep over shallow**: Modules expose simple interfaces and hide complex internals
- [ ] **Composition over inheritance**: Inheritance depth <= 1; behavior assembled, not chained
- [ ] **No circular dependencies**: Dependency graph is a DAG
- [ ] **Cohesive modules**: Related functionality grouped; changes don't cascade across boundaries

### Abstraction Quality
- [ ] **Each layer earns its cost**: Every abstraction reduces net cognitive load
- [ ] **No pass-through layers**: Layers that just forward calls are removed
- [ ] **Framework at edges only**: Business logic readable without framework knowledge
- [ ] **Explicit wiring**: Dependencies visible, not auto-discovered/injected magically

### Service Architecture
- [ ] **Independent deployment**: Each service deploys without coordinating with others
- [ ] **No shared databases**: Services own their data; communicate through contracts
- [ ] **Justified boundaries**: Service splits driven by team scaling needs, not theoretical purity
- [ ] **Monolith-first**: New systems start monolithic with good module boundaries

### DRY vs Coupling
- [ ] **Cross-boundary copying OK**: Incidental similarity across services is duplicated, not shared
- [ ] **Shared code has one owner**: Shared libraries owned by one team with clear versioning
- [ ] **Abstractions earned**: Patterns extracted after 3+ genuine uses, not preemptively

---

## Design Decision Audit

For each significant design decision, evaluate:

| Question | Good Answer | Warning Sign |
|----------|------------|--------------|
| How many concepts must a reader hold to understand this? | 1-3 | 4+ |
| Can a new developer trace execution linearly? | Yes, top to bottom | Requires jumping between files/services |
| Does this hide complexity or just move it? | Hides behind simple interface | Adds indirection without simplification |
| What happens when requirements change? | Change localized to one area | Ripples across multiple modules/services |
| Could a simpler approach achieve the same goal? | This IS the simple approach | "We might need this flexibility later" |
| Will this feel simple to someone who didn't write it? | Yes, follows standard patterns | Requires learning project-specific conventions |

---

## Scoring Guide

After reviewing, assign an overall cognitive load score:

### Low (Target)
- New developer productive within minutes
- Code reads linearly, top to bottom
- Few abstractions, each earning its keep
- Standard patterns, no project-specific conventions to learn

### Moderate (Acceptable)
- Some patterns require context to understand
- New developer productive within one session
- Abstractions mostly justified
- Minor areas of unnecessary complexity

### High (Needs Work)
- Multiple mental models required simultaneously
- New developer needs days to become productive
- Abstractions add indirection without clear benefit
- Framework knowledge required to understand business logic

### Severe (Architectural Issue)
- Architecture itself is the primary source of complexity
- New developer needs weeks to onboard
- Changes routinely cascade across boundaries
- Team velocity decreasing over time despite stable requirements

---

## Red Flags (Immediate Action)

If you see any of these, flag immediately:

1. **Nesting depth > 3**: Almost always fixable with early returns
2. **Function > 80 lines**: Split is almost certainly beneficial
3. **Inheritance > 2 levels**: Composition refactor needed
4. **"It's how the framework does it"**: Business logic likely coupled to framework
5. **Shared mutable state across modules**: Race conditions AND cognitive load
6. **12+ files touched for one feature**: Boundaries drawn incorrectly
7. **"You need to understand X, Y, and Z before reading this"**: Extraneous load
