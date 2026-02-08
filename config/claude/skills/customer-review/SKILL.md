# customer-review

Review customer feedback from multiple channels and plan prioritized improvements.

## Orchestration

1. **Parallel Analysis Phase** (spawn all analysts simultaneously)
   - **sales-engineer**: Analyze field feedback, sales calls, competitive losses
   - **support-analyst**: Review support tickets, common issues, escalations
   - **ux-researcher**: Examine user research, usability tests, NPS/CSAT scores
   - **product-manager**: Identify feature gaps, unmet needs, strategic alignment

2. **Synthesis Phase**
   - Each agent outputs:
     * Top 5 pain points (with frequency/severity)
     * Supporting evidence (quotes, metrics, ticket IDs)
     * Quick wins vs strategic bets
   - Agents share findings via broadcast

3. **Joint Prioritization**
   - Convene all agents for debate on impact vs effort matrix
   - Resolve conflicts (sales urgency vs product strategy)
   - Build consensus roadmap with quarterly milestones

4. **Output**
   - Prioritized improvement roadmap (now/next/later)
   - Evidence-backed rationale for each item
   - Deferred items with reasoning

## Usage

```bash
/customer-review [options]

# Analyze specific feedback sources
/customer-review --source tickets --timeframe "Q1 2026"

# Focus on a product area
/customer-review --area "checkout flow"

# Include competitive analysis
/customer-review --include-competitive
```

## Team Structure

- **Team size**: 4 agents (sales-engineer, support-analyst, ux-researcher, product-manager)
- **Pattern**: Parallel research → collaborative prioritization
- **Duration**: 10-15 minutes for comprehensive review

## Key Principles

- **Multi-source**: Never rely on single feedback channel
- **Quantitative + Qualitative**: Balance metrics with customer quotes
- **Action-oriented**: Every insight maps to a concrete improvement
- **Transparent tradeoffs**: Document why items are deferred
- **Customer voice**: Preserve authentic customer language in evidence
