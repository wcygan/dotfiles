---
name: data-review
description: >
  Review data pipelines, warehouses, analytics infrastructure for reliability, quality,
  performance, governance, and cost. Spawns specialized agents (data-engineer, data-scientist,
  performance-analyst, security-auditor) to audit in parallel, then debate architecture trade-offs.
  Use when evaluating data platforms, assessing pipeline health, optimizing queries, or auditing
  data governance and compliance. Keywords: data pipeline, warehouse, analytics, ETL, data quality,
  query optimization, data governance, compliance, data platform.
disable-model-invocation: true
argument-hint: [platform-description or config-path]
---

# Data Review Skill

A multi-agent data platform review system that audits pipelines, warehouses, analytics infrastructure,
and produces a prioritized health report with actionable recommendations.

## Prerequisites

None required. Works with any data platform that provides:
- Pipeline configuration files (Airflow DAGs, dbt models, etc.)
- Query logs or analytics code
- Infrastructure-as-code (Terraform, CloudFormation)
- Data quality metrics or monitoring dashboards

## Inputs

The user provides:

1. **Platform description** (required) — Overview of the data platform architecture
   - OR: Path to configuration directory (e.g., `dbt/`, `airflow/dags/`, `terraform/`)
2. **Key data flows** (optional) — Critical pipelines to prioritize, e.g. "user events → warehouse → BI dashboards"
3. **Known pain points** (optional) — Current issues, slow queries, quality problems
4. **Compliance requirements** (optional) — GDPR, HIPAA, SOC2, etc.
5. **Context file** (optional) — Markdown file with platform details, constraints, team size

If the user doesn't provide optional inputs, use reasonable defaults and note assumptions.

## Agent Roster

Each agent has a specialized domain. All agents read the same platform artifacts in parallel.

| # | Agent | Focus | Reference |
|---|-------|-------|-----------|
| 1 | **Data Engineer** | Pipeline reliability, orchestration, dependencies, error handling, monitoring | `agents/data-engineer.md` |
| 2 | **Data Scientist** | Analytics quality, model pipelines, feature engineering, reproducibility | `agents/data-scientist.md` |
| 3 | **Performance Analyst** | Query optimization, indexing, partitioning, compute costs, bottlenecks | `agents/performance-analyst.md` |
| 4 | **Security Auditor** | Data governance, access controls, PII handling, compliance, lineage | `agents/security-auditor.md` |
| 5 | **Synthesizer** | Reads all agent reports → produces prioritized action plan with trade-offs | Built-in coordinator role |

## Workflow

### Phase 1: Discovery

1. Confirm the platform description or config path
2. Identify platform type (dbt, Airflow, Databricks, Snowflake, custom, etc.)
3. Scan for key artifacts:
   - Pipeline definitions (DAGs, models, workflows)
   - Query files (SQL, notebooks)
   - Infrastructure code (Terraform, YAML configs)
   - Data quality tests or schema definitions
   - Monitoring/alerting configurations
4. Build a platform inventory listing:
   - Pipeline count and types
   - Data sources and destinations
   - Compute/storage components
   - Orchestration tools
5. Save discovery results to `workspace/discovery.md`

This discovery output is shared with all review agents as context.

### Phase 2: Parallel Review (Sub-agents)

Spawn agents 1-4 in parallel using the Task tool. Each agent receives:

- The platform description and discovery file
- Their specific agent instructions (from `agents/*.md`)
- The review checklists and scoring rubric (`REFERENCE.md`)
- An output file path for their findings

Each agent:
1. Reads relevant platform artifacts (configs, code, schemas)
2. Applies their domain-specific audit checklist
3. Scores each dimension (1-5 scale)
4. Documents findings with file/line references
5. Writes prioritized recommendations to their output file

Agent output files:
- `workspace/agents/data-engineer.md`
- `workspace/agents/data-scientist.md`
- `workspace/agents/performance-analyst.md`
- `workspace/agents/security-auditor.md`

### Phase 3: Architecture Debate

After all agents complete their audits, spawn a debate session:

1. Create a debate prompt with all agent findings
2. Agents discuss conflicting recommendations (e.g., performance vs. cost)
3. Identify trade-offs and prioritization criteria
4. Build consensus on critical vs. nice-to-have improvements
5. Save debate transcript to `workspace/debate.md`

### Phase 4: Synthesis

The coordinator (you) acts as the Synthesizer:

1. Read all 4 agent reports and debate transcript
2. Deduplicate overlapping findings
3. Categorize by severity (Critical / High / Medium / Low)
4. Rank by impact-vs-effort for small teams
5. Produce the final health report

### Phase 5: Output

Generate the final deliverable using the report template in `REFERENCE.md`.

Save to `workspace/data-platform-health-report.md` and present to the user.

## Output Structure

```
workspace/
├── discovery.md                    # Platform inventory from Phase 1
├── agents/
│   ├── data-engineer.md
│   ├── data-scientist.md
│   ├── performance-analyst.md
│   └── security-auditor.md
├── debate.md                       # Architecture trade-offs discussion
└── data-platform-health-report.md  # Final synthesized report
```

## Coordinator Responsibilities

1. Run the discovery phase to build platform inventory
2. Spawn review agents in parallel with Task tool
3. Ensure each agent has access to the discovery file and reference materials
4. Collect all agent reports
5. Facilitate the architecture debate (spawn debate agents or synthesize manually)
6. Produce the final health report with scoring and prioritized recommendations
7. Present the report to the user with executive summary

## Customization

The user can customize the review by:

- **Skipping agents**: "Skip data science review, focus on infrastructure and performance"
- **Focusing on specific pipelines**: "Only review the user_events ETL and downstream models"
- **Prioritizing dimensions**: "I care most about compliance, less about performance"
- **Adding comparisons**: "Compare our approach to industry best practices for event streaming"
- **Specifying constraints**: "We're a 2-person team, recommend low-maintenance solutions only"
- **Setting compliance scope**: "Audit for GDPR compliance specifically"

Adapt the agent roster and instructions accordingly.

## Scoring System

Each agent rates their domain on a 1-5 scale:

- **5 (Excellent)**: Industry best practices, fully automated, no issues
- **4 (Good)**: Minor improvements possible, well-maintained
- **3 (Adequate)**: Functional but needs attention, some technical debt
- **2 (Poor)**: Significant issues, requires immediate action
- **1 (Critical)**: Broken or severely compromised, blocking business value

The final report includes:
- Overall platform health score (average across domains)
- Per-domain scores with justification
- Critical findings (score ≤ 2)
- Quick wins (high impact, low effort)
- Strategic improvements (high impact, high effort)

## Common Review Scenarios

### Scenario 1: New Team Inheriting a Data Platform
```bash
/data-review "Inherited a Snowflake + dbt + Airflow stack. Need to understand health and risks."
```

### Scenario 2: Pre-Migration Assessment
```bash
/data-review "Planning to migrate from on-prem Postgres to BigQuery. Audit current state."
```

### Scenario 3: Performance Investigation
```bash
/data-review "Dashboard queries taking 2+ minutes. Focus on query optimization and indexing."
```

### Scenario 4: Compliance Audit
```bash
/data-review "Need HIPAA compliance audit of our analytics platform. Check PII handling and access controls."
```

### Scenario 5: Cost Optimization
```bash
/data-review "Warehouse costs doubled this quarter. Identify waste and optimization opportunities."
```

## Agent Invocation Pattern

```fish
# Example internal workflow
use Task tool to spawn:
  - data-engineer with discovery.md + REFERENCE.md → workspace/agents/data-engineer.md
  - data-scientist with discovery.md + REFERENCE.md → workspace/agents/data-scientist.md
  - performance-analyst with discovery.md + REFERENCE.md → workspace/agents/performance-analyst.md
  - security-auditor with discovery.md + REFERENCE.md → workspace/agents/security-auditor.md

# Wait for all agents to complete

# Spawn debate session (optional)
use Task tool to spawn debate with all agent findings

# Synthesize final report
Read all outputs + debate transcript
Apply report template from REFERENCE.md
Generate data-platform-health-report.md
```

## References

- `REFERENCE.md` — Audit checklists, scoring rubric, common issues and fixes
- `agents/data-engineer.md` — Pipeline reliability and orchestration focus
- `agents/data-scientist.md` — Analytics quality and reproducibility focus
- `agents/performance-analyst.md` — Query optimization and cost efficiency focus
- `agents/security-auditor.md` — Governance, compliance, and access control focus
