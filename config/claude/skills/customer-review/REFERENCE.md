# Customer Review - Reference Guide

Frameworks and templates for multi-source feedback analysis and prioritization.

---

## Feedback Analysis Framework

### Data Source Credibility Matrix

| Source | Strength | Weakness | Best For |
|--------|----------|----------|----------|
| **Sales Calls** | Pre-purchase intent, competitive context | Skewed to largest/loudest buyers | Strategic features, market gaps |
| **Support Tickets** | Post-purchase reality, pain severity | Over-represents edge cases | Bug fixes, UX confusion |
| **User Research** | Deep behavioral context, "why" behind actions | Small sample size, lab conditions | Usability improvements, mental models |
| **NPS/CSAT** | Quantitative trends, sentiment at scale | Lacks actionable detail | Prioritization signal, tracking changes |

### Evidence Quality Standards

**Strong Evidence** (high confidence):
- Direct customer quotes with context
- Quantitative metrics (ticket volume, revenue impact, conversion rates)
- Multiple independent sources confirming same issue
- Behavioral data (recordings, analytics) showing struggle

**Weak Evidence** (needs validation):
- Secondhand summaries ("customers want...")
- Single anecdote extrapolated broadly
- Feature requests without stated problem
- Opinions from internal team, not customers

---

## Prioritization Matrix (Impact × Effort)

```
     High Impact
        ↑
        │  [Quick Win]     │  [Strategic Bet]
        │  ────────────────┼───────────────
        │  - Low effort    │  - High effort
        │  - High impact   │  - High impact
        │  DO NOW          │  ROADMAP (Q2+)
        │                  │
────────┼──────────────────┼────────────────────→
        │                  │              High Effort
        │  [Fill]          │  [Time Sink]
        │  ────────────────┼───────────────
        │  - Low effort    │  - High effort
        │  - Low impact    │  - Low impact
        │  IF TIME         │  DECLINE
        │                  │
        ↓ Low Impact
```

### Scoring Rubric

**Impact Score** (1-10):
- **10**: Blocker for large deals, major churn driver, top 3 NPS detractor
- **7-9**: Significant friction, affects 20%+ of users, competitive disadvantage
- **4-6**: Nice-to-have, improves workflow but not critical
- **1-3**: Edge case, minor annoyance, low evidence

**Effort Score** (1-10):
- **1-3**: Copy change, config tweak, < 1 day
- **4-6**: UI redesign, new API endpoint, 1-2 weeks
- **7-9**: New subsystem, third-party integration, 1-2 months
- **10**: Architectural change, platform rebuild, > 3 months

**Priority Formula**: `Impact² ÷ Effort`

Why squared? High-impact items warrant disproportionate investment.

---

## Roadmap Template

```markdown
# Customer Feedback Roadmap - [Quarter] [Year]

## Now (Sprint Ready)
High-impact quick wins and critical blockers.

1. **[Improvement Title]** - [Impact: X | Effort: Y | Priority: Z]
   - **Problem**: [Customer pain in their words]
   - **Evidence**: [Sources with links/IDs]
   - **Success Metric**: [How we'll measure improvement]
   - **Owner**: [Team/Person]

## Next (This Quarter)
Strategic bets that need design/planning before execution.

[Same format]

## Later (Next Quarter+)
Important but not urgent; needs more research or dependencies.

[Same format]

## Deferred (Not Now)
Items we explicitly decided not to pursue (with reasoning).

1. **[Request]** - Declined because:
   - Low impact (only 2 customers requested)
   - Workaround exists (use feature X instead)
   - Doesn't align with strategy (moving away from Y)
```

---

## Debate Resolution Framework

When agents disagree during prioritization:

### Common Conflicts

**Sales urgency vs Product strategy**
- Sales: "Customer will pay $100k if we build X"
- Product: "X doesn't fit our vision, creates tech debt"
- **Resolution**: Time-box decision (will customer wait 2 quarters?), explore alternatives (can we meet need differently?), calculate opportunity cost (what else could we build with that effort?)

**Support volume vs UX depth**
- Support: "300 tickets/month on issue Y, fix it!"
- UX: "Root cause is confusing navigation, not the specific bug"
- **Resolution**: Distinguish band-aid from cure. Quick fix for support relief + longer-term UX redesign.

**Quantitative vs Qualitative**
- Analyst: "Only 5% of users affected by Z"
- Researcher: "But those 5% are power users, extremely frustrated"
- **Resolution**: Segment impact (revenue from affected cohort?), consider strategic importance (are they reference customers, early adopters?).

### Decision-Making Protocol

1. **State the disagreement clearly**: "We disagree on whether to prioritize A or B"
2. **Surface assumptions**: "I think A is higher impact because [assumption]"
3. **Identify missing data**: "We don't know X, which would resolve this"
4. **Set decision criteria**: "We'll choose based on revenue impact vs time-to-market"
5. **Make the call**: Product-manager has tiebreaker authority
6. **Document reasoning**: Future team needs to understand why

---

## Customer Voice Preservation

### Good Quote Usage

✅ **Direct, contextual, actionable**
> "I spent 20 minutes looking for the export button. I finally gave up and asked support. Why isn't it with the other data actions?"
> - Enterprise user, onboarding session, [Recording: 00:14:32]

❌ **Vague, editorialized, unhelpful**
> "Users find the UI confusing."

### Organizing Feedback Evidence

Create a shared evidence repository:

```
evidence/
  sales/
    calls/
      2026-01-15-acme-corp-discovery.md
    losses/
      2026-01-20-lost-to-competitor-x.md
  support/
    ticket-clusters/
      checkout-flow-errors-jan-2026.md
  research/
    usability-tests/
      2026-01-10-new-user-onboarding-5-participants.md
  metrics/
    nps-detractors-jan-2026.csv
```

Link liberally from roadmap to evidence files.

---

## Anti-Patterns to Avoid

❌ **HiPPO prioritization** (Highest Paid Person's Opinion)
- Building features because exec asked, not because customers need

❌ **Squeaky wheel syndrome**
- Over-indexing on loudest customer, ignoring silent majority

❌ **Build-it-and-pray**
- Skipping validation, assuming feature will solve problem

❌ **Analysis paralysis**
- Endless research, no decisions or action

❌ **Feature factory**
- Shipping without measuring if it actually improved customer outcomes

---

## Success Metrics

Track before/after to validate improvements worked:

| Improvement Type | Metric to Watch |
|------------------|----------------|
| Bug fix | Support ticket volume ↓, CSAT ↑ |
| UX redesign | Task completion time ↓, error rate ↓, feature adoption ↑ |
| Missing feature | Sales win rate ↑, expansion revenue ↑ |
| Documentation | Self-service resolution ↑, "how do I..." tickets ↓ |

**Review cadence**: 30 days post-launch for quick wins, 90 days for strategic bets.

---

## Collaboration Norms

### For Agent Teams

- **Parallel analysis**: All agents work simultaneously on their data sources
- **Broadcast findings**: Share top insights via team broadcast
- **Joint debate**: Convene for prioritization discussion (don't decide in silos)
- **Transparent tradeoffs**: Document what we're NOT doing and why
- **Customer-centric**: When in doubt, choose option that reduces customer pain fastest

### For Human Teams

This framework adapts to real product teams:
- Replace "agents" with team roles (PM, UX, Support Lead, Sales Eng)
- Run quarterly review sessions (not ad-hoc)
- Maintain shared evidence repository (Notion, Confluence, etc.)
- Present roadmap to exec/board with customer quotes as supporting evidence
