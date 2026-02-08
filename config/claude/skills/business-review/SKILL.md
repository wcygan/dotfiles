---
name: business-review
description: >
  Launch a multi-function business review team to evaluate product ideas, features, or applications
  from stakeholder perspectives. Agents represent product management, marketing, engineering,
  finance, data science, data engineering, sales, and synthesis roles. Use when evaluating a new
  feature, assessing product viability, planning launches, or need cross-functional input on business
  decisions. Keywords: business review, product evaluation, feature assessment, stakeholder analysis,
  cross-functional review, product viability, go-to-market, unit economics, technical feasibility
context: fork
disable-model-invocation: true
argument-hint: [feature-or-product-description]
---

# Business Review

Orchestrate an 8-agent cross-functional team to evaluate a product idea, feature, or application from multiple business stakeholder perspectives. Phase 1 runs 4 parallel strategy agents (PM, PMM, EM, Finance). Phase 2 runs 3 parallel data agents (Data Scientist, Data Engineer, Sales Engineer). Phase 3 runs a synthesizer to consolidate findings into a balanced recommendation.

## Workflow

### 1. Parse Input

**Target: `$ARGUMENTS`**

If the target above is non-empty, use it immediately — do NOT ask the user to confirm or re-provide it. Parse it as follows:

- **Feature/Product description**: Extract the core idea, target users, and expected outcomes
- **Context flags**: Parse optional flags like `--skip-data-team`, `--focus=sales,pm`, `--quick`

If the target above is empty, ask the user what feature or product to evaluate and wait for their response.

Store the parsed values:
- `FEATURE_DESC`: The product/feature being evaluated
- `FLAGS`: Any processing flags (skip flags, focus filters)

**IMPORTANT**: When a target is provided, begin Phase 1 immediately after parsing. Do not pause for user input.

### 2. Phase 1 — Strategy Agents (Parallel)

Spawn 4 agents in parallel using the Task tool. Each agent is `general-purpose` (needs full tool access). Run all 4 with `run_in_background: true` for maximum parallelism.

Read [REFERENCE.md](REFERENCE.md) first to get detailed evaluation frameworks and output templates for each agent.

#### Agent 1: Product Manager

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a product manager evaluating the following feature/product:

{FEATURE_DESC}

Follow the "Product Manager" template in the reference below. Provide feature prioritization,
user stories, acceptance criteria, and roadmap fit analysis.

{paste Product Manager section from REFERENCE.md}
```

#### Agent 2: Product Marketing Manager

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a product marketing manager evaluating the following feature/product:

{FEATURE_DESC}

Follow the "Product Marketing Manager" template in the reference below. Analyze market
positioning, competitive differentiation, messaging, and go-to-market strategy.

{paste Product Marketing Manager section from REFERENCE.md}
```

#### Agent 3: Engineering Manager

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are an engineering manager evaluating the following feature/product:

{FEATURE_DESC}

Follow the "Engineering Manager" template in the reference below. Assess technical feasibility,
team capacity, architecture implications, and velocity impact.

{paste Engineering Manager section from REFERENCE.md}
```

#### Agent 4: Financial Analyst

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a financial analyst evaluating the following feature/product:

{FEATURE_DESC}

Follow the "Financial Analyst" template in the reference below. Analyze unit economics,
pricing strategy, revenue projections, and cost structure.

{paste Financial Analyst section from REFERENCE.md}
```

### 3. Collect Phase 1 Results

Wait for all 4 background agents to complete. Read their output files to collect results.

Compile a **Phase 1 Summary** containing the key findings from each agent. This summary feeds into Phase 2 agents.

### 4. Phase 2 — Data & Sales Agents (Parallel)

**Check for `--skip-data-team` flag**: If present, skip this entire phase and proceed to Phase 3.

Phase 2 agents run in parallel. Run all 3 with `run_in_background: true`.

Read [REFERENCE.md](REFERENCE.md) for detailed templates.

#### Agent 5: Data Scientist

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a data scientist evaluating the following feature/product:

{FEATURE_DESC}

## Phase 1 Findings
{paste compiled Phase 1 findings}

Follow the "Data Scientist" template in the reference below. Define analytics requirements,
ML opportunities, experiment design, and success metrics.

{paste Data Scientist section from REFERENCE.md}
```

#### Agent 6: Data Engineer

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a data engineer evaluating the following feature/product:

{FEATURE_DESC}

## Phase 1 Findings
{paste compiled Phase 1 findings}

Follow the "Data Engineer" template in the reference below. Analyze data infrastructure needs,
pipeline design, storage strategy, and data quality requirements.

{paste Data Engineer section from REFERENCE.md}
```

#### Agent 7: Sales Engineer

```
subagent_type: general-purpose
run_in_background: true
```

Prompt:

```
You are a sales engineer evaluating the following feature/product:

{FEATURE_DESC}

## Phase 1 Findings
{paste compiled Phase 1 findings}

Follow the "Sales Engineer" template in the reference below. Identify customer objections,
deal blockers, demo readiness, and integration requirements.

{paste Sales Engineer section from REFERENCE.md}
```

### 5. Collect Phase 2 Results

Wait for all Phase 2 background agents to complete (or skip if `--skip-data-team` was set).

Compile a **Phase 2 Summary** with findings from data and sales agents.

### 6. Phase 3 — Synthesis Agent (Sequential)

Run a single synthesis agent that consumes all prior results.

```
subagent_type: general-purpose
```

Prompt:

```
You are a business strategist synthesizing cross-functional input on the following feature/product:

{FEATURE_DESC}

## Phase 1 Findings (Strategy)
{paste compiled Phase 1 findings}

## Phase 2 Findings (Data & Sales)
{paste compiled Phase 2 findings}

Follow the "Synthesizer" template in the reference below. Consolidate all perspectives into
a balanced recommendation with prioritized next steps.

{paste Synthesizer section from REFERENCE.md}
```

### 7. Final Report

Combine all agent outputs into a single comprehensive business review. Present to the user with this structure:

```markdown
# Business Review: {FEATURE_DESC}

## Executive Summary
[3-5 bullet points: strategic value, feasibility, risks, recommendation]

## Table of Contents
1. Product Management Perspective
2. Product Marketing Perspective
3. Engineering Perspective
4. Financial Analysis
5. Data Science Perspective (if Phase 2 ran)
6. Data Engineering Perspective (if Phase 2 ran)
7. Sales Engineering Perspective (if Phase 2 ran)
8. Synthesis & Recommendation

---

## 1. Product Management Perspective

[Agent 1 output]

---

## 2. Product Marketing Perspective

[Agent 2 output]

---

## 3. Engineering Perspective

[Agent 3 output]

---

## 4. Financial Analysis

[Agent 4 output]

---

## 5. Data Science Perspective

[Agent 5 output, if Phase 2 ran]

---

## 6. Data Engineering Perspective

[Agent 6 output, if Phase 2 ran]

---

## 7. Sales Engineering Perspective

[Agent 7 output, if Phase 2 ran]

---

## 8. Synthesis & Recommendation

[Agent 8 output — Synthesizer]

---

## Decision Matrix

### GO / NO-GO Factors

| Factor | Status | Impact |
|--------|--------|--------|
| Strategic alignment | {Green/Yellow/Red} | {rationale} |
| Technical feasibility | {Green/Yellow/Red} | {rationale} |
| Financial viability | {Green/Yellow/Red} | {rationale} |
| Market opportunity | {Green/Yellow/Red} | {rationale} |
| Execution risk | {Green/Yellow/Red} | {rationale} |

### Recommended Action

**Decision**: {GO / NO-GO / CONDITIONAL GO}

**Rationale**: {2-3 sentence summary of why}

### Next Steps (Prioritized)

1. {Most critical action}
2. {Second priority}
3. {Third priority}
4. {Fourth priority}
5. {Fifth priority}

### Open Questions

1. {Critical question requiring research/decision}
2. {Second question}
3. {Third question}
```

## Flags & Options

### `--skip-data-team`

Skip Phase 2 entirely (data science, data engineering, sales engineering). Useful for early-stage idea validation when data infrastructure and sales engineering aren't yet relevant.

Example:
```
/business-review --skip-data-team Add real-time collaboration to our text editor
```

### `--focus=<roles>`

Only run specific agents. Comma-separated list from: `pm`, `pmm`, `em`, `finance`, `ds`, `de`, `sales`, `synth`.

Example:
```
/business-review --focus=pm,em,finance Evaluate migrating to microservices
```

### `--quick`

Run a fast review with reduced depth. Agents produce shorter analyses focused on critical factors only.

Example:
```
/business-review --quick Should we add dark mode?
```

## Example Invocations

```
/business-review Add AI-powered code suggestions to our IDE
/business-review --skip-data-team Launch a community forum for users
/business-review --focus=pm,pmm,sales Evaluate entering the healthcare vertical
/business-review --quick Should we support SSO with Okta?
/business-review Build a mobile app for field technicians with offline-first architecture
```

## Anti-Patterns

- **Don't skip synthesis**: The synthesizer is critical for consolidating conflicting perspectives into a coherent recommendation.
- **Don't run all agents for trivial decisions**: Use `--quick` or `--focus` for small features that don't warrant a full cross-functional review.
- **Don't ignore red flags**: If multiple agents raise concerns about the same issue (e.g., technical debt, market timing), that's a strong signal.
- **Don't expect unanimous agreement**: Cross-functional reviews surface trade-offs. The synthesizer's job is to balance competing priorities, not achieve consensus.
- **Don't fabricate data**: If agents lack information (e.g., no competitive pricing data), they should say so explicitly and recommend research rather than guessing.

## Notes

- Total runtime is typically 4-10 minutes depending on complexity and whether Phase 2 runs.
- Phase 1 and Phase 2 agents run in parallel within their phases; Phase 3 runs sequentially after Phase 2.
- If an agent fails or returns thin results, note the gap in the final report rather than blocking synthesis.
- Use `--focus` to run only the perspectives most relevant to your decision (e.g., skip finance for internal tools).
