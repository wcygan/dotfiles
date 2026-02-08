# Launch Readiness Reference

Quick reference for severity scoring, go/no-go criteria, and launch checklist templates.

---

## Severity Definitions

### Blocker (Cannot Ship)

**Criteria**: Issue **prevents safe deployment** or causes **unacceptable risk** to users, business, or compliance.

**Examples**:
- **Security**: Unauthenticated access to sensitive data; SQL injection vulnerability
- **Data Loss**: Risk of deleting/corrupting customer data with no recovery path
- **Legal/Compliance**: GDPR violation; missing required terms of service
- **Production Impact**: Change will take down existing production service
- **No Rollback**: Cannot safely undo deployment; no recovery procedure

**Action**: **Must fix before launch.** No exceptions.

---

### Critical (High Risk)

**Criteria**: Issue creates **high likelihood** of major incident, significant user impact, or brand damage if left unfixed.

**Examples**:
- **Performance**: Service becomes unusable under realistic load (response time >10s)
- **Monitoring Gaps**: No alerts for critical failure modes (users report incidents before we detect)
- **UX Blockers**: Core workflow is confusing or broken for new users (high abandonment)
- **Support Overwhelm**: Feature ships without docs/training; support will be flooded
- **Partial Rollback**: Can roll back but with significant manual effort or data loss

**Action**: **Strongly recommend fixing before launch.** If accepting risk, require explicit mitigation plan (e.g., deploy with feature flag, add monitoring, limit rollout).

---

### High (Should Fix)

**Criteria**: Issue causes **noticeable friction** or **moderate risk** but doesn't block core functionality.

**Examples**:
- **UX Friction**: Workflow works but requires excessive clicks or is confusing
- **Documentation Gaps**: Important use cases or error scenarios are undocumented
- **Performance**: Service is slower than expected but still functional (<10s response)
- **Monitoring**: Alerts exist but are noisy or missing important edge cases
- **Support Load**: Users will need help but support can handle it

**Action**: **Fix if time permits before launch.** If shipping with issue, ensure mitigation (add FAQ, plan support capacity, improve error messages).

---

### Medium (Nice to Fix)

**Criteria**: Issue reduces quality or creates minor friction but **low impact** on launch success.

**Examples**:
- **Polish**: UI inconsistencies, minor visual bugs, suboptimal but functional UX
- **Documentation**: Missing advanced examples; basic docs are adequate
- **Performance**: Not optimally tuned but acceptable under normal load
- **Monitoring**: Basic alerts in place; could add more granular metrics
- **Support**: Self-service exists; some users will still contact support

**Action**: **Backlog for post-launch.** Note as known limitation in release notes if customer-facing.

---

### Low (Backlog)

**Criteria**: Cosmetic, edge case, or **future enhancement** with minimal impact.

**Examples**:
- **Cosmetic**: Minor typos, color inconsistencies, formatting issues
- **Edge Cases**: Obscure scenarios unlikely to occur in normal use
- **Enhancements**: Nice-to-have features not critical for launch
- **Internal Quality**: Code cleanup, better tests (existing tests pass)
- **Documentation**: Typos, missing nice-to-have examples

**Action**: **Backlog.** Track as technical debt or future improvement.

---

## Go/No-Go Decision Criteria

### 🔴 No-Go (Do Not Launch)

**Triggers**:
- **Any Blocker** severity issue unresolved
- **Multiple Critical** issues without clear mitigation plans
- **Insufficient audit coverage** (key areas not evaluated)
- **Team consensus** that risk is unacceptable

**Next Steps**:
1. Fix all blockers
2. Re-audit affected areas
3. Reassess launch readiness

---

### 🟡 Conditional Go (Launch with Conditions)

**Triggers**:
- **Blockers resolved** but Critical issues remain
- **Clear mitigation plans** for all Critical risks (feature flags, monitoring, rollback procedures)
- **Stakeholder agreement** to accept risk with mitigations

**Conditions** (examples):
- Deploy behind feature flag (gradual rollout)
- Add real-time monitoring dashboards
- On-call engineer assigned for first 48h
- Limit to beta customers or specific accounts
- Rollback procedure tested and documented

**Next Steps**:
1. Execute mitigations **before** launch
2. Monitor closely during rollout
3. Fast rollback if issues detected

---

### 🟢 Ready to Ship (Green Light)

**Triggers**:
- **No Blockers or Critical** issues (or mitigated to High/Medium)
- **High/Medium issues** accepted or mitigated
- **Audit coverage** sufficient for feature scope
- **Stakeholder confidence** in readiness

**Next Steps**:
1. Execute launch plan
2. Monitor normal metrics
3. Track backlog items (Medium/Low) for future sprints

---

## Launch Checklist Template

Use this as a pre-launch verification checklist:

### Security
- [ ] Authentication/authorization tested for all endpoints
- [ ] Input validation for all user-supplied data
- [ ] Secrets/credentials not hardcoded or logged
- [ ] HTTPS enforced for all customer-facing services
- [ ] Dependencies scanned for known vulnerabilities
- [ ] Compliance requirements met (GDPR, SOC2, etc.)

### Performance
- [ ] Load tested under realistic traffic (2x expected peak)
- [ ] Response times acceptable (<3s for user-facing, <1s for APIs)
- [ ] Database queries optimized (no N+1, indexes in place)
- [ ] Caching strategy implemented where appropriate
- [ ] Resource limits configured (memory, CPU, connections)
- [ ] Autoscaling tested if applicable

### Reliability
- [ ] Failure modes identified and mitigated
- [ ] Monitoring/alerts configured for critical metrics
- [ ] Logging sufficient for debugging production issues
- [ ] Rollback procedure documented and tested
- [ ] Rate limiting/circuit breakers in place
- [ ] Incident response runbook exists
- [ ] On-call rotation aware of launch

### Documentation
- [ ] User-facing docs complete (getting started, API reference)
- [ ] Operator docs complete (deployment, configuration, runbooks)
- [ ] Release notes written (customer-facing changelog)
- [ ] Internal training materials for support team
- [ ] Architecture decisions documented (ADRs)
- [ ] Known limitations documented

### Customer Readiness
- [ ] Onboarding UX tested with fresh users
- [ ] Core workflows functional and intuitive
- [ ] Error messages user-friendly and actionable
- [ ] Support team trained on new feature
- [ ] Sales team has demo environment and talking points
- [ ] Marketing assets ready (screenshots, blog posts)
- [ ] Migration guide for breaking changes (if applicable)

### Deployment
- [ ] Deploy procedure documented step-by-step
- [ ] Database migrations tested in staging
- [ ] Feature flags configured for gradual rollout
- [ ] Rollback procedure tested (can we undo this safely?)
- [ ] Deployment window scheduled (off-peak if risky)
- [ ] Stakeholders notified of deployment plan

---

## Confidence Assessment Guide

### High Confidence
- **Audit Coverage**: All critical areas reviewed by specialists
- **No Surprises**: Known risks identified and mitigated
- **Testing**: Comprehensive tests in staging/production-like environment
- **Team Alignment**: Engineering, product, support all agree on readiness
- **Past Success**: Similar features launched successfully with this process

### Medium Confidence
- **Partial Coverage**: Some areas audited, others assumed safe
- **Known Unknowns**: Gaps in testing or coverage (e.g., no load test at scale)
- **Assumptions**: Relying on "should be fine" for some risks
- **New Territory**: First time launching this type of feature/tech
- **Mixed Signals**: Some teams confident, others hesitant

### Low Confidence
- **Minimal Coverage**: Limited or no audit in critical areas
- **Unknown Unknowns**: Haven't thought through failure modes
- **Rushed Timeline**: Insufficient time for proper testing/review
- **Red Flags**: Recent incidents, bugs found late, key people unavailable
- **Team Hesitation**: Multiple stakeholders express concerns

**How to Increase Confidence**:
- Run additional audits in gap areas
- Add monitoring/observability to reduce unknowns
- Test in production-like environment (load, data, integrations)
- Mitigate risks with feature flags, gradual rollout, rollback plans
- Get stakeholder buy-in and alignment

---

## Common Anti-Patterns

### The "Ship It and See" Launch
**Problem**: No audits, just deploy and hope for the best.
**Risk**: High likelihood of incidents, customer churn, brand damage.
**Fix**: Run at minimum security + reliability audits before launch.

### The "Perfect Is the Enemy of Good" Stall
**Problem**: Every Medium issue is treated as Blocker; never ship.
**Risk**: Missed market opportunity, team burnout, feature goes stale.
**Fix**: Use severity rubric objectively; accept Medium/Low risks.

### The "Checkbox Compliance" Audit
**Problem**: Audits run but don't find real issues ("looks good!").
**Risk**: False confidence; issues discovered post-launch.
**Fix**: Give auditors permission to be critical; reward finding issues.

### The "Post-Launch Documentation" Plan
**Problem**: Ship first, write docs later.
**Risk**: Support overwhelmed, users frustrated, adoption suffers.
**Fix**: Documentation is part of the feature; must ship together.

### The "Ignore the Auditors" Launch
**Problem**: Audits find Blockers/Critical issues but leadership ships anyway.
**Risk**: Predictable incidents; team loses trust in process.
**Fix**: Respect severity rubric; if shipping despite Blockers, mitigate explicitly.

---

## Stakeholder Communication Templates

### No-Go Decision

```
Launch Decision: 🔴 No-Go

We've completed a launch readiness audit and identified [N] blocker issues that prevent safe deployment:

1. [Blocker description + impact]
2. [Blocker description + impact]

Next Steps:
- Engineering will address blockers by [date]
- We'll re-audit and reassess readiness on [date]
- Revised target launch date: [date]

This delay protects our customers and our brand. Thank you for your patience.
```

### Conditional Go Decision

```
Launch Decision: 🟡 Conditional Go

We're ready to launch with the following risk mitigations in place:

Conditions:
1. Deploy behind feature flag (gradual rollout to 10% → 50% → 100%)
2. Real-time monitoring dashboard + on-call engineer assigned
3. Rollback procedure tested and documented

Critical Risks Accepted:
- [Risk description + mitigation plan]

We'll monitor closely for the first 48 hours and roll back immediately if issues arise.
```

### Ready to Ship Decision

```
Launch Decision: 🟢 Ready to Ship

All audits complete. No blockers or critical issues. Launch approved.

Highlights:
- Security: ✅ No vulnerabilities found
- Performance: ✅ Load tested to 3x expected traffic
- Reliability: ✅ Monitoring and runbooks in place
- Documentation: ✅ User and operator docs complete
- Customer Readiness: ✅ Support trained, UX polished

Launch Plan:
- Deploy: [date/time]
- Rollout: [gradual/full]
- On-call: [team/person]

Let's ship it!
```

---

## Example Severity Scoring

| Finding | Area | Severity | Rationale |
|---------|------|----------|-----------|
| SQL injection in search endpoint | Security | **Blocker** | Unauthenticated data access; regulatory risk |
| No rollback procedure documented | Reliability | **Blocker** | Can't safely undo deployment |
| API response time 8s under load | Performance | **Critical** | Users will abandon (high bounce rate) |
| Support team not trained | Customer | **Critical** | Support will be overwhelmed day 1 |
| Getting started guide incomplete | Docs | **High** | Users can onboard but with friction |
| UI button alignment off by 2px | UX | **Low** | Cosmetic; doesn't affect functionality |
| Missing CHANGELOG entry | Docs | **Low** | Nice to have but not customer-blocking |

---

## FAQ

**Q: What if we disagree on severity?**
A: Use the rubric examples. If a finding doesn't clearly fit, default to the higher severity (safer) and discuss with stakeholders.

**Q: Can we ship with Critical issues?**
A: Yes, but only with explicit mitigation plans (feature flags, extra monitoring, limited rollout). Document the accepted risk.

**Q: How do we handle "unknown unknowns"?**
A: Call out audit gaps in the confidence assessment. If confidence is Low, consider more discovery before launch.

**Q: What if leadership wants to ship despite Blockers?**
A: Escalate. Blockers are defined as "cannot ship safely." If overridden, document the decision and who accepted the risk.

**Q: How long should audits take?**
A: Depends on scope. Small feature: 2-4 hours. Major release: 1-2 days. Parallel execution speeds this up significantly.
