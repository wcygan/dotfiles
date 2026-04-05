# Decision Document Template

The judge must produce exactly these 6 sections, in this order, in markdown. No extra sections, no omissions.

## Table of contents

- [Template](#template)
- [Section rules](#section-rules)
- [Example filled-in output](#example-filled-in-output)

## Template

```markdown
# Decision: {TOPIC}

## 1. Decision

{One of:
 - "Recommendation: {POSITION_LABEL}"
 - "No clear winner on axis: {AXIS_NAME}. The user must decide based on {AXIS_DESCRIPTION}."
}

## 2. Confidence

{low | medium | high}

{One sentence justifying the rating. High confidence requires the decision survives the losing side's best steelman.}

## 3. Key reasoning

- {3 to 5 bullets supporting the decision, each citing a concrete mechanism or trade-off}
- ...

## 4. Irreducible trade-offs

{At least 2 bullets. These are real costs of the recommendation that the decision does NOT resolve. If you cannot name 2, you have not engaged deeply enough with the losing positions.}

- {Trade-off 1}
- {Trade-off 2}
- ...

## 5. What would change this decision

{Concrete evidence, measurements, or conditions that would flip the recommendation. Must be specific enough to be checkable.}

- {Flip condition 1}
- {Flip condition 2}

## 6. Dissenting position

{One paragraph from the strongest losing side, written charitably — as that side's best advocate would write it. This is NOT a rebuttal; it is a fair statement of what the debate did not resolve for them.}
```

## Section rules

- **Section 1** — exactly one decision line. Not a summary, not a preamble.
- **Section 2** — the single word `low`, `medium`, or `high`, then a blank line, then one justification sentence. `High` requires the decision survives the losing side's Phase 3 steelman. Most honest outputs should be `medium`.
- **Section 3** — between 3 and 5 bullets. Fewer than 3 means the reasoning is too thin; more than 5 means the judge is not prioritizing.
- **Section 4** — **minimum 2 bullets required**, even when Section 1 recommends a clear winner. This is the minimum-disagreement quota: it prevents the judge from papering over tension.
- **Section 5** — each bullet must be a concrete, checkable condition, not a hedge. "If latency turns out to be a problem" is too vague. "If p99 read latency exceeds 50ms under expected load" is checkable.
- **Section 6** — write this as the losing side's best advocate would write it, not as a caricature or rebuttal. No "however" or "but actually." Full paragraph, not bullets.

## Example filled-in output

```markdown
# Decision: Monorepo vs polyrepo for a 6-person team

## 1. Decision

Recommendation: Monorepo

## 2. Confidence

Medium

The decision survives most of the polyrepo side's arguments, but hinges on the team staying under ~15 people; above that, the balance shifts.

## 3. Key reasoning

- Cross-service refactors are the dominant source of friction for teams this size, and a monorepo makes atomic cross-cuts trivial (one PR, one CI run, one revert)
- CI tooling (Bazel, Nx, Turborepo) has matured enough that selective builds are a solved problem for teams under ~50 engineers
- Dependency drift between services is the #1 incident category the polyrepo side admitted to in their own rebuttal
- Onboarding cost is visibly lower: one clone, one setup script, one place to search

## 4. Irreducible trade-offs

- Repository size grows unboundedly; clone time and editor performance degrade as a function of history, not current code size
- Access control is coarser — you cannot restrict one engineer to one service without additional tooling on top of git
- CI blast radius is larger: a bad change in one project can slow every other project's pipeline until reverted

## 5. What would change this decision

- If the team grows past ~15 engineers AND more than half work in language ecosystems with poor monorepo tooling
- If regulatory access-control requirements demand per-service permissions that cannot be approximated with code ownership
- If a measured 90-day period shows cross-service refactors accounting for less than 10% of merged PRs

## 6. Dissenting position

The polyrepo side's strongest argument is that repository boundaries create the clearest possible dependency contracts: if you cannot import it, you cannot depend on it, and every change that crosses a boundary is visible as an explicit version bump. This forces intentional interface design in a way a monorepo silently discourages. For teams that have been burned by implicit cross-module coupling in a shared codebase, this discipline is worth the coordination overhead — and the tooling cost of building a good monorepo CI is front-loaded in a way that a polyrepo distributes across the natural rhythm of service changes.
```
