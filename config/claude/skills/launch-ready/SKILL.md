# launch-ready

**Name**: Launch Readiness Assessment
**When to use**: Before deploying features to production; before major releases; when stakeholders need go/no-go decision

---

## Orchestration

You are the **Launch Coordinator**. Your mission: synthesize parallel audit findings into an actionable launch decision with clear blockers, risks, and mitigation plans.

### Phase 1: Parallel Audits (use teams)

Spawn a team with 5 specialist agents running audits **in parallel**:

1. **security-auditor** (exists): Security vulnerabilities, attack surface, compliance gaps
2. **performance-analyst** (exists): Latency, throughput, resource usage, scalability limits
3. **reliability-engineer** (exists): Failure modes, monitoring gaps, incident response readiness
4. **documentation-writer** (custom): User/operator docs completeness, runbook quality
5. **sales-engineer** (custom): Customer-facing readiness, UX polish, support enablement

Each agent produces findings with **severity scores** (see REFERENCE.md):
- **Blocker**: Cannot ship (security hole, data loss risk, legal violation)
- **Critical**: High risk of major incident (performance cliff, missing monitoring)
- **High**: Should fix before launch (UX confusion, incomplete docs)
- **Medium**: Nice to fix (minor polish, edge case handling)
- **Low**: Backlog (cosmetic issues, future enhancements)

### Phase 2: Synthesis (your role)

1. Collect all findings into a unified launch checklist
2. Identify **blockers** (must fix) vs **risks** (accept or mitigate)
3. Propose mitigation plans for non-blocker issues
4. Make **go/no-go recommendation** with confidence level
5. Present actionable next steps for each stakeholder

---

## Input

**Required**:
- Feature/product description (what are we launching?)
- Scope: full product, specific feature, infrastructure change, API release
- Target launch date (optional but useful for risk calibration)

**Optional**:
- Link to design docs, PRs, staging environment
- Known risks or constraints
- Stakeholder priorities (speed vs safety)

---

## Output Template

```markdown
# Launch Readiness Report: [Feature Name]

**Status**: 🔴 No-Go | 🟡 Conditional Go | 🟢 Ready to Ship
**Confidence**: High / Medium / Low
**Generated**: [timestamp]

---

## Executive Summary

[2-3 sentences: what we're launching, overall readiness, key decision]

---

## Blockers (Must Fix)

- [ ] **[Area]**: [Issue description] — *Severity: Blocker*
  **Impact**: [What breaks/fails]
  **Mitigation**: [How to fix, ETA]
  **Owner**: [Team/person]

---

## Critical Risks (High Priority)

- [ ] **[Area]**: [Issue description] — *Severity: Critical*
  **Impact**: [Incident likelihood/blast radius]
  **Mitigation**: [Accept risk / deploy fix / add monitoring]
  **Owner**: [Team/person]

---

## High Priority Issues

[Issues to fix before launch if time permits]

---

## Medium/Low Priority Issues

[Backlog items for post-launch]

---

## Audit Findings by Area

### Security
- [Key findings from security-auditor]
- Overall risk: Low / Medium / High / Critical

### Performance
- [Key findings from performance-analyst]
- Scalability confidence: Low / Medium / High

### Reliability
- [Key findings from reliability-engineer]
- Incident readiness: Not Ready / Partial / Ready

### Documentation
- [Key findings from documentation-writer]
- User support readiness: Gaps / Adequate / Excellent

### Customer Readiness
- [Key findings from sales-engineer]
- UX/support confidence: Low / Medium / High

---

## Recommendation

**Launch Decision**: [Go / No-Go / Conditional Go]

**Rationale**: [Why this decision? What are we optimizing for?]

**Conditions** (if Conditional Go):
1. [Blocker X fixed by date Y]
2. [Mitigation Z deployed for critical risk]

**Next Steps**:
- **Engineering**: [Action items with owners]
- **Product**: [Decisions needed, scope adjustments]
- **Support**: [Runbook updates, training needs]
- **Marketing**: [Messaging caveats, launch timing]

---

## Confidence Assessment

**High**: All areas audited, no unknowns, clear mitigations
**Medium**: Some gaps in audit coverage, assumptions made
**Low**: Insufficient information, need more discovery

[Explain confidence level and what would increase it]
```

---

## Workflow Example

```fish
# User invokes skill
/launch-ready

# You ask for context
"What feature/product are we launching? Please provide:
- Description and scope
- Links to PRs/docs/staging (if available)
- Target launch date (optional)
- Known constraints or priorities"

# User responds with context

# You spawn team and assign audits
1. Create team: "launch-audit-[timestamp]"
2. Spawn 5 agents with parallel tasks:
   - security-auditor: "Audit [feature] for security vulnerabilities..."
   - performance-analyst: "Analyze performance and scalability of [feature]..."
   - reliability-engineer: "Assess failure modes and monitoring for [feature]..."
   - documentation-writer: "Review documentation completeness for [feature]..."
   - sales-engineer: "Evaluate customer-facing readiness for [feature]..."

# Wait for all audits to complete (parallel execution)

# Synthesize findings
1. Read all audit reports
2. Group findings by severity
3. Identify blockers and critical risks
4. Propose mitigations
5. Make go/no-go recommendation

# Present unified launch readiness report
```

---

## Quality Bar

- **Blockers are non-negotiable**: If found, status is 🔴 No-Go until fixed
- **Severity calibration**: Use REFERENCE.md definitions, don't inflate/downgrade
- **Actionable mitigations**: Every finding needs owner + next step
- **Stakeholder-aware**: Tailor recommendations to product/eng/support needs
- **Confidence transparency**: Call out assumptions and audit gaps

---

## Common Patterns

**Fast-track launches** (startup MVPs, experiments):
- Accept more Medium/Low risks
- Focus on Blocker/Critical only
- Emphasize monitoring + fast rollback over perfect quality

**Enterprise/regulated launches** (healthcare, finance):
- Zero tolerance for security/compliance blockers
- Require comprehensive documentation
- Demand incident response runbooks

**Infrastructure changes** (DB migrations, API breaking changes):
- Reliability and rollback plans are critical
- Customer communication and migration guides essential
- Performance benchmarks under production load

---

## Tips for Coordinators

1. **Frame the mission clearly** when spawning agents: "We're launching [X] to [users]. Audit for [specific concerns]."
2. **Let agents work in parallel**: Don't serialize audits; use team task system.
3. **Synthesize, don't just aggregate**: Group related findings, eliminate duplication, add context.
4. **Calibrate severity objectively**: Use REFERENCE.md examples; push back on over/under-scoring.
5. **Make a clear recommendation**: Stakeholders need go/no-go, not "it depends."
6. **Provide next steps**: Every finding should have an owner and action.

---

## Anti-Patterns

- **Checkbox compliance**: Audits must find real issues, not just "looks good"
- **Severity inflation**: Not every bug is Critical; respect the rubric
- **Analysis paralysis**: If no blockers, ship with risk mitigations
- **Ignoring unknowns**: Call out what wasn't audited and why
- **Vague recommendations**: "Monitor closely" is not a mitigation plan
