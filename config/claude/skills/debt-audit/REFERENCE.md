# Technical Debt Audit Reference

Taxonomy, scoring rubrics, and calculation formulas for comprehensive debt assessment.

---

## Debt Taxonomy

### 1. Code Quality Debt

**Indicators**:
- **Duplication**: Repeated logic across files (DRY violations)
- **Complexity**: High cyclomatic complexity (>10), deep nesting (>4 levels)
- **Code smells**: Long functions (>50 lines), large classes (>300 lines), god objects
- **Naming**: Unclear variable/function names, abbreviations without docs
- **Dead code**: Unused functions, commented-out blocks, unreachable branches

**Impact examples**:
- High: Core business logic duplicated 5+ times, changes require 5-file edits
- Medium: Helper utils duplicated 2-3 times, increases bug surface
- Low: Minor duplication in test fixtures

**Common causes**: Rushed deadlines, lack of refactoring time, evolving understanding

---

### 2. Performance Debt

**Indicators**:
- **Algorithmic**: O(n²) loops, inefficient data structures
- **Database**: N+1 queries, missing indexes, full table scans
- **Memory**: Leaks, unbounded caches, large object retention
- **Network**: Excessive API calls, no batching/caching, large payloads
- **Rendering**: Unnecessary re-renders, blocking UI operations

**Impact examples**:
- High: User-facing page takes >5s to load, API times out under load
- Medium: Background job takes 10x longer than necessary
- Low: Admin tool is sluggish but rarely used

**Common causes**: Premature optimization avoided, scale exceeded original design

---

### 3. Security Debt

**Indicators**:
- **Vulnerabilities**: CVEs in dependencies (npm audit, cargo audit)
- **Authentication**: Weak password policies, missing 2FA, session issues
- **Authorization**: Missing access controls, privilege escalation risks
- **Data exposure**: Secrets in code, logs containing PII, insecure APIs
- **Outdated deps**: Libraries 2+ major versions behind, EOL packages

**Impact examples**:
- High: Critical CVE (CVSS >7), customer data at risk
- Medium: Non-exploited CVE, deprecated crypto algorithm
- Low: Dev dependency with low-severity issue

**Common causes**: Fast-moving threat landscape, upgrade complexity, lack of security review

**NOTE**: Security debt often scores High impact regardless of effort

---

### 4. Test Debt

**Indicators**:
- **Coverage gaps**: Critical paths untested, <70% line coverage
- **Flaky tests**: Non-deterministic failures, race conditions
- **Slow tests**: Test suite >10min, blocks CI/CD
- **Brittle tests**: Breaks on unrelated changes, over-mocked
- **Missing types**: E2E tests absent, no integration tests

**Impact examples**:
- High: No tests for payment flow, regressions reach production
- Medium: Flaky tests require 2-3 CI retries, slows velocity
- Low: Legacy module untested but rarely changed

**Common causes**: Tests seen as "extra work", legacy code too coupled to test

---

### 5. Documentation Debt

**Indicators**:
- **Missing docs**: No README, undocumented APIs, no architecture diagrams
- **Outdated docs**: Refers to removed features, wrong examples
- **Poor onboarding**: New devs take weeks to be productive
- **No runbooks**: Ops procedures tribal knowledge only
- **Inline docs**: Complex logic without comments, no docstrings

**Impact examples**:
- High: Zero docs for critical service, only 1 person knows how it works
- Medium: API docs lag reality, causes support tickets
- Low: Minor helper function lacks docstring

**Common causes**: Docs not required for PRs, async updates forgotten, seen as low priority

---

## Scoring Rubric

### Impact Score (Business/User/Developer Impact)

| Score | Label  | Business Impact | User Impact | Developer Impact |
|-------|--------|-----------------|-------------|------------------|
| 3     | High   | Revenue loss, legal risk, customer churn | Broken workflows, slow performance, security risk | Blocks features, causes frequent bugs, 50%+ dev time lost |
| 2     | Medium | Minor revenue impact, competitive disadvantage | Workarounds required, occasional failures | Slows development, tech decisions constrained |
| 1     | Low    | Negligible business impact | Minor UX degradation | Annoyance, slight velocity hit |

**High impact examples**:
- Payment processing has no error handling (business)
- Login page takes 8 seconds (user)
- Codebase so coupled that feature takes 3 weeks instead of 3 days (developer)

**Medium impact examples**:
- Admin report missing filters (business)
- Search results sometimes stale (user)
- Test suite takes 20 minutes (developer)

**Low impact examples**:
- Internal tool has ugly UI (business)
- Tooltip grammar error (user)
- Dev setup script has hardcoded path (developer)

---

### Effort Score (Time to Remediate)

| Score | Label        | Days  | Complexity | Risk |
|-------|--------------|-------|------------|------|
| 1     | Small (S)    | 1-2   | Isolated change, low risk | Safe refactor, good test coverage |
| 2     | Medium (M)   | 3-5   | Touches 2-3 modules, moderate risk | Requires careful testing, minor API changes |
| 3     | Large (L)    | 6-10  | Cross-cutting change, significant risk | May require feature flag, migration script |
| 4     | Extra-Large (XL) | 10+ | Architectural change, high risk | Phased rollout, backward compat required |

**Estimation tips**:
- Include time for: implementation, testing, code review, deployment, monitoring
- Add buffer for unknowns (20% for S/M, 50% for L/XL)
- Consider: team familiarity, dependency on other teams, data migration needs

**Small effort examples**:
- Extract duplicated function into shared util
- Add index to database table
- Update dependency version (no breaking changes)

**Medium effort examples**:
- Refactor class into smaller components
- Optimize N+1 query with eager loading
- Write missing integration tests for API

**Large effort examples**:
- Replace inefficient algorithm throughout codebase
- Migrate from deprecated auth library
- Add comprehensive error handling to service

**Extra-large effort examples**:
- Rewrite monolith service as microservices
- Replace ORM with different solution
- Comprehensive security hardening across stack

---

## ROI Calculation

### Base ROI Formula

```
ROI = Impact Score / Effort Score

Impact:  High=3, Medium=2, Low=1
Effort:  S=1, M=2, L=3, XL=4

Examples:
- High impact, Small effort:  3/1 = 3.0 (Critical priority)
- High impact, Large effort:  3/3 = 1.0 (High priority)
- Medium impact, Medium effort: 2/2 = 1.0 (High priority)
- Low impact, Large effort:   1/3 = 0.33 (Low priority)
```

---

### Age Multiplier

Older debt accumulates "interest" - becomes harder to fix over time:

| Age Range | Multiplier | Rationale |
|-----------|-----------|-----------|
| < 3 months | 1.0x | Recent, context fresh |
| 3-6 months | 1.1x | Context fading, some workarounds built around it |
| 6-12 months | 1.25x | Significant context loss, more code depends on it |
| > 12 months | 1.5x | Critical context loss, possibly blocking multiple features |

**Adjusted ROI** = Base ROI × Age Multiplier

**Example**:
```
Item: Duplicated validation logic in 5 places
- Impact: High (3) - causes 40% of bugs
- Effort: Medium (2) - extract to shared util
- Base ROI: 3/2 = 1.5
- Age: 8 months → 1.25x multiplier
- Adjusted ROI: 1.5 × 1.25 = 1.875 (High priority)
```

---

### Priority Tiers

| Tier     | Adjusted ROI | Action                          |
|----------|--------------|----------------------------------|
| Critical | ≥ 2.0        | Address immediately (current sprint) |
| High     | 1.0 - 2.0    | Schedule within 1-2 sprints      |
| Medium   | 0.5 - 1.0    | Add to backlog, allocate 20% capacity |
| Low      | < 0.5        | Defer or won't fix               |

**Special cases** (override calculated priority):
- Security: Any High impact security debt → Critical (regardless of effort)
- Blockers: Debt blocking planned features → bump one tier
- Quick wins: High impact + Small effort → flag for immediate attention
- Strategic: Debt preventing architectural goals → Tech leadership decides

---

## Aging Analysis

### Finding Age of Debt

```bash
# When was problematic code introduced?
git log --all --oneline --follow -- path/to/file.ts

# Specific line range
git blame -L 100,150 path/to/file.ts

# When was the anti-pattern first copied?
git log -p --all -S "antiPatternCode" | head -50

# Find oldest occurrence of smell
rg "TODO: fix this hack" -l | xargs -I {} git log --format="%ai {}" -- {} | sort | head -1
```

### Age Categories

- **Fresh debt** (<3mo): Recent shortcuts, possibly intentional technical tradeoffs
- **Accumulating debt** (3-6mo): Starting to cause friction, workarounds being built
- **Established debt** (6-12mo): Embedded in system, multiple dependencies
- **Ancient debt** (>12mo): High risk to fix, but also high cost to keep

**Report insight**:
```markdown
## Debt Age Distribution

- < 3 months:  X items (Y%)
- 3-6 months:  X items (Y%)
- 6-12 months: X items (Y%)
- > 12 months: X items (Y%) ← **Highest priority candidates**

Oldest debt: [Item Name] - **NN months old**
```

---

## Anti-Patterns to Watch For

### During Audit

- **Over-reporting**: Flagging every minor issue inflates backlog
- **Under-estimating effort**: "Quick fix" often requires testing, deployment, monitoring
- **Ignoring dependencies**: Item may seem isolated but touches many modules
- **Recency bias**: Recent debt more visible, but old debt more costly

### During Prioritization

- **Optimism bias**: "We'll fix this later" - schedule it or acknowledge it won't happen
- **Perfectionism**: Not all debt needs fixing; some is acceptable tradeoff
- **Analysis paralysis**: Don't spend more time auditing than fixing
- **Ignoring capacity**: Team can realistically handle 1-2 Large items per sprint

---

## Reporting Templates

### Executive Summary Template

```markdown
## Executive Summary

**Total Debt Items**: N
**Critical (ROI ≥ 2.0)**: X items - **recommend immediate attention**
**High (ROI 1.0-2.0)**: Y items - schedule in next 1-2 sprints
**Medium/Low**: Z items - backlog for future capacity

### Key Findings

1. **Security**: [X critical CVEs, Y outdated deps] - **URGENT**
2. **Performance**: [Slowest endpoint: /api/foo takes 8s] - user-facing impact
3. **Code Quality**: [5 areas of 3x+ duplication] - causing 40% of bugs
4. **Test Coverage**: [Payment flow has 0% coverage] - high-risk area
5. **Documentation**: [Core service has no runbook] - bus factor = 1

### Quick Wins (High Impact, Small Effort)

- [ ] [Item 1]: ROI 3.0, 2 days effort
- [ ] [Item 2]: ROI 2.5, 1 day effort
- [ ] [Item 3]: ROI 2.0, 2 days effort

**Recommendation**: Tackle quick wins this sprint, schedule Critical items for next sprint.
```

### Per-Item Template

```markdown
### [Concise Item Title] (ROI: X.X, Age: Xmo)

- **Domain**: Code Quality | Performance | Security | Test | Documentation
- **Impact**: High | Medium | Low
  - *Business*: [Revenue/legal/competitive impact]
  - *User*: [UX/performance/reliability impact]
  - *Developer*: [Velocity/maintainability impact]
- **Effort**: S | M | L | XL (X days)
- **Age**: X months (introduced YYYY-MM)
- **Location**: `path/to/file.ts:100-150`, `other/file.py:50`
- **Current State**: [What's wrong - be specific]
- **Why It Matters**: [Consequences if not fixed]
- **Remediation**:
  1. [Concrete step 1]
  2. [Concrete step 2]
  3. [Testing requirements]
- **Dependencies**: [Blocks/blocked by other items or features]
- **Risk**: [What could go wrong during fix]
```

---

## Example Debt Items

### High ROI Example (Critical Priority)

```markdown
### Duplicate Input Validation in 5 Controllers (ROI: 3.0, Age: 10mo)

- **Domain**: Code Quality
- **Impact**: High
  - *Business*: Inconsistent validation causes 40% of customer support tickets
  - *User*: Confusing error messages, some fields rejected incorrectly
  - *Developer*: Bug fix requires changing 5 files, often miss one
- **Effort**: S (2 days)
- **Age**: 10 months (introduced 2025-04)
- **Location**:
  - `src/controllers/user.ts:45-80`
  - `src/controllers/order.ts:120-155`
  - `src/controllers/payment.ts:30-65`
  - `src/controllers/profile.ts:90-125`
  - `src/controllers/settings.ts:200-235`
- **Current State**: Email/phone validation duplicated with slight variations
- **Why It Matters**: Each copy has subtle bugs, changes must be synchronized
- **Remediation**:
  1. Extract to `src/validators/input.ts`
  2. Write comprehensive tests for all edge cases
  3. Replace 5 call sites with shared util
  4. Add validation to schema layer (prevent future duplication)
- **Dependencies**: None
- **Risk**: Low - well-tested area, can deploy incrementally
```

**ROI Calculation**: Impact=3 (High), Effort=1 (S), Age=10mo → 3/1 × 1.5 = 4.5

---

### Low ROI Example (Defer)

```markdown
### Inconsistent Logging Format in Admin Tool (ROI: 0.33, Age: 4mo)

- **Domain**: Code Quality
- **Impact**: Low
  - *Business*: None - internal tool
  - *User*: None - not user-facing
  - *Developer*: Minor annoyance when debugging admin issues
- **Effort**: L (1 week)
- **Age**: 4 months
- **Location**: `src/admin/**/*.ts` (20+ files)
- **Current State**: Mix of console.log, custom logger, structured logs
- **Why It Matters**: Slightly harder to debug admin issues (rare)
- **Remediation**:
  1. Standardize on structured logger
  2. Update 20+ files with consistent format
  3. Add linting rule to prevent regression
- **Dependencies**: None
- **Risk**: Low impact if not done
```

**ROI Calculation**: Impact=1 (Low), Effort=3 (L), Age=4mo → 1/3 × 1.1 = 0.37

**Recommendation**: Defer indefinitely unless admin tool becomes critical

---

## Calibration Notes

- **First audit**: Scores will be rough estimates; improve over time
- **Team alignment**: Have team review first few items together to calibrate
- **Track outcomes**: After fixing debt, did impact match prediction? Adjust rubric
- **Velocity data**: Use actual time spent on past refactors to estimate future effort
- **Bias check**: Are you inflating impact to justify fixing something you personally dislike?

---

## Related Practices

- **Debt tracking**: Add items to backlog tool (Jira/Linear) with "tech-debt" label
- **Debt budget**: Allocate 10-20% of sprint capacity to debt
- **Debt retrospectives**: Review if debt was worth paying down
- **Preventive measures**: Code review checklists, refactoring time, boy scout rule
- **Re-audit cadence**: Quarterly for active projects, bi-annually for stable systems
