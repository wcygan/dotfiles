# Spike Team Reference Guide

## Spike Report Template

```markdown
# Spike: [Topic]

**Date**: YYYY-MM-DD
**Duration**: X hours
**Team**: investigator-1, investigator-2, api-designer, devils-advocate, tech-lead

## Executive Summary

[2-3 sentences: What we explored, what we recommend, why]

## Approaches Investigated

### Approach A: [Name]

**Investigator**: [name]
**Effort**: [S/M/L/XL]
**Dependencies**: [list new deps]

**Pros**:
- Point 1
- Point 2

**Cons**:
- Point 1
- Point 2

**PoC**: [link or code snippet]

### Approach B: [Name]

[Same structure as A]

### Approach C: [Name] (optional)

[Same structure as A]

## Comparison Matrix

| Criterion | Approach A | Approach B | Approach C |
|-----------|------------|------------|------------|
| Effort | M | S | L |
| Dependencies | 2 new | 0 new | 5 new |
| Complexity | Medium | Low | High |
| Performance | Fast | Moderate | Fastest |
| Maintainability | Good | Excellent | Poor |
| Risk | Low | Low | Medium |

## Interface Evaluation

**API Designer Assessment**:
- Ergonomics: [comparison]
- Integration: [impact on existing code]
- Developer experience: [learning curve, debugging]

## Simplicity Challenge

**Devils Advocate Questions**:
- Do we need this? [answer]
- Simplest alternative: [description]
- Can we defer this? [yes/no + rationale]

## Recommendation

**Chosen Approach**: [A/B/C or minimal alternative]

**Rationale**:
1. [Key reason 1]
2. [Key reason 2]
3. [Key reason 3]

**Implementation Plan**:
1. Step 1 (effort: X)
2. Step 2 (effort: Y)
3. Step 3 (effort: Z)

**Total Estimated Effort**: [S/M/L/XL]

## Rollback Strategy

If chosen approach fails:
1. [Immediate rollback steps]
2. [Fallback to approach X]
3. [Risk mitigation]

## Next Steps

- [ ] Action 1 (owner: X)
- [ ] Action 2 (owner: Y)
- [ ] Action 3 (owner: Z)

## Appendix

### Prototype Code

[Links to PoC branches/commits]

### Research References

- [Source 1]
- [Source 2]
```

## Effort Estimation Scale

| Size | Time | Complexity | Risk |
|------|------|------------|------|
| **S** (Small) | 1-4 hours | Single file, straightforward | Low |
| **M** (Medium) | 1-2 days | Multiple files, some unknowns | Low-Medium |
| **L** (Large) | 3-5 days | Cross-cutting, new patterns | Medium |
| **XL** (Extra Large) | 1-2 weeks | Architectural change | High |

**Factors to consider**:
- Learning curve (new tools/patterns)
- Integration points (how many systems touched)
- Testing complexity (unit/integration/e2e)
- Documentation needs
- Code review cycles

## Investigation Checklist

Per approach, investigators should:

- [ ] **Research** existing implementations
  - GitHub repos using this pattern
  - Library documentation
  - Known issues/limitations

- [ ] **Prototype** minimal proof of concept
  - Core functionality only
  - 50-150 lines of code
  - Runnable demo/test

- [ ] **Document** dependencies
  - New packages required
  - Version constraints
  - Build tool changes

- [ ] **Identify** edge cases
  - Error scenarios
  - Performance bottlenecks
  - Platform differences

- [ ] **Estimate** effort
  - Use S/M/L/XL scale
  - Include testing + docs
  - Factor in team experience

## Comparison Criteria

Standard dimensions for comparison matrix:

1. **Effort**: S/M/L/XL implementation time
2. **Dependencies**: Number/weight of new dependencies
3. **Complexity**: Cognitive load for team
4. **Performance**: Runtime/build time impact
5. **Maintainability**: Long-term code health
6. **Risk**: Likelihood of issues/blockers
7. **Reversibility**: Can we easily undo this?
8. **Team Familiarity**: Existing expertise

Add domain-specific criteria as needed (e.g., security, accessibility, i18n).

## Time Boxing Guidelines

### 2-Hour Spike (minimal)
- 2 approaches
- 45 min per investigation
- 15 min synthesis
- High-level comparison only

### 3-Hour Spike (standard)
- 2-3 approaches
- 60-75 min per investigation
- 30 min synthesis
- Detailed PoCs + docs

### 4-Hour Spike (deep)
- 3 approaches
- 90 min per investigation
- 45 min synthesis
- Production-ready prototypes

**Hard stop at 4 hours**: Synthesize with incomplete data rather than extending scope.

## Red Flags

Stop spike early if:
- All approaches clearly inferior to status quo
- One approach obviously dominant (no need to explore others)
- Fundamental blocker discovered (pivot focus)
- Scope creep beyond original question

## Output Artifacts

Required deliverables:
1. **Spike report** (markdown doc)
2. **PoC code** (branches/commits)
3. **Comparison matrix** (in report)
4. **Recommendation** (with rationale)

Optional:
- Presentation slides (for broader team)
- Migration guide (if recommending change)
- Benchmark results (if performance-critical)

## Example Topics

- "Choosing state management library (Redux vs Zustand vs Jotai)"
- "Database migration strategy (Blue-Green vs Shadow vs Dual-Write)"
- "Auth implementation (OAuth library vs roll-our-own vs managed service)"
- "Testing framework migration (Jest → Vitest)"
- "Build tool evaluation (Webpack vs Vite vs Turbopack)"
