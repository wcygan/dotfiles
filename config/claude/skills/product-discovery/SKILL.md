# Product Discovery

```yaml
---
name: product-discovery
description: >
  Comprehensive market discovery using an 8-agent research team. Discovers ALL products
  in a given space (commercial, open source, community tools), analyzes features, positioning,
  sentiment, and technical architecture, then identifies market opportunities. Use when
  exploring a new market, evaluating a product category, finding competitors, or identifying
  white space. Keywords: market research, product discovery, competitive landscape,
  market analysis, find competitors, product catalog, market map
context: fork
disable-model-invocation: true
argument-hint: [market-or-product-space]
---
```

## What This Skill Does

Orchestrates an 8-agent research team to:
1. **Discover** all products in a market space (commercial, OSS, community)
2. **Analyze** features, positioning, sentiment, tech stacks, and trends
3. **Identify** market opportunities and white space
4. **Synthesize** a comprehensive market landscape report

**Key Distinction:** `/competitor-analysis` does a deep dive on ONE known competitor → MVP spec. `/product-discovery` discovers MANY products → catalog + positioning map + opportunities.

## When to Use This

- **Exploring new markets:** "What tools exist for CS2 demo analysis?"
- **Evaluating product categories:** "Map the project management landscape"
- **Finding competitors:** "Who else is building developer analytics?"
- **Identifying white space:** "Where are the gaps in the market?"

## Example Invocations

```bash
/product-discovery CS2 Demo Analysis
/product-discovery project management tools for remote teams
/product-discovery developer analytics platforms
/product-discovery Linear and similar tools
```

## Output Deliverables

- **Product Catalog:** Table of 10-30 products with type, category, description
- **Feature Comparison Matrix:** What each product offers (gaps highlighted)
- **Market Positioning Map:** Who targets which segments, messaging themes
- **User Sentiment Analysis:** Praise patterns and complaint themes per product
- **Technical Landscape:** Tech stacks and architecture patterns
- **Market Trends:** Funding, acquisitions, emerging features, new entrants
- **Opportunity Analysis:** 3+ opportunities scored on effort/impact/risk
- **Entry Strategies:** Build/partner/differentiate recommendations

---

## Workflow

### 1. Parse Input & Setup

**Parse the user's query into structured search parameters:**

- **Market category:** Extract the core category (e.g., "CS2 Demo Analysis", "Project Management Tools")
- **Search terms:** Derive 3-5 search terms for discovery (e.g., "CS2 demo analyzer", "Counter-Strike replay tool")
- **Filters:** Note any constraints (e.g., "for remote teams", "open source only")

**If input is empty or too vague:**
- Use AskUserQuestion to clarify target market
- Provide examples: project management, developer tools, game analytics, design tools
- Get specific use case if possible

**Create workspace directory:**
```bash
mkdir -p workspace/product-discovery-{timestamp}
```

**Store context in `workspace/product-discovery-{timestamp}/context.md`:**
```markdown
# Discovery Context

**Market Category:** {category}
**Search Terms:** {term1}, {term2}, {term3}
**Filters:** {constraints if any}
**Timestamp:** {ISO timestamp}
```

---

### 2. Phase 0 — Market Discovery (Mandatory)

**Why mandatory:** Unlike competitor-analysis (starts with known company), product-discovery starts with vague query. Phase 0 transforms "CS2 Demo Analysis" into structured catalog of 15-25 products. Without this, Phase 1 agents don't know what to research.

**Spawn Market Scout Agent:**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: true
- name: "market-scout"
- description: "Discover products in {category}"
- prompt: |
  You are the Market Scout for a product discovery engagement.

  **Mission:** Discover ALL products in the "{category}" space.

  **Your goal:** Create a comprehensive product catalog with 10-30 products.
  Include commercial products, open source tools, and community projects.

  **Research Checklist (see REFERENCE.md § Agent 0):**
  - WebSearch: "best {category} tools 2026"
  - WebSearch: "{category} comparison"
  - WebSearch: "reddit {category} tools"
  - WebSearch: "product hunt {category}"
  - WebSearch: "github {category}"
  - WebSearch: "{category} alternatives"
  - WebSearch: "{search_term1}", "{search_term2}", "{search_term3}"

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/product-catalog.md` with:

  | Name | URL | Type | Category | Description |
  |------|-----|------|----------|-------------|
  | Example Tool | https://example.com | Commercial | SaaS | Brief description |
  | OSS Project | https://github.com/... | Open Source | CLI | Brief description |

  **Types:** Commercial, Open Source, Community, Freemium
  **Categories:** SaaS, Desktop, CLI, Library, API, etc.

  **Citation Rule:** Every product must have a source URL where you found it.

  **Coverage Target:** 10-30 products (if fewer exist, note market is nascent).

  Consult REFERENCE.md § Agent 0 for detailed research guidelines.
```

**Wait for Market Scout completion:**
- Read `workspace/product-discovery-{timestamp}/product-catalog.md`
- Verify 10+ products cataloged (if fewer, adjust expectations)
- Count products by type (Commercial/OSS/Community) and category

**Checkpoint:** Do not proceed to Phase 1 until catalog exists.

---

### 3. Phase 1 — Parallel Research (5 Agents)

**Why 5 agents (not 4):** Covering MANY products requires broader lenses:
- Features (what they do)
- Positioning (who they target)
- Sentiment (what users feel)
- Tech (how they're built)
- Trends (what's changing)

**All Phase 1 agents run in background (run_in_background: true) for parallel execution.**

---

#### Agent 1: Product Features Researcher

**Spawn Agent:**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: true
- name: "features-researcher"
- description: "Analyze product features"
- prompt: |
  You are the Product Features Researcher for a product discovery engagement.

  **Mission:** Build a feature comparison matrix for the top 8-12 products.

  **Input:** Read `workspace/product-discovery-{timestamp}/product-catalog.md`

  **Research Checklist (see REFERENCE.md § Agent 1):**
  For each of the top 8-12 products:
  - WebFetch the landing page
  - Extract feature lists from homepage, features page, pricing page
  - Note which features are free vs paid
  - Check platform availability (web/desktop/mobile/API)

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/features.md` with:

  ## Feature Comparison Matrix

  | Feature | Product A | Product B | Product C | ... |
  |---------|-----------|-----------|-----------|-----|
  | Feature 1 | ✓ | ✗ | Premium | ... |
  | Feature 2 | ✓ | ✓ | ✓ | ... |

  Legend: ✓ (included), ✗ (missing), Premium (paid tier only)

  ## Gap Analysis

  **Features users want but no one offers:**
  - Gap 1: Evidence from user feedback
  - Gap 2: Evidence from complaints

  **Features only 1-2 products offer (differentiation angles):**
  - Unique Feature 1: Only offered by Product X
  - Unique Feature 2: Only offered by Product Y

  Consult REFERENCE.md § Agent 1 for detailed research guidelines.
```

---

#### Agent 2: Market Positioning Analyst

**Spawn Agent:**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: true
- name: "positioning-analyst"
- description: "Analyze market positioning"
- prompt: |
  You are the Market Positioning Analyst for a product discovery engagement.

  **Mission:** Map how products position themselves and identify white space.

  **Input:** Read `workspace/product-discovery-{timestamp}/product-catalog.md`

  **Research Checklist (see REFERENCE.md § Agent 2):**
  For each product:
  - WebFetch landing page
  - Extract tagline, hero message, target persona
  - Note pricing model (free/freemium/paid, price points)
  - Identify market segment (individual/team/enterprise)

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/positioning.md` with:

  ## Positioning Map

  **Axis 1: Target User (Individual → Enterprise)**
  **Axis 2: Price Point (Free → Premium)**

  | Quadrant | Products | Messaging Theme |
  |----------|----------|-----------------|
  | Individual/Free | Product A, B | "Simple, fast, no-signup" |
  | Team/Mid-Market | Product C, D | "Collaboration, integrations" |
  | Enterprise/Premium | Product E | "Security, compliance, SSO" |

  ## Messaging Themes

  | Theme | Products | Example Taglines |
  |-------|----------|------------------|
  | Developer-first | A, B | "Built by devs, for devs" |
  | Business-first | C, D | "Align teams, ship faster" |

  ## White Space

  **Underserved segments:** Personas ignored by incumbents.
  **Unoccupied quadrants:** Positioning combinations no one targets.

  Consult REFERENCE.md § Agent 2 for detailed research guidelines.
```

---

#### Agent 3: User Sentiment Researcher

**Spawn Agent:**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: true
- name: "sentiment-researcher"
- description: "Analyze user sentiment"
- prompt: |
  You are the User Sentiment Researcher for a product discovery engagement.

  **Mission:** Extract praise patterns and complaint themes for each product.

  **Input:** Read `workspace/product-discovery-{timestamp}/product-catalog.md`

  **Research Checklist (see REFERENCE.md § Agent 3):**
  For top 8-12 products:
  - WebSearch: "reddit {product name} review"
  - WebSearch: "hacker news {product name}"
  - WebSearch: "g2 {product name} reviews" (if B2B)
  - WebSearch: "twitter {product name} complaints"
  - Extract common praise and complaints

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/sentiment.md` with:

  ## Sentiment Summary

  ### Product A
  **Praise:**
  - "Fast and intuitive" (Reddit, HN)
  - "Great API" (G2)

  **Complaints:**
  - "Expensive for individuals" (Reddit)
  - "Missing feature X" (Twitter)

  **Switching Triggers:**
  - Users switch FROM Product A when: pricing increases, missing features
  - Users switch TO Product A when: frustrated with Product B complexity

  ### Product B
  ... (repeat for each product)

  ## Top Complaint Themes (Across All Products)

  1. **Theme:** Pricing too high for individuals → Evidence: 12 mentions across Reddit/Twitter
  2. **Theme:** Missing feature X → Evidence: 8 mentions, requested on Product A, B, C
  3. **Theme:** Poor onboarding → Evidence: 6 mentions on HN

  Consult REFERENCE.md § Agent 3 for detailed research guidelines.
```

---

#### Agent 4: Technical Stack Investigator

**Spawn Agent:**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: true
- name: "tech-investigator"
- description: "Investigate tech stacks"
- prompt: |
  You are the Technical Stack Investigator for a product discovery engagement.

  **Mission:** Map how products are built and identify architecture patterns.

  **Input:** Read `workspace/product-discovery-{timestamp}/product-catalog.md`

  **Research Checklist (see REFERENCE.md § Agent 4):**
  For each product:
  - If OSS: Check GitHub repo, README, dependencies
  - If commercial: WebSearch "{product name} tech stack", engineering blog, job postings
  - Check StackShare, Built With, Wappalyzer
  - Note architecture (SaaS, desktop app, CLI, library)
  - Note API availability and integration ecosystem

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/tech-stack.md` with:

  ## Tech Stack Table

  | Product | Frontend | Backend | Infrastructure | API? |
  |---------|----------|---------|----------------|------|
  | Product A | React | Node.js | AWS | REST |
  | Product B | Electron | Rust | Desktop | None |
  | Product C | N/A | Go | CLI | N/A |

  ## Architecture Patterns

  **SaaS (web-based):** Products A, D, E
  **Desktop (local-first):** Products B, F
  **CLI/Library (developer-focused):** Products C, G
  **Hybrid (web + desktop):** Product H

  ## Integration Ecosystem

  **Rich APIs:** Products A, D (REST, webhooks, SDKs)
  **Limited APIs:** Product E (read-only)
  **No APIs:** Products B, C (desktop/CLI only)

  Consult REFERENCE.md § Agent 4 for detailed research guidelines.
```

---

#### Agent 5: Market Trends Scout

**Spawn Agent:**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: true
- name: "trends-scout"
- description: "Research market trends"
- prompt: |
  You are the Market Trends Scout for a product discovery engagement.

  **Mission:** Identify funding, acquisitions, emerging features, and new entrants.

  **Input:** Read `workspace/product-discovery-{timestamp}/product-catalog.md`

  **Research Checklist (see REFERENCE.md § Agent 5):**
  - WebSearch: "{category} funding news 2025 2026"
  - WebSearch: "{category} acquisitions 2025 2026"
  - WebSearch: "{category} shutdowns 2025 2026"
  - WebSearch: "state of {category} 2026"
  - WebSearch: "{category} emerging features"
  - WebSearch: "new {category} tools 2026"

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/trends.md` with:

  ## Trend Timeline

  **2025-Q4:**
  - Product A raised $10M Series A (Source: TechCrunch)
  - Product B acquired by BigCo (Source: Press Release)

  **2026-Q1:**
  - Product C launched v2 with AI features (Source: Blog)
  - New entrant Product D launched (Source: Product Hunt)

  ## Market Dynamics

  **Funding Activity:**
  - Total funding: $XM across Y companies
  - Hot areas: AI features, collaboration, automation

  **Consolidation:**
  - Acquisitions: B acquired by BigCo, E acquired by MegaCorp
  - Shutdowns: Product F shut down (reason: market saturation)

  **Emerging Features:**
  - AI-powered analysis (added by Products A, C, D)
  - Real-time collaboration (added by Product E)
  - API-first architecture (trend in new entrants)

  **New Entrants (launched 2025-2026):**
  - Product D: AI-native approach
  - Product G: Open source alternative

  Consult REFERENCE.md § Agent 5 for detailed research guidelines.
```

---

**Wait for all Phase 1 agents to complete:**

Use TaskOutput or monitor background tasks to ensure all 5 agents finish before proceeding to Phase 2.

**Read all Phase 1 outputs:**
- `workspace/product-discovery-{timestamp}/features.md`
- `workspace/product-discovery-{timestamp}/positioning.md`
- `workspace/product-discovery-{timestamp}/sentiment.md`
- `workspace/product-discovery-{timestamp}/tech-stack.md`
- `workspace/product-discovery-{timestamp}/trends.md`

**Compile Phase 1 summary:**
Create `workspace/product-discovery-{timestamp}/phase1-summary.md` with key findings from each agent.

---

### 4. Phase 2 — Sequential Synthesis (2 Agents)

**Why 2 agents (not 1):**
- Opportunity Identifier focuses on gaps/white space
- Landscape Synthesizer creates market map and strategy
- Separating ensures opportunities are identified BEFORE strategy is recommended

**Why sequential (NOT background):** Agent 7 needs Agent 6's output. Running them in sequence ensures proper data flow.

---

#### Agent 6: Opportunity Identifier

**Spawn Agent (NOT background):**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: false  # Sequential, not background
- name: "opportunity-identifier"
- description: "Identify market opportunities"
- prompt: |
  You are the Opportunity Identifier for a product discovery engagement.

  **Mission:** Cross-reference all Phase 1 findings to identify market opportunities.

  **Input Files (read all):**
  - `workspace/product-discovery-{timestamp}/product-catalog.md`
  - `workspace/product-discovery-{timestamp}/features.md`
  - `workspace/product-discovery-{timestamp}/positioning.md`
  - `workspace/product-discovery-{timestamp}/sentiment.md`
  - `workspace/product-discovery-{timestamp}/tech-stack.md`
  - `workspace/product-discovery-{timestamp}/trends.md`

  **Analysis Framework (see REFERENCE.md § Agent 6):**

  1. **Feature Gaps:** Features users want but no one offers (from features.md + sentiment.md)
  2. **Underserved Segments:** Personas ignored by incumbents (from positioning.md)
  3. **Positioning White Space:** Unoccupied 2x2 quadrants (from positioning.md)
  4. **Technical Differentiation:** Architecture patterns no one uses (from tech-stack.md)
  5. **Trend Opportunities:** Emerging features not yet mainstream (from trends.md)

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/opportunities.md` with:

  ## Opportunity Matrix

  | # | Opportunity | Gap/Evidence | TAM Estimate | Effort | Impact | Risk |
  |---|-------------|--------------|--------------|--------|--------|------|
  | 1 | Feature X for Segment Y | Users want X (8 mentions), no one offers for Y | Medium | M | High | Low |
  | 2 | Open source alternative | All products are paid, users request free tier | Large | L | Medium | Medium |
  | 3 | AI-native approach | Emerging trend (3 new entrants), incumbents slow to adopt | Small | XL | High | High |

  **Scoring:**
  - **Effort:** S (weeks), M (months), L (quarters), XL (years)
  - **Impact:** High (10x better), Medium (2-3x better), Low (incremental)
  - **Risk:** High (unproven), Medium (proven demand, hard execution), Low (clear path)

  **TAM Estimate:** Small (<$10M), Medium ($10-100M), Large (>$100M) — rough order of magnitude based on market size and segment.

  **Evidence Rules:**
  - Every opportunity must cite specific findings (e.g., "8 user complaints about X")
  - Link to source files (features.md § Gap Analysis)

  **Coverage Target:** Identify 3-7 opportunities (prioritize by impact/effort ratio).

  Consult REFERENCE.md § Agent 6 for detailed analysis guidelines.
```

**Wait for Agent 6 completion:**
- Read `workspace/product-discovery-{timestamp}/opportunities.md`
- Verify 3+ opportunities identified with scoring

---

#### Agent 7: Landscape Synthesizer

**Spawn Agent (sequential, waits for Agent 6):**

```markdown
Use the Task tool with:
- subagent_type: general-purpose
- run_in_background: false  # Sequential, waits for Agent 6
- name: "landscape-synthesizer"
- description: "Synthesize final report"
- prompt: |
  You are the Landscape Synthesizer for a product discovery engagement.

  **Mission:** Create the final market landscape report with executive summary, market map, and entry strategies.

  **Input Files (read all):**
  - `workspace/product-discovery-{timestamp}/product-catalog.md`
  - `workspace/product-discovery-{timestamp}/features.md`
  - `workspace/product-discovery-{timestamp}/positioning.md`
  - `workspace/product-discovery-{timestamp}/sentiment.md`
  - `workspace/product-discovery-{timestamp}/tech-stack.md`
  - `workspace/product-discovery-{timestamp}/trends.md`
  - `workspace/product-discovery-{timestamp}/opportunities.md` (from Agent 6)

  **Synthesis Framework (see REFERENCE.md § Agent 7):**

  1. **Executive Summary:** 3-5 bullets on market state and top opportunities
  2. **Market Map:** Visual representation of product landscape (ASCII or markdown table)
  3. **Entry Strategies:** Build/partner/differentiate recommendations
  4. **Prioritization:** Rank top 3 opportunities by impact/effort/risk

  **Output Format:**
  Create `workspace/product-discovery-{timestamp}/FINAL-REPORT.md` with:

  # {Market Category} — Product Discovery Report

  **Generated:** {timestamp}
  **Products Analyzed:** {count}

  ---

  ## Executive Summary

  - **Market State:** {1-2 sentences on maturity, competition, growth}
  - **Key Finding:** {Top insight from research}
  - **Top Opportunity:** {Highest-impact opportunity from opportunities.md}
  - **Recommended Entry:** {Build/partner/differentiate + rationale}

  ---

  ## Product Catalog

  {Paste full table from product-catalog.md}

  **Market Breakdown:**
  - Commercial: X products
  - Open Source: Y products
  - Community: Z products

  ---

  ## Feature Comparison Matrix

  {Paste feature table from features.md}

  **Key Gaps:**
  - {Gap 1 from features.md}
  - {Gap 2 from features.md}

  ---

  ## Market Positioning Map

  {Paste positioning map from positioning.md}

  **White Space:**
  - {Underserved segment 1}
  - {Unoccupied quadrant 1}

  ---

  ## User Sentiment Analysis

  {Summarize top complaint themes from sentiment.md}

  **Switching Triggers:**
  - Users leave products when: {trigger 1, trigger 2}
  - Users join products when: {trigger 1, trigger 2}

  ---

  ## Technical Landscape

  {Paste tech stack table from tech-stack.md}

  **Architecture Patterns:**
  - {Pattern 1: X products}
  - {Pattern 2: Y products}

  ---

  ## Market Trends

  {Paste trend timeline from trends.md}

  **Emerging Features:**
  - {Feature 1: adoption status}
  - {Feature 2: adoption status}

  ---

  ## Opportunity Analysis

  {Paste opportunity matrix from opportunities.md}

  ### Top 3 Opportunities (Prioritized)

  **1. {Opportunity Name}**
  - **Gap:** {What's missing}
  - **Evidence:** {User demand, market size}
  - **Effort:** {S/M/L/XL} | **Impact:** {High/Med/Low} | **Risk:** {High/Med/Low}
  - **Rationale:** {Why this is #1}

  **2. {Opportunity Name}**
  ... (repeat for #2 and #3)

  ---

  ## Recommended Entry Strategies

  **Primary Strategy:** {Build/Partner/Differentiate}
  - **Rationale:** {Why this approach fits the market state and top opportunity}
  - **Tactics:** {3-5 specific actions}

  **Alternative Strategy:** {Second-best approach}
  - **When to use:** {Conditions where this makes sense}

  ---

  ## Next Steps

  1. **Validate Opportunity #1:** {Specific research or prototype to build}
  2. **Engage Users:** {Where to find early adopters}
  3. **Monitor Trends:** {What to watch in the market}
  4. **Revisit in:** {3/6/12 months — when to refresh this research}

  ---

  **Sources:** All findings cited in component files (features.md, positioning.md, etc.)

  Consult REFERENCE.md § Agent 7 for detailed synthesis guidelines.
```

**Wait for Agent 7 completion:**
- Read `workspace/product-discovery-{timestamp}/FINAL-REPORT.md`
- Verify report follows template structure

---

### 5. Final Report Compilation

**Present the final report to the user:**

1. **Display Executive Summary** (copy from FINAL-REPORT.md § Executive Summary)
2. **Display Top 3 Opportunities** (copy from FINAL-REPORT.md § Top 3 Opportunities)
3. **Display Recommended Entry Strategies** (copy from FINAL-REPORT.md § Recommended Entry Strategies)
4. **Provide link to full report:** `workspace/product-discovery-{timestamp}/FINAL-REPORT.md`

**Example output:**

```markdown
# Product Discovery Complete

**Market:** CS2 Demo Analysis
**Products Analyzed:** 18
**Report:** workspace/product-discovery-1234567890/FINAL-REPORT.md

## Executive Summary

- **Market State:** Nascent market with 18 tools (12 OSS, 4 commercial, 2 community). Fragmented landscape, no clear leader.
- **Key Finding:** Users want AI-powered round analysis and team performance tracking, but only 2 products offer basic versions.
- **Top Opportunity:** AI-native demo analyzer targeting competitive teams (Medium TAM, M effort, High impact, Low risk).
- **Recommended Entry:** Build a focused product for competitive teams, differentiate on AI features and team analytics.

## Top 3 Opportunities

1. **AI Round Analysis for Competitive Teams**
   - Gap: Users want AI insights, incumbents offer basic stats
   - Effort: M | Impact: High | Risk: Low

2. **Open Source Demo Parser Library**
   - Gap: All parsers are fragmented, no standard library
   - Effort: L | Impact: Medium | Risk: Medium

3. **Real-time Match Coaching Tool**
   - Gap: All tools are post-match, no live analysis
   - Effort: XL | Impact: High | Risk: High

## Recommended Entry Strategy

**Primary: Build AI-native SaaS for competitive teams**
- Rationale: Clear demand, underserved segment, differentiation angle
- Tactics: MVP with round analysis, target semi-pro teams, freemium pricing

See full report for feature matrix, positioning map, sentiment analysis, and detailed opportunity breakdown.
```

---

## Anti-Patterns (What NOT to Do)

**❌ Don't skip Phase 0:**
Phase 1 agents need the product catalog. Without it, they don't know what to research.

**❌ Don't limit to top 3 products:**
The goal is to discover the FULL landscape (10-30 products), not deep-dive on a few.

**❌ Don't run Phase 2 before Phase 1 completes:**
Agent 6 needs all Phase 1 findings. Agent 7 needs Agent 6's output. Respect the sequence.

**❌ Don't fabricate products:**
Every product in the catalog must have a source URL. If the market is thin (only 3-5 products), say so explicitly.

**❌ Don't skip OSS and community tools:**
They're part of the landscape. Many users start with OSS before upgrading to commercial.

**❌ Don't score opportunities without evidence:**
Every opportunity must cite specific findings (user complaints, feature gaps, positioning holes).

**❌ Don't create 20 opportunities:**
Focus on the top 3-7. More than that overwhelms users and dilutes impact.

---

## Edge Cases

**Thin market coverage (only 3-5 products):**
- Note in Phase 0 summary: "Market is nascent, only 5 products discovered."
- Adjust Phase 1: Go deeper on fewer products (more features, more sentiment).
- Opportunity section: Highlight market creation angle (not just competition).

**Mature saturated market (50+ products):**
- Phase 0: Filter to top 20-30 by popularity, funding, or user base.
- Group by segments/clusters in catalog (e.g., "Enterprise Tools", "Individual Tools").
- Opportunity section: Focus on differentiation vs greenfield (hard to displace incumbents).

**Ambiguous query:**
- If query is too vague (e.g., "tools"), use AskUserQuestion to clarify.
- Suggest examples: "Did you mean project management tools, developer tools, design tools?"

**No user sentiment available:**
- If products are too niche for Reddit/HN/G2, note in sentiment.md: "Limited public feedback available."
- Focus on GitHub issues (for OSS) or support forums.

**No tech stack info (commercial closed-source):**
- Note in tech-stack.md: "Closed-source, limited public info."
- Infer from job postings, Wappalyzer, or BuiltWith.

---

## Runtime Expectations

**Total runtime:** 8-15 minutes for Phase 0-2 (depends on market size and web search responsiveness).

**Phase breakdown:**
- Phase 0 (Market Scout): 2-4 minutes (10-15 WebSearch queries)
- Phase 1 (5 parallel agents): 4-8 minutes (each agent runs 8-12 queries in parallel)
- Phase 2 (2 sequential agents): 2-3 minutes (synthesis, no web searches)

**If runtime exceeds 20 minutes:**
- Check for stuck agents (use TaskOutput to monitor)
- Verify agents aren't re-fetching the same URLs (caching should work)
- Consider reducing product count in Phase 1 (focus on top 8 instead of 12)

---

## Success Criteria

✅ Skill discovers 10-30 products per query (not just top 3)
✅ Catalog includes commercial, OSS, and community tools
✅ Feature matrix reveals gaps (areas no one serves well)
✅ Positioning map shows clusters and white space
✅ Opportunity matrix scores 3+ opportunities on effort/impact/risk
✅ Final report follows template structure
✅ Total runtime: 8-15 minutes for Phase 0-2
✅ All products have source citations (no fabrication)
✅ User receives actionable next steps

---

## Reference

See `REFERENCE.md` for:
- Detailed research checklists for each of the 8 agents
- Output templates and formatting guidelines
- Citation rules and evidence standards
- Example queries and expected outputs
