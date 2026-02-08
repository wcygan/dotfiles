# debt-audit

**Purpose**: Comprehensive technical debt inventory with ROI-based prioritization

**Pattern**: Parallel domain audits → unified backlog with aging analysis

---

## Orchestration

You are the **tech-lead** coordinating a technical debt audit. Your mission:

1. **Spawn parallel auditors** (5 agents):
   - `refactoring-strategist`: Code quality debt (duplication, complexity, smells)
   - `performance-analyst`: Performance debt (bottlenecks, inefficiencies)
   - `security-auditor`: Security debt (vulnerabilities, outdated deps)
   - `test-strategist`: Test debt (coverage gaps, flaky tests)
   - `doc-strategist`: Documentation debt (missing/outdated docs)

2. **Each auditor produces**:
   ```markdown
   ## [Domain] Debt Items

   ### [Item Title]
   - **Impact**: High/Medium/Low (business/user/dev impact)
   - **Effort**: S/M/L/XL (small/medium/large/extra-large)
   - **Age**: X months (git log analysis)
   - **Location**: file:line references
   - **Description**: What's wrong and why it matters
   - **Remediation**: Concrete fix steps
   ```

3. **Calculate ROI score** for each item:
   ```
   ROI = (Impact Score) / (Effort Score)

   Impact: High=3, Medium=2, Low=1
   Effort: S=1, M=2, L=3, XL=4

   Priority tiers:
   - Critical: ROI ≥ 2.0 (high impact, low effort)
   - High:     ROI 1.0-2.0
   - Medium:   ROI 0.5-1.0
   - Low:      ROI < 0.5
   ```

4. **Age multiplier** (older debt gets priority boost):
   ```
   Age < 3mo:   1.0x
   Age 3-6mo:   1.1x
   Age 6-12mo:  1.25x
   Age > 12mo:  1.5x
   ```

5. **Synthesize final roadmap**:
   - Group by priority tier
   - Within tier, sort by adjusted ROI (base ROI × age multiplier)
   - Include quick wins section (High impact, S effort)
   - Flag critical blockers (security/performance issues blocking features)

---

## Workflow

```fish
# 1. Spawn team
spawnTeam("debt-audit", "tech-lead")

# 2. Create audit tasks (parallel)
for domain in [code, perf, security, test, docs]
    createTask(
        domain + "-audit",
        "Inventory all " + domain + " debt with impact/effort/age",
        agent=domain + "-specialist"
    )

# 3. Wait for all audits → aggregate results

# 4. Calculate ROI scores → prioritize

# 5. Produce final backlog report
```

---

## Output Format

````markdown
# Technical Debt Backlog

**Generated**: YYYY-MM-DD
**Total Items**: N
**Critical Items**: X (ROI ≥ 2.0)

---

## Executive Summary

- **Quick Wins**: X items (high impact, small effort) - recommend tackling first
- **Critical Blockers**: Y items blocking features/security
- **Oldest Debt**: Item Z (NN months old)

---

## Priority: CRITICAL (ROI ≥ 2.0)

### [Item Title] (ROI: 3.0, Age: 8mo)
- **Domain**: Code Quality
- **Impact**: High - causes 40% of customer bugs
- **Effort**: S (2 days)
- **Location**: `src/core/parser.ts:145-200`
- **Fix**: Refactor nested conditionals into strategy pattern
- **Dependencies**: None

[... more critical items ...]

---

## Priority: HIGH (ROI 1.0-2.0)

[... high priority items ...]

---

## Priority: MEDIUM (ROI 0.5-1.0)

[... medium priority items ...]

---

## Priority: LOW (ROI < 0.5)

[... low priority items, consider deferring ...]

---

## Debt Distribution

- **Code Quality**: X items (Y% of total)
- **Performance**: X items
- **Security**: X items
- **Test Coverage**: X items
- **Documentation**: X items

---

## Recommended Action Plan

1. **Sprint 1**: All Critical items (Est: N days)
2. **Sprint 2**: High-priority quick wins
3. **Ongoing**: Allocate 20% capacity to Medium tier
4. **Re-audit**: Schedule next audit in 3 months
````

---

## Agent Instructions

### For Domain Auditors

When assigned an audit task:

1. **Scan codebase** for your domain:
   - Use `rg`, `fd`, static analysis tools
   - Check for patterns/anti-patterns
   - Review recent bug reports related to your domain

2. **Assess age** for each item:
   ```bash
   # Find when problematic code was introduced
   git log -p --all -S "pattern" -- path/to/file
   # or blame for specific lines
   git blame -L start,end path/to/file
   ```

3. **Score honestly**:
   - Impact: Would fixing this improve user/dev experience significantly?
   - Effort: Realistic estimate (S=1-2d, M=3-5d, L=1-2w, XL=>2w)

4. **Provide context**:
   - Why is this debt? (rushed deadline, evolving requirements, lack of knowledge)
   - What's the risk of NOT fixing? (accumulates interest, blocks features)

5. **Report findings** to tech-lead via message

### For Tech-Lead

1. **Coordinate audits**: Spawn agents, assign tasks, monitor progress
2. **Aggregate results**: Collect all domain reports
3. **Calculate scores**: Apply ROI formula + age multiplier
4. **Resolve conflicts**: If items overlap domains, merge/deduplicate
5. **Produce report**: Final backlog with actionable recommendations
6. **Present to user**: Clear executive summary + detailed breakdown

---

## Success Criteria

- [ ] All 5 domains audited thoroughly
- [ ] Every debt item has impact/effort/age/location
- [ ] ROI scores calculated consistently
- [ ] Backlog sorted by adjusted priority
- [ ] Quick wins identified (≥3 items recommended for immediate action)
- [ ] Report is actionable (clear next steps)

---

## Notes

- **Debt is not failure** - it's a tradeoff. The goal is visibility and prioritization.
- **Age matters** - old debt has more context loss, harder to fix later
- **ROI is a guide** - use judgment for strategic items (e.g., security always critical)
- **Re-audit regularly** - debt grows; quarterly audits prevent accumulation
