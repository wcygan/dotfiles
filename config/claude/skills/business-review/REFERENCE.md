# Business Review — Agent Reference

Detailed evaluation frameworks and output templates for each of the 8 business review agents.

## Common Evaluation Guidelines

All agents must follow these rules:

### Decision Framework Rules
- Ground recommendations in evidence, not intuition
- Surface assumptions explicitly and test them
- Quantify impact where possible (users affected, revenue impact, cost)
- Identify what you don't know and flag it as a research gap
- Distinguish between "must-have" and "nice-to-have" features

### Communication Standards
- Use structured tables for comparative analysis
- Flag risks with severity levels (Critical / High / Medium / Low)
- Provide confidence levels (High / Medium / Low) for estimates
- Include "What would change my mind" sections for key recommendations
- Be concise but substantive — actionable insights over filler

### Cross-Functional Awareness
- Consider how your function's priorities interact with others
- Flag dependencies on other teams or functions
- Acknowledge trade-offs between competing priorities
- Note where your perspective might conflict with others (intentionally)

---

## Agent 1: Product Manager

### Evaluation Framework

1. **Strategic Alignment**: How does this feature fit with product vision and roadmap?
2. **User Value**: What problem does this solve? Who benefits? How much?
3. **Prioritization**: Where does this rank relative to other work?
4. **Requirements**: What are the acceptance criteria? What's in/out of scope?
5. **Success Metrics**: How will we measure success? What's the target?
6. **User Research**: What evidence supports this? What's missing?
7. **Dependencies**: What needs to happen first? Who else is involved?

### Output Template

```markdown
## Product Management Perspective

### Strategic Alignment

| Dimension | Assessment | Rationale |
|-----------|-----------|-----------|
| Vision fit | {Strong/Moderate/Weak} | {how this advances product vision} |
| Roadmap priority | {P0/P1/P2/P3} | {where this ranks} |
| Customer impact | {High/Medium/Low} | {who benefits, how many users} |
| Competitive positioning | {Critical/Important/Nice-to-have} | {competitive implications} |

### User Value Proposition

**Problem statement**: {What problem are we solving?}

**Target users**: {Who experiences this problem?}

**Current workaround**: {How do users solve this today?}

**Value delivered**: {How much better is our solution?}

**Evidence**: {User research, support tickets, feature requests that support this}

### User Stories

#### Epic
As a {user type}, I want {capability} so that {benefit}.

#### Supporting Stories

1. As a {user}, I want {specific capability} so that {specific benefit}
   - **Acceptance criteria**: {testable criteria}
   - **Priority**: {P0/P1/P2}

2. As a {user}, I want {specific capability} so that {specific benefit}
   - **Acceptance criteria**: {testable criteria}
   - **Priority**: {P0/P1/P2}

3. {Additional stories as needed}

### Prioritization Analysis

| Criterion | Score (1-5) | Weight | Weighted Score | Notes |
|-----------|------------|--------|----------------|-------|
| User impact | {N} | 30% | {N} | {rationale} |
| Strategic value | {N} | 25% | {N} | {rationale} |
| Urgency | {N} | 20% | {N} | {rationale} |
| Feasibility | {N} | 15% | {N} | {rationale} |
| Revenue impact | {N} | 10% | {N} | {rationale} |
| **Total** | | | **{Total}** | |

**Recommendation**: {P0/P1/P2/Backlog}

### Success Metrics

| Metric | Current Baseline | Target | Measurement Method | Timeline |
|--------|-----------------|--------|-------------------|----------|
| {Primary metric} | {value} | {value} | {how to measure} | {when to assess} |
| {Secondary metric} | {value} | {value} | {how to measure} | {when to assess} |
| {Tertiary metric} | {value} | {value} | {how to measure} | {when to assess} |

**Leading indicators**: {Early signals that predict success}

**Lagging indicators**: {Outcome metrics that confirm success}

### Scope Definition

#### In Scope (v1)
- {Feature component 1}
- {Feature component 2}
- {Feature component 3}

#### Out of Scope (v1)
- {Explicitly excluded 1} — {reason}
- {Explicitly excluded 2} — {reason}
- {Explicitly excluded 3} — {reason}

#### Future Consideration (v2+)
- {Potential extension 1}
- {Potential extension 2}

### Dependencies & Blockers

| Dependency | Type | Owner | Status | Risk |
|------------|------|-------|--------|------|
| {Dependency} | {Technical/Design/Legal/etc} | {Team} | {Blocked/At-risk/On-track} | {High/Med/Low} |

### Research Gaps

**What we know**: {Key validated assumptions}

**What we don't know**: {Critical unknowns requiring research}

**Recommended research**: {What research would derisk this decision?}

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Risk} | {High/Med/Low} | {High/Med/Low} | {Mitigation strategy} |

### PM Recommendation

**Decision**: {Build / Don't Build / Research First / Defer}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What evidence would flip this recommendation}
```

---

## Agent 2: Product Marketing Manager

### Evaluation Framework

1. **Market Opportunity**: How big is the addressable market? Is it growing?
2. **Positioning**: How do we position this relative to competitors?
3. **Messaging**: What's the value proposition? What story do we tell?
4. **Target Audience**: Who are the ideal customers? What segments?
5. **Competitive Differentiation**: What makes us unique? Why choose us?
6. **Go-to-Market**: How do we launch? What channels? What's the plan?
7. **Pricing & Packaging**: How do we monetize? What tier? What price point?

### Output Template

```markdown
## Product Marketing Perspective

### Market Opportunity

| Dimension | Assessment |
|-----------|-----------|
| Total addressable market (TAM) | {$ estimate or user count} |
| Serviceable addressable market (SAM) | {$ estimate or user count} |
| Serviceable obtainable market (SOM) | {$ estimate or user count} |
| Market growth rate | {% CAGR} |
| Market maturity | {Emerging/Growth/Mature/Declining} |

**Market trends supporting this**:
1. {Trend 1 and impact}
2. {Trend 2 and impact}
3. {Trend 3 and impact}

### Target Segments

| Segment | Size | Pain Level | Willingness to Pay | Priority |
|---------|------|-----------|-------------------|----------|
| {Segment 1} | {users/companies} | {High/Med/Low} | {High/Med/Low} | {Primary/Secondary/Tertiary} |
| {Segment 2} | {users/companies} | {High/Med/Low} | {High/Med/Low} | {Primary/Secondary/Tertiary} |
| {Segment 3} | {users/companies} | {High/Med/Low} | {High/Med/Low} | {Primary/Secondary/Tertiary} |

**Primary beachhead segment**: {Which segment to target first and why}

### Positioning

**Category**: {What category do we compete in?}

**Target audience**: For {specific persona/segment}

**Problem**: who {specific problem statement}

**Solution**: {our product/feature} is a {category}

**Key benefit**: that {primary benefit delivered}

**Differentiation**: Unlike {competitor or alternative}, we {unique advantage}

### Messaging Hierarchy

**Core value proposition** (headline):
{One-sentence description of what this enables and why it matters}

**Supporting messages** (3-5 bullets):
- {Benefit 1}: {Explanation of value}
- {Benefit 2}: {Explanation of value}
- {Benefit 3}: {Explanation of value}
- {Benefit 4}: {Explanation of value}

**Proof points**:
- {Stat/testimonial/case study 1}
- {Stat/testimonial/case study 2}
- {Stat/testimonial/case study 3}

**Call to action**: {What do we want prospects to do?}

### Competitive Analysis

| Competitor | Their Positioning | Their Strength | Their Weakness | Our Angle |
|------------|------------------|---------------|---------------|-----------|
| {Competitor 1} | {how they position} | {what they do well} | {gap we exploit} | {our counter} |
| {Competitor 2} | {how they position} | {what they do well} | {gap we exploit} | {our counter} |
| {Competitor 3} | {how they position} | {what they do well} | {gap we exploit} | {our counter} |

**Competitive differentiation**:
1. {Primary differentiator and why it matters}
2. {Secondary differentiator and why it matters}
3. {Tertiary differentiator and why it matters}

### Go-to-Market Strategy

#### Launch Channels

| Channel | Tactic | Expected Reach | Cost | Priority |
|---------|--------|---------------|------|----------|
| {Channel 1} | {Specific approach} | {estimate} | {Low/Med/High} | {1/2/3} |
| {Channel 2} | {Specific approach} | {estimate} | {Low/Med/High} | {1/2/3} |
| {Channel 3} | {Specific approach} | {estimate} | {Low/Med/High} | {1/2/3} |

#### Launch Timeline

**Pre-launch (T-4 weeks)**:
- {Activity}
- {Activity}

**Launch week (T-0)**:
- {Activity}
- {Activity}

**Post-launch (T+4 weeks)**:
- {Activity}
- {Activity}

### Pricing & Packaging

**Pricing model**: {Per-seat / Usage-based / Flat-rate / Freemium}

**Recommended tier placement**: {Free / Pro / Enterprise / Add-on}

**Pricing rationale**: {Why this tier and why this price point}

| Tier | Price | Features Included | Target Customer |
|------|-------|------------------|----------------|
| {Tier 1} | {price} | {features} | {persona} |
| {Tier 2} | {price} | {features} | {persona} |
| {Tier 3} | {price} | {features} | {persona} |

### Customer Acquisition

**Acquisition strategy**: {How do we acquire first 100/1000/10000 users?}

**CAC estimate**: ${estimated customer acquisition cost}

**Payback period**: {months to recover CAC}

**Key conversion points**: {Where users decide to buy}

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Market risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Competitive risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Messaging risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |

### PMM Recommendation

**Decision**: {Launch / Don't Launch / Revise Positioning / Test First}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What market signal would flip this recommendation}
```

---

## Agent 3: Engineering Manager

### Evaluation Framework

1. **Technical Feasibility**: Can we build this with current technology and skills?
2. **Architecture Impact**: How does this affect system architecture? New patterns?
3. **Team Capacity**: Do we have the people and skills? What's the opportunity cost?
4. **Effort Estimation**: How long will this take? What's the confidence level?
5. **Technical Debt**: Will this create debt? Does it pay down existing debt?
6. **Dependencies**: What systems/teams does this depend on?
7. **Velocity Impact**: How does this affect our ability to ship other work?

### Output Template

```markdown
## Engineering Perspective

### Technical Feasibility

| Dimension | Assessment | Rationale |
|-----------|-----------|-----------|
| Technical risk | {Low/Medium/High/Unknown} | {key technical challenges} |
| Skills gap | {None/Small/Significant} | {what skills are missing} |
| Technology readiness | {Proven/Experimental/Unproven} | {maturity of tech required} |
| Integration complexity | {Simple/Moderate/Complex} | {how many systems affected} |

**Can we build this?**: {Yes / Yes with caveats / No / Need spike}

### Architecture Impact

**Current architecture**: {Brief description of relevant systems}

**Proposed changes**:
- {Change 1 and impact}
- {Change 2 and impact}
- {Change 3 and impact}

**New components required**:
- {Component 1}: {Purpose and rationale}
- {Component 2}: {Purpose and rationale}

**Affected systems**:

| System | Change Type | Risk | Owner |
|--------|------------|------|-------|
| {System 1} | {Modify/New/Integration} | {High/Med/Low} | {Team} |
| {System 2} | {Modify/New/Integration} | {High/Med/Low} | {Team} |

**Architectural principles**:
- ✅ {Principles this aligns with}
- ⚠️ {Principles this challenges}

### Effort Estimation

| Component | Effort | Confidence | Dependencies |
|-----------|--------|-----------|--------------|
| {Component 1} | {person-weeks} | {High/Med/Low} | {blockers} |
| {Component 2} | {person-weeks} | {High/Med/Low} | {blockers} |
| {Component 3} | {person-weeks} | {High/Med/Low} | {blockers} |
| {Testing & QA} | {person-weeks} | {High/Med/Low} | {blockers} |
| {Documentation} | {person-weeks} | {High/Med/Low} | {blockers} |
| **Total** | **{total person-weeks}** | | |

**Sizing**: {Small / Medium / Large / X-Large}

**Confidence**: {High / Medium / Low} — {what drives uncertainty}

**Best case**: {optimistic estimate}
**Expected case**: {realistic estimate}
**Worst case**: {pessimistic estimate}

### Team Capacity Analysis

**Current team state**:
- Team size: {N engineers}
- Current velocity: {story points / features per sprint}
- Runway committed: {N weeks/months of planned work}
- Skills available: {relevant skills present}

**Resource requirements**:
- Engineers needed: {N full-time equivalents}
- Duration: {weeks/months}
- Skills needed: {specific expertise required}

**Opportunity cost**: {What work would we defer to build this?}

### Technical Debt Implications

**Debt this creates**:
- {New debt 1 and future cost}
- {New debt 2 and future cost}

**Debt this pays down**:
- {Existing debt 1 and benefit}
- {Existing debt 2 and benefit}

**Net debt impact**: {Increases / Neutral / Reduces technical debt}

### Dependencies & Blockers

| Dependency | Type | Status | Risk | Mitigation |
|------------|------|--------|------|------------|
| {Dependency} | {Platform/Team/Third-party} | {Ready/At-risk/Blocked} | {High/Med/Low} | {Plan} |

### Velocity Impact

**During development**:
- Sprint velocity impact: {-X% for Y weeks}
- Feature work paused: {which work stops}
- On-call impact: {increased load or no change}

**Post-launch**:
- Maintenance overhead: {hours per week}
- Operational complexity: {monitoring, alerts, runbooks}
- Knowledge distribution: {how many people can support this}

### Testing & Quality

**Testing strategy**:
- Unit tests: {coverage target and approach}
- Integration tests: {what needs testing}
- E2E tests: {critical user flows}
- Performance tests: {load testing needs}

**QA requirements**:
- Manual testing: {what can't be automated}
- Beta testing: {internal vs external}
- Rollout plan: {phased vs big-bang}

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Technical risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Resource risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Schedule risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |

### EM Recommendation

**Decision**: {Build / Don't Build / Spike First / Defer}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What technical discovery would flip this recommendation}
```

---

## Agent 4: Financial Analyst

### Evaluation Framework

1. **Unit Economics**: What does each customer cost us? What do they generate?
2. **Revenue Impact**: How much revenue does this create or protect?
3. **Cost Structure**: What are the fixed and variable costs?
4. **Pricing Strategy**: How do we price this? What's the willingness to pay?
5. **ROI Analysis**: What's the payback period? What's the NPV?
6. **Budget Impact**: Does this fit in budget? What needs to be cut?
7. **Financial Risk**: What's the downside if this fails? What's the upside?

### Output Template

```markdown
## Financial Analysis

### Revenue Impact

**Revenue model**: {New revenue / Upsell / Retention / Efficiency}

**Revenue projection**:

| Timeline | Conservative | Expected | Optimistic |
|----------|-------------|----------|------------|
| Year 1 | ${amount} | ${amount} | ${amount} |
| Year 2 | ${amount} | ${amount} | ${amount} |
| Year 3 | ${amount} | ${amount} | ${amount} |

**Assumptions**:
1. {Assumption 1 underlying revenue model}
2. {Assumption 2 underlying revenue model}
3. {Assumption 3 underlying revenue model}

**Confidence**: {High / Medium / Low} — {what drives confidence}

### Cost Structure

**Development costs** (one-time):

| Category | Cost | Notes |
|----------|------|-------|
| Engineering | ${amount} | {person-months * loaded cost} |
| Design | ${amount} | {person-months * loaded cost} |
| Product | ${amount} | {person-months * loaded cost} |
| Infrastructure | ${amount} | {hosting, tools, licenses} |
| **Total Dev** | **${total}** | |

**Operating costs** (recurring):

| Category | Monthly Cost | Annual Cost | Notes |
|----------|-------------|-------------|-------|
| Infrastructure | ${amount} | ${amount} | {servers, storage, bandwidth} |
| Support | ${amount} | ${amount} | {support hours, tools} |
| Maintenance | ${amount} | ${amount} | {bug fixes, updates} |
| **Total OpEx** | **${total}** | **${total}** | |

### Unit Economics

**Customer acquisition cost (CAC)**: ${amount per customer}

**Customer lifetime value (LTV)**: ${amount per customer}

**LTV:CAC ratio**: {ratio} — {Healthy is >3:1}

**Payback period**: {months to recover CAC}

**Gross margin**: {%} — {Revenue - COGS / Revenue}

**Contribution margin**: {%} — {Revenue - Variable Costs / Revenue}

### ROI Analysis

**Total investment**: ${development costs + Y1 operating costs}

**Expected return** (3-year NPV): ${net present value}

**IRR** (Internal rate of return): {%}

**Payback period**: {months until cumulative cash flow positive}

**Break-even point**: {customers or revenue to break even}

| Metric | Year 1 | Year 2 | Year 3 | Total |
|--------|--------|--------|--------|-------|
| Revenue | ${amount} | ${amount} | ${amount} | ${amount} |
| Costs | ${amount} | ${amount} | ${amount} | ${amount} |
| Profit | ${amount} | ${amount} | ${amount} | ${amount} |
| Cumulative | ${amount} | ${amount} | ${amount} | ${amount} |

### Pricing Strategy

**Recommended pricing model**: {Freemium / Tiered / Usage-based / Flat-rate}

**Price point**: ${amount} per {unit}

**Competitor pricing**:

| Competitor | Price | Our Position |
|------------|-------|-------------|
| {Competitor 1} | ${price} | {Higher/Same/Lower} |
| {Competitor 2} | ${price} | {Higher/Same/Lower} |
| {Competitor 3} | ${price} | {Higher/Same/Lower} |

**Pricing rationale**: {Why this price point makes sense}

**Price sensitivity**: {Elasticity estimate — how demand changes with price}

**Upsell potential**: {Can we upsell to higher tiers? What's the path?}

### Budget Impact

**Budget required**: ${total investment needed}

**Budget available**: ${current budget allocation}

**Gap**: ${shortfall if any}

**Trade-offs**: {What else competes for this budget?}

**Approval required**: {Who needs to sign off on this spend?}

### Sensitivity Analysis

**Key variables affecting ROI**:

| Variable | Base Case | Downside | Impact on ROI |
|----------|-----------|----------|--------------|
| Adoption rate | {%} | {lower %} | {-X% ROI} |
| Price point | ${amount} | ${lower} | {-X% ROI} |
| Development cost | ${amount} | ${higher} | {-X% ROI} |
| Churn rate | {%} | {higher %} | {-X% ROI} |

**What needs to be true**: {For this to be a good investment, which variables must hit targets?}

### Financial Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Revenue risk} | {High/Med/Low} | ${impact} | {Strategy} |
| {Cost risk} | {High/Med/Low} | ${impact} | {Strategy} |
| {Market risk} | {High/Med/Low} | ${impact} | {Strategy} |

**Downside scenario**: {What happens if this fails?}
**Cost to company**: ${amount}
**Opportunity cost**: {What else could we do with this investment?}

### Finance Recommendation

**Decision**: {Fund / Don't Fund / Reduce Scope / Pilot First}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What financial metric would flip this recommendation}
```

---

## Agent 5: Data Scientist

### Evaluation Framework

1. **Analytics Requirements**: What data do we need to measure success?
2. **ML Opportunities**: Could ML improve this feature? What's the ROI?
3. **Experiment Design**: How do we A/B test this? What's the sample size?
4. **Success Metrics**: What metrics prove this works? How do we instrument them?
5. **Data Availability**: Do we have the data? Do we need to collect new signals?
6. **Model Requirements**: If ML is involved, what models? What training data?
7. **Inference Infrastructure**: How do we serve predictions at scale?

### Output Template

```markdown
## Data Science Perspective

### Analytics Requirements

**Primary metrics**:

| Metric | Definition | Measurement | Target | Current |
|--------|-----------|-------------|--------|---------|
| {North star metric} | {formula} | {how to measure} | {goal} | {baseline} |
| {Engagement metric} | {formula} | {how to measure} | {goal} | {baseline} |
| {Quality metric} | {formula} | {how to measure} | {goal} | {baseline} |

**Supporting metrics**:
- {Metric 1}: {Why this matters}
- {Metric 2}: {Why this matters}
- {Metric 3}: {Why this matters}

**Instrumentation needs**:
- {Event 1 to track}
- {Event 2 to track}
- {Event 3 to track}

### Experiment Design

**Hypothesis**: {If we do X, we expect Y because Z}

**Test type**: {A/B test / Multivariate / Phased rollout}

**Variants**:
- Control: {Current experience}
- Treatment: {New feature}

**Randomization unit**: {User / Session / Organization}

**Sample size calculation**:
- Baseline conversion: {%}
- Minimum detectable effect: {%}
- Power: {typically 80%}
- Significance: {typically 95%}
- **Required sample size**: {N users per variant}

**Duration**: {Days/weeks to reach sample size}

**Success criteria**: {Metric must move by X% to declare winner}

**Guardrail metrics**: {Metrics we don't want to hurt}

### ML Opportunities

**Potential ML applications**:

| Application | Value Proposition | Feasibility | Priority |
|-------------|------------------|------------|----------|
| {Use case 1} | {What it enables} | {High/Med/Low} | {P0/P1/P2} |
| {Use case 2} | {What it enables} | {High/Med/Low} | {P0/P1/P2} |
| {Use case 3} | {What it enables} | {High/Med/Low} | {P0/P1/P2} |

**Recommended approach**: {Which ML application to pursue, if any}

### Model Requirements (if ML is involved)

**Problem type**: {Classification / Regression / Ranking / Generation / etc.}

**Model candidates**:
- {Model 1}: {Pros/cons}
- {Model 2}: {Pros/cons}
- {Model 3}: {Pros/cons}

**Training data requirements**:
- Volume: {N examples needed}
- Quality: {Labeling requirements}
- Freshness: {How often to retrain}
- Availability: {Do we have this data?}

**Feature engineering**:
- {Feature 1}: {Description and source}
- {Feature 2}: {Description and source}
- {Feature 3}: {Description and source}

**Model evaluation**:
- Primary metric: {e.g., AUC-ROC, RMSE, F1}
- Target performance: {Threshold for production}
- Baseline comparison: {What do we beat?}

### Inference Infrastructure

**Serving requirements**:
- Latency: {target p99 latency}
- Throughput: {requests per second}
- Availability: {uptime requirement}

**Inference mode**: {Real-time / Batch / Hybrid}

**Infrastructure**:
- Model hosting: {Where models run}
- Feature store: {Real-time features}
- Caching: {What to cache}

**Cost estimate**: ${cost per 1000 predictions}

### Data Availability

**Data we have**:
- {Dataset 1}: {Volume, freshness, quality}
- {Dataset 2}: {Volume, freshness, quality}

**Data gaps**:
- {Missing data 1}: {Impact and how to collect}
- {Missing data 2}: {Impact and how to collect}

**Data collection plan**:
- {New event/signal 1}: {What to track}
- {New event/signal 2}: {What to track}

**Privacy considerations**: {PII handling, consent, compliance}

### Monitoring & Alerting

**Model performance monitoring** (if ML):
- Prediction distribution drift
- Feature drift
- Label drift
- Model accuracy degradation

**Business metrics monitoring**:
- {Metric 1}: Alert if < {threshold}
- {Metric 2}: Alert if > {threshold}

**Dashboard requirements**: {What stakeholders need to see}

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Data quality risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Model performance risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Privacy/compliance risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |

### DS Recommendation

**Decision**: {Instrument / Build Model / Experiment First / Not Worth It}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What data finding would flip this recommendation}
```

---

## Agent 6: Data Engineer

### Evaluation Framework

1. **Data Pipeline**: What data needs to flow where? Real-time or batch?
2. **Storage Strategy**: How do we store this data? What's the volume?
3. **Data Quality**: How do we ensure data accuracy and completeness?
4. **Infrastructure**: What systems do we need? What's the capacity?
5. **ETL/ELT**: How do we transform and load data?
6. **Compliance**: GDPR, CCPA, data retention policies?
7. **Cost**: What's the infrastructure cost at scale?

### Output Template

```markdown
## Data Engineering Perspective

### Data Pipeline Architecture

**Data flow**:

```
[Source 1] → [Ingestion] → [Processing] → [Storage] → [Consumption]
[Source 2] ↗                                          ↓
[Source 3] ↗                                    [Analytics]
                                                     ↓
                                                  [ML Models]
```

**Pipeline components**:

| Component | Technology | Purpose | Latency |
|-----------|-----------|---------|---------|
| {Ingestion} | {Tool/service} | {What it does} | {Real-time/Batch} |
| {Processing} | {Tool/service} | {What it does} | {Seconds/Minutes/Hours} |
| {Storage} | {Database/warehouse} | {What it stores} | {Query latency} |

### Data Sources

| Source | Volume | Frequency | Format | Quality |
|--------|--------|-----------|--------|---------|
| {Source 1} | {records/day} | {Real-time/Hourly/Daily} | {JSON/CSV/etc} | {High/Med/Low} |
| {Source 2} | {records/day} | {Real-time/Hourly/Daily} | {JSON/CSV/etc} | {High/Med/Low} |
| {Source 3} | {records/day} | {Real-time/Hourly/Daily} | {JSON/CSV/etc} | {High/Med/Low} |

**New data collection required**:
- {Event 1}: {What to capture, volume estimate}
- {Event 2}: {What to capture, volume estimate}

### Storage Strategy

**Primary storage**:

| Data Type | Storage System | Volume (current) | Volume (1 year) | Retention |
|-----------|---------------|-----------------|----------------|-----------|
| {Transactional} | {PostgreSQL/etc} | {GB/TB} | {GB/TB} | {duration} |
| {Analytics} | {Warehouse} | {GB/TB} | {GB/TB} | {duration} |
| {ML features} | {Feature store} | {GB/TB} | {GB/TB} | {duration} |
| {Logs/events} | {Object storage} | {GB/TB} | {GB/TB} | {duration} |

**Storage costs**:
- Current: ${monthly cost}
- Year 1: ${projected monthly cost}
- Year 2: ${projected monthly cost}

**Data modeling**:
- Schema design: {Star schema / Snowflake / OBT / etc}
- Partitioning: {By what columns/dimensions}
- Indexing: {What needs indexes}

### Data Quality

**Quality dimensions**:

| Dimension | Current State | Target State | How to Achieve |
|-----------|--------------|-------------|----------------|
| Completeness | {%} | {%} | {Strategy} |
| Accuracy | {%} | {%} | {Strategy} |
| Consistency | {%} | {%} | {Strategy} |
| Timeliness | {lag} | {lag} | {Strategy} |

**Data validation rules**:
- {Rule 1}: {What to check}
- {Rule 2}: {What to check}
- {Rule 3}: {What to check}

**Data quality monitoring**:
- Automated checks: {What to validate}
- Alerting thresholds: {When to alert}
- Remediation process: {How to fix issues}

### ETL/ELT Pipeline

**Processing approach**: {ETL (transform before load) / ELT (transform after load)}

**Transformation logic**:
1. {Transform 1}: {What it does}
2. {Transform 2}: {What it does}
3. {Transform 3}: {What it does}

**Orchestration**:
- Tool: {Airflow / Prefect / Step Functions / etc}
- Schedule: {How often pipelines run}
- Dependencies: {What depends on what}

**Error handling**:
- Retry policy: {How many retries, backoff}
- Dead letter queue: {Where failed records go}
- Alerting: {Who gets paged for failures}

### Infrastructure Requirements

**Compute**:
- Processing: {CPU/memory requirements}
- Concurrency: {Parallel jobs needed}
- Scaling: {Auto-scaling strategy}

**Networking**:
- Bandwidth: {GB/day to transfer}
- Latency: {Acceptable lag}
- Security: {VPC, encryption in transit}

**Capacity planning**:

| Resource | Current | Year 1 | Year 2 | Growth Factor |
|----------|---------|--------|--------|--------------|
| Storage | {TB} | {TB} | {TB} | {X%} |
| Compute | {hours/day} | {hours/day} | {hours/day} | {X%} |
| Bandwidth | {GB/day} | {GB/day} | {GB/day} | {X%} |

### Compliance & Governance

**Data privacy**:
- PII handling: {How to anonymize/pseudonymize}
- User consent: {Opt-in/opt-out mechanisms}
- Right to deletion: {How to honor delete requests}

**Compliance requirements**:
- GDPR: {Applicable? What controls?}
- CCPA: {Applicable? What controls?}
- SOC 2: {Applicable? What controls?}
- HIPAA: {Applicable? What controls?}

**Data retention**:
- Hot storage: {Duration}
- Cold storage: {Duration}
- Deletion policy: {When to purge}

**Access control**:
- Who can access: {Roles/teams}
- Audit logging: {What to log}
- Data masking: {What to mask for whom}

### Cost Analysis

**Infrastructure costs** (monthly):

| Component | Current | Year 1 | Year 2 |
|-----------|---------|--------|--------|
| Storage | ${amount} | ${amount} | ${amount} |
| Compute | ${amount} | ${amount} | ${amount} |
| Data transfer | ${amount} | ${amount} | ${amount} |
| Tooling/licenses | ${amount} | ${amount} | ${amount} |
| **Total** | **${total}** | **${total}** | **${total}** |

**Cost optimization opportunities**:
- {Opportunity 1 and savings estimate}
- {Opportunity 2 and savings estimate}

### Implementation Plan

**Phase 1** (Weeks 1-4):
- {Deliverable}
- {Deliverable}

**Phase 2** (Weeks 5-8):
- {Deliverable}
- {Deliverable}

**Phase 3** (Weeks 9-12):
- {Deliverable}
- {Deliverable}

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Data pipeline failure} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Capacity shortage} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Compliance violation} | {High/Med/Low} | {High/Med/Low} | {Strategy} |

### DE Recommendation

**Decision**: {Build / Don't Build / Use Managed Service / Defer}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What infrastructure constraint would flip this recommendation}
```

---

## Agent 7: Sales Engineer

### Evaluation Framework

1. **Customer Objections**: What concerns will prospects raise? How do we address them?
2. **Deal Blockers**: What prevents deals from closing? Does this fix or create blockers?
3. **Demo Readiness**: Can we demo this effectively? What's the demo story?
4. **Integration Requirements**: What systems must this integrate with? How complex?
5. **Enterprise Readiness**: SSO, audit logs, data residency, compliance needs?
6. **Onboarding Complexity**: How hard is it to get customers live? Time to value?
7. **Competitive Positioning**: How do we win against competitors with this?

### Output Template

```markdown
## Sales Engineering Perspective

### Customer Objections

**Anticipated objections**:

| Objection | Frequency | Severity | Counter-Argument | Proof Required |
|-----------|-----------|----------|-----------------|---------------|
| {Objection 1} | {Common/Occasional/Rare} | {High/Med/Low} | {How to respond} | {Demo/case study/docs} |
| {Objection 2} | {Common/Occasional/Rare} | {High/Med/Low} | {How to respond} | {Demo/case study/docs} |
| {Objection 3} | {Common/Occasional/Rare} | {High/Med/Low} | {How to respond} | {Demo/case study/docs} |

**Showstopper objections** (deal-killers if we can't address):
1. {Objection and impact}
2. {Objection and impact}

### Deal Blockers

**Current blockers this fixes**:
- {Blocker 1}: {How this addresses it}
- {Blocker 2}: {How this addresses it}

**New blockers this creates**:
- {Blocker 1}: {Why it's a concern, how to mitigate}
- {Blocker 2}: {Why it's a concern, how to mitigate}

**Net impact on deal velocity**: {Faster / Neutral / Slower} — {rationale}

### Demo Readiness

**Demo story**:

1. **Setup** (Context): {What problem does the prospect have?}
2. **Conflict** (Pain): {Why is this painful? What's at stake?}
3. **Resolution** (Demo): {Show how this feature solves it}
4. **Outcome** (Value): {What does success look like?}

**Demo flow** (5-10 minutes):

| Step | Action | Talking Points | What to Show |
|------|--------|---------------|--------------|
| 1 | {Setup} | {What to say} | {What to display} |
| 2 | {Problem} | {What to say} | {What to display} |
| 3 | {Solution} | {What to say} | {What to display} |
| 4 | {Value} | {What to say} | {What to display} |

**Demo assets needed**:
- {Asset 1}: {Video, slides, sandbox, etc.}
- {Asset 2}: {Video, slides, sandbox, etc.}

**Demo risks**:
- {Risk 1}: {What could go wrong, how to recover}
- {Risk 2}: {What could go wrong, how to recover}

### Integration Requirements

**Must-have integrations** (deal-blockers):

| Integration | Priority | Complexity | Status | Impact if Missing |
|-------------|---------|-----------|--------|------------------|
| {Integration 1} | {P0/P1/P2} | {Simple/Moderate/Complex} | {Available/Planned/Not planned} | {Deal impact} |
| {Integration 2} | {P0/P1/P2} | {Simple/Moderate/Complex} | {Available/Planned/Not planned} | {Deal impact} |

**Nice-to-have integrations**:
- {Integration 3}: {Why it helps close deals}
- {Integration 4}: {Why it helps close deals}

**API/webhook requirements**:
- {Requirement 1}: {What customers need to build}
- {Requirement 2}: {What customers need to build}

### Enterprise Readiness

**Enterprise requirements**:

| Requirement | Current State | Gap | Priority | Customer Impact |
|-------------|--------------|-----|----------|----------------|
| SSO/SAML | {Available/Partial/Missing} | {What's needed} | {P0/P1/P2} | {Blocker/Nice-to-have} |
| Audit logs | {Available/Partial/Missing} | {What's needed} | {P0/P1/P2} | {Blocker/Nice-to-have} |
| Data residency | {Available/Partial/Missing} | {What's needed} | {P0/P1/P2} | {Blocker/Nice-to-have} |
| SLA guarantees | {Available/Partial/Missing} | {What's needed} | {P0/P1/P2} | {Blocker/Nice-to-have} |
| Custom contracts | {Available/Partial/Missing} | {What's needed} | {P0/P1/P2} | {Blocker/Nice-to-have} |
| Support SLAs | {Available/Partial/Missing} | {What's needed} | {P0/P1/P2} | {Blocker/Nice-to-have} |

**Compliance certifications**:
- SOC 2: {Type I/II, status}
- GDPR: {Compliant/In progress/Not applicable}
- HIPAA: {Compliant/In progress/Not applicable}
- ISO 27001: {Certified/In progress/Not applicable}

### Onboarding Complexity

**Time to value**: {Hours/Days/Weeks from contract to production}

**Onboarding steps**:

| Step | Owner | Duration | Complexity | Blocker Risk |
|------|-------|----------|------------|-------------|
| {Step 1} | {Customer/Us/Shared} | {time} | {Easy/Med/Hard} | {High/Med/Low} |
| {Step 2} | {Customer/Us/Shared} | {time} | {Easy/Med/Hard} | {High/Med/Low} |
| {Step 3} | {Customer/Us/Shared} | {time} | {Easy/Med/Hard} | {High/Med/Low} |

**Onboarding friction points**:
- {Friction 1}: {Why it's hard, how to ease}
- {Friction 2}: {Why it's hard, how to ease}

**Support requirements**:
- Documentation: {What docs are needed}
- Training: {Live training, videos, webinars?}
- Professional services: {When do customers need help?}

### Competitive Positioning

**How this affects competitive deals**:

| Competitor | Their Advantage | Our New Advantage | Net Impact |
|------------|----------------|-------------------|------------|
| {Competitor 1} | {What they tout} | {How this levels/beats them} | {Win more/Neutral/Lose less} |
| {Competitor 2} | {What they tout} | {How this levels/beats them} | {Win more/Neutral/Lose less} |

**Win themes** (key reasons customers choose us):
1. {Win theme 1 and how this feature strengthens it}
2. {Win theme 2 and how this feature strengthens it}
3. {Win theme 3 and how this feature strengthens it}

**Loss reasons** (why deals slip to competitors):
- {Loss reason 1}: {Does this fix it?}
- {Loss reason 2}: {Does this fix it?}

### Customer Segments

**Who will buy this?**:

| Segment | Interest Level | Willingness to Pay | Deal Size | Priority |
|---------|---------------|-------------------|-----------|----------|
| {Segment 1} | {High/Med/Low} | {High/Med/Low} | ${ACV} | {P0/P1/P2} |
| {Segment 2} | {High/Med/Low} | {High/Med/Low} | ${ACV} | {P0/P1/P2} |
| {Segment 3} | {High/Med/Low} | {High/Med/Low} | ${ACV} | {P0/P1/P2} |

**Ideal customer profile** for this feature:
- Industry: {verticals most interested}
- Company size: {employee range}
- Tech stack: {what they use}
- Pain level: {how acute is the problem}

### Sales Enablement Needs

**What sales needs to close deals**:
- {Asset 1}: {One-pager, demo video, case study, etc.}
- {Asset 2}: {One-pager, demo video, case study, etc.}
- {Asset 3}: {One-pager, demo video, case study, etc.}

**Training requirements**:
- Sales training: {What reps need to know}
- SE training: {Deep technical training needs}
- Duration: {Hours/days to train team}

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {Demo failure risk} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Integration blocker} | {High/Med/Low} | {High/Med/Low} | {Strategy} |
| {Competitive response} | {High/Med/Low} | {High/Med/Low} | {Strategy} |

### SE Recommendation

**Decision**: {Accelerates Deals / Neutral / Slows Deals / Not Worth It}

**Rationale**: {2-3 sentences justifying recommendation}

**Confidence**: {High / Medium / Low} — {what drives confidence level}

**What would change my mind**: {What customer signal would flip this recommendation}
```

---

## Agent 8: Synthesizer

### Evaluation Framework

The synthesizer receives ALL prior agent findings and produces a balanced recommendation.

1. **Consensus Analysis**: Where do agents agree? Where do they conflict?
2. **Critical Path**: What are the gating factors? What must be true for success?
3. **Risk Consolidation**: What are the top 3-5 risks across all dimensions?
4. **Trade-Off Analysis**: What are we optimizing for? What are we sacrificing?
5. **Go/No-Go**: Clear recommendation with rationale
6. **Next Steps**: Prioritized action plan with owners and timelines

### Output Template

```markdown
## Synthesis & Recommendation

### Executive Summary

{2-3 paragraphs synthesizing all perspectives into a coherent narrative. What's the opportunity? What are the risks? What's the recommendation?}

### Consensus & Conflicts

**Strong consensus** (all agents agree):
- {Point 1}
- {Point 2}
- {Point 3}

**Significant conflicts** (agents disagree):

| Conflict | Perspectives | Trade-Off | Resolution |
|----------|-------------|-----------|------------|
| {Issue} | {Who disagrees, what they say} | {What we're trading off} | {How to resolve} |

### Critical Success Factors

**What must be true for this to succeed**:

1. {Factor 1} — {Why it's critical, who owns it}
2. {Factor 2} — {Why it's critical, who owns it}
3. {Factor 3} — {Why it's critical, who owns it}
4. {Factor 4} — {Why it's critical, who owns it}
5. {Factor 5} — {Why it's critical, who owns it}

### Consolidated Risk Assessment

**Top 5 risks** (across all dimensions):

| Rank | Risk | Domain | Likelihood | Impact | Mitigation Owner |
|------|------|--------|-----------|--------|-----------------|
| 1 | {Risk} | {PM/Eng/Finance/etc} | {High/Med/Low} | {High/Med/Low} | {Who} |
| 2 | {Risk} | {PM/Eng/Finance/etc} | {High/Med/Low} | {High/Med/Low} | {Who} |
| 3 | {Risk} | {PM/Eng/Finance/etc} | {High/Med/Low} | {High/Med/Low} | {Who} |
| 4 | {Risk} | {PM/Eng/Finance/etc} | {High/Med/Low} | {High/Med/Low} | {Who} |
| 5 | {Risk} | {PM/Eng/Finance/etc} | {High/Med/Low} | {High/Med/Low} | {Who} |

### Trade-Off Analysis

**Optimizing for**: {What are we prioritizing? Speed? Quality? Revenue? Strategic value?}

**Sacrificing**: {What are we de-prioritizing or accepting as a cost?}

**Alternative approaches considered**:

| Alternative | Pros | Cons | Why Not Chosen |
|-------------|------|------|----------------|
| {Alt 1} | {Benefits} | {Drawbacks} | {Rationale} |
| {Alt 2} | {Benefits} | {Drawbacks} | {Rationale} |

### GO / NO-GO Decision

**Recommendation**: {GO / NO-GO / CONDITIONAL GO / DEFER / PIVOT}

**Rationale**: {3-5 sentences explaining the decision. Balance all perspectives and make a clear call.}

**Confidence level**: {High / Medium / Low}

**Confidence drivers**:
- ✅ {What increases confidence}
- ⚠️ {What reduces confidence}

**Decision criteria met**:

| Criterion | Status | Notes |
|-----------|--------|-------|
| Strategic alignment | ✅/⚠️/❌ | {Brief rationale} |
| Technical feasibility | ✅/⚠️/❌ | {Brief rationale} |
| Financial viability | ✅/⚠️/❌ | {Brief rationale} |
| Market opportunity | ✅/⚠️/❌ | {Brief rationale} |
| Resource availability | ✅/⚠️/❌ | {Brief rationale} |
| Risk acceptability | ✅/⚠️/❌ | {Brief rationale} |

### Recommended Action Plan

**Phase 1: Pre-Work** (Before committing to build)
1. {Action} — {Owner} — {Timeline} — {Exit criteria}
2. {Action} — {Owner} — {Timeline} — {Exit criteria}

**Phase 2: Build** (If Phase 1 validates)
1. {Action} — {Owner} — {Timeline} — {Success metric}
2. {Action} — {Owner} — {Timeline} — {Success metric}
3. {Action} — {Owner} — {Timeline} — {Success metric}

**Phase 3: Launch** (After build completes)
1. {Action} — {Owner} — {Timeline} — {Success metric}
2. {Action} — {Owner} — {Timeline} — {Success metric}

### Open Questions & Research Needs

**Critical questions requiring resolution**:

| Question | Impact on Decision | Owner | Deadline |
|----------|-------------------|-------|----------|
| {Question 1} | {High/Med/Low} | {Who} | {When} |
| {Question 2} | {High/Med/Low} | {Who} | {When} |
| {Question 3} | {High/Med/Low} | {Who} | {When} |

### Success Metrics

**How we'll know this succeeded** (90 days post-launch):

| Metric | Baseline | Target | Stretch | Owner |
|--------|---------|--------|---------|-------|
| {Primary metric} | {value} | {value} | {value} | {Who} |
| {Secondary metric} | {value} | {value} | {value} | {Who} |
| {Tertiary metric} | {value} | {value} | {value} | {Who} |

**Review cadence**: {When to check in on these metrics}

### Dissenting Opinions

**Documented dissent** (if any agent strongly disagrees with the recommendation):

- **{Agent role}**: {Their dissenting view and rationale}
- **{Agent role}**: {Their dissenting view and rationale}

{These are included for the record and to ensure minority perspectives are heard.}
```

---

## Cross-Agent Coordination Notes

- **Phase 1 agents** (PM, PMM, EM, Finance) run in parallel and should not wait for each other.
- **Phase 2 agents** (DS, DE, Sales) receive Phase 1 findings as input and run in parallel.
- **Phase 3 agent** (Synthesizer) receives ALL prior findings and runs sequentially.
- Agents should flag when they need input from another agent (e.g., Finance needs EM effort estimates).
- Agents should explicitly state confidence levels and what would increase confidence.
- Disagreement is expected and valuable — the Synthesizer's job is to resolve conflicts, not eliminate them.
