# Postmortem Reference

## Postmortem Document Template

```markdown
# [Service/System] Incident - [YYYY-MM-DD]

**Status:** Draft | Review | Final
**Incident Commander:** [Role]
**Start Time:** YYYY-MM-DD HH:MM UTC
**End Time:** YYYY-MM-DD HH:MM UTC
**Duration:** X hours Y minutes
**Severity:** SEV-[1-4]

---

## Executive Summary

[2-3 sentence summary: What happened, what was the impact, what was the root cause]

---

## Impact Assessment

**User Impact:**
* [Quantified impact: X users affected, Y% error rate, Z minutes of degradation]
* [User experience description: what users saw/experienced]

**Business Impact:**
* [Revenue/SLA impact if applicable]
* [Reputation/customer trust impact]

**Internal Impact:**
* [Engineering time spent on incident]
* [Other teams/systems affected]

---

## Timeline

All times in UTC. **Bold** indicates key decision points.

| Time | Event | Actor/System |
|------|-------|--------------|
| HH:MM | Deployment of version X.Y.Z started | CI/CD |
| HH:MM | First error spike in logs | System |
| HH:MM | **On-call paged by monitoring** | PagerDuty |
| HH:MM | **Incident declared, war room opened** | On-call |
| HH:MM | Root cause hypothesis formed | Team |
| HH:MM | **Rollback initiated** | Incident Commander |
| HH:MM | Service recovered | System |
| HH:MM | **Incident closed** | Incident Commander |

---

## Root Cause Analysis

### Immediate Trigger
[What directly caused the failure - the "what"]

### Root Cause (5-Whys)
1. **Why did [immediate trigger] happen?**
   [Answer]

2. **Why did [answer 1] happen?**
   [Answer]

3. **Why did [answer 2] happen?**
   [Answer]

4. **Why did [answer 3] happen?**
   [Answer]

5. **Why did [answer 4] happen?**
   [Answer - this is often the root cause]

**Root Cause:** [Concise statement of systemic issue]

---

## Contributing Factors

These factors enabled or amplified the incident:

1. **[Factor category - e.g., Monitoring]**
   [Description of gap or issue]

2. **[Factor category - e.g., Testing]**
   [Description of gap or issue]

3. **[Factor category - e.g., Process]**
   [Description of gap or issue]

---

## What Went Well

Celebrate resilience and effective response:

* **[What worked]**: [Why it helped]
* **[What worked]**: [Why it helped]
* **[What worked]**: [Why it helped]

---

## Action Items

### Immediate (Complete within 24-48 hours)

| Action | Owner | Deadline | Status | Success Criteria |
|--------|-------|----------|--------|------------------|
| [Action] | [Role] | YYYY-MM-DD | 🔴 Open / 🟡 In Progress / 🟢 Done | [Measurable outcome] |

### Short-Term (Complete within 1-2 weeks)

| Action | Owner | Deadline | Status | Success Criteria |
|--------|-------|----------|--------|------------------|
| [Action] | [Role] | YYYY-MM-DD | Status | [Measurable outcome] |

### Medium-Term (Complete within 1-2 months)

| Action | Owner | Deadline | Status | Success Criteria |
|--------|-------|----------|--------|------------------|
| [Action] | [Role] | YYYY-MM-DD | Status | [Measurable outcome] |

### Long-Term (Complete within quarter)

| Action | Owner | Deadline | Status | Success Criteria |
|--------|-------|----------|--------|------------------|
| [Action] | [Role] | YYYY-MM-DD | Status | [Measurable outcome] |

---

## Appendix

### Metrics & Graphs
[Links to dashboards, screenshots of key metrics]

### Logs & Traces
[Sanitized relevant log excerpts, trace IDs]

### Related Incidents
[Links to similar past incidents]

### Agent Investigation Reports
[Links or summaries of detailed investigation by each agent]
```

---

## 5-Whys Framework

### What is 5-Whys?

A root cause analysis technique that drills down from symptoms to systemic causes by repeatedly asking "Why?"

### How to Apply

1. **Start with the symptom/incident**: State what happened (e.g., "Database crashed")
2. **Ask "Why?" to find immediate cause**: E.g., "Why did database crash? Out of memory"
3. **Ask "Why?" again**: E.g., "Why out of memory? Memory leak in new code"
4. **Continue 4-5 times**: Until you reach a process/systemic gap
5. **Validate**: Does the root cause explain all observations?

### Quality Checks

✅ **Good 5-Whys:**
* Reaches a process or systemic gap (not just technical details)
* Each "Why?" has evidence from investigation
* Root cause is actionable (we can fix the process)
* Avoids blame (focuses on systems, not people)

❌ **Bad 5-Whys:**
* Stops at technical symptom ("bad deployment")
* Blames individual ("engineer made mistake")
* Too generic ("need better testing")
* Not actionable ("need to be more careful")

### Example: E-commerce Checkout Outage

**Symptom:** Checkout API returned 500 errors for 45 minutes

1. **Why did checkout API return 500s?**
   Payment service timeout after 30 seconds

2. **Why did payment service timeout?**
   Database queries took 60+ seconds (normally <100ms)

3. **Why did queries slow down?**
   Missing index on new `fraud_score` column added in v2.3.0

4. **Why was the index missing?**
   Migration script in PR didn't include index creation (added in follow-up commit)

5. **Why didn't we catch missing index before production?**
   Staging database is 100x smaller than production; query plans differ

**Root Cause:** Staging environment doesn't replicate production scale, so performance issues aren't caught in testing.

**Actionable Fix:** Create performance test suite using production-scale data snapshots.

---

## Timeline Format

### Minute-by-Minute During Critical Period

Use this format for the critical incident window:

```
14:23 UTC - Deployment v2.3.0 started (5% canary)
14:24 UTC - Canary health checks passing, no errors
14:26 UTC - Canary expanded to 50% of traffic
14:27 UTC - First 500 errors appear in logs (0.1% error rate)
14:28 UTC - Error rate spikes to 5% as slow queries accumulate
14:29 UTC - Monitoring alert fires: "API Error Rate > 1%"
14:30 UTC - On-call engineer paged
14:32 UTC - On-call joins, reviews dashboards
14:35 UTC - War room opened, incident declared SEV-2
14:36 UTC - Database team paged for query analysis
14:40 UTC - Slow query log identifies missing index on fraud_score
14:42 UTC - Decision: Rollback faster than index creation
14:43 UTC - Rollback initiated to v2.2.9
14:47 UTC - Rollback complete, traffic shifted to v2.2.9
14:49 UTC - Error rate drops to 0%, latency returns to normal
14:52 UTC - Incident downgraded to monitoring
15:15 UTC - Incident closed after 30min observation period
```

### Hourly for Extended Incidents

For multi-hour incidents, switch to hourly granularity after initial crisis:

```
Day 1:
14:00 - Incident begins (see minute-by-minute above)
15:00 - Rollback complete, service recovered
16:00 - Root cause identified, fix developed
17:00 - Fix tested in staging with proper index
18:00 - Deploy v2.3.1 with index (gradual rollout)
20:00 - Full deployment complete

Day 2:
10:00 - Postmortem meeting scheduled
14:00 - Draft postmortem circulated
```

---

## Action Item Templates

### Format

```
**Action:** [Verb] [specific outcome]
**Owner:** [Role or team - not individual name]
**Deadline:** YYYY-MM-DD
**Success Criteria:** [Measurable outcome]
**Priority:** P0 (immediate) | P1 (this week) | P2 (this month) | P3 (this quarter)
```

### Examples

#### Immediate Fix (P0)

```
**Action:** Add index on payments.fraud_score column in production
**Owner:** Database Team
**Deadline:** 2026-02-09
**Success Criteria:** Query execution time <100ms for checkout queries
**Priority:** P0
```

#### Monitoring Gap (P1)

```
**Action:** Add alert for P95 database query latency > 500ms
**Owner:** SRE Team
**Deadline:** 2026-02-15
**Success Criteria:** Alert fires in staging when simulated slow query injected
**Priority:** P1
```

#### Testing Gap (P1)

```
**Action:** Create performance test suite using production-scale data snapshot
**Owner:** QA Team
**Deadline:** 2026-02-22
**Success Criteria:** Test suite catches query performance regressions before deploy
**Priority:** P1
```

#### Process Improvement (P2)

```
**Action:** Establish database migration review checklist (includes index planning)
**Owner:** Engineering Lead
**Deadline:** 2026-03-15
**Success Criteria:** All DB migrations reviewed against checklist for 1 month
**Priority:** P2
```

#### Cultural Change (P3)

```
**Action:** Run monthly game days simulating production incidents
**Owner:** SRE Team
**Deadline:** 2026-05-01 (first game day)
**Success Criteria:** 80% of on-call engineers participate in first 3 months
**Priority:** P3
```

---

## Blameless Language Guide

### Core Principle

**Blameless doesn't mean no accountability** - it means focusing on systems and processes that allowed the incident, not individuals who were involved.

### Language Transformations

| ❌ Blame Language | ✅ Blameless Language |
|-------------------|----------------------|
| "Engineer X deployed bad code" | "Deployment process allowed untested code path to reach production" |
| "Team Y didn't monitor the system" | "Alert threshold tuned for normal load didn't trigger on spike" |
| "DBA forgot to add the index" | "Migration review process didn't catch missing index" |
| "On-call was slow to respond" | "Page escalation policy didn't account for off-hours delays" |
| "QA didn't test thoroughly" | "Test coverage gaps didn't catch edge case with large datasets" |
| "Manager approved risky change" | "Change approval process lacked risk assessment framework" |

### Framing Questions

Instead of "Who made the mistake?", ask:

* **What process gap allowed this?**
* **What signals did we miss?**
* **What made the wrong decision seem right at the time?**
* **How can we make the right choice easier next time?**

### Handling Human Error

When human error is involved, focus on *why the error was possible*:

```
❌ "Engineer made a typo in the config file"

✅ "Configuration syntax allowed typo to pass validation.
    Action item: Add schema validation to config files."
```

```
❌ "On-call clicked the wrong button"

✅ "UI placed destructive 'Delete Production DB' button next to
    'Delete Test DB' button with similar styling.
    Action item: Add confirmation dialog and distinct colors for
    production actions."
```

### Active Voice for Systems, Not People

Use active voice for systems/processes:

* ✅ "Deployment pipeline deployed version X"
* ✅ "Monitoring system alerted on-call"
* ✅ "Load balancer routed traffic to unhealthy instances"

Use passive voice when describing impact:

* ✅ "Users were unable to complete checkout"
* ✅ "Database connections were exhausted"
* ✅ "Alerts were delayed by 15 minutes"

---

## Severity Classification

Use consistent severity levels to prioritize response and action items:

### SEV-1 (Critical)
* **Impact:** Complete service outage or severe degradation
* **Scope:** All users affected
* **Response:** Immediate all-hands, executive notification
* **Example:** Payment processing down globally

### SEV-2 (High)
* **Impact:** Significant feature degradation
* **Scope:** Majority of users affected
* **Response:** War room within 15 min, stakeholder updates
* **Example:** Checkout success rate drops 50%

### SEV-3 (Medium)
* **Impact:** Minor feature degradation
* **Scope:** Subset of users affected
* **Response:** Standard on-call response, monitor
* **Example:** Search results occasionally stale

### SEV-4 (Low)
* **Impact:** Cosmetic or internal issue
* **Scope:** Minimal user impact
* **Response:** Track in backlog, fix in normal cycle
* **Example:** Dashboard rendering glitch

---

## Postmortem Meeting Facilitation

### Pre-Meeting (Coordinator)

1. **Schedule within 24-48 hours** of incident resolution
2. **Circulate draft timeline** to all participants
3. **Share preliminary findings** from agent investigations
4. **Set expectations**: Blameless, learning-focused, time-boxed

### Meeting Structure (60 minutes)

**0-10 min:** Timeline review
* Walk through incident minute-by-minute
* Clarify any gaps or questions
* Ensure shared understanding

**10-30 min:** Root cause analysis
* Present 5-Whys findings
* Discuss contributing factors
* Validate with team

**30-45 min:** What went well
* Celebrate effective response
* Identify resilience patterns to preserve
* Build team confidence

**45-55 min:** Action items
* Brainstorm prevention measures
* Prioritize by impact/effort
* Assign owners and deadlines

**55-60 min:** Follow-up
* Schedule action item review
* Assign postmortem document finalization
* Thank participants

### Facilitation Tips

* **Redirect blame:** "Let's focus on the process that allowed X"
* **Encourage participation:** "What did you observe during the incident?"
* **Time-box discussions:** "Let's capture this and move on"
* **Validate feelings:** "This was stressful, and the team responded well"
* **End positively:** Emphasize learning and improvements

---

## Follow-Up & Tracking

### Action Item Review Cadence

* **P0 (immediate):** Daily standup until complete
* **P1 (short-term):** Weekly review in team meeting
* **P2 (medium-term):** Bi-weekly check-ins
* **P3 (long-term):** Monthly updates in all-hands

### Metrics to Track

* **Action item completion rate:** Target >90% on-time completion
* **Time to postmortem:** Target <48 hours from incident close
* **Repeat incidents:** Track if similar incidents recur
* **MTTR trend:** Are incidents resolving faster over time?

### Postmortem of Postmortems

Quarterly review of incident trends:

* What categories of incidents are most common?
* Are action items actually preventing recurrence?
* What systemic patterns need addressing?
* Is blameless culture healthy?

---

## Additional Resources

### Templates & Tools

* [Google SRE Postmortem Culture](https://sre.google/sre-book/postmortem-culture/)
* [Etsy Debriefing Facilitation Guide](https://extfiles.etsy.com/DebriefingFacilitationGuide.pdf)
* [PagerDuty Incident Response Guide](https://response.pagerduty.com/)

### Books

* **Site Reliability Engineering** (Google) - Chapter on postmortems
* **The Field Guide to Understanding Human Error** (Dekker) - Blameless culture foundations

### Internal Resources

* Link to your organization's incident response runbooks
* Link to your postmortem repository/wiki
* Link to action item tracking system
