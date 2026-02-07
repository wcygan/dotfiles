# Competitor Analysis — Agent Reference

Detailed research checklists and output templates for each of the 7 research agents.

## Common Research Guidelines

All agents must follow these rules:

### Citation Rules
- Every factual claim must include a source URL
- Use `[Source](url)` format for inline citations
- If information cannot be verified, prefix with "Unverified:" or "Estimated:"
- Distinguish between official sources (company website, docs) and third-party sources (reviews, articles, social media)

### WebSearch Strategies
- Start with the company's own website and docs
- Search for `"{company name}" {topic}` with quotes for precise matches
- Check recent results (past 12 months) for current information
- Cross-reference claims across multiple sources
- Try variations: company blog, engineering blog, press releases, job postings

### Time-Boxing
- Spend no more than 8-12 search queries per agent
- If information isn't found after reasonable effort, note "Not publicly available" and move on
- Prioritize breadth over depth — cover all template sections rather than exhaustively researching one

### Output Quality
- Use tables where structured data is available
- Include confidence levels (High/Medium/Low) for inferred information
- Keep sections concise but substantive — aim for actionable intelligence, not padding
- Flag anything surprising or counterintuitive

---

## Agent 1: Product Overview

### Research Checklist

1. **WebFetch** the product homepage — extract tagline, value proposition, hero messaging
2. **WebSearch** `"{company}" product features` — find feature pages, comparison pages
3. **WebSearch** `"{company}" pricing plans` — find pricing page or pricing announcements
4. **WebFetch** the pricing page if it exists
5. **WebSearch** `"{company}" integrations marketplace` — find integration/plugin ecosystem
6. **WebSearch** `"{company}" about company founded funding` — find company background
7. **WebSearch** `"{company}" changelog "what's new" updates 2025 2026` — find recent product updates
8. **WebSearch** `"{company}" vs` — find competitor comparison pages (reveals positioning)

### Output Template

```markdown
## Product Overview: {Company}

### Company Snapshot

| Field | Value |
|-------|-------|
| Founded | {year} |
| Headquarters | {location} |
| Funding | {total raised, last round} |
| Estimated employees | {range} |
| Estimated revenue | {range if available} |
| Category | {e.g., "Project Management", "Design Tool"} |

### Value Proposition
{One-paragraph summary of what the product does and who it's for}

### The "Aha" Moment
{What makes users go "wow" — the core differentiator that hooks people}

### Feature Breakdown

| Feature | Description | Tier Availability | Competitive Strength |
|---------|-------------|-------------------|---------------------|
| {feature 1} | {brief description} | {Free/Pro/Enterprise} | {Strong/Average/Weak} |
| {feature 2} | ... | ... | ... |
| {feature 3} | ... | ... | ... |
| ... | ... | ... | ... |

List 8-15 key features. Focus on what drives purchasing decisions.

### Pricing Tiers

| Tier | Price | Key Limits | Target User |
|------|-------|-----------|-------------|
| {Free/Starter} | {price} | {limits} | {persona} |
| {Pro} | {price} | {limits} | {persona} |
| {Enterprise} | {price} | {limits} | {persona} |

### Platform Availability

| Platform | Status |
|----------|--------|
| Web app | {Yes/No} |
| Desktop (macOS) | {Yes/No} |
| Desktop (Windows) | {Yes/No} |
| Desktop (Linux) | {Yes/No} |
| iOS | {Yes/No} |
| Android | {Yes/No} |
| API | {Yes/No — link to docs} |
| CLI | {Yes/No} |

### Integrations Ecosystem

| Category | Integrations |
|----------|-------------|
| Communication | {Slack, Teams, etc.} |
| Development | {GitHub, GitLab, etc.} |
| Productivity | {Google Workspace, etc.} |
| Other | {notable integrations} |

Total integration count: {N}

### Recent Product Updates (last 6 months)
- {date}: {update summary}
- {date}: {update summary}
- {date}: {update summary}
```

---

## Agent 2: Marketing Analysis

### Research Checklist

1. **WebFetch** the homepage — analyze messaging hierarchy, CTAs, social proof
2. **WebSearch** `"{company}" blog` — find and sample their content strategy
3. **WebSearch** `site:twitter.com OR site:x.com "{company}"` — find social presence
4. **WebSearch** `site:linkedin.com "{company}"` — find LinkedIn presence and employee count
5. **WebSearch** `"{company}" case study customer story` — find customer stories
6. **WebSearch** `"{company}" webinar event conference 2025 2026` — find event marketing
7. **WebSearch** `"{company}" vs {likely competitor}` — find comparison marketing
8. **WebSearch** `"{company}" review G2 Capterra` — find review site presence

### Output Template

```markdown
## Marketing Analysis: {Company}

### Target Personas

| Persona | Title/Role | Pain Points Addressed | Messaging Angle |
|---------|-----------|----------------------|-----------------|
| {Primary} | {e.g., "Engineering Manager"} | {pain points} | {how they message to this persona} |
| {Secondary} | ... | ... | ... |
| {Tertiary} | ... | ... | ... |

### Messaging Hierarchy

**Tagline**: "{exact tagline from homepage}"

**Primary message**: {the main value proposition as communicated}

**Supporting messages**:
1. {supporting message 1}
2. {supporting message 2}
3. {supporting message 3}

**Emotional vs Rational**: {ratio assessment — does messaging lean emotional ("delight") or rational ("save 40% time")?}

### Social Proof Strategy

| Type | Examples | Volume |
|------|----------|--------|
| Customer logos | {notable logos} | {count on homepage} |
| Testimonials | {example quote} | {count} |
| Case studies | {titles} | {count} |
| Metrics | {e.g., "50,000 teams"} | {types of metrics used} |
| Awards/badges | {G2 badges, etc.} | {count} |

### Acquisition Channels

| Channel | Activity Level | Evidence |
|---------|---------------|----------|
| SEO/Content | {High/Medium/Low} | {blog frequency, topic coverage} |
| Paid Search | {High/Medium/Low} | {ad presence for key terms} |
| Social Media | {High/Medium/Low} | {platforms, posting frequency} |
| Community | {High/Medium/Low} | {forums, Discord, Slack community} |
| Events | {High/Medium/Low} | {conferences, webinars} |
| Product-led Growth | {High/Medium/Low} | {free tier, viral mechanics} |
| Partnerships | {High/Medium/Low} | {integration partnerships, co-marketing} |

### Content Strategy

| Content Type | Frequency | Quality | Topics |
|-------------|-----------|---------|--------|
| Blog posts | {posts/month} | {assessment} | {topic themes} |
| Docs/Guides | {assessment} | {assessment} | {coverage} |
| Video | {frequency} | {assessment} | {types} |
| Podcasts | {if any} | {assessment} | {themes} |
| Newsletter | {if any} | {assessment} | {themes} |

### Review Site Presence

| Platform | Rating | Review Count | Sentiment Summary |
|----------|--------|-------------|-------------------|
| G2 | {rating} | {count} | {key themes} |
| Capterra | {rating} | {count} | {key themes} |
| Product Hunt | {upvotes} | {launch date} | {reception} |
| TrustRadius | {rating} | {count} | {key themes} |
```

---

## Agent 3: UX Analysis

### Research Checklist

1. **WebFetch** the signup/registration page — analyze friction, required fields, social login options
2. **WebFetch** the product page or demo page — look for interactive demos, screenshots, videos
3. **WebSearch** `"{company}" onboarding experience review` — find UX reviews and teardowns
4. **WebSearch** `"{company}" user interface design` — find design commentary
5. **WebSearch** `site:youtube.com "{company}" demo walkthrough` — find product demos
6. **WebSearch** `"{company}" mobile app review` — find app store reviews and UX commentary
7. **WebFetch** their docs/help center — assess information architecture
8. **WebSearch** `"{company}" UX redesign update new` — find recent UX changes

### Output Template

```markdown
## UX Analysis: {Company}

### Signup Flow

| Step | Action Required | Friction Level |
|------|----------------|----------------|
| 1 | {e.g., "Enter email"} | {Low/Medium/High} |
| 2 | {e.g., "Verify email"} | ... |
| 3 | {e.g., "Set password"} | ... |
| 4 | {e.g., "Choose plan"} | ... |

**Total steps to first value**: {N}
**Social login options**: {Google, GitHub, SSO, etc.}
**Credit card required for free tier**: {Yes/No}
**Time to signup (estimated)**: {seconds/minutes}

### Onboarding Experience

| Element | Present | Description |
|---------|---------|-------------|
| Welcome wizard | {Yes/No} | {description} |
| Template gallery | {Yes/No} | {description} |
| Interactive tutorial | {Yes/No} | {description} |
| Sample data | {Yes/No} | {description} |
| Checklist/progress | {Yes/No} | {description} |
| Contextual tooltips | {Yes/No} | {description} |
| Empty state guidance | {Yes/No} | {description} |

**Time to "aha" moment**: {estimated time from signup to core value}

### Core Usage Loop

```
{Describe the primary user workflow as a loop}
Example:
1. Create task → 2. Assign + prioritize → 3. Work on task → 4. Update status → 5. Review in board view → repeat
```

**Primary interaction pattern**: {e.g., "kanban drag-and-drop", "command palette", "inline editing"}

### Key UX Patterns

| Pattern | Implementation | Quality |
|---------|---------------|---------|
| Navigation | {sidebar/top-nav/command-palette} | {assessment} |
| Search | {global/contextual/command-palette} | {assessment} |
| Keyboard shortcuts | {extensive/basic/none} | {assessment} |
| Real-time collaboration | {cursors/presence/comments} | {assessment} |
| Mobile experience | {native/responsive/none} | {assessment} |
| Dark mode | {Yes/No/System} | {assessment} |
| Accessibility | {WCAG level if known} | {assessment} |
| Performance feel | {snappy/adequate/sluggish} | {assessment} |

### Upgrade/Paywall Experience

| Trigger | What Happens | Friction |
|---------|-------------|----------|
| {e.g., "Hit member limit"} | {modal, inline, banner?} | {assessment} |
| {e.g., "Try premium feature"} | {description} | {assessment} |

**Upgrade CTA style**: {aggressive/subtle/contextual}
**Trial offered**: {Yes/No, duration}

### UX Strengths and Weaknesses

**Strengths**:
1. {top UX strength}
2. {second strength}
3. {third strength}

**Weaknesses**:
1. {top UX weakness}
2. {second weakness}
3. {third weakness}
```

---

## Agent 4: Technical Stack

### Research Checklist

1. **WebSearch** `"{company}" tech stack technology engineering` — find tech blog posts
2. **WebSearch** `"{company}" engineering blog architecture` — find architecture posts
3. **WebSearch** `site:stackshare.io "{company}"` — find StackShare profile
4. **WebSearch** `"{company}" API documentation developer` — find API docs
5. **WebFetch** their API docs page if it exists
6. **WebSearch** `"{company}" open source github` — find open-source projects
7. **WebSearch** `"{company}" hiring engineer job posting` — infer stack from job postings
8. **WebSearch** `"{company}" infrastructure performance scale` — find infrastructure details
9. **WebSearch** `"{company}" security SOC compliance` — find security posture

### Output Template

```markdown
## Technical Stack: {Company}

### Technology Table

| Layer | Technology | Confidence | Source |
|-------|-----------|------------|--------|
| Frontend framework | {e.g., React, Vue} | {High/Medium/Low} | {source} |
| Frontend language | {e.g., TypeScript} | ... | ... |
| Backend language | {e.g., Go, Rust, Node.js} | ... | ... |
| Backend framework | {e.g., Express, Gin} | ... | ... |
| Database (primary) | {e.g., PostgreSQL} | ... | ... |
| Database (cache) | {e.g., Redis} | ... | ... |
| Search | {e.g., Elasticsearch} | ... | ... |
| Message queue | {e.g., Kafka, RabbitMQ} | ... | ... |
| Cloud provider | {e.g., AWS, GCP} | ... | ... |
| CDN | {e.g., Cloudflare} | ... | ... |
| CI/CD | {e.g., GitHub Actions} | ... | ... |
| Monitoring | {e.g., Datadog} | ... | ... |
| Real-time | {e.g., WebSockets, SSE} | ... | ... |

Confidence levels:
- **High**: Confirmed via official source (blog post, docs, job posting)
- **Medium**: Inferred from multiple signals (headers, DNS, StackShare)
- **Low**: Single weak signal or educated guess

### Architecture Patterns

| Pattern | Evidence |
|---------|----------|
| Monolith vs microservices | {evidence} |
| Server-rendered vs SPA | {evidence} |
| REST vs GraphQL vs gRPC | {evidence} |
| Multi-tenant vs single-tenant | {evidence} |
| Edge computing | {evidence} |
| Real-time sync strategy | {evidence} |

### API Analysis

| Aspect | Details |
|--------|---------|
| API type | {REST/GraphQL/gRPC/None public} |
| Authentication | {OAuth/API key/JWT/etc.} |
| Rate limiting | {limits if documented} |
| Documentation quality | {Excellent/Good/Basic/None} |
| SDK availability | {languages covered} |
| Webhook support | {Yes/No} |
| API versioning | {strategy} |

### Open Source Presence

| Repository | Stars | Language | Purpose |
|-----------|-------|---------|---------|
| {repo name} | {stars} | {language} | {what it does} |
| ... | ... | ... | ... |

### Engineering Culture Signals

| Signal | Evidence |
|--------|---------|
| Blog post frequency | {posts/quarter} |
| Conference talks | {recent talks} |
| Open source activity | {assessment} |
| Hiring velocity | {open roles count} |
| Tech blog topics | {themes — infrastructure, ML, product, etc.} |
| Developer community | {Discord, forums, etc.} |

### Security Posture

| Aspect | Status |
|--------|--------|
| SOC 2 | {Type I/Type II/Unknown} |
| GDPR compliance | {Yes/No/Unknown} |
| SSO/SAML | {Available on which tier} |
| Bug bounty | {Yes/No} |
| Security page | {URL if exists} |
| Data residency options | {regions} |
```

---

## Agent 5: MVP Specification

This agent receives all Phase 1 findings as input.

### Research Checklist

1. Review all Phase 1 findings for feature gaps and user pain points
2. **WebSearch** `"{company}" complaints limitations missing feature` — find user frustrations
3. **WebSearch** `"{company}" alternative switching from` — find reasons users switch away
4. **WebSearch** `"{company}" wishlist feature request` — find requested features

### Output Template

```markdown
## MVP Specification: Competing with {Company}

### The Must-Nail Feature
{One feature/experience that MUST be better than the competitor to justify switching. This is the single most important thing to get right.}

**Why this feature**: {reasoning based on research findings}

### Prioritized Feature Set

#### P0 — Launch Blockers (must have for v1.0)

| Feature | Description | Effort Estimate | Rationale |
|---------|-------------|----------------|-----------|
| {feature} | {description} | {S/M/L/XL} | {why it's P0} |
| ... | ... | ... | ... |

#### P1 — Competitive Parity (needed within 3 months)

| Feature | Description | Effort Estimate | Rationale |
|---------|-------------|----------------|-----------|
| {feature} | {description} | {S/M/L/XL} | {why it's P1} |
| ... | ... | ... | ... |

#### P2 — Differentiation (target for 6 months)

| Feature | Description | Effort Estimate | Rationale |
|---------|-------------|----------------|-----------|
| {feature} | {description} | {S/M/L/XL} | {why it's P2} |
| ... | ... | ... | ... |

### Explicitly Out of Scope (v1.0)

| Feature | Reason for Exclusion |
|---------|---------------------|
| {feature} | {why we're not building this} |
| ... | ... |

### Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk} | {High/Medium/Low} | {High/Medium/Low} | {mitigation strategy} |
| ... | ... | ... | ... |

### Effort Estimate Summary

| Priority | Feature Count | Estimated Effort |
|----------|--------------|-----------------|
| P0 | {N} | {total} |
| P1 | {N} | {total} |
| P2 | {N} | {total} |

### Technical Architecture Implications
{Based on the Technical Stack analysis, what architectural decisions does this MVP require?}
- {implication 1}
- {implication 2}
- {implication 3}
```

---

## Agent 6: Go-to-Market Strategy

This agent receives Phase 1 findings AND the MVP Specification.

### Research Checklist

1. Review Phase 1 Marketing Analysis for channel opportunities
2. Review MVP Specification for positioning angles
3. **WebSearch** `"{company}" alternative for {underserved segment}` — validate segment
4. **WebSearch** `{product category} market size 2025 2026` — find market data
5. **WebSearch** `{product category} trends predictions 2026` — find market trends

### Output Template

```markdown
## Go-to-Market Strategy: Competing with {Company}

### Positioning Statement
For {target audience} who {pain point}, {our product} is a {category} that {key benefit}.
Unlike {Company}, we {primary differentiator}.

### Target Segment (Beachhead)

| Dimension | Definition |
|-----------|-----------|
| Industry | {specific verticals} |
| Company size | {employee range} |
| Role/buyer | {title} |
| Pain level | {why they're most frustrated with current solutions} |
| Willingness to switch | {why they'd switch now} |

### Pricing Strategy

| Tier | Price | Rationale |
|------|-------|-----------|
| {Free/Community} | {price} | {why this tier exists} |
| {Pro/Team} | {price} | {why this price point} |
| {Enterprise} | {price} | {why this price point} |

**Pricing model**: {per seat / per workspace / usage-based / flat rate}
**vs Competitor pricing**: {how this compares and why}
**Free tier strategy**: {what's free, what's gated, why}

### Launch Channels

| Channel | Strategy | Expected Impact | Cost |
|---------|----------|----------------|------|
| {channel 1} | {specific tactic} | {High/Medium/Low} | {Free/Low/Medium/High} |
| {channel 2} | ... | ... | ... |
| {channel 3} | ... | ... | ... |
| {channel 4} | ... | ... | ... |

### 90-Day Launch Timeline

#### Days 1-30: Foundation
- {action items}

#### Days 31-60: Launch
- {action items}

#### Days 61-90: Growth
- {action items}

### Early Adopter Acquisition

| Tactic | Target Count | Approach |
|--------|-------------|----------|
| Direct outreach | {N} | {strategy} |
| Community seeding | {N} | {strategy} |
| Content/SEO | {N} | {strategy} |
| Partnerships | {N} | {strategy} |

**First 100 users goal**: {timeline and strategy}

### Key Metrics to Track

| Metric | Target (90 days) | Why It Matters |
|--------|-----------------|----------------|
| {metric 1} | {target} | {reasoning} |
| {metric 2} | {target} | {reasoning} |
| {metric 3} | {target} | {reasoning} |
```

---

## Agent 7: Competitive Landscape

This agent receives all prior findings (Phase 1 + MVP Spec + GTM Strategy).

### Research Checklist

1. Review all prior findings for landscape context
2. **WebSearch** `{product category} market landscape competitors` — find competitor lists
3. **WebSearch** `{product category} market map 2025 2026` — find market maps
4. **WebSearch** `"{company}" vs {competitor 1} vs {competitor 2}` — find comparisons
5. **WebSearch** `site:reddit.com "{company}" alternative` — find Reddit discussions
6. **WebSearch** `site:news.ycombinator.com "{company}"` — find Hacker News discussions
7. **WebSearch** `"{company}" review complaint frustration` — find user complaints
8. **WebSearch** `"{company}" switching cost migration` — find switching friction

### Output Template

```markdown
## Competitive Landscape: {Company}'s Market

### Market Map

| Segment | Players | Positioning |
|---------|---------|-------------|
| {segment 1: e.g., "Enterprise"} | {player 1, player 2} | {how they position} |
| {segment 2: e.g., "SMB"} | {player 1, player 2} | {how they position} |
| {segment 3: e.g., "Developer-first"} | {player 1, player 2} | {how they position} |
| {segment 4: e.g., "Vertical-specific"} | {player 1, player 2} | {how they position} |

### Competitor Comparison Matrix

| Dimension | {Company} | {Competitor 2} | {Competitor 3} | {Our Opportunity} |
|-----------|-----------|---------------|---------------|-------------------|
| Price | {assessment} | {assessment} | {assessment} | {gap} |
| UX quality | {assessment} | {assessment} | {assessment} | {gap} |
| Feature depth | {assessment} | {assessment} | {assessment} | {gap} |
| API/extensibility | {assessment} | {assessment} | {assessment} | {gap} |
| Enterprise readiness | {assessment} | {assessment} | {assessment} | {gap} |
| Mobile experience | {assessment} | {assessment} | {assessment} | {gap} |

### Underserved Segments

| Segment | Current Pain | Why Underserved | Opportunity Size |
|---------|-------------|----------------|-----------------|
| {segment 1} | {pain description} | {why no one serves them well} | {S/M/L} |
| {segment 2} | ... | ... | ... |
| {segment 3} | ... | ... | ... |

### User Complaints (Reddit, HN, G2)

| Source | Complaint Theme | Frequency | Severity |
|--------|----------------|-----------|----------|
| Reddit | {theme} | {common/occasional/rare} | {High/Medium/Low} |
| Hacker News | {theme} | ... | ... |
| G2/Capterra | {theme} | ... | ... |
| Twitter/X | {theme} | ... | ... |

**Top 5 complaints (by frequency)**:
1. {complaint + source links}
2. {complaint + source links}
3. {complaint + source links}
4. {complaint + source links}
5. {complaint + source links}

### Switching Cost Analysis

| Factor | Friction Level | Description |
|--------|---------------|-------------|
| Data migration | {High/Medium/Low} | {what needs to move} |
| Integration rewiring | {High/Medium/Low} | {what breaks} |
| Workflow retraining | {High/Medium/Low} | {learning curve} |
| Contract/billing | {High/Medium/Low} | {lock-in terms} |
| Team adoption | {High/Medium/Low} | {social friction} |

**Overall switching cost**: {High/Medium/Low}
**Switching cost reduction strategy**: {how to make it easier to switch}

### Differentiation Angles

| Angle | Description | Defensibility | Evidence from Research |
|-------|-------------|--------------|----------------------|
| {angle 1} | {what makes us different} | {High/Medium/Low} | {supporting evidence} |
| {angle 2} | ... | ... | ... |
| {angle 3} | ... | ... | ... |

**Recommended primary differentiation**: {the single best angle and why}

### Market Trends Favoring Entry

| Trend | Impact on {Company} | Opportunity for Us |
|-------|--------------------|--------------------|
| {trend 1} | {how it affects them} | {how we can leverage it} |
| {trend 2} | ... | ... |
| {trend 3} | ... | ... |
```
