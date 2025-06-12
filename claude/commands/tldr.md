# /tldr

Generate concise, actionable summaries of complex topics, documentation, codebases, or discussions. Focus on essential information and immediate next steps.

## Usage

```
/tldr [topic, document, codebase, or discussion]
```

## Summary Framework

### Key Principles

- **Brevity**: Maximum 5 bullet points per section
- **Actionability**: Focus on what to do, not just what to know
- **Hierarchy**: Most important information first
- **Clarity**: Use simple, direct language
- **Context**: Include just enough background for understanding

### Structure Template

```markdown
# TL;DR: [Topic]

## 🎯 Bottom Line

[1-2 sentences with the most critical takeaway]

## ✅ Key Points

- [Most important fact/decision]
- [Second most important point]
- [Third critical element]
- [Supporting detail if needed]
- [Context or constraint]

## 🚀 Next Steps

1. [Immediate action - what to do first]
2. [Follow-up action - what to do next]
3. [Future consideration - what to plan for]

## ⚠️ Critical Notes

- [Important warning or constraint]
- [Key dependency or requirement]
- [Risk or limitation to be aware of]

## 📚 Resources

- [Essential link or document]
- [Key person to contact]
- [Tool or system to use]
```

## Context-Specific Formats

### Code/Technical TL;DR

```markdown
# TL;DR: [Component/System]

## What It Does

[One sentence description of purpose]

## Key Components

- [Main module/service]: [What it handles]
- [Secondary component]: [Its role]
- [Integration point]: [How it connects]

## To Get Started

1. [Setup/installation step]
2. [Configuration requirement]
3. [First thing to run/test]

## Common Issues

- [Most frequent problem and fix]
- [Performance consideration]

## Who to Ask

- [Subject matter expert]
- [Documentation location]
```

### Meeting/Discussion TL;DR

```markdown
# TL;DR: [Meeting Topic]

## Decisions Made

- [Key decision 1]
- [Key decision 2]

## Action Items

- [Person]: [Task by date]
- [Person]: [Task by date]

## Open Questions

- [Unresolved issue requiring follow-up]
- [Decision pending more information]

## Next Meeting

- [Date/time] - [Main agenda item]
```

### Documentation TL;DR

```markdown
# TL;DR: [Document Name]

## Main Message

[Core thesis or argument in one sentence]

## Key Takeaways

- [Most important insight]
- [Critical fact or data point]
- [Actionable recommendation]

## Implementation

1. [First step to apply this knowledge]
2. [How to measure success]

## Skip This If

- [When this doesn't apply]
- [Prerequisites not met]
```

### Project/Feature TL;DR

```markdown
# TL;DR: [Project Name]

## Goal

[What we're trying to achieve]

## Status

[Current phase and % complete]

## Key Risks

- [Biggest concern]
- [Timeline risk]

## Need From You

- [Specific ask or decision needed]
- [Resource requirement]

## Timeline

-
-
```

## Summarization Techniques

### Information Hierarchy

1. **Critical**: Must know for immediate action
2. **Important**: Affects decision-making
3. **Useful**: Provides helpful context
4. **Interesting**: Nice to know but not essential

### The 5W+H Filter

- **Who**: Key people/stakeholders
- **What**: Core facts/decisions
- **When**: Critical timelines
- **Where**: Location/context constraints
- **Why**: Essential reasoning
- **How**: Implementation approach

### Progressive Disclosure

```markdown
## 30-Second Version

[One paragraph with absolute essentials]

## 2-Minute Version

[Add key details and context]

## 5-Minute Version

[Include important nuances and background]
```

## Examples by Use Case

### Codebase Analysis TL;DR

```markdown
# TL;DR: Payment Service

## What It Does

Processes credit card payments through Stripe with retry logic and fraud detection.

## Key Files

- `payment_processor.rs`: Main business logic
- `stripe_client.rs`: External API integration
- `fraud_detector.rs`: Risk assessment rules

## To Debug Issues

1. Check logs in `/var/log/payments/`
2. Verify Stripe webhook status
3. Look for fraud blocks in dashboard

## Critical Dependencies

- Stripe API (payment processing)
- Redis (rate limiting)
- Postgres (transaction history)

## Contact: Sarah Chen (payment-team@company.com)
```

### Architecture Decision TL;DR

```markdown
# TL;DR: Database Choice - ScyllaDB

## Decision

Migrate from Postgres to ScyllaDB for event storage.

## Why

- 10x better write performance at scale
- Native time-series support
- Compatible with Cassandra tools

## Next Steps

1. Proof of concept by Jan 15
2. Migration plan by Feb 1
3. Production rollout Q2

## Risks

- Team learning curve (2-3 weeks)
- Data migration complexity
- Operational tooling gaps

## Resources

- ScyllaDB docs: [link]
- POC repository: [link]
- Migration champion: Alex Kim
```

### Bug Investigation TL;DR

```markdown
# TL;DR: Login Timeout Bug

## Problem

Users getting logged out after 5 minutes instead of 30 minutes.

## Root Cause

JWT expiration misconfigured in auth service config.

## Fix Applied

Changed `token_expiry` from 300s to 1800s in `auth.yaml`

## Prevention

- Added integration test for token expiry
- Documented config in runbook
- Set up monitoring alert for short sessions

## Status: RESOLVED (deployed to prod 2024-01-15)
```

### Research Summary TL;DR

```markdown
# TL;DR: State Management Options

## Recommendation

Use Zustand for client state, React Query for server state.

## Why

- Simpler than Redux (less boilerplate)
- Better TypeScript support
- Proven at scale (used by Vercel, etc.)

## Implementation

1. Replace Redux store with Zustand (1 week)
2. Add React Query for API calls (1 week)
3. Remove unnecessary middleware (2 days)

## Tradeoffs

- ✅ Faster development, fewer bugs
- ❌ Team relearning curve
- ❌ Less ecosystem/tooling than Redux
```

## Quality Checklist

### Essential Elements

- [ ] Can be read in under 2 minutes
- [ ] Includes concrete next steps
- [ ] Highlights biggest risks/concerns
- [ ] Provides contact info or resources
- [ ] Uses bullet points and short sentences

### Common Mistakes to Avoid

- ❌ Including too much background/context
- ❌ Using jargon without explanation
- ❌ Listing facts without actionable conclusions
- ❌ Burying the most important information
- ❌ Making it longer than the original content

### Audience Considerations

- **Executive**: Focus on business impact and timeline
- **Technical**: Include implementation details and risks
- **Operational**: Emphasize process and responsibilities
- **Cross-functional**: Balance technical and business context

## Integration with Other Commands

- Use after `/investigate` to summarize findings
- Apply to `/deep-dive` outputs to extract key insights
- Follow `/think` sessions to distill conclusions
- Create TL;DR versions of `/elaborate` content
- Summarize `/dependencies` analysis for stakeholders

The goal is to make complex information immediately accessible and actionable for busy stakeholders who need to make quick, informed decisions.
