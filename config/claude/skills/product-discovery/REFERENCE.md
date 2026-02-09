# Product Discovery Reference Guide

This document provides detailed research checklists, output templates, and guidelines for each of the 8 agents in the product discovery workflow.

---

## Table of Contents

- [Agent 0: Market Scout](#agent-0-market-scout)
- [Agent 1: Product Features Researcher](#agent-1-product-features-researcher)
- [Agent 2: Market Positioning Analyst](#agent-2-market-positioning-analyst)
- [Agent 3: User Sentiment Researcher](#agent-3-user-sentiment-researcher)
- [Agent 4: Technical Stack Investigator](#agent-4-technical-stack-investigator)
- [Agent 5: Market Trends Scout](#agent-5-market-trends-scout)
- [Agent 6: Opportunity Identifier](#agent-6-opportunity-identifier)
- [Agent 7: Landscape Synthesizer](#agent-7-landscape-synthesizer)
- [Research Best Practices](#research-best-practices)
- [Citation Standards](#citation-standards)

---

## Agent 0: Market Scout

### Mission
Discover ALL products in the target market space. Create a comprehensive product catalog with 10-30 products including commercial, OSS, and community tools.

### Research Checklist

**Core Discovery Queries (8-12 WebSearch calls):**

1. **Broad discovery:**
   - `"best {category} tools 2026"`
   - `"{category} comparison"`
   - `"{category} alternatives"`

2. **Community sources:**
   - `"reddit {category} tools"`
   - `"hacker news {category}"`
   - `"product hunt {category}"`

3. **Developer ecosystem:**
   - `"github {category}"`
   - `"github awesome {category}"`
   - `"{category} open source"`

4. **Specific search terms (from context.md):**
   - `"{search_term_1}"` (e.g., "CS2 demo analyzer")
   - `"{search_term_2}"` (e.g., "Counter-Strike replay tool")
   - `"{search_term_3}"` (e.g., "CSGO demo parser")

5. **Niche discovery:**
   - `"{category} indie tools"`
   - `"{category} lesser known alternatives"`

**Coverage Targets:**
- **Minimum:** 10 products (if fewer, note market is nascent)
- **Target:** 15-25 products (good coverage)
- **Maximum:** 30 products (filter to most relevant if more)

**Product Type Breakdown (aim for diversity):**
- **Commercial:** 40-60% (SaaS, desktop apps, paid tools)
- **Open Source:** 30-40% (GitHub repos, libraries, CLI tools)
- **Community:** 10-20% (free tools, hobby projects, Discord bots)

### Output Template

```markdown
# Product Catalog — {Market Category}

**Generated:** {ISO timestamp}
**Products Discovered:** {count}

---

## Product Table

| Name | URL | Type | Category | Description |
|------|-----|------|----------|-------------|
| Example SaaS | https://example.com | Commercial | SaaS | AI-powered analysis platform for teams |
| Example Desktop | https://example.app | Commercial | Desktop | Local-first tool for individuals |
| OSS Library | https://github.com/user/repo | Open Source | Library | Go library for parsing demo files |
| CLI Tool | https://github.com/user/cli | Open Source | CLI | Command-line analyzer for power users |
| Community Bot | https://discord.gg/... | Community | Bot | Discord bot for match stats |

**Types:**
- **Commercial:** Paid products (SaaS, desktop, mobile)
- **Open Source:** GitHub repos, libraries, CLI tools
- **Community:** Free tools, hobby projects, browser extensions
- **Freemium:** Free tier + paid upgrades

**Categories:**
- **SaaS:** Web-based, cloud-hosted
- **Desktop:** Native apps (Windows, macOS, Linux)
- **CLI:** Command-line tools
- **Library:** SDKs, packages, frameworks
- **API:** API-first services
- **Bot:** Discord/Slack/Telegram bots
- **Extension:** Browser extensions, IDE plugins

---

## Market Breakdown

**By Type:**
- Commercial: {count} products
- Open Source: {count} products
- Community: {count} products

**By Category:**
- SaaS: {count} products
- Desktop: {count} products
- CLI/Library: {count} products
- Other: {count} products

---

## Discovery Notes

**Sources Used:**
- Comparison articles: {list URLs}
- Reddit threads: {list URLs}
- GitHub awesome lists: {list URLs}
- Product Hunt: {list URLs}

**Market State:**
- [X] Mature (50+ products found, filtered to top 30)
- [X] Established (15-30 products, good coverage)
- [X] Nascent (5-10 products, limited options)
- [X] Thin (0-5 products, new/niche market)

**Coverage Notes:**
{Any gaps, regional products excluded, enterprise-only tools not publicly listed, etc.}
```

### Research Tips

**Finding hidden gems:**
- Check "awesome-{topic}" GitHub lists (curated by community)
- Search HN "Show HN: {category}" for indie launches
- Check Product Hunt "Upcoming" and "Recently Launched"
- Look for academic papers citing tools (Google Scholar)

**Filtering noise:**
- Skip dead projects (no commits in 2+ years, archived repos)
- Skip exact clones (forks with no unique features)
- Skip vaporware (announced but never launched)

**Handling regional products:**
- Note if product is region-specific (e.g., China-only)
- Include if relevant to global market analysis

**Citation rule:**
Every product must have a source URL where you found it (comparison article, Reddit thread, GitHub search result, etc.).

---

## Agent 1: Product Features Researcher

### Mission
Build a feature comparison matrix for the top 8-12 products. Extract feature lists, pricing tiers, and platform availability. Identify gaps and unique features.

### Research Checklist

**For each of the top 8-12 products:**

1. **Landing page analysis:**
   - WebFetch `{product_homepage_url}`
   - Extract: Hero message, feature highlights, CTA buttons

2. **Features page:**
   - WebFetch `{product_url}/features` (or /product, /capabilities)
   - Extract: Full feature list, categorized features

3. **Pricing page:**
   - WebFetch `{product_url}/pricing`
   - Extract: Free tier features, paid tier features, price points

4. **Platform availability:**
   - WebFetch `{product_url}/download` or `/apps`
   - Note: Web, desktop (Win/Mac/Linux), mobile (iOS/Android), API

**For open source products:**
- Read `README.md` on GitHub
- Check `docs/` folder for feature documentation
- Review recent release notes for new features

**Coverage target:**
- **Top-tier products:** 8-12 products (most popular, highest funding, most users)
- **Feature depth:** 15-30 features per product (major features only, skip minor ones)

### Output Template

```markdown
# Feature Comparison Matrix — {Market Category}

**Generated:** {ISO timestamp}
**Products Analyzed:** {count}

---

## Feature Matrix

| Feature | Product A | Product B | Product C | Product D | Product E | Product F | Product G | Product H |
|---------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
| **Core Features** |
| Feature 1 | ✓ | ✓ | Premium | ✗ | ✓ | ✓ | ✗ | Premium |
| Feature 2 | ✓ | ✗ | ✓ | ✓ | Premium | ✗ | ✓ | ✓ |
| Feature 3 | Premium | ✓ | ✓ | ✗ | ✓ | ✓ | ✓ | ✗ |
| **Advanced Features** |
| Feature 4 | ✗ | ✗ | Premium | ✗ | ✗ | Premium | ✗ | ✗ |
| Feature 5 | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| **Integrations** |
| Integration A | ✓ | ✓ | ✓ | ✗ | Premium | ✓ | ✗ | ✗ |
| Integration B | Premium | ✓ | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Platform Availability** |
| Web App | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Desktop App | ✓ | ✗ | ✓ | ✗ | ✓ | ✗ | ✗ | ✗ |
| Mobile App | Premium | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | ✗ |
| API Access | Premium | ✓ | Premium | ✗ | ✓ | ✗ | ✗ | ✗ |

**Legend:**
- ✓ = Included in free/base tier
- Premium = Paid tier only
- ✗ = Not available

---

## Gap Analysis

### Features Users Want But No One Offers

**Gap 1: {Feature Name}**
- **Evidence:** {User complaints, forum requests, social media mentions}
- **Source:** {URLs where users requested this feature}
- **Opportunity:** {Why this is valuable}

**Gap 2: {Feature Name}**
- **Evidence:** {User complaints, feature requests, competitor analysis}
- **Source:** {URLs}
- **Opportunity:** {Why this is valuable}

**Gap 3: {Feature Name}**
- **Evidence:** {User behavior patterns, workaround usage}
- **Source:** {URLs}
- **Opportunity:** {Why this is valuable}

### Features Only 1-2 Products Offer (Differentiation Angles)

**Unique Feature 1: {Feature Name}**
- **Offered by:** Product A (only)
- **Value:** {Why this matters to users}
- **Moat:** {Is this defensible or easily copied?}

**Unique Feature 2: {Feature Name}**
- **Offered by:** Product B, Product C (only 2)
- **Value:** {Why this matters to users}
- **Moat:** {Technical difficulty, data advantage, network effect?}

---

## Feature Trends

**Table stakes (everyone has this):**
- {Feature 1}
- {Feature 2}
- {Feature 3}

**Emerging (2-3 products, growing adoption):**
- {Feature 4} — Added by Product A (2025-Q3), Product B (2026-Q1)
- {Feature 5} — Added by Product C (2025-Q4)

**Premium/Enterprise only (paywalled by most):**
- {Feature 6} — Premium tier in 5/8 products
- {Feature 7} — Enterprise tier in 6/8 products

---

## Platform Availability Summary

| Platform | Products Available | Notes |
|----------|-------------------|-------|
| Web | 8/8 | Universal support |
| Desktop | 3/8 | Product A, C, E only |
| Mobile | 2/8 | Product A, C only (both iOS + Android) |
| API | 4/8 | Product A (Premium), B, E, others planned |

**Platform Gaps:**
- **Mobile:** Only 2 products have mobile apps (opportunity for mobile-first)
- **API:** 50% have APIs, but only Product B offers generous free tier
- **Desktop:** Most are web-only (opportunity for local-first/offline)

---

## Pricing Tier Summary

| Product | Free Tier? | Paid Tiers | Starting Price |
|---------|-----------|------------|----------------|
| Product A | Yes (limited) | Pro, Team, Enterprise | $10/month |
| Product B | Yes (generous) | Pro | $5/month |
| Product C | No | Starter, Pro, Enterprise | $20/month |
| Product D | Yes (ads) | Ad-free | $3/month |
| Product E | No | Solo, Team | $15/month |
| Product F | OSS (free) | N/A | Free |

**Pricing Patterns:**
- **Freemium:** Products A, B, D (3/8)
- **Paid-only:** Products C, E (2/8)
- **Open source:** Products F, G, H (3/8)

**Median price:** $10/month for individual tier

---

## Sources

{List all URLs fetched, organized by product}

**Product A:**
- Homepage: https://...
- Features: https://...
- Pricing: https://...

{Repeat for each product}
```

### Research Tips

**Extracting features from landing pages:**
- Hero section: 3-5 key features (biggest selling points)
- Features page: Full list (15-30 items)
- Pricing tiers: Compare what's free vs paid (reveals priority)

**Handling vague feature descriptions:**
- If a product says "Advanced Analytics" without details, note as "✓ (details unclear)"
- Prefer concrete features over marketing buzzwords

**Platform availability:**
- Check footer links (Desktop, Mobile, API usually listed there)
- For OSS: Check GitHub releases (Windows .exe, macOS .dmg, Linux .deb)

**Pricing tier nuances:**
- "Free forever" vs "Free trial" (different implications)
- "Contact Sales" = Enterprise tier (usually $100k+ annual)
- Self-hosted OSS may have paid cloud hosting option

---

## Agent 2: Market Positioning Analyst

### Mission
Map how products position themselves. Identify positioning clusters (e.g., "Dev-first" vs "Business-first"), target personas, pricing models, and white space.

### Research Checklist

**For each product (top 8-12):**

1. **Landing page messaging:**
   - WebFetch `{product_homepage_url}`
   - Extract: Tagline, hero message, value proposition

2. **Target persona analysis:**
   - Note: Language used (e.g., "developers", "teams", "enterprises")
   - Check: Case studies, testimonials, customer logos (SMB vs Enterprise)

3. **Pricing model:**
   - Note: Free/Freemium/Paid-only
   - Extract: Price points ($/month for individual, team, enterprise)

4. **Market segment:**
   - Determine: Individual/Team/Enterprise focus
   - Evidence: Feature tiers, pricing structure, messaging

**Additional sources:**
- WebFetch "About Us" page (company mission, founding story)
- Check customer page (who uses this? SMBs or Fortune 500?)

### Output Template

```markdown
# Market Positioning Analysis — {Market Category}

**Generated:** {ISO timestamp}
**Products Analyzed:** {count}

---

## Positioning Map

**Axes:**
- **X-Axis:** Target User (Individual ← → Enterprise)
- **Y-Axis:** Price Point (Free/Low ← → Premium/High)

| Quadrant | Products | Positioning Theme |
|----------|----------|-------------------|
| **Individual / Free** | Product A, Product B, Product F (OSS) | "Simple, fast, no-signup required" |
| **Individual / Paid** | Product D | "Premium experience for power users" |
| **Team / Mid-Market** | Product C, Product E | "Collaboration, integrations, shared workflows" |
| **Enterprise / Premium** | Product G | "Security, compliance, SSO, dedicated support" |

**Alternative 2x2 Map:**
- **X-Axis:** Developer-first ← → Business-first
- **Y-Axis:** Technical ← → Non-technical

| Quadrant | Products | Messaging Examples |
|----------|----------|-------------------|
| **Dev + Technical** | Product A, Product F (OSS) | "API-first", "CLI available", "Git integration" |
| **Dev + Approachable** | Product B | "Developer-friendly UI", "No config needed" |
| **Business + Technical** | Product C | "For engineering teams", "Analytics + integrations" |
| **Business + Non-technical** | Product D, Product E | "Designed for managers", "No coding required" |

---

## Messaging Themes

| Theme | Products | Example Taglines | Target Persona |
|-------|----------|------------------|----------------|
| **Developer-first** | A, B, F | "Built by devs, for devs", "API-first", "Open source" | Software engineers, indie hackers |
| **Business-first** | C, D, E | "Align teams, ship faster", "From strategy to execution" | Product managers, team leads |
| **Individual/Solo** | A, B, D | "For individuals", "No team needed", "Personal workspace" | Freelancers, students, hobbyists |
| **Collaboration** | C, E, G | "Built for teams", "Real-time collaboration", "Shared workspace" | Teams of 5-50 |
| **Enterprise** | G | "Security-first", "SSO, SAML", "Dedicated support", "On-premise" | Enterprises (500+ employees) |
| **Simple/Easy** | B, D | "No setup", "Works in 5 minutes", "Zero config" | Non-technical users |
| **Powerful/Advanced** | A, F | "Power user features", "Advanced customization", "CLI + API" | Technical power users |

---

## Pricing Model Analysis

| Product | Model | Individual Price | Team Price | Enterprise Price | Notes |
|---------|-------|-----------------|------------|------------------|-------|
| Product A | Freemium | Free → $10/mo | $15/user/mo | Custom | Free tier limited to 5 projects |
| Product B | Freemium | Free → $5/mo | $8/user/mo | N/A | Generous free tier, no enterprise plan |
| Product C | Paid-only | N/A | $20/user/mo | Custom | Minimum 5 seats ($100/mo) |
| Product D | Freemium (ads) | Free → $3/mo | N/A | N/A | Individual-focused, no team plan |
| Product E | Paid-only | N/A | $15/user/mo | $30/user/mo | No free tier, team-focused |
| Product F | Open Source | Free | Free (self-host) | Paid hosting | OSS core + optional managed hosting |
| Product G | Paid-only | N/A | N/A | Custom | Enterprise-only, starts at $50k/year |
| Product H | Open Source | Free | Free | Free | Community-driven, no commercial offering |

**Pricing Patterns:**
- **Freemium:** A, B, D (38% of products)
- **Paid-only:** C, E, G (38% of products)
- **Open Source:** F, H (25% of products)

**Price Point Distribution:**
- **Low ($0-5/mo):** Products B, D (individual tier)
- **Mid ($10-20/mo):** Products A, C, E (team tier)
- **High ($30+/mo or custom):** Products G (enterprise tier)

**Median individual price:** $8/month
**Median team price:** $15/user/month

---

## Target Persona Analysis

| Persona | Products Targeting | Evidence | Market Share Estimate |
|---------|-------------------|----------|----------------------|
| **Individual Developers** | A, B, D, F, H | Free tiers, CLI tools, API-first | 40% of market |
| **Small Teams (2-10)** | A, B, C, E | Team pricing, collaboration features | 30% of market |
| **Mid-Market (10-100)** | C, E | Integrations, admin controls | 20% of market |
| **Enterprise (100+)** | G | SSO, compliance, on-premise | 10% of market |

**Persona Depth:**

**Individual Developers:**
- Pain points: Cost, complexity, lock-in
- Values: Simplicity, speed, free/cheap, API access
- Decision driver: Personal preference (not procurement)

**Small Teams:**
- Pain points: Coordination, version control, sharing
- Values: Real-time collaboration, integrations, fair pricing
- Decision driver: Team lead or founder

**Mid-Market:**
- Pain points: Scalability, integrations, reporting
- Values: Reliability, support, analytics
- Decision driver: Engineering manager or VP

**Enterprise:**
- Pain points: Security, compliance, vendor risk
- Values: SSO, audit logs, SLA, dedicated support
- Decision driver: Procurement team (IT, Legal, Finance approval)

---

## White Space Analysis

### Underserved Segments

**Segment 1: {Persona not well-served}**
- **Current offerings:** {Which products barely serve this segment}
- **Gaps:** {What they need but don't have}
- **Evidence:** {User complaints, forum posts, Twitter threads}
- **Opportunity size:** {TAM estimate: Small/Medium/Large}

**Example:**
**Segment: Competitive gaming teams (semi-pro)**
- **Current offerings:** Product A (expensive), Product F (too technical)
- **Gaps:** Affordable team plan, easy onboarding, coach-friendly UX
- **Evidence:** Reddit threads requesting team features, Product A pricing complaints
- **Opportunity size:** Medium (10k teams globally, $50/mo willingness-to-pay = $6M TAM)

### Unoccupied Quadrants

**Quadrant: {Position no one occupies}**
- **Why it's open:** {Technical difficulty, low demand, not viable?}
- **Potential:** {Is this white space or dead space?}

**Example:**
**Quadrant: Enterprise + Free**
- **Why it's open:** Enterprise requires SSO, compliance, support → can't be free
- **Potential:** Dead space (not viable economically)

**Quadrant: Individual + Premium ($50+/mo)**
- **Why it's open:** Individuals price-sensitive, won't pay enterprise prices
- **Potential:** Niche (could work for power users with high WTP, e.g., traders, streamers)

---

## Positioning Recommendations

**Crowded positions (avoid or differentiate heavily):**
- Individual + Free (3 OSS products + 2 freemium)
- Team + Mid-Market (3 paid products, competitive)

**Opportunity positions (less competition):**
- Individual + Premium ($20-50/mo for power users)
- Small Teams + Free (open source for teams, not just individuals)
- Mid-Market + Developer-first (most mid-market tools are business-focused)

---

## Sources

{List all URLs, organized by product}

**Product A:**
- Homepage: https://...
- About: https://...
- Pricing: https://...
- Customers: https://...

{Repeat for each product}
```

### Research Tips

**Extracting positioning from messaging:**
- Tagline = primary positioning (e.g., "Built for developers" vs "Built for teams")
- Hero message = value prop (what problem they solve)
- CTA buttons = action they want (e.g., "Start for free" vs "Request demo" signals individual vs enterprise)

**Identifying target persona:**
- **Language clues:** "you" (individual), "your team" (team), "your organization" (enterprise)
- **Case studies:** SMB logos (mid-market), Fortune 500 logos (enterprise)
- **Pricing structure:** No free tier + "Contact Sales" = enterprise

**White space vs dead space:**
- **White space:** Underserved segment with demand (opportunity)
- **Dead space:** No demand or economically unviable (not worth pursuing)
- Test: Is there user demand? Can it be monetized?

---

## Agent 3: User Sentiment Researcher

### Mission
Extract praise patterns and complaint themes for each product. Identify switching triggers (why users leave/join products).

### Research Checklist

**For each product (top 8-12):**

1. **Reddit mentions:**
   - WebSearch `"reddit {product name} review"`
   - WebSearch `"reddit {product name} vs {competitor}"`
   - WebSearch `"reddit best {category} {product name}"`

2. **Hacker News discussions:**
   - WebSearch `"hacker news {product name}"`
   - WebSearch `"hn {product name} Show HN"`

3. **Review sites (B2B products):**
   - WebSearch `"g2 {product name} reviews"`
   - WebSearch `"capterra {product name} reviews"`
   - WebSearch `"trustpilot {product name}"`

4. **Social media sentiment:**
   - WebSearch `"twitter {product name} complaints"`
   - WebSearch `"twitter {product name} vs {competitor}"`

5. **GitHub issues (OSS products):**
   - WebFetch `https://github.com/{user}/{repo}/issues`
   - Sort by: Most commented, most reactions

**Coverage target:**
- 8-12 WebSearch queries per product
- Extract 5-10 praise points and 5-10 complaints per product

### Output Template

```markdown
# User Sentiment Analysis — {Market Category}

**Generated:** {ISO timestamp}
**Products Analyzed:** {count}

---

## Sentiment Summary by Product

### Product A

**Overall Sentiment:** {Positive / Mixed / Negative}

**Praise Themes:**
1. **Fast and intuitive** (8 mentions)
   - "Product A is the fastest tool I've used" — Reddit, r/{subreddit}
   - "Love how simple the UI is" — Hacker News
   - Source: {URL}

2. **Great API** (6 mentions)
   - "API is well-documented and reliable" — G2 review
   - "Easy to integrate" — GitHub issue #123
   - Source: {URL}

3. **Responsive support** (5 mentions)
   - "Support team helped me in 10 minutes" — Twitter
   - Source: {URL}

**Complaint Themes:**
1. **Expensive for individuals** (12 mentions)
   - "$10/month is too much for personal use" — Reddit, r/{subreddit}
   - "Wish there was a cheaper tier" — Twitter
   - Source: {URL}

2. **Missing feature X** (8 mentions)
   - "Really need feature X, considering switching" — HN
   - "Feature X is a dealbreaker" — G2 review
   - Source: {URL}

3. **Slow on large datasets** (4 mentions)
   - "Performance degrades with 10k+ records" — GitHub issue #456
   - Source: {URL}

**Switching Triggers:**

**Users switch FROM Product A when:**
- Pricing increases (6 mentions of leaving after price hike)
- Missing critical feature X (8 mentions)
- Performance issues on large datasets (4 mentions)

**Users switch TO Product A when:**
- Frustrated with Product B complexity (10 mentions)
- Need faster performance than Product C (7 mentions)
- Want better API than Product D (5 mentions)

---

### Product B

{Repeat structure for each product}

---

## Cross-Product Sentiment Analysis

### Top Complaint Themes (Across All Products)

**1. Pricing too high for individuals**
- **Mentions:** 35 across 5 products (A, C, D, E, G)
- **Evidence:** Reddit threads, Twitter complaints, G2 reviews
- **Sources:** {URLs}
- **Opportunity:** Affordable individual tier or OSS alternative

**2. Missing feature X**
- **Mentions:** 28 across 6 products (A, B, C, D, E, F)
- **Evidence:** GitHub issues, feature request forums, Reddit threads
- **Sources:** {URLs}
- **Opportunity:** First to implement feature X well could capture market

**3. Poor onboarding / steep learning curve**
- **Mentions:** 18 across 4 products (C, E, F, G)
- **Evidence:** HN comments, YouTube tutorials (high demand = pain point), G2 "Cons"
- **Sources:** {URLs}
- **Opportunity:** Simplified onboarding flow, better docs, video tutorials

**4. Vendor lock-in / no export**
- **Mentions:** 15 across 3 products (A, C, E)
- **Evidence:** Reddit threads about switching pain, HN complaints
- **Sources:** {URLs}
- **Opportunity:** Emphasize data portability, open formats, easy export

**5. Performance issues at scale**
- **Mentions:** 12 across 3 products (A, D, F)
- **Evidence:** GitHub issues, Stack Overflow posts, Twitter threads
- **Sources:** {URLs}
- **Opportunity:** Performance-optimized architecture, better caching

---

### Top Praise Themes (Across All Products)

**1. Fast and intuitive**
- **Mentions:** 42 across 6 products (A, B, D, F, H)
- **Products doing this well:** Product A ("fastest"), Product B ("simplest UI")

**2. Great API / Developer-friendly**
- **Mentions:** 31 across 5 products (A, B, F, G)
- **Products doing this well:** Product B ("best API docs"), Product F ("OSS, easy to fork")

**3. Responsive support**
- **Mentions:** 24 across 4 products (A, C, G)
- **Products doing this well:** Product A ("10-min response time"), Product G ("dedicated success manager")

**4. Fair pricing / Good value**
- **Mentions:** 19 across 3 products (B, D, H)
- **Products doing this well:** Product B ("generous free tier"), Product H ("100% free OSS")

**5. Reliable / No downtime**
- **Mentions:** 16 across 3 products (A, C, G)
- **Products doing this well:** Product A ("99.9% uptime"), Product G ("enterprise SLA")

---

## Switching Behavior Patterns

### Users Leave Products When:

1. **Pricing increases** (18 mentions)
   - Product A increased prices 40% → users fled to Product B
   - Product C removed free tier → users switched to OSS Product F

2. **Missing critical features** (22 mentions)
   - Product D lacks feature X → users switch to Product A
   - Product E doesn't support API → developers switch to Product B

3. **Performance degrades** (10 mentions)
   - Product A slows down at scale → users move to Product G (enterprise)

4. **Poor support** (8 mentions)
   - Product D stopped responding to tickets → users left for Product A

5. **Product shuts down or acquired** (5 mentions)
   - Product F was acquired, roadmap changed → users migrated to Product H

### Users Join Products When:

1. **Frustrated with complexity** (25 mentions)
   - "Product C was too hard, Product B is simple" — Reddit
   - "Switched from E to A because of ease of use" — HN

2. **Need better performance** (15 mentions)
   - "Product D was too slow, Product A is 10x faster" — Twitter
   - "Switched to Product G for scale" — G2

3. **Want better pricing** (20 mentions)
   - "Product A was expensive, Product B has generous free tier" — Reddit
   - "Moved to OSS Product F to cut costs" — HN

4. **Seeking specific feature** (18 mentions)
   - "Only Product A has feature X" — Reddit
   - "Switched to Product C for integrations" — G2

5. **Better API / Developer experience** (12 mentions)
   - "Product B's API is way better than Product D" — HN
   - "Switched to Product F because it's OSS and forkable" — GitHub

---

## Sentiment Insights

**Products with strongest positive sentiment:**
1. Product B: 4.5/5 avg (praise >> complaints)
2. Product A: 4.2/5 avg (mostly positive)
3. Product H: 4.0/5 avg (OSS love, but niche)

**Products with most negative sentiment:**
1. Product D: 2.8/5 avg (pricing backlash, missing features)
2. Product E: 3.1/5 avg (poor onboarding, steep learning curve)

**Products with most polarized sentiment (love it or hate it):**
- Product F: Power users love it (technical, OSS), non-technical users find it too hard
- Product G: Enterprises love it (reliability, support), individuals hate it (expensive, overkill)

---

## Opportunity Signals from Sentiment

**Gap 1: Affordable for individuals, powerful for teams**
- Evidence: 35 mentions of "too expensive for individuals"
- Current offerings: Either cheap but limited (Product B) or powerful but expensive (Product A, C)
- Opportunity: Build a product that scales pricing with usage, not seats

**Gap 2: Easy onboarding without sacrificing power**
- Evidence: 18 mentions of "steep learning curve"
- Current offerings: Either simple but limited (Product B, D) or powerful but hard (Product F, G)
- Opportunity: Guided onboarding flow that progressively reveals complexity

**Gap 3: Performance at scale**
- Evidence: 12 mentions of performance issues
- Current offerings: Most products struggle with large datasets (10k+ records)
- Opportunity: Architecture designed for scale from day one

---

## Sources

{List all URLs, organized by product}

**Product A:**
- Reddit threads: {URLs}
- Hacker News: {URLs}
- G2 reviews: {URLs}
- Twitter: {URLs}

{Repeat for each product}
```

### Research Tips

**Finding authentic sentiment:**
- Reddit/HN are more honest than review sites (no incentives for positive reviews)
- GitHub issues reveal real pain points (users took time to report bugs)
- Twitter shows real-time frustration (less filtered than review sites)

**Quantifying sentiment:**
- Count mentions: "expensive" appears 35 times → strong signal
- Track over time: Recent complaints (2025-2026) vs old ones (2023-2024)

**Identifying switching triggers:**
- Look for "switched from X to Y because..." phrases
- Track product migrations: "Migrated from Product A to Product B"
- Note pricing-driven switches: "Left after price increase"

**Handling bias:**
- G2/Capterra reviews may be incentivized (companies offer gift cards)
- Reddit can have astroturfing (check account age, post history)
- Prefer organic mentions over obviously promotional content

---

## Agent 4: Technical Stack Investigator

### Mission
Map how products are built. Identify tech stacks, architecture patterns, API availability, and integration ecosystems.

### Research Checklist

**For open source products:**

1. **GitHub repository analysis:**
   - WebFetch `https://github.com/{user}/{repo}`
   - Read `README.md`, `package.json` (Node), `requirements.txt` (Python), `go.mod` (Go), `Cargo.toml` (Rust)
   - Check: Languages used, frameworks, dependencies

2. **Documentation:**
   - WebFetch `https://github.com/{user}/{repo}/tree/main/docs`
   - Look for: Architecture diagrams, API docs, deployment guides

**For commercial products:**

1. **Engineering blog:**
   - WebSearch `"{product name} engineering blog"`
   - WebSearch `"{product name} tech stack"`
   - WebSearch `"{product name} architecture"`

2. **Job postings:**
   - WebSearch `"{company name} job openings"`
   - Extract: Required skills (React, Node.js, AWS → likely their stack)

3. **Tech stack discovery tools:**
   - WebSearch `"stackshare {product name}"`
   - WebSearch `"builtwith {product name}"`
   - WebSearch `"wappalyzer {product name}"`

4. **API documentation:**
   - WebFetch `{product_url}/api` or `/docs/api`
   - Note: REST, GraphQL, gRPC, webhooks, SDKs

**Coverage target:**
- 8-12 products analyzed
- Identify: Frontend, backend, infrastructure, API availability

### Output Template

```markdown
# Technical Stack Analysis — {Market Category}

**Generated:** {ISO timestamp}
**Products Analyzed:** {count}

---

## Tech Stack Table

| Product | Type | Frontend | Backend | Infrastructure | Database | API | Integration Ecosystem |
|---------|------|----------|---------|----------------|----------|-----|----------------------|
| Product A | SaaS | React | Node.js | AWS (ECS, RDS, S3) | PostgreSQL | REST + GraphQL | Zapier, Webhooks, SDK (JS, Python) |
| Product B | SaaS | Vue.js | Go | GCP (Cloud Run, Cloud SQL) | PostgreSQL | REST | REST API, no webhooks |
| Product C | Desktop | Electron | Rust | N/A (local) | SQLite | None | Plugins via JS API |
| Product F | CLI | N/A | Go | N/A (local) | N/A | N/A | Library (import as Go module) |
| Product G | SaaS | Angular | Java (Spring) | On-premise / AWS | Oracle | REST + SOAP | Enterprise integrations (SAP, Salesforce) |
| Product H | Library | N/A | Python | N/A | N/A | N/A | Import as Python package |

**Stack Categories:**
- **Modern SaaS:** React/Vue + Node/Go + AWS/GCP + PostgreSQL (Products A, B)
- **Desktop-first:** Electron + Rust/C++ + Local storage (Product C)
- **CLI/Library:** Go/Rust/Python + No UI (Products F, H)
- **Enterprise:** Angular/Java + Oracle + On-premise (Product G)

---

## Architecture Patterns

### SaaS (Web-based, Cloud-hosted)

**Products:** A, B, E, G

**Common Patterns:**
- **Frontend:** React (most popular), Vue.js, Angular
- **Backend:** Node.js, Go, Python (Flask/Django), Java (Spring)
- **Infrastructure:** AWS (60%), GCP (30%), Azure (10%)
- **Database:** PostgreSQL (most popular), MySQL, MongoDB
- **Hosting:** Containerized (Docker + Kubernetes/ECS), serverless (Lambda for some)

**Example: Product A (Modern SaaS)**
- Frontend: React + TypeScript + Tailwind CSS
- Backend: Node.js + Express + GraphQL
- Infrastructure: AWS ECS (containers), RDS (PostgreSQL), S3 (storage), CloudFront (CDN)
- CI/CD: GitHub Actions → AWS CodeDeploy
- Monitoring: Datadog, Sentry

**Example: Product G (Enterprise SaaS)**
- Frontend: Angular + Java-based templating
- Backend: Java Spring Boot + REST + SOAP
- Infrastructure: On-premise (customer-hosted) or AWS (managed)
- Database: Oracle (enterprise), PostgreSQL (smaller customers)
- Monitoring: New Relic, Splunk

---

### Desktop (Local-first, Native Apps)

**Products:** C

**Common Patterns:**
- **Framework:** Electron (cross-platform), native (Swift for macOS, C# for Windows)
- **Backend:** Rust (performance), C++ (legacy), Node.js (Electron-embedded)
- **Storage:** SQLite (local database), file system (JSON, CSV)
- **Updates:** Auto-update via Squirrel (Windows), Sparkle (macOS)

**Example: Product C (Desktop App)**
- Framework: Electron (Chromium + Node.js)
- Frontend: React (inside Electron)
- Backend: Rust (native modules for performance)
- Storage: SQLite (local database), IndexedDB (browser storage)
- Distribution: DMG (macOS), MSI (Windows), AppImage (Linux)

---

### CLI / Library (Developer-focused, No UI)

**Products:** F, H

**Common Patterns:**
- **Language:** Go (fast, single binary), Rust (performance), Python (ease of use)
- **Distribution:** Homebrew (macOS), apt/yum (Linux), Scoop/Chocolatey (Windows), npm/pip/cargo (package managers)
- **Architecture:** Single binary (Go, Rust) or interpreted script (Python)

**Example: Product F (CLI Tool)**
- Language: Go
- Architecture: Single binary, no external dependencies
- Distribution: Homebrew (`brew install product-f`), GitHub releases
- Configuration: YAML config file, environment variables

**Example: Product H (Library)**
- Language: Python
- Distribution: PyPI (`pip install product-h`)
- API: Import as module (`import product_h`)
- Dependencies: NumPy, Pandas (for data processing)

---

### Hybrid (Web + Desktop + Mobile)

**Products:** A (has web + desktop + mobile apps)

**Pattern:** Shared backend (API), multiple frontends (React for web, React Native for mobile, Electron for desktop)

---

## API Availability & Integration Ecosystem

| Product | API Type | Free Tier? | Webhooks? | SDKs | Zapier? | Native Integrations |
|---------|----------|-----------|-----------|------|---------|---------------------|
| Product A | REST + GraphQL | Yes (rate-limited) | Yes | JS, Python, Go | Yes | Slack, GitHub, Jira, 20+ |
| Product B | REST | Yes (generous) | No | JS, Python | No | Slack, Discord |
| Product C | Plugin API (JS) | N/A (local) | N/A | Plugin SDK | No | None (plugins only) |
| Product E | REST | No (paid only) | Yes | JS | Yes | 50+ integrations |
| Product F | Library (Go) | N/A (OSS) | N/A | Go module | No | Use as library in Go apps |
| Product G | REST + SOAP | No (enterprise only) | Yes | Java, C# | No | SAP, Salesforce, Oracle HCM |
| Product H | Library (Python) | N/A (OSS) | N/A | Python package | No | Use as library in Python apps |

**API Ecosystem Patterns:**

**Rich APIs (Product A, E, G):**
- REST + GraphQL (modern)
- REST + SOAP (legacy/enterprise)
- Webhooks for real-time events
- Multiple SDKs (JS, Python, Go, etc.)
- Zapier integration for no-code automation
- 20-50+ native integrations (Slack, GitHub, Salesforce, etc.)

**Limited APIs (Product B):**
- REST only (no GraphQL)
- No webhooks (polling required)
- 1-2 SDKs (JS, Python)
- Few integrations (2-5)

**No APIs (Product C — Desktop, Product F/H — CLI/Library):**
- Desktop apps: Plugin APIs for extensibility (not web APIs)
- CLI/Library: Import as module (not API in traditional sense)

---

## Infrastructure & Deployment Patterns

### Cloud-Native SaaS

**Products:** A, B, E

**Patterns:**
- **Containers:** Docker + Kubernetes (GKE, EKS) or AWS ECS/Fargate
- **Serverless:** AWS Lambda, Cloud Functions (for background jobs, webhooks)
- **CI/CD:** GitHub Actions, GitLab CI, CircleCI
- **Monitoring:** Datadog, New Relic, Sentry (error tracking)
- **CDN:** CloudFront, Cloudflare (static assets, edge caching)

**Example: Product A**
- Hosting: AWS ECS (containers), Application Load Balancer
- Database: RDS PostgreSQL (multi-AZ for HA)
- Storage: S3 (user uploads), CloudFront (CDN)
- Background Jobs: SQS + Lambda (async processing)
- CI/CD: GitHub Actions → ECR (container registry) → ECS (blue-green deployment)

---

### On-Premise / Hybrid (Enterprise)

**Products:** G

**Patterns:**
- **Deployment:** Customer-hosted (on-premise) or cloud-managed (AWS, Azure)
- **Architecture:** Monolith or microservices (depends on enterprise requirements)
- **Database:** Oracle (most enterprises), PostgreSQL (smaller customers)
- **Security:** VPC, VPN, SSO (SAML, LDAP), audit logs

**Example: Product G**
- Deployment: Docker Compose (small), Kubernetes (large)
- Database: Oracle RAC (high availability), PostgreSQL (alternative)
- Auth: SAML SSO, LDAP, Active Directory
- Monitoring: Customer-provided (Splunk, New Relic)

---

### Desktop / Local-First

**Products:** C

**Patterns:**
- **No backend:** All data stored locally (SQLite, file system)
- **Optional sync:** Cloud sync via Dropbox, Google Drive, iCloud (file-based)
- **Updates:** Auto-update framework (Squirrel, Sparkle)

**Example: Product C**
- Storage: SQLite (local database)
- Sync: Optional cloud sync via third-party (Dropbox, Google Drive)
- Updates: Auto-update on launch (check GitHub releases)

---

## Open Source Stack Analysis

**Products:** F, H

**Languages:**
- **Go:** Product F (fast, single binary, no runtime)
- **Python:** Product H (ease of use, rich ecosystem)

**Why Go for CLI tools:**
- Single binary (no dependencies, easy distribution)
- Fast compilation and execution
- Cross-platform (Windows, macOS, Linux)
- Example: demoinfocs-golang (CS2 demo parser)

**Why Python for libraries:**
- Rich ecosystem (NumPy, Pandas, SciPy)
- Easy to prototype and extend
- Popular in data science, ML communities

---

## Technical Differentiation Opportunities

**Gap 1: Local-first SaaS (Hybrid)**
- **Current state:** Either cloud-only (Products A, B, E) or desktop-only (Product C)
- **Opportunity:** Build SaaS with optional local mode (offline-first, sync when online)
- **Example:** Linear's offline mode, Notion's desktop app with local cache

**Gap 2: API-first from Day 1**
- **Current state:** Many products add APIs later (Product C has no API, Product B has limited API)
- **Opportunity:** Design API-first, then build UI on top (Stripe model)
- **Benefit:** Developers can integrate before UI is polished

**Gap 3: Serverless Architecture (Cost Efficiency)**
- **Current state:** Most SaaS use containers (ECS, Kubernetes) → expensive at low scale
- **Opportunity:** Serverless (Lambda, Cloud Run) → pay per request, scale to zero
- **Benefit:** Cheaper for small users, auto-scales for large users

**Gap 4: WASM for Performance**
- **Current state:** Web apps use JS (slow for heavy computation)
- **Opportunity:** Use WebAssembly (WASM) for performance-critical code (parsing, analysis)
- **Example:** Figma uses WASM for rendering, 10x faster than JS

---

## Sources

{List all URLs, organized by product}

**Product A (SaaS):**
- Engineering blog: {URL}
- Job postings: {URL}
- StackShare: {URL}
- API docs: {URL}

**Product F (OSS):**
- GitHub repo: {URL}
- README: {URL}
- Documentation: {URL}

{Repeat for each product}
```

### Research Tips

**Finding tech stacks for closed-source products:**
- **Job postings:** "Looking for React developer" → Frontend is React
- **Wappalyzer:** Browser extension to detect tech (JS frameworks, analytics, hosting)
- **BuiltWith:** Web service to analyze tech stack (less accurate than Wappalyzer)
- **Engineering blog:** Companies often write about tech choices (migrations, scaling)

**Reading GitHub repos:**
- `package.json` (Node.js): Lists dependencies → tells you frameworks (Express, React, etc.)
- `go.mod` (Go): Lists dependencies → tells you libraries used
- `requirements.txt` (Python): Lists dependencies → tells you frameworks (Django, Flask)
- `Dockerfile`: Tells you deployment approach (containerized)

**Identifying architecture patterns:**
- **Monolith:** Single repo, single deployment
- **Microservices:** Multiple repos or monorepo with services/
- **Serverless:** Mentions Lambda, Cloud Functions, API Gateway

**API quality indicators:**
- **Good:** REST + GraphQL, webhooks, multiple SDKs, Zapier
- **Okay:** REST only, 1-2 SDKs, no webhooks
- **Poor:** No API, or API is undocumented

---

## Agent 5: Market Trends Scout

### Mission
Identify funding, acquisitions, shutdowns, emerging features, and new entrants. Track what's changing in the market.

### Research Checklist

**Funding & Acquisitions:**

1. **Recent funding:**
   - WebSearch `"{category} funding news 2025"`
   - WebSearch `"{category} funding news 2026"`
   - WebSearch `"{category} Series A"`

2. **Acquisitions:**
   - WebSearch `"{category} acquisitions 2025 2026"`
   - WebSearch `"{product name} acquired"`

3. **Shutdowns:**
   - WebSearch `"{category} shutdowns 2025 2026"`
   - WebSearch `"{product name} shut down"`

**Market Reports:**

4. **State of X reports:**
   - WebSearch `"state of {category} 2026"`
   - WebSearch `"{category} market report 2026"`
   - WebSearch `"{category} trends 2026"`

**Emerging Features:**

5. **New feature trends:**
   - WebSearch `"{category} AI features"`
   - WebSearch `"{category} emerging features 2026"`
   - WebSearch `"{product name} launches {feature}"`

**New Entrants:**

6. **Recent launches:**
   - WebSearch `"new {category} tools 2026"`
   - WebSearch `"product hunt {category} 2025 2026"`
   - WebSearch `"show hn {category} 2025 2026"`

**Coverage target:**
- 10-15 WebSearch queries total
- Track events from 2025-Q1 to 2026-Q1 (last 12 months)

### Output Template

```markdown
# Market Trends Analysis — {Market Category}

**Generated:** {ISO timestamp}
**Time Period:** 2025-Q1 to 2026-Q1 (12 months)

---

## Trend Timeline

### 2025-Q1

**Funding:**
- Product A raised $5M seed round (Source: TechCrunch, {URL})
- Product B raised $10M Series A led by Accel (Source: VentureBeat, {URL})

**Launches:**
- Product D launched beta (Source: Product Hunt, {URL})

---

### 2025-Q2

**Acquisitions:**
- Product E acquired by MegaCorp for $50M (Source: Press Release, {URL})

**Feature Launches:**
- Product A launched AI-powered analysis (Source: Blog post, {URL})
- Product C added real-time collaboration (Source: Changelog, {URL})

---

### 2025-Q3

**Funding:**
- Product F raised $15M Series A (Source: TechCrunch, {URL})

**Shutdowns:**
- Product G shut down due to lack of traction (Source: Founder blog, {URL})

**Feature Launches:**
- Product B added API webhooks (Source: API docs, {URL})

---

### 2025-Q4

**Launches:**
- Product H launched (OSS alternative to Product A) (Source: GitHub, {URL})

**Feature Launches:**
- Product A added mobile app (Source: App Store, {URL})
- Product D added integrations with Slack, Discord (Source: Blog, {URL})

---

### 2026-Q1

**Funding:**
- Product A raised $25M Series B led by Sequoia (Source: TechCrunch, {URL})

**Acquisitions:**
- Product F acquired by AnotherCorp for $100M (Source: Press Release, {URL})

**Feature Launches:**
- Product C added AI features (following Product A) (Source: Blog, {URL})
- Product E launched v2 (major redesign) (Source: Product update, {URL})

---

## Market Dynamics

### Funding Activity (2025-2026)

**Total Funding:** $55M across 4 companies (A, B, F, others)

**Breakdown:**
- Seed: $5M (Product A)
- Series A: $25M (Product B $10M, Product F $15M)
- Series B: $25M (Product A)

**Investors:**
- Most active: Accel (invested in Product B), Sequoia (invested in Product A)
- Thesis: Investing in AI-powered tools, API-first platforms

**Funding Trends:**
- **Early-stage (seed/A):** $20M total (4 companies)
- **Growth-stage (B+):** $25M total (1 company)
- **Hot areas:** AI features, collaboration, API-first

---

### Consolidation (Acquisitions & Shutdowns)

**Acquisitions (2025-2026):**
1. **Product E acquired by MegaCorp ($50M):**
   - Reason: MegaCorp wanted to add {category} to their suite
   - Impact: Product E roadmap changed, some features deprecated
   - User reaction: Mixed (some users left, others happy for enterprise support)

2. **Product F acquired by AnotherCorp ($100M):**
   - Reason: AnotherCorp wanted to enter {category} market
   - Impact: Product F became part of larger suite
   - User reaction: Positive (more resources, faster development)

**Shutdowns (2025-2026):**
1. **Product G shut down:**
   - Reason: Lack of traction, couldn't compete with Product A
   - Impact: Users migrated to Product A, Product H (OSS)
   - Source: Founder blog post ({URL})

**Consolidation Trends:**
- **Acqui-hires:** MegaCorp acquired Product E for team, not product
- **Strategic acquisitions:** AnotherCorp acquired Product F to enter market
- **Failed startups:** Product G couldn't differentiate, shut down

---

## Emerging Features

### AI-Powered Analysis

**Adoption:**
- Product A: Launched Q2 2025 (first mover)
- Product C: Launched Q1 2026 (follower)
- Product D: Announced Q1 2026 (in beta)

**Description:**
- Uses AI (GPT-4, Claude) to analyze data and provide insights
- Example: Auto-generate summaries, identify patterns, suggest actions

**Market Impact:**
- Becoming table stakes (users expect AI features)
- Differentiation: Quality of AI insights (Product A > Product C)

**Opportunity:**
- AI-native approach (not bolted-on feature) could differentiate
- Example: Build entire product around AI analysis, not just add AI to existing product

---

### Real-Time Collaboration

**Adoption:**
- Product C: Launched Q2 2025 (first mover)
- Product A: Announced Q1 2026 (in beta)

**Description:**
- Multiple users can edit/view same data simultaneously (like Google Docs)
- Live cursors, presence indicators, conflict resolution

**Market Impact:**
- Shifts product from individual to team use case
- Increases pricing power (team plans > individual plans)

**Opportunity:**
- Real-time collab + AI could be powerful combo (no one offers both yet)

---

### API-First / Headless

**Adoption:**
- Product B: Launched Q3 2025 (redesigned as API-first)
- Product D: Launched with API from day 1 (2025-Q1)

**Description:**
- API is primary interface, UI is secondary (built on top of API)
- Developers can build custom UIs, automations, integrations

**Market Impact:**
- Appeals to technical users (developers, power users)
- Enables ecosystem (third-party integrations, plugins)

**Opportunity:**
- API-first is still rare (only 2/12 products) → early mover advantage

---

### Mobile Apps

**Adoption:**
- Product A: Launched Q4 2025 (iOS + Android)
- Product C: Announced Q1 2026 (iOS only, beta)

**Description:**
- Native mobile apps (not just responsive web)
- Offline mode, push notifications, mobile-optimized UX

**Market Impact:**
- Expands use cases (on-the-go access, mobile-first workflows)
- Premium feature (often gated behind paid tier)

**Opportunity:**
- Mobile-first approach could differentiate (most products are web-first)

---

## New Entrants (Launched 2025-2026)

### Product D (Launched 2025-Q1)

**Background:**
- Founded by ex-Product A engineers
- $2M seed funding from Y Combinator

**Positioning:**
- Affordable alternative to Product A ($5/mo vs $10/mo)
- Simpler UX, faster onboarding

**Tech:**
- Go backend, React frontend, PostgreSQL
- API-first from day 1

**Traction:**
- 5k users in first year
- Growing 20% MoM

**Impact on Market:**
- Puts pricing pressure on Product A
- Appeals to individual users (not teams)

---

### Product H (Launched 2025-Q4)

**Background:**
- Open source alternative to Product A
- Built by community, no VC funding

**Positioning:**
- 100% free, self-hosted
- No feature limits, no data lock-in

**Tech:**
- Python backend, Vue.js frontend, SQLite/PostgreSQL
- Docker Compose for easy deployment

**Traction:**
- 2k GitHub stars in 3 months
- 500 self-hosted instances

**Impact on Market:**
- Provides free alternative for price-sensitive users
- Forces commercial products to justify pricing

---

## Market Dynamics Summary

### Market Maturity

**Current State:**
- **Early growth:** 12 products, $55M funding in 12 months
- **No clear leader:** Product A has most traction, but not dominant (20% market share estimate)
- **Fragmentation:** Many niche products, no consolidation yet

**Prediction:**
- **Next 12 months:** Consolidation likely (2-3 more acquisitions)
- **Next 2-3 years:** Winner(s) emerge, smaller players acquired or shut down

---

### Key Trends

**1. AI is becoming table stakes**
- 3/12 products have AI features (2025-2026)
- Expectation: 8/12 will have AI by end of 2026

**2. Shift from individual to team**
- Collaboration features (real-time, shared workspaces) becoming standard
- Pricing shift: Individual $10/mo → Team $15/user/mo (higher revenue)

**3. API-first architecture**
- 2/12 products are API-first (2025-2026)
- Trend: More products will expose APIs (developer demand)

**4. Open source alternatives gaining traction**
- Product H (OSS) launched, growing fast
- Pressure on commercial products to justify pricing

**5. Mobile is premium (not default)**
- Only 2/12 products have mobile apps
- Mobile is gated behind paid tier (not table stakes yet)

---

## Opportunity Signals from Trends

**Opportunity 1: AI-native from Day 1**
- **Trend:** AI is bolted-on feature (not core architecture)
- **Gap:** No product is AI-native (entire UX designed around AI)
- **Example:** Perplexity (AI-native search) vs Google (search with AI features)

**Opportunity 2: Real-time collab + AI combo**
- **Trend:** Some products have collab (Product C), some have AI (Product A), none have both
- **Gap:** No product combines real-time collaboration + AI insights
- **Example:** Notion (collab) + Perplexity (AI) = Notion AI (but not real-time)

**Opportunity 3: Mobile-first (not mobile-later)**
- **Trend:** Desktop/web products add mobile apps later
- **Gap:** No product designed mobile-first (most are web-first)
- **Example:** Instagram (mobile-first) vs Facebook (web-first, mobile-later)

**Opportunity 4: Open source core + managed hosting**
- **Trend:** Either 100% OSS (Product H, free) or 100% commercial (Product A, paid)
- **Gap:** No hybrid (OSS core + paid managed hosting)
- **Example:** GitLab (OSS core + paid GitLab.com), Sentry (OSS + paid SaaS)

---

## Sources

{List all URLs, organized by category}

**Funding News:**
- {URL 1}
- {URL 2}

**Acquisitions:**
- {URL 1}
- {URL 2}

**Feature Launches:**
- {URL 1}
- {URL 2}

**Market Reports:**
- {URL 1}
- {URL 2}
```

### Research Tips

**Finding funding news:**
- TechCrunch, VentureBeat cover Series A+
- AngelList, Crunchbase for seed rounds
- Twitter (founders announce rounds)

**Finding acquisitions:**
- Press releases (company blogs, PR Newswire)
- TechCrunch, VentureBeat (large acquisitions)
- Twitter (smaller acquisitions)

**Finding shutdowns:**
- Founder blog posts (most graceful shutdowns have post-mortem)
- HN "Ask HN: What happened to {product}?" threads
- Wayback Machine (check if site is down)

**Identifying emerging features:**
- Product changelogs (Product A blog, Product C release notes)
- Product Hunt launches (new products often showcase cutting-edge features)
- HN "Show HN" (indie hackers launch new tools)

**Estimating market maturity:**
- **Nascent:** <10 products, <$10M funding, no acquisitions
- **Early growth:** 10-30 products, $10-100M funding, 1-2 acquisitions
- **Maturing:** 30-100 products, $100M+ funding, consolidation
- **Mature:** 100+ products, clear leader(s), plateau

---

## Agent 6: Opportunity Identifier

### Mission
Cross-reference all Phase 1 findings to identify market opportunities. Score opportunities on effort/impact/risk.

### Research Checklist

**This is a synthesis agent (no new WebSearch queries). Read all Phase 1 outputs:**

1. Read `product-catalog.md` (Product landscape)
2. Read `features.md` (Feature gaps)
3. Read `positioning.md` (Positioning white space)
4. Read `sentiment.md` (User pain points)
5. Read `tech-stack.md` (Technical differentiation)
6. Read `trends.md` (Emerging opportunities)

**Analysis Framework:**

1. **Feature Gaps:**
   - Cross-reference features.md (gaps) + sentiment.md (complaints)
   - Find: Features users want but no one offers

2. **Underserved Segments:**
   - Cross-reference positioning.md (quadrants) + sentiment.md (personas)
   - Find: Personas ignored by incumbents

3. **Positioning White Space:**
   - Read positioning.md (2x2 map)
   - Find: Unoccupied quadrants with demand

4. **Technical Differentiation:**
   - Read tech-stack.md (architecture patterns)
   - Find: Architecture approaches no one uses

5. **Trend Opportunities:**
   - Read trends.md (emerging features)
   - Find: Features not yet mainstream

**Coverage target:**
- Identify 3-7 opportunities (focus on highest impact)
- Score each on effort/impact/risk

### Output Template

```markdown
# Opportunity Analysis — {Market Category}

**Generated:** {ISO timestamp}
**Phase 1 Inputs:** product-catalog.md, features.md, positioning.md, sentiment.md, tech-stack.md, trends.md

---

## Opportunity Matrix

| # | Opportunity | Gap / Evidence | TAM Estimate | Effort | Impact | Risk | Priority |
|---|-------------|---------------|--------------|--------|--------|------|----------|
| 1 | AI-native demo analyzer for competitive teams | Users want AI insights (28 mentions), only Product A offers basic version | Medium ($10-100M) | M | High | Low | ⭐⭐⭐ |
| 2 | Open source demo parser library | All parsers fragmented (8 different libraries), no standard | Large (>$100M) | L | Medium | Medium | ⭐⭐ |
| 3 | Real-time match coaching tool | All tools are post-match (12 mentions of "wish I had this during game") | Small (<$10M) | XL | High | High | ⭐ |
| 4 | Affordable team plan ($5/user/mo) | 35 mentions of "too expensive for small teams" | Medium ($10-100M) | S | Medium | Low | ⭐⭐⭐ |
| 5 | Mobile-first demo viewer | Only 2/12 products have mobile apps (18 mentions of mobile requests) | Medium ($10-100M) | M | Medium | Medium | ⭐⭐ |

**Scoring Legend:**
- **Effort:** S (weeks), M (months), L (quarters), XL (years)
- **Impact:** High (10x better), Medium (2-3x better), Low (incremental)
- **Risk:** High (unproven demand), Medium (proven demand, hard execution), Low (clear path)
- **Priority:** ⭐⭐⭐ (do first), ⭐⭐ (do second), ⭐ (do later)

**TAM Estimate Methodology:**
- Small (<$10M): Niche segment, <100k potential users
- Medium ($10-100M): Underserved segment, 100k-1M potential users
- Large (>$100M): Broad market, >1M potential users

---

## Detailed Opportunity Breakdown

### Opportunity 1: AI-Native Demo Analyzer for Competitive Teams

**Gap:**
- Users want AI-powered round analysis, but only Product A offers basic version (features.md § Gap 2)
- Product A's AI is bolted-on, not core to UX (trends.md § Emerging Features)
- Competitive teams (semi-pro) are underserved: Product A is expensive ($10/mo individual, $15/user/mo team), Product F (OSS) is too technical (positioning.md § White Space)

**Evidence:**
- 28 mentions of "want AI insights" (sentiment.md § Top Complaint Themes)
- Product A's AI feature has highest engagement (trends.md § AI-Powered Analysis)
- Reddit threads requesting AI round analysis for competitive teams (sentiment.md § Product A complaints)

**Target Segment:**
- Competitive CS2 teams (semi-pro, aspiring pro)
- 10k-50k teams globally (5 players each = 50k-250k users)
- Willingness-to-pay: $10-20/user/mo (team plan)

**TAM Estimate:**
- Conservative: 10k teams × 5 players × $10/mo = $500k/mo = $6M/year
- Optimistic: 50k teams × 5 players × $15/mo = $3.75M/mo = $45M/year
- **Estimate: Medium ($10-100M TAM)**

**Effort:**
- AI integration: 2-3 months (use OpenAI API, Claude API)
- Demo parsing: 1-2 months (use existing OSS library like demoinfocs-golang)
- UX design: 2-3 months (round-by-round analysis, heatmaps, insights)
- **Total: 6-8 months (M effort)**

**Impact:**
- **High:** 10x better than existing tools (AI-native vs bolt-on AI)
- Competitive advantage: First to market with AI-native approach
- Network effects: Teams share insights → viral growth

**Risk:**
- **Low:** Proven demand (28 mentions), existing products validate market
- Execution risk: Medium (AI quality must be good, not generic)
- Competition risk: Low (Product A focused on individuals, not teams)

**Recommended Priority:** ⭐⭐⭐ (High — proven demand, medium effort, high impact, low risk)

---

### Opportunity 2: Open Source Demo Parser Library

**Gap:**
- 8 different OSS demo parsers (product-catalog.md), all fragmented (tech-stack.md § OSS Stack)
- No standard library (developers must choose between demoinfocs-golang, demoparser-python, etc.)
- Each parser has different API, missing features, incomplete docs

**Evidence:**
- GitHub issues requesting unified parser (tech-stack.md § Product F, Product H)
- 12 mentions of "wish there was a standard library" (sentiment.md § Product F complaints)
- Developers build custom parsers because existing ones incomplete

**Target Segment:**
- Developers building CS2 tools (demo analyzers, stat trackers, highlight reels)
- Estimated 1k-5k developers globally

**TAM Estimate:**
- Direct revenue: $0 (open source, free)
- Indirect revenue: Ecosystem growth → managed hosting, premium features
- Market impact: Enables 100+ new tools to be built
- **Estimate: Large (>$100M ecosystem value, even if library itself is free)**

**Effort:**
- Core parser: 3-6 months (Go or Rust for performance)
- API design: 1-2 months (stable, versioned API)
- Docs + examples: 1-2 months
- Community building: Ongoing (6-12 months to critical mass)
- **Total: 6-12 months (L effort)**

**Impact:**
- **Medium:** Doesn't directly generate revenue, but enables ecosystem
- Network effects: More devs use library → more contributors → better library
- Long-term: Becomes de facto standard (like demoinfocs-golang for Go)

**Risk:**
- **Medium:** Adoption risk (will devs switch from existing libraries?)
- Maintenance burden: Must keep up with CS2 updates (game changes frequently)
- Monetization unclear: OSS library doesn't generate direct revenue

**Recommended Priority:** ⭐⭐ (Medium — large ecosystem impact, but indirect revenue, medium risk)

---

### Opportunity 3: Real-Time Match Coaching Tool

**Gap:**
- All existing tools are post-match (analyze after game ends)
- No tool for real-time coaching (during match)
- 12 mentions of "wish I had this during game" (sentiment.md)

**Evidence:**
- Coaches want real-time insights (Reddit r/GlobalOffensive threads)
- Esports teams use manual coaching (coaches watch stream, give verbal feedback)
- No product offers automated real-time coaching

**Target Segment:**
- Esports coaches (pro and semi-pro teams)
- Estimated 1k-5k teams with coaches globally

**TAM Estimate:**
- 1k teams × $100/mo (premium coaching tool) = $100k/mo = $1.2M/year
- Optimistic: 5k teams × $100/mo = $500k/mo = $6M/year
- **Estimate: Small (<$10M TAM) — niche segment**

**Effort:**
- Real-time parsing: 6-9 months (parse demo while match is live, not after)
- Low-latency architecture: 3-6 months (WebSocket, sub-second updates)
- AI coaching: 3-6 months (AI suggests strategies based on live state)
- **Total: 12-18 months (XL effort)**

**Impact:**
- **High:** 10x better than existing tools (real-time vs post-match)
- First-mover advantage: No competitors in this space

**Risk:**
- **High:** Unproven demand (coaches may prefer manual coaching)
- Technical risk: Real-time parsing is hard (CS2 doesn't expose live data easily)
- Market risk: Small TAM (only 1k-5k teams with coaches)

**Recommended Priority:** ⭐ (Low — high impact, but XL effort, high risk, small TAM)

---

### Opportunity 4: Affordable Team Plan ($5/user/mo)

**Gap:**
- Product A charges $15/user/mo for teams (35 mentions of "too expensive")
- Product B has no team plan (individual-only)
- No product offers affordable team plan ($5-8/user/mo)

**Evidence:**
- 35 mentions of pricing complaints (sentiment.md § Top Complaint Themes)
- Reddit threads: "Product A is great but too expensive for our 5-person team"
- Users switch to OSS Product F to cut costs (sentiment.md § Switching Behavior)

**Target Segment:**
- Small teams (2-10 people): hobbyist teams, semi-pro teams, friend groups
- Estimated 50k-100k teams globally

**TAM Estimate:**
- 50k teams × 5 players × $5/user/mo = $1.25M/mo = $15M/year
- Optimistic: 100k teams × 5 players × $8/user/mo = $4M/mo = $48M/year
- **Estimate: Medium ($10-100M TAM)**

**Effort:**
- Product development: Same as Opportunity 1 (6-8 months)
- Pricing strategy: 1 month (set $5/user/mo, design free tier)
- **Total: 6-8 months (S effort if building on top of existing product, M effort if building from scratch)**

**Impact:**
- **Medium:** 2-3x better pricing than Product A (not 10x better product)
- Competitive advantage: First affordable team plan
- Churn risk: Low (teams sticky once onboarded)

**Risk:**
- **Low:** Proven demand (35 pricing complaints), clear WTP ($5-8/user/mo)
- Competition risk: Medium (Product A could lower prices)
- Unit economics: Must validate profitability at $5/user/mo

**Recommended Priority:** ⭐⭐⭐ (High — proven demand, low effort, medium impact, low risk)

---

### Opportunity 5: Mobile-First Demo Viewer

**Gap:**
- Only 2/12 products have mobile apps (features.md § Platform Availability)
- 18 mentions of "wish I could view demos on mobile" (sentiment.md)
- Existing mobile apps are web wrappers (not native, slow)

**Evidence:**
- Users want to review demos on commute, between games (sentiment.md)
- Product A's mobile app is premium-only ($10/mo) (features.md § Pricing Tier Summary)
- No mobile-first product (all are web-first with mobile app added later)

**Target Segment:**
- Mobile-first users: students, commuters, casual players
- Estimated 100k-500k potential users

**TAM Estimate:**
- 100k users × $3/mo (lower price for mobile-only) = $300k/mo = $3.6M/year
- Optimistic: 500k users × $5/mo = $2.5M/mo = $30M/year
- **Estimate: Medium ($10-100M TAM)**

**Effort:**
- Mobile app development: 4-6 months (React Native or Flutter for iOS + Android)
- Demo parsing on mobile: 2-3 months (optimize for mobile CPU/memory)
- UX design for mobile: 2-3 months (touch-first, small screen)
- **Total: 8-12 months (M effort)**

**Impact:**
- **Medium:** 2-3x better than desktop (mobile convenience)
- Not 10x better (still same core features, just on mobile)

**Risk:**
- **Medium:** Proven demand (18 mentions), but mobile market is competitive
- Monetization risk: Users may expect lower pricing for mobile-only
- Platform risk: Must maintain iOS + Android (double effort)

**Recommended Priority:** ⭐⭐ (Medium — proven demand, medium effort, medium impact, medium risk)

---

## Opportunity Prioritization

**Tier 1 (Build First):**
1. **Opportunity 1:** AI-native demo analyzer for competitive teams (M effort, High impact, Low risk)
2. **Opportunity 4:** Affordable team plan ($5/user/mo) (S effort, Medium impact, Low risk)

**Tier 2 (Build Second):**
3. **Opportunity 2:** Open source demo parser library (L effort, Medium impact, Medium risk)
4. **Opportunity 5:** Mobile-first demo viewer (M effort, Medium impact, Medium risk)

**Tier 3 (Build Later or Skip):**
5. **Opportunity 3:** Real-time match coaching tool (XL effort, High impact, High risk)

---

## Next Steps for Validation

**For Opportunity 1 (AI-native analyzer):**
- Interview 10 competitive team players/coaches (validate WTP, feature priorities)
- Build AI demo prototype (test AI quality with real demos)
- Launch landing page with email signup (measure demand)

**For Opportunity 4 (Affordable team plan):**
- Survey users who complained about pricing (confirm $5/user/mo WTP)
- Calculate unit economics (can we be profitable at $5/user/mo?)
- Launch waitlist for team plan (measure demand)

**For Opportunity 2 (OSS parser library):**
- Survey developers building CS2 tools (would they switch to standard library?)
- Build prototype parser (validate API design with community)
- Gauge community interest (GitHub stars, Discord engagement)

---

## Sources

All findings sourced from Phase 1 outputs:
- `product-catalog.md` (product landscape)
- `features.md` (feature gaps)
- `positioning.md` (white space)
- `sentiment.md` (user pain points)
- `tech-stack.md` (technical differentiation)
- `trends.md` (emerging opportunities)
```

### Research Tips

**Finding feature gaps:**
- Cross-reference features.md (gaps) + sentiment.md (complaints)
- Look for: Features requested but not offered by anyone

**Identifying underserved segments:**
- Cross-reference positioning.md (quadrants) + sentiment.md (personas)
- Look for: Personas mentioned in sentiment but not targeted by any product

**Estimating TAM:**
- **Small (<$10M):** Niche segment, <100k users, <$100/year WTP
- **Medium ($10-100M):** Underserved segment, 100k-1M users, $50-200/year WTP
- **Large (>$100M):** Broad market, >1M users, >$100/year WTP

**Scoring effort:**
- **S (weeks):** Pricing change, simple feature add
- **M (months):** New product feature, integration
- **L (quarters):** New product, major rewrite
- **XL (years):** Unproven technology, research-heavy

**Scoring impact:**
- **High (10x):** Order-of-magnitude better (AI-native vs bolt-on AI)
- **Medium (2-3x):** Significantly better (better pricing, better UX)
- **Low (incremental):** Slightly better (minor improvements)

**Scoring risk:**
- **High:** Unproven demand, hard execution, competitive threats
- **Medium:** Proven demand, medium execution difficulty
- **Low:** Proven demand, clear path, low competition

---

## Agent 7: Landscape Synthesizer

### Mission
Create the final market landscape report. Synthesize all Phase 1 + Agent 6 findings into executive summary, market map, and entry strategies.

### Research Checklist

**This is a synthesis agent (no new WebSearch queries). Read all prior outputs:**

1. Read `product-catalog.md` (Product landscape)
2. Read `features.md` (Feature comparison)
3. Read `positioning.md` (Market positioning)
4. Read `sentiment.md` (User sentiment)
5. Read `tech-stack.md` (Technical landscape)
6. Read `trends.md` (Market trends)
7. Read `opportunities.md` (Opportunity analysis from Agent 6)

**Synthesis Framework:**

1. **Executive Summary:** 3-5 bullets on market state and top opportunities
2. **Market Map:** Visual representation of product landscape (ASCII or markdown table)
3. **Entry Strategies:** Build/partner/differentiate recommendations
4. **Prioritization:** Rank top 3 opportunities by impact/effort/risk

**Coverage target:**
- Final report should be comprehensive but concise (10-15 pages markdown)
- Executive summary should be readable in 2 minutes
- Market map should visualize landscape at a glance

### Output Template

```markdown
# {Market Category} — Product Discovery Report

**Generated:** {ISO timestamp}
**Products Analyzed:** {count from product-catalog.md}
**Time Period:** {date range from trends.md}

---

## Executive Summary

**Market State:** {1-2 sentences on maturity, competition, growth}
- Example: "The CS2 demo analysis market is nascent with 18 products (12 OSS, 4 commercial, 2 community). No clear leader; Product A has ~20% market share. $55M funding in past 12 months signals early growth phase."

**Key Finding:** {Top insight from research}
- Example: "Users want AI-powered round analysis and affordable team plans, but only Product A offers basic AI (expensive at $15/user/mo) and no product targets competitive teams specifically."

**Top Opportunity:** {Highest-impact opportunity from opportunities.md}
- Example: "AI-native demo analyzer for competitive teams (Medium TAM $10-100M, M effort, High impact, Low risk). First-mover advantage in underserved segment."

**Recommended Entry:** {Build/partner/differentiate + rationale}
- Example: "Build AI-native SaaS targeting competitive teams. Differentiate on AI quality and affordable team pricing ($5-8/user/mo vs Product A's $15/user/mo). Go-to-market via Reddit r/GlobalOffensive and esports Discord communities."

**Next Steps:**
- {Step 1: e.g., Interview 10 competitive teams to validate WTP}
- {Step 2: e.g., Build AI demo prototype to test quality}
- {Step 3: e.g., Launch landing page with waitlist to measure demand}

---

## Product Catalog

{Paste full table from product-catalog.md}

**Market Breakdown:**
- Commercial: {count} products ({percentage}%)
- Open Source: {count} products ({percentage}%)
- Community: {count} products ({percentage}%)

**Category Breakdown:**
- SaaS: {count} products
- Desktop: {count} products
- CLI/Library: {count} products
- Other: {count} products

**Market Coverage Notes:**
{Any gaps, thin coverage, regional exclusions from product-catalog.md § Discovery Notes}

---

## Feature Comparison Matrix

{Paste feature table from features.md}

**Key Gaps:**
- {Gap 1 from features.md § Gap Analysis}
- {Gap 2 from features.md § Gap Analysis}
- {Gap 3 from features.md § Gap Analysis}

**Unique Features (Differentiation Angles):**
- {Unique Feature 1 from features.md § Gap Analysis}
- {Unique Feature 2 from features.md § Gap Analysis}

**Feature Trends:**
- **Table stakes:** {Features everyone has}
- **Emerging:** {Features 2-3 products added recently}
- **Premium/Enterprise only:** {Features gated behind paid tiers}

---

## Market Positioning Map

{Paste positioning map from positioning.md}

**Positioning Clusters:**
- {Cluster 1: e.g., "Developer-first + Technical" — Products A, B, F}
- {Cluster 2: e.g., "Business-first + Non-technical" — Products C, D, E}

**White Space:**
- {Underserved segment 1 from positioning.md § White Space}
- {Unoccupied quadrant 1 from positioning.md § White Space}

**Pricing Analysis:**
- **Median individual price:** ${amount}/month
- **Median team price:** ${amount}/user/month
- **Pricing models:** {Freemium X%, Paid-only Y%, OSS Z%}

---

## User Sentiment Analysis

{Summarize top complaint themes from sentiment.md § Cross-Product Sentiment}

**Top Complaints (Across All Products):**
1. {Complaint 1: e.g., "Pricing too high for individuals" — 35 mentions}
2. {Complaint 2: e.g., "Missing feature X" — 28 mentions}
3. {Complaint 3: e.g., "Poor onboarding" — 18 mentions}

**Top Praise (Across All Products):**
1. {Praise 1: e.g., "Fast and intuitive" — 42 mentions}
2. {Praise 2: e.g., "Great API" — 31 mentions}
3. {Praise 3: e.g., "Responsive support" — 24 mentions}

**Switching Triggers:**
- **Users leave products when:** {Trigger 1, Trigger 2, Trigger 3 from sentiment.md}
- **Users join products when:** {Trigger 1, Trigger 2, Trigger 3 from sentiment.md}

**Products with Strongest Sentiment:**
- **Positive:** {Product name} (4.5/5 avg sentiment)
- **Negative:** {Product name} (2.8/5 avg sentiment)
- **Polarized:** {Product name} (love it or hate it)

---

## Technical Landscape

{Paste tech stack table from tech-stack.md}

**Architecture Patterns:**
- {Pattern 1: e.g., "SaaS (web-based, cloud-hosted)" — Products A, B, E}
- {Pattern 2: e.g., "Desktop (local-first, native apps)" — Product C}
- {Pattern 3: e.g., "CLI/Library (developer-focused)" — Products F, H}

**API Availability:**
- **Rich APIs:** {Product names} (REST + GraphQL, webhooks, SDKs)
- **Limited APIs:** {Product names} (REST only, no webhooks)
- **No APIs:** {Product names} (desktop/CLI only)

**Technical Differentiation Opportunities:**
- {Opportunity 1 from tech-stack.md § Technical Differentiation Opportunities}
- {Opportunity 2 from tech-stack.md § Technical Differentiation Opportunities}

---

## Market Trends

{Paste trend timeline from trends.md}

**Funding Activity (Past 12 Months):**
- Total funding: ${amount}M across {count} companies
- Hot areas: {Trend 1, Trend 2, Trend 3}

**Consolidation:**
- Acquisitions: {Count} (Products {names})
- Shutdowns: {Count} (Products {names})

**Emerging Features:**
- {Feature 1: e.g., "AI-powered analysis" — adoption status, products offering}
- {Feature 2: e.g., "Real-time collaboration" — adoption status, products offering}
- {Feature 3: e.g., "API-first architecture" — adoption status, products offering}

**New Entrants (Launched Past 12 Months):**
- {Product name 1}: {Brief description, traction, positioning}
- {Product name 2}: {Brief description, traction, positioning}

---

## Opportunity Analysis

{Paste opportunity matrix from opportunities.md}

### Top 3 Opportunities (Prioritized)

**1. {Opportunity Name from opportunities.md}**
- **Gap:** {What's missing in the market}
- **Evidence:** {User demand, complaint mentions, market size}
- **Effort:** {S/M/L/XL} | **Impact:** {High/Med/Low} | **Risk:** {High/Med/Low}
- **TAM:** {Small/Medium/Large — dollar estimate}
- **Rationale:** {Why this is #1 — proven demand, medium effort, high impact, low risk}
- **Next Steps:**
  - {Validation step 1}
  - {Validation step 2}
  - {Validation step 3}

**2. {Opportunity Name from opportunities.md}**
- **Gap:** {What's missing}
- **Evidence:** {User demand}
- **Effort:** {S/M/L/XL} | **Impact:** {High/Med/Low} | **Risk:** {High/Med/Low}
- **TAM:** {Small/Medium/Large}
- **Rationale:** {Why this is #2}
- **Next Steps:**
  - {Validation step 1}
  - {Validation step 2}

**3. {Opportunity Name from opportunities.md}**
- **Gap:** {What's missing}
- **Evidence:** {User demand}
- **Effort:** {S/M/L/XL} | **Impact:** {High/Med/Low} | **Risk:** {High/Med/Low}
- **TAM:** {Small/Medium/Large}
- **Rationale:** {Why this is #3}
- **Next Steps:**
  - {Validation step 1}
  - {Validation step 2}

---

## Recommended Entry Strategies

### Primary Strategy: {Build / Partner / Differentiate}

**Rationale:**
{Why this approach fits the market state and top opportunity}

**Example (Build):**
- "Build an AI-native SaaS targeting competitive teams. Market is fragmented with no clear leader, early-stage funding ($55M past 12 months) signals room for new entrants. Top opportunity (AI-native for teams) has proven demand (28 mentions), medium effort (6-8 months), high impact (10x better than bolt-on AI), low risk (clear path)."

**Tactics:**
1. {Specific action 1}
   - Example: "Build MVP with AI round analysis and team features (6-8 months)"
2. {Specific action 2}
   - Example: "Price at $5-8/user/mo (undercut Product A's $15/user/mo)"
3. {Specific action 3}
   - Example: "GTM via Reddit r/GlobalOffensive, esports Discord communities, Twitch streamers"
4. {Specific action 4}
   - Example: "Offer free tier for individual players, paid tier for teams (freemium model)"
5. {Specific action 5}
   - Example: "Partner with esports orgs for testimonials and case studies"

**Timeline:**
- **Months 1-3:** Build MVP (core parsing + AI round analysis)
- **Months 4-6:** Private beta with 10 competitive teams (validate AI quality, WTP)
- **Months 7-9:** Public launch (freemium model, GTM via Reddit/Discord)
- **Months 10-12:** Iterate based on feedback, add team features

**Investment Required:**
- **Development:** $50-100k (1-2 eng × 6-8 months)
- **Infrastructure:** $5-10k/year (AWS, OpenAI API)
- **Marketing:** $10-20k (paid ads, influencer partnerships)
- **Total:** $65-130k for MVP → public launch

---

### Alternative Strategy: {Partner / Buy / Wait}

**When to use this instead of primary strategy:**
{Conditions where alternative makes more sense}

**Example (Partner):**
- "If building from scratch is too risky (XL effort), partner with existing OSS project (Product F or H) and add managed hosting + premium features. Reduces development effort (S-M instead of M-L) but shares revenue with OSS maintainers."

**Example (Buy):**
- "If market consolidates quickly (2-3 acquisitions next 12 months per trends.md), consider acquiring a struggling product (e.g., Product D, which has traction but poor unit economics). Faster time-to-market (3-6 months vs 12-18 months build) but requires capital ($500k-2M acquisition)."

**Example (Wait):**
- "If top opportunity has high risk (e.g., Opportunity 3: Real-time coaching, XL effort, high risk), wait for market to mature and demand to crystallize. Monitor trends for 6-12 months, validate demand via interviews, then build when risk is lower."

---

## Market Map (Visual)

```
[Market Positioning Map]

Price Point (High)
      ↑
      |  Enterprise / Premium
      |  ┌─────────────┐
      |  │ Product G   │  (SSO, compliance, dedicated support)
      |  └─────────────┘
      |
      |  Team / Mid-Market
      |  ┌───────┐  ┌───────┐  ┌───────┐
      |  │Prod C │  │Prod E │  │Prod A │  (Collaboration, integrations)
      |  └───────┘  └───────┘  └───────┘
      |
      |  Individual / Paid
      |  ┌───────┐
      |  │Prod D │  (Premium for power users)
      |  └───────┘
      |
      |  Individual / Free
      |  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐
      |  │Prod A │  │Prod B │  │Prod F │  │Prod H │  (Simple, fast, OSS)
      |  │(Free) │  │(Free) │  │ (OSS) │  │ (OSS) │
      |  └───────┘  └───────┘  └───────┘  └───────┘
      |
      └──────────────────────────────────────────────→
    Individual                               Enterprise
                    Target User
```

**White Space (Opportunities):**
- ⭐ **Competitive Teams + Affordable:** No product targets competitive teams at $5-8/user/mo (Opportunity 1 + 4)
- ⭐ **Mobile-First:** Only 2/12 products have mobile apps, none are mobile-first (Opportunity 5)
- ⭐ **API-First + Individual:** No product offers generous API for individuals (Opportunity from tech-stack.md)

---

## Next Steps

### Immediate Actions (Weeks 1-4)

1. **Validate Top Opportunity:**
   - Interview 10 competitive CS2 teams (players + coaches)
   - Questions: WTP for AI round analysis? Current tools used? Pain points?
   - Success metric: 7/10 teams willing to pay $5-8/user/mo

2. **Build Prototype:**
   - AI demo analysis prototype (use existing OSS parser + OpenAI API)
   - Test with 3-5 real demos from competitive matches
   - Success metric: AI insights are useful (validated by teams)

3. **Launch Landing Page:**
   - Simple landing page with value prop, demo video, email signup
   - GTM: Post to Reddit r/GlobalOffensive, esports Discord servers
   - Success metric: 100 email signups in first week

### Short-Term (Months 1-3)

4. **Build MVP:**
   - Core features: Demo upload, AI round analysis, team dashboard
   - Tech stack: React (frontend), Node.js (backend), PostgreSQL (database), OpenAI API (AI)
   - Timeline: 8-12 weeks

5. **Private Beta:**
   - Recruit 10 competitive teams for private beta
   - Collect feedback on AI quality, UX, pricing
   - Iterate based on feedback

### Medium-Term (Months 4-9)

6. **Public Launch:**
   - Freemium model: Free for individuals, $5-8/user/mo for teams
   - GTM: Reddit, Discord, Twitch streamers, esports influencers
   - Goal: 100 paying teams (500 users) in first 3 months

7. **Iterate & Scale:**
   - Add requested features (mobile app, integrations, advanced AI)
   - Expand to other esports (Valorant, Overwatch, Rainbow Six)
   - Raise seed funding ($500k-1M) if traction is strong

### Long-Term (Months 10-24)

8. **Scale & Grow:**
   - Enterprise tier for pro esports orgs ($100-500/mo)
   - API for third-party developers (ecosystem growth)
   - International expansion (EU, APAC markets)

9. **Monitor Market:**
   - Track competitors (Product A pricing changes, new entrants)
   - Watch for acquisitions (consolidation signals)
   - Revisit this discovery report every 6-12 months

---

## Revisit Schedule

**Update this discovery report:**
- **Every 6 months:** Refresh trends, new entrants, emerging features
- **When market shifts:** Major funding, acquisition, or product launch
- **Before major decisions:** Before raising funding, launching new features, or pivoting

**Signs to revisit sooner:**
- Product A lowers prices (competitive threat)
- New AI-native competitor launches (opportunity window closing)
- CS2 releases major update (parser must adapt)

---

## Sources

All findings sourced from Phase 1 + Phase 2 outputs:
- **Phase 0:** `product-catalog.md` (product landscape)
- **Phase 1:** `features.md`, `positioning.md`, `sentiment.md`, `tech-stack.md`, `trends.md`
- **Phase 2:** `opportunities.md` (from Agent 6)

External sources cited in component files.
```

### Research Tips

**Writing executive summaries:**
- Lead with market state (maturity, competition, growth)
- Highlight key finding (biggest insight from research)
- Identify top opportunity (highest impact/effort ratio)
- Recommend entry strategy (build/partner/differentiate)
- Keep it short (5 bullets max, readable in 2 minutes)

**Creating market maps:**
- Use 2x2 matrix (axes: Target User × Price Point, or Dev-first × Business-first)
- Plot products in quadrants (use text-based diagram for markdown)
- Highlight white space (unoccupied quadrants with demand)

**Recommending entry strategies:**
- **Build:** Market is fragmented, no clear leader, room for new entrant
- **Partner:** Existing OSS or struggling product you can acquire/partner with
- **Differentiate:** Market is crowded, must differentiate on unique angle
- **Wait:** Market is immature, demand is unproven, risk is too high

**Prioritizing opportunities:**
- Rank by impact/effort ratio (High impact + Low effort = do first)
- Consider risk (Low risk > High risk, all else equal)
- Account for TAM (Large TAM > Small TAM, if impact/effort similar)

---

## Research Best Practices

### Time-Boxing

**Per-agent limits:**
- **Agent 0 (Market Scout):** 10-15 WebSearch queries, 2-4 minutes runtime
- **Agent 1-5 (Phase 1):** 8-12 queries each, 4-8 minutes total (parallel)
- **Agent 6-7 (Phase 2):** No new queries (synthesis only), 2-3 minutes total (sequential)

**Total skill runtime:** 8-15 minutes for Phase 0-2

**If exceeding time limits:**
- Reduce product count (analyze top 8 instead of top 12)
- Reduce query count (10 queries instead of 12)
- Skip low-value sources (skip G2 reviews if no B2B products)

### Coverage vs Depth Trade-offs

**Broad coverage (10-30 products):**
- Better for: Product discovery (goal is to find ALL products)
- Worse for: Deep analysis (can't analyze 30 products in depth)

**Deep analysis (3-5 products):**
- Better for: Competitor analysis (goal is to understand ONE competitor deeply)
- Worse for: Market discovery (might miss important products)

**Recommended for product-discovery:**
- **Phase 0:** Broad coverage (10-30 products discovered)
- **Phase 1:** Medium depth (analyze top 8-12 products in detail, summarize others)
- **Phase 2:** Synthesis (prioritize top 3-5 opportunities)

### Citation Standards

**Every claim needs a source:**
- ✅ Good: "Users want AI insights (28 mentions) — Reddit r/GlobalOffensive, HN threads (URLs)"
- ❌ Bad: "Users want AI insights" (no evidence, no source)

**Citation format:**
- Inline: "(28 mentions) — Reddit r/GlobalOffensive, HN threads"
- Footnotes: "Users want AI insights[^1]" with [^1]: {URL} at bottom

**Acceptable sources:**
- Reddit, Hacker News, Product Hunt, GitHub (community feedback)
- G2, Capterra, Trustpilot (review sites)
- TechCrunch, VentureBeat (funding news)
- Company blogs, changelogs (product updates)
- Twitter, LinkedIn (social media)

**Unacceptable sources:**
- No source (fabricated claim)
- Paywalled content (user can't verify)
- Dead links (must use Wayback Machine if link is dead)

### Handling Incomplete Data

**If WebSearch returns no results:**
- Note in output: "Limited public information available"
- Use alternative sources (GitHub issues for OSS, job postings for closed-source)
- Adjust confidence: "Estimated" instead of "Confirmed"

**If product has no pricing page:**
- Check alternatives: GitHub repo (OSS, free), job postings (tech stack)
- Note: "Pricing not publicly listed (enterprise-only, contact sales)"

**If market is thin (only 3-5 products):**
- Don't fabricate products to hit quota
- Note in Phase 0 summary: "Market is nascent, only 5 products discovered"
- Adjust Phase 1: Go deeper on fewer products (more features, more sentiment)

### Quality Checks

**Before submitting final report:**
- ✅ All products have source URLs (no fabrication)
- ✅ All claims have evidence (no speculation)
- ✅ Opportunity matrix has 3+ opportunities with scoring
- ✅ Executive summary is concise (5 bullets, readable in 2 minutes)
- ✅ Market map visualizes landscape (ASCII or table)
- ✅ Entry strategies are actionable (specific tactics, timeline, investment)
- ✅ Report follows template structure (all sections present)
