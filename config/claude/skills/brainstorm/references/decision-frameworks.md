---
title: Decision Frameworks
description: Structured frameworks for evaluating software architecture decisions
tags: [frameworks, ADR, pre-mortem, WWHTBT, ATAM, trade-off]
---

# Decision Frameworks

## 1. Architecture Decision Records (ADRs)

Introduced by Michael Nygard (2011). Document the context, decision, and consequences of each architectural choice.

**Key principles** (from AWS Architecture Blog):
- Keep concise: 1-2 pages, readable in 5 minutes
- Immutable: supersede rather than edit
- Collaborative: reviewed by affected teams (cap ~10 participants)
- Force articulation of rejected alternatives

**Template**:

```
# ADR-NNN: [Title]

## Status
Proposed | Accepted | Superseded by ADR-XXX

## Context
[What forces are at play? What constraints exist?]

## Decision
[What we decided to do and why]

## Alternatives Considered
### Option A: [Name]
- Pros: ...
- Cons: ...
- Why rejected: ...

### Option B: [Name]
...

## Consequences
### Positive
- ...
### Negative
- ...
### Risks
- ...

## Review Triggers
[Conditions that should cause us to revisit this decision]
```

Sources:
- https://adr.github.io/
- https://aws.amazon.com/blogs/architecture/master-architecture-decision-records-adrs-best-practices-for-effective-decision-making/
- https://www.infoq.com/articles/framework-architectural-decisions/

---

## 2. Pre-Mortem Analysis

Imagine the project has already failed and work backward to identify causes. Studies show ~30% improvement in risk identification over standard brainstorming.

**Process**:
1. Assume the decision was made and it's 6 months later
2. The project/feature has FAILED catastrophically
3. Each participant independently writes "why it failed"
4. Collect and categorize failure causes
5. Assess likelihood and create mitigations

**Pre-mortem checklist for software** (adapted from Josh Clemm):
- [ ] Scalability: Did it break at 10x load?
- [ ] Data integrity: Did we lose or corrupt data?
- [ ] Performance: Did latency become unacceptable?
- [ ] Security: Was there a breach or vulnerability?
- [ ] Developer experience: Did the team struggle to maintain it?
- [ ] Operational: Was it impossible to debug in production?
- [ ] Integration: Did it break other systems?
- [ ] Timeline: Did it take 3x longer than estimated?
- [ ] Adoption: Did users/developers not use it as intended?

Sources:
- https://joshclemm.com/writing/the-premortem-software-engineering-best-practice/
- https://medium.com/paypal-tech/pre-mortem-technically-working-backwards-1724eafbba02

---

## 3. WWHTBT (What Would Have to Be True)

Developed by Roger Martin. Transforms adversarial debate into collaborative inquiry.

**Process**:
1. List all options
2. For each option, ask: "What would have to be true about [our codebase / our team / our users / our timeline] for this to be the best choice?"
3. Test those conditions against reality
4. The option whose conditions are most likely true wins

**Example**:

```
Decision: Monolith vs microservices for new feature

Option A: Keep in monolith
WWHTBT:
- Team is small enough that coordination overhead of services exceeds benefit
- Feature is tightly coupled to existing data models
- Deployment frequency is acceptable as-is
- Performance requirements don't demand independent scaling

Option B: Extract to microservice
WWHTBT:
- Team will grow to need independent deployment
- Feature has genuinely different scaling characteristics
- API boundary between feature and monolith is clean
- Team has operational maturity for distributed systems
```

Source:
- https://rogermartin.medium.com/what-would-have-to-be-true-83dac5bd2189

---

## 4. ATAM (Architecture Tradeoff Analysis Method)

Developed by the Software Engineering Institute at Carnegie Mellon.

**Core concepts**:
- **Quality attribute scenarios**: Concrete, measurable descriptions of quality requirements (e.g., "Under 200ms response time at 1000 concurrent users")
- **Sensitivity points**: Where a small change in the architecture significantly affects a quality attribute
- **Tradeoff points**: Where satisfying one quality attribute negatively affects another
- **Risks**: Architectural decisions that may be problematic
- **Non-risks**: Decisions that are considered safe

**Simplified process for agent-assisted evaluation**:
1. Present the architecture approaches
2. Identify quality attribute scenarios (performance, availability, security, modifiability, etc.)
3. For each approach, analyze how well it satisfies each scenario
4. Identify sensitivity and tradeoff points
5. Catalog risks and non-risks

Source:
- https://www.sei.cmu.edu/library/architecture-tradeoff-analysis-method-collection/

---

## 5. Trade-off Matrix

A scoring approach for comparing options systematically.

**Template**:

| Quality Attribute | Weight | Option A | Option B | Option C |
|-------------------|--------|----------|----------|----------|
| Performance       | High   | 4        | 3        | 5        |
| Security          | High   | 5        | 4        | 3        |
| Maintainability   | Medium | 3        | 5        | 2        |
| Developer UX      | Medium | 4        | 4        | 3        |
| Operability       | Low    | 3        | 3        | 4        |
| Cost              | Low    | 4        | 3        | 2        |
| **Weighted Sum**  |        | **X**    | **Y**    | **Z**    |

**Weights**: High=3, Medium=2, Low=1
**Scores**: 1=Poor, 2=Below Average, 3=Average, 4=Good, 5=Excellent

**Important caveats**:
- Scores are subjective — make assumptions explicit
- Identify which weights would flip the decision (sensitivity analysis)
- Don't let the matrix make the decision — it structures the conversation
