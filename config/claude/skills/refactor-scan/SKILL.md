---
name: refactor-scan
description: Scan code for refactoring opportunities to improve modularity, testability, extensibility, reusability, understandability, and cognitive complexity. Use when reviewing code quality, identifying technical debt, planning a refactor, or improving code structure. Keywords: refactor, refactoring, code quality, modularity, testability, extensibility, reusability, cognitive complexity, code smell, clean code, SOLID, DRY, coupling, cohesion
disable-model-invocation: true
argument-hint: [path-or-file]
---

Analyze the code at `$ARGUMENTS` (or the current working directory if no argument given) and identify refactoring opportunities that improve:

- **Modularity**: Components are loosely coupled and highly cohesive
- **Testability**: Code is easy to test in isolation
- **Extensibility**: Easy to add new features without modifying existing code
- **Reusability**: Components can be used in different contexts
- **Understandability**: Code is clear and self-documenting
- **Cognitive Complexity**: Reduced mental overhead to comprehend logic

# Analysis Framework

## 1. Modularity Assessment

**Check for:**
- High coupling between components (shared mutable state, deep dependencies)
- Low cohesion (modules doing multiple unrelated things)
- Missing abstraction boundaries
- God objects/classes doing too much
- Circular dependencies

**Suggest:**
- Extract interfaces/traits for dependency injection
- Break large modules into focused components
- Apply facade pattern for complex subsystems
- Use dependency inversion (depend on abstractions, not concretions)

## 2. Testability Issues

**Check for:**
- Hard-coded dependencies (direct instantiation of collaborators)
- Static/global state access
- Complex setup requirements
- Untestable side effects (I/O, time, randomness)
- Missing seams for test doubles

**Suggest:**
- Constructor injection for dependencies
- Extract and inject side effects (clock, random, I/O)
- Separate pure logic from effects
- Apply ports and adapters architecture
- Add factory methods for object creation

## 3. Extensibility Barriers

**Check for:**
- Switch/case statements on types (closed for extension)
- Hard-coded algorithms (no strategy injection)
- Tight coupling to concrete implementations
- Missing plugin points
- Violation of Open/Closed Principle

**Suggest:**
- Replace conditionals with polymorphism
- Apply strategy pattern for varying algorithms
- Use template method for extension points
- Create hooks/callbacks for customization
- Introduce builder pattern for complex construction

## 4. Reusability Blockers

**Check for:**
- Business logic mixed with presentation/infrastructure
- Assumptions about execution context
- Hard-coded configuration values
- Platform-specific code without abstraction
- Duplicate code across modules

**Suggest:**
- Extract pure business logic to core layer
- Parameterize context-specific behavior
- Externalize configuration
- Abstract platform-specific operations
- Create shared utility functions/modules
- Apply DRY principle with careful abstraction

## 5. Understandability Problems

**Check for:**
- Long methods/functions (>20-30 lines)
- Deep nesting (>3 levels)
- Poor naming (abbreviations, unclear intent)
- Magic numbers/strings
- Missing documentation for non-obvious behavior
- Complex boolean expressions

**Suggest:**
- Extract methods with intention-revealing names
- Use guard clauses to reduce nesting
- Rename variables/functions for clarity
- Extract constants with descriptive names
- Add docstrings for public APIs
- Apply De Morgan's laws to simplify conditionals
- Use early returns to flatten logic

## 6. Cognitive Complexity Reduction

**Check for:**
- High cyclomatic complexity (many execution paths)
- Nested loops and conditionals
- Multiple responsibilities in one unit
- Inconsistent abstraction levels
- Hidden control flow (exceptions for flow control)

**Suggest:**
- Break complex functions into simpler steps
- Extract nested loops to separate functions
- Apply Single Responsibility Principle
- Keep abstraction levels consistent within method
- Use functional patterns (map, filter, reduce) where appropriate
- Replace exception handling with explicit error types

# Output Format

For each refactoring opportunity found:

```
## [PRIORITY] Category: Brief Description

**Location**: file.ext:line_number (or function/class name)

**Current State:**
```language
// Show problematic code snippet
```

**Issue:**
Explain why this impacts the quality attributes (modularity, testability, etc.)

**Refactoring Approach:**
```language
// Show improved code example
```

**Benefits:**
- ✓ Quality attribute 1 improved (explain how)
- ✓ Quality attribute 2 improved (explain how)

**Effort**: Small / Medium / Large

**Risk**: Low / Medium / High

---
```

# Priority Levels

- 🔴 **High**: Major impediment to quality attributes, high impact
- 🟡 **Medium**: Noticeable improvement opportunity, moderate impact
- 🟢 **Low**: Nice-to-have improvement, polish

# Prioritization Strategy

1. **Quick wins**: High impact, low effort, low risk
2. **Strategic refactorings**: High impact, medium effort, medium risk
3. **Technical debt**: Medium impact, various effort levels
4. **Polish**: Low impact improvements

# Final Recommendations

Provide:
1. **Summary**: Count of findings by priority and category
2. **Suggested order**: Which refactorings to tackle first and why
3. **Testing strategy**: How to ensure refactorings don't break behavior
4. **Incremental approach**: How to break large refactorings into safe steps

# Guiding Principles

- Prefer composition over inheritance
- Favor immutability and pure functions
- Make illegal states unrepresentable
- Separate concerns (business logic, presentation, infrastructure)
- Code should read like well-written prose
- Optimize for change (make common changes easy)
- Leave code better than you found it
