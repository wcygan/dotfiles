# Architecture Review Reference

Detailed review checklists, RFC template, and debate facilitation guide for the `/arch-review` skill.

## RFC Template (for proposal authors)

When creating a proposal for architecture review, use this template:

```markdown
# RFC-XXX: [Title]

**Status**: Draft | In Review | Approved | Rejected
**Author**: [name]
**Created**: [date]
**Reviewers**: [assigned when review starts]

## Summary

[2-3 sentences: What are we proposing and why?]

## Motivation

### Problem
[What problem are we solving? What's broken or missing?]

### Why Now
[Why is this important right now? What's the cost of delay?]

### Success Criteria
[How do we know this worked? Measurable outcomes.]

## Proposal

### High-Level Design
[Architecture diagram, component overview, data flow]

### Detailed Design
[Specifics: APIs, data models, interfaces, protocols]

### Migration Path
[How do we get from current state to proposed state? Rollback plan?]

## Alternatives Considered

### Alternative 1: [Name]
**Pros**: [advantages]
**Cons**: [disadvantages]
**Why not**: [reason for rejection]

### Alternative 2: [Name]
...

### Do Nothing
**Pros**: No migration cost
**Cons**: [what we lose by not doing this]
**Why not**: [why status quo is insufficient]

## Trade-offs

### [Trade-off 1: e.g., Complexity vs Flexibility]
[Explain the trade-off and which side we're choosing]

### [Trade-off 2]
...

## Dependencies

**Upstream**: [What needs to happen before this? Blocking dependencies?]
**Downstream**: [What will this unblock? What breaks if we do this?]

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | High/Med/Low | High/Med/Low | [How we handle it] |

## Open Questions

1. [Unresolved questions requiring input]
2. [...]

## Appendix

[Supporting material: benchmarks, research, prototypes, examples]
```

## Agent Review Checklists

Each agent should use these lenses when reviewing a proposal. Agents can adapt the checklist to the specific proposal context.

### Tech Lead Review Checklist

**Perspective**: Senior technical leadership, architecture coherence, team impact

#### Architecture Quality
- [ ] Does this fit our existing architecture, or does it create inconsistency?
- [ ] Are the component boundaries clear and well-defined?
- [ ] Does it introduce new patterns, or follow established ones?
- [ ] Is the abstraction level appropriate (not over-engineered, not too specific)?
- [ ] Are failure domains properly isolated?

#### Team Impact
- [ ] Do we have the skills to build and maintain this?
- [ ] What's the learning curve for the team?
- [ ] How does this affect onboarding new engineers?
- [ ] Does it increase or decrease cognitive load?

#### Maintainability
- [ ] Can we debug this in production?
- [ ] Is the design testable?
- [ ] How hard is it to change later?
- [ ] Does it reduce or increase technical debt?
- [ ] Are there clear ownership boundaries?

#### Strategic Fit
- [ ] Does this align with long-term technical direction?
- [ ] Are we solving the right problem?
- [ ] Is the scope appropriate, or should it be split?
- [ ] What doors does this open or close for the future?

#### Deliverability
- [ ] Is the migration path realistic?
- [ ] Can we ship this incrementally?
- [ ] What's the rollback plan?
- [ ] Are the risks proportional to the value?

**Output**: Approve / Approve with conditions / Reject, with reasoning focused on architecture coherence and team impact.

---

### Security Auditor Review Checklist

**Perspective**: Threat modeling, attack surface, security implications

#### Threat Model
- [ ] What's the trust boundary? What crosses it?
- [ ] Who are the potential attackers? What are their capabilities?
- [ ] What's the worst-case scenario if this is compromised?
- [ ] Does this expand or reduce our attack surface?

#### Authentication & Authorization
- [ ] How is identity established? Any authentication weaknesses?
- [ ] Are authorization checks consistent and complete?
- [ ] Can users access data they shouldn't?
- [ ] Are there privilege escalation paths?
- [ ] How are service-to-service calls authenticated?

#### Data Protection
- [ ] Is sensitive data encrypted at rest and in transit?
- [ ] Are secrets managed properly (no hardcoding, using secret manager)?
- [ ] Is PII handled according to privacy requirements?
- [ ] Are there data leakage risks (logs, errors, debugging output)?
- [ ] Is data sanitized before logging?

#### Input Validation
- [ ] Are all external inputs validated?
- [ ] Are there injection risks (SQL, command, XSS, template)?
- [ ] Is there proper output encoding/escaping?
- [ ] Are file uploads handled safely?
- [ ] Are API rate limits enforced?

#### Dependencies
- [ ] Do new dependencies have known vulnerabilities?
- [ ] Are dependencies from trusted sources?
- [ ] Is the supply chain risk acceptable?
- [ ] Are dependency versions pinned?

#### Operational Security
- [ ] Does this require new secrets or credentials?
- [ ] Are there security-relevant logs for monitoring?
- [ ] Can we detect and respond to attacks?
- [ ] Are there security implications for the deployment process?

**Output**: Security risk rating (Critical/High/Medium/Low), specific vulnerabilities found, required mitigations.

---

### Performance Analyst Review Checklist

**Perspective**: Scalability, efficiency, resource usage, latency

#### Scalability
- [ ] How does this scale with data volume?
- [ ] How does this scale with concurrent users?
- [ ] Are there bottlenecks in the design?
- [ ] Can we scale horizontally, or are we limited to vertical scaling?
- [ ] What breaks first under load?

#### Latency
- [ ] What's the expected latency for common operations?
- [ ] Are there unnecessary round-trips or blocking calls?
- [ ] Do we have timeout and deadline propagation?
- [ ] Are there opportunities for parallelization?
- [ ] Does this add latency to critical paths?

#### Resource Usage
- [ ] What are the CPU, memory, disk, network requirements?
- [ ] Are there memory leaks or unbounded growth risks?
- [ ] Is caching used effectively?
- [ ] Are there expensive computations that could be precomputed?
- [ ] Can we batch operations to reduce overhead?

#### Database Performance
- [ ] Are queries efficient? Any N+1 problems?
- [ ] Are indexes appropriate?
- [ ] Do we avoid full table scans?
- [ ] Is pagination used for large result sets?
- [ ] Are there connection pooling or transaction issues?

#### Efficiency
- [ ] Are algorithms appropriate for the problem size?
- [ ] Do we minimize data copying?
- [ ] Are there obvious inefficiencies?
- [ ] Can we use streaming instead of buffering?
- [ ] Are there opportunities for lazy evaluation?

#### Benchmarking
- [ ] Are there benchmarks or load tests?
- [ ] What are the SLOs/SLAs for this component?
- [ ] Have we tested under realistic load?
- [ ] What's the resource cost per request?

**Output**: Performance risk rating, bottlenecks identified, optimization recommendations, acceptable cost/benefit trade-offs.

---

### Reliability Engineer Review Checklist

**Perspective**: Failure modes, observability, operational complexity, resilience

#### Failure Mode Analysis
- [ ] What can go wrong? What are the failure modes?
- [ ] How does this fail? Gracefully or catastrophically?
- [ ] What's the blast radius of a failure?
- [ ] Are failure domains properly isolated?
- [ ] Can a failure cascade to other components?

#### Error Handling
- [ ] Are errors handled consistently?
- [ ] Do we retry transient failures appropriately?
- [ ] Are there circuit breakers for failing dependencies?
- [ ] Do we avoid masking errors?
- [ ] Is error context preserved for debugging?

#### Resilience Patterns
- [ ] Are timeouts set on all external calls?
- [ ] Do we have bulkheads to limit resource exhaustion?
- [ ] Is there backpressure handling?
- [ ] Can we degrade gracefully if dependencies fail?
- [ ] Are there health checks for all components?

#### Observability
- [ ] Can we tell if this is working correctly in production?
- [ ] Are there metrics for golden signals (latency, traffic, errors, saturation)?
- [ ] Is logging sufficient for debugging?
- [ ] Are there distributed traces for request flow?
- [ ] Can we set meaningful alerts?

#### Operational Complexity
- [ ] How hard is this to deploy?
- [ ] What's the deployment risk?
- [ ] Do we need new operational runbooks?
- [ ] How do we troubleshoot this in production?
- [ ] What new failure modes does this introduce?

#### Data Integrity
- [ ] How do we handle data inconsistency?
- [ ] Are there data validation checks?
- [ ] Can we detect and recover from corruption?
- [ ] Is there a backup and restore strategy?
- [ ] How do we handle schema migrations?

#### Incident Response
- [ ] Can we rollback quickly if needed?
- [ ] Are there manual override mechanisms?
- [ ] Do we have sufficient access to debug in production?
- [ ] Are there automated remediation options?

**Output**: Reliability risk rating, failure modes, missing resilience patterns, operational readiness assessment.

---

### Devils Advocate Review Checklist

**Perspective**: Necessity, simplicity, hidden assumptions, alternative approaches

#### Necessity
- [ ] Do we actually need this?
- [ ] What happens if we do nothing?
- [ ] Is this solving the root cause or treating symptoms?
- [ ] Are we building this because it's interesting, or because it's necessary?
- [ ] Can we achieve 80% of the value with 20% of the complexity?

#### Assumptions
- [ ] What unstated assumptions is this based on?
- [ ] Are those assumptions valid? How do we know?
- [ ] What happens if those assumptions change?
- [ ] Are we solving today's problem or tomorrow's?
- [ ] Are we over-optimizing for a rare case?

#### Complexity
- [ ] Is this the simplest solution?
- [ ] Can we solve this with existing tools/systems?
- [ ] Are we adding more moving parts than necessary?
- [ ] Will this make the system harder to reason about?
- [ ] Are we introducing accidental complexity?

#### Alternatives
- [ ] Could we use an off-the-shelf solution instead of building?
- [ ] Could we use a simpler architecture pattern?
- [ ] Could we defer this decision until we have more information?
- [ ] Could we do a smaller version first to validate assumptions?
- [ ] What's the "boring" way to solve this?

#### Scope Creep
- [ ] Is the scope well-defined, or is it growing?
- [ ] Are there "nice to have" features that could be cut?
- [ ] Can we ship an MVP and iterate?
- [ ] Are we solving multiple problems at once?
- [ ] Should this be split into phases?

#### Cost-Benefit
- [ ] What's the cost in engineering time?
- [ ] What's the ongoing maintenance burden?
- [ ] What's the opportunity cost (what aren't we building)?
- [ ] Is the value proportional to the cost?
- [ ] Have we quantified the benefit?

#### Reversibility
- [ ] If this doesn't work out, can we undo it?
- [ ] Are we creating lock-in?
- [ ] Can we experiment cheaply before committing?
- [ ] Is there a safe way to validate this incrementally?

**Output**: Challenge the premise, identify hidden assumptions, propose simpler alternatives, question necessity.

## Debate Facilitation Guide

The team lead (or skill orchestrator) should facilitate the debate using this structure.

### Phase 1: Opening Statements (Round 1)

**Format**: Each agent gets 1-2 minutes to state their key concern.

**Facilitation**:
- Call on each agent in order: tech-lead → security → performance → reliability → devils-advocate
- Ask: "What's your biggest concern with this proposal?"
- Keep it concise — just the headline, not full analysis yet

**Example**:
```
security-auditor: "The biggest concern is the expanded attack surface from exposing this API publicly without rate limiting."
performance-analyst: "I'm worried about the O(n²) query pattern in the proposal that won't scale past 10k users."
```

### Phase 2: Trade-off Discussion (Rounds 2-4)

**Format**: Identify the top 3 conflicts across reviews and discuss each one.

**How to identify conflicts**:
- Look for agent disagreements (e.g., security wants encryption, performance warns of cost)
- Find trade-offs where we must choose (e.g., consistency vs availability)
- Spot different priorities (e.g., simplicity vs flexibility)

**Facilitation per trade-off**:
1. **State the conflict**: "security-auditor wants X, but performance-analyst warns Y"
2. **Ask each side to clarify**: "security-auditor, why is X critical? performance-analyst, how bad is Y?"
3. **Ask for middle ground**: "Is there a way to get most of X without too much Y?"
4. **Ask other agents to weigh in**: "tech-lead, reliability-engineer, how do you think about this trade-off?"
5. **Push for recommendation**: "What's the concrete recommendation? How do we resolve this?"

**Example exchange**:
```
Facilitator: "Security wants all data encrypted at rest, but performance warns this adds 30% latency. Security, why is this critical?"

security-auditor: "We handle PII, and regulatory requirements mandate encryption. Non-negotiable."

performance-analyst: "Understood. Can we encrypt only PII columns instead of entire database? That reduces latency impact to 5%."

security-auditor: "Yes, that works if we ensure column-level encryption is properly configured."

reliability-engineer: "Just flagging: column-level encryption complicates backups. We'll need to update our restore procedures."

Facilitator: "Sounds like column-level encryption is the resolution. Tech-lead, does that fit the design?"

tech-lead: "Yes, we can use database-native column encryption. I'll add that as a condition."
```

### Phase 3: Alternative Exploration (Round 5)

**Format**: Devils-advocate presents simpler alternatives, team responds.

**Facilitation**:
- Ask devils-advocate: "What's the simplest way to solve the underlying problem?"
- Have devils-advocate present 1-2 alternatives
- Ask each agent: "Would this simpler approach work from your perspective?"
- Look for legitimate simplifications vs. oversimplifications

**Example**:
```
devils-advocate: "Instead of building a new notification service, could we use AWS SNS? We'd avoid all this custom infrastructure."

tech-lead: "SNS doesn't support the retry logic we need for critical notifications."

devils-advocate: "Could we add retry logic in the consumer instead of the service?"

reliability-engineer: "That pushes complexity to every consumer. Better to centralize it."

devils-advocate: "Fair. What if we use SNS for non-critical notifications and keep the custom service only for critical ones?"

tech-lead: "That's worth considering. Smaller scope, less risk."
```

### Phase 4: Consensus Building (Round 6)

**Format**: Identify what the team agrees on.

**Facilitation**:
- Ask: "What do we all agree on?"
- List consensus points
- Ask: "What's still contentious?"
- For contentious points: can we defer, test with a prototype, or gather more data?

**Example**:
```
Facilitator: "Let's identify consensus points."

Team agrees:
- We need better notification reliability (all agents agree)
- Current system is insufficient (all agents agree)
- Column-level encryption is acceptable (security + performance agree)

Still contentious:
- Whether to build vs. buy (devils-advocate vs. tech-lead)
- Whether to support webhooks (performance warns cost, reliability wants it)

Resolution:
- Condition for approval: prototype webhook performance before full build
- Defer build vs. buy decision until we evaluate one commercial option
```

### Phase 5: Final Positions (Round 7)

**Format**: Each agent gives final recommendation.

**Facilitation**:
- Ask each agent: "Based on the discussion, what's your final position: Approve, Approve with conditions, or Reject?"
- For conditional approvals: "What are your must-have conditions?"
- For rejections: "What alternative do you recommend?"

**Example**:
```
tech-lead: "Approve with conditions: (1) use column-level encryption, (2) prototype webhooks first."
security-auditor: "Approve with conditions: (1) column-level encryption, (2) rate limiting on public API."
performance-analyst: "Approve with conditions: (1) fix the O(n²) query, (2) validate webhook performance."
reliability-engineer: "Approve with conditions: (1) add health checks, (2) define SLOs before launch."
devils-advocate: "Conditional approval: evaluate AWS EventBridge as alternative before building."
```

**Tally**: 5 conditional approvals, 0 rejections.

**Outcome**: Proposal approved pending 5 conditions being met.

### Debate Anti-Patterns

**Avoid**:
- Letting debate run indefinitely — time-box to 7 rounds
- Allowing groupthink — push back if everyone agrees too quickly
- Focusing on trivial details — keep discussion on high-level trade-offs
- Letting one agent dominate — ensure all voices are heard
- Accepting "it depends" as a final answer — push for a decision

**Do**:
- Highlight and explore disagreements — that's where the value is
- Ask "why" repeatedly to get to root concerns
- Look for data that could resolve uncertainty
- Defer low-priority decisions to reduce scope
- Document dissenting opinions even if outvoted

## Example Decision Document

```markdown
# Architecture Review: Unified Notification Service

**Date**: 2026-02-08
**Reviewers**: tech-lead, security-auditor, performance-analyst, reliability-engineer, devils-advocate
**Proposal**: RFC-042 - Unified Notification Service

## Executive Summary

Proposal to build a unified notification service for email, SMS, and push notifications. Team **approves with 5 conditions**. Biggest trade-off: build custom service for retry logic vs. use managed service (AWS SNS/EventBridge). Team converged on custom build with reduced scope after devils-advocate pushed for alternatives.

## Recommendation

**Decision**: Approve with conditions
**Confidence**: Medium (conditions are testable and will increase to High)

**Conditions**:
1. Use column-level encryption for PII (security)
2. Fix O(n²) query pattern in notification history lookup (performance)
3. Add rate limiting to public webhook ingestion API (security)
4. Define SLOs and add health checks before production (reliability)
5. Evaluate AWS EventBridge as alternative and document decision (devils-advocate)

## Review Summary

### Consensus Points
- Current notification system is unreliable and inconsistent
- Centralized retry logic is better than consumer-side retry
- Column-level encryption acceptable trade-off
- Need better observability for notifications

### Key Trade-offs

#### Security vs Performance: Encryption Cost
- **security-auditor**: All data must be encrypted at rest (regulatory requirement)
- **performance-analyst**: Full database encryption adds 30% latency
- **Resolution**: Use column-level encryption for PII only (5% latency impact)

#### Build vs Buy: Custom Service vs Managed Solution
- **devils-advocate**: Use AWS SNS/EventBridge instead of building
- **tech-lead**: SNS lacks retry semantics we need, custom gives control
- **Resolution**: Build custom but with reduced scope; evaluate EventBridge for non-critical notifications

#### Flexibility vs Complexity: Webhook Support
- **reliability-engineer**: Webhooks increase operational complexity
- **performance-analyst**: Webhooks could create DoS risk without careful design
- **Resolution**: Prototype webhook performance before committing; make it optional in v1

### Dissenting Opinions

**devils-advocate** still believes the scope is too large and recommends:
- Evaluate AWS EventBridge more thoroughly (not just SNS)
- Consider building only the retry layer, use managed services for delivery
- Phase the rollout: start with email only, add SMS/push later

Team acknowledges this concern. Condition #5 addresses it.

### Questions Requiring Clarification
1. What are the target SLOs for each notification type? (reliability-engineer)
2. What's the expected notification volume at 12 months? (performance-analyst)
3. Do we need multi-region support in v1? (tech-lead)

## Detailed Findings

### Architecture (tech-lead)
- Design is sound with clear component boundaries
- Fits existing architecture well
- Migration path is incremental and safe
- Concern: webhook support adds complexity; recommend making it optional in v1
- **Recommendation**: Approve with condition to define SLOs

### Security (security-auditor)
- Attack surface increases with public webhook API
- Column-level encryption acceptable after discussion
- Missing rate limiting on webhook ingestion
- Secrets management looks good (using AWS Secrets Manager)
- **Recommendation**: Approve with conditions: (1) column encryption, (2) rate limiting

### Performance (performance-analyst)
- O(n²) query in notification history lookup will not scale
- Webhook endpoint could become a DoS vector without backpressure
- Caching strategy looks good
- Concern: no load testing planned
- **Recommendation**: Approve with conditions: (1) fix query, (2) load test webhooks

### Reliability (reliability-engineer)
- Retry logic is solid
- Missing health checks and SLOs
- Observability plan is good (metrics + traces)
- Concern: webhook delivery failures could cascade
- **Recommendation**: Approve with conditions: (1) health checks, (2) define SLOs

### Simplicity (devils-advocate)
- Scope is large; recommends phased rollout
- Alternative approach using EventBridge not fully explored
- Concerns about ongoing maintenance burden
- Acknowledge necessity but question timing
- **Recommendation**: Conditional approval pending EventBridge evaluation

## Action Items

### Before Approval
1. Implement column-level encryption for PII fields
2. Fix O(n²) query pattern (use pagination + indexing)
3. Add rate limiting to webhook API (token bucket, 100 req/min per client)
4. Define SLOs for each notification type
5. Evaluate AWS EventBridge and document decision

### Post-Approval
1. Add health check endpoints for all components
2. Set up alerts for SLO violations
3. Load test webhook endpoint under realistic traffic
4. Create operational runbook for incident response
5. Plan phased rollout (email → SMS → push)

### If Rejected
1. Continue using existing per-service notification logic
2. Evaluate managed services (EventBridge, SNS, Twilio) more thoroughly
3. Consider smaller scope: just retry layer, not full service

## Appendix: Individual Reviews

[Full reviews from each agent would be included here]

---

**Approval Status**: Pending conditions being met
**Next Review**: After conditions addressed (estimated 2 weeks)
```

## Tips for Successful Reviews

### For Proposal Authors
- Include enough context in the RFC so agents have full information
- Explicitly state trade-offs you've already considered
- Include diagrams, data models, API contracts
- Document why alternatives were rejected
- Specify what you're uncertain about

### For the Orchestrator
- Give agents time to review independently before debate
- Don't let the debate drag on — 7 rounds max
- Focus on high-level trade-offs, not implementation details
- Push for concrete recommendations, not just analysis
- Document dissent even if it's a minority view
- Make conditions specific and testable

### For the Team
- Read the full proposal before reviewing
- Use your specific lens, don't try to cover everything
- Identify trade-offs, not just problems
- Propose solutions, not just critiques
- Update your position if persuaded during debate
- Be willing to say "approve" if conditions are met
