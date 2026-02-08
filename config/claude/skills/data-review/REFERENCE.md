# Data Platform Review Reference

Comprehensive reference for data platform audits: checklists, scoring rubric, common issues, and solutions.

## Table of Contents

1. [Scoring Rubric](#scoring-rubric)
2. [Audit Checklists](#audit-checklists)
3. [Common Issues & Solutions](#common-issues--solutions)
4. [Platform-Specific Guides](#platform-specific-guides)
5. [Health Metrics](#health-metrics)
6. [Report Template](#report-template)

---

## Scoring Rubric

All agents use a consistent 1-5 scale:

### 5 - Excellent
- **Industry best practices** implemented
- Fully automated with monitoring
- Proactive issue detection
- Documentation complete and current
- No technical debt

**Examples:**
- Pipelines with comprehensive tests, auto-rollback, and SLA monitoring
- All PII encrypted, access controlled, compliance automated
- Queries optimized, costs tracked, autoscaling configured

### 4 - Good
- Above average implementation
- Minor improvements possible
- Well-maintained, no critical gaps
- Monitoring in place
- Manageable technical debt

**Examples:**
- Most pipelines tested, some manual steps remain
- Data quality checks on critical tables, gaps in non-critical areas
- Query performance acceptable, some optimization opportunities

### 3 - Adequate
- Functional but needs attention
- Reactive rather than proactive
- Some technical debt
- Gaps in monitoring or documentation
- Works until it doesn't

**Examples:**
- Pipelines work but fail unpredictably
- Data quality issues discovered by end users
- Performance degrades over time without investigation

### 2 - Poor
- Significant issues affecting reliability or usability
- Requires immediate action
- High technical debt
- Frequent failures or incidents
- Blocking productivity or business value

**Examples:**
- Daily pipeline failures require manual intervention
- No data quality validation, frequent bad data
- Queries time out regularly, users complain

### 1 - Critical
- Broken or severely compromised
- Compliance violations or security risks
- Blocking business operations
- Urgent remediation required
- May require full rebuild

**Examples:**
- Pipeline down for days, no recovery path
- PII exposed, compliance violation imminent
- Infrastructure at capacity, cannot scale

---

## Audit Checklists

### Data Engineering Checklist

#### Pipeline Reliability
- [ ] All pipelines idempotent (safe to retry)
- [ ] Exponential backoff on transient failures
- [ ] Dead letter queues for unrecoverable errors
- [ ] Data quality checks at pipeline boundaries
- [ ] Atomic operations (all-or-nothing commits)
- [ ] Checkpointing for long-running jobs
- [ ] Graceful degradation when upstream delays

#### Orchestration
- [ ] Dependency graph clear and acyclic
- [ ] Parallelism maximizes throughput without bottlenecks
- [ ] SLAs defined and monitored
- [ ] Resource pools prevent contention
- [ ] Dynamic task generation where appropriate
- [ ] Backfill strategy documented

#### Monitoring
- [ ] Pipeline execution metrics (duration, success rate)
- [ ] Data quality metrics (row counts, null rates, schema drift)
- [ ] Resource utilization (CPU, memory, I/O)
- [ ] Alerts on failures and SLA breaches
- [ ] Logs aggregated and searchable
- [ ] Dashboards for pipeline health

#### Code Quality
- [ ] All pipeline code in version control
- [ ] CI/CD for testing and deployment
- [ ] Unit tests for transformation logic
- [ ] Integration tests for end-to-end flows
- [ ] Code reviews required
- [ ] Onboarding documentation exists

#### Scalability
- [ ] Resource allocation appropriate for workload
- [ ] Autoscaling configured
- [ ] Partitioning and clustering used effectively
- [ ] Incremental processing (not full refreshes)
- [ ] Cost monitoring and budgets

### Data Science Checklist

#### Data Quality
- [ ] Schema validation at ingestion
- [ ] Null rate monitoring
- [ ] Referential integrity checks
- [ ] Business rule validation
- [ ] Statistical anomaly detection
- [ ] Data lineage tracking

#### Reproducibility
- [ ] All notebooks in version control
- [ ] Dependencies pinned (requirements.txt, Poetry, Conda)
- [ ] Random seeds set
- [ ] Data versions tracked (DVC, lakeFS)
- [ ] Model registry (MLflow, W&B)
- [ ] CI/CD for model training/deployment

#### Feature Engineering
- [ ] Features defined as reusable modules
- [ ] Point-in-time correctness (no leakage)
- [ ] Feature documentation
- [ ] Feature store or registry
- [ ] Drift detection
- [ ] Unit tests for feature logic

#### MLOps
- [ ] Automated model training pipeline
- [ ] Model versioning and registry
- [ ] A/B testing framework
- [ ] Production performance monitoring
- [ ] Automated retraining triggers
- [ ] Rollback mechanism

#### Code Quality
- [ ] Notebooks for exploration, scripts for production
- [ ] SQL style guide and formatting
- [ ] Code reviews for analytics changes
- [ ] Tests for complex transformations
- [ ] Parameterized queries (no SQL injection)
- [ ] DRY principle (no copy-paste)

### Performance Analyst Checklist

#### Query Performance
- [ ] Top 10 slow queries identified and optimized
- [ ] EXPLAIN plans reviewed for full table scans
- [ ] Indexes on join/filter columns
- [ ] No Cartesian products or skewed joins
- [ ] Explicit column selection (no SELECT *)
- [ ] Query result caching enabled

#### Partitioning & Clustering
- [ ] Large tables partitioned by date/region/tenant
- [ ] Partition pruning verified in query plans
- [ ] Clustering keys match query filters
- [ ] Avoid over-partitioning (>10k partitions)
- [ ] Partition expiration for compliance/cost
- [ ] Table statistics current

#### Compute Efficiency
- [ ] CPU/memory utilization monitored
- [ ] Parallelism configured appropriately
- [ ] Query result caching effective
- [ ] Materialized views for expensive aggregations
- [ ] Spill to disk alerts
- [ ] Autoscaling for variable loads

#### Cost Optimization
- [ ] Cost allocation tags/labels
- [ ] Budget alerts configured
- [ ] Top cost drivers identified
- [ ] Storage tiering (hot/warm/cold)
- [ ] Spot instances for batch workloads
- [ ] Reserved capacity for predictable workloads

#### Scalability
- [ ] Load testing for 2x, 10x growth
- [ ] Concurrency limits configured
- [ ] Autoscaling triggers appropriate
- [ ] Resource pools for priority queries
- [ ] Monitoring for saturation

### Security Auditor Checklist

#### Access Controls
- [ ] RBAC implemented
- [ ] Least privilege enforced
- [ ] Service accounts use limited scopes
- [ ] MFA required for production access
- [ ] Access reviews conducted regularly
- [ ] Orphaned accounts removed promptly

#### PII & Sensitive Data
- [ ] PII columns identified and classified
- [ ] Encryption at rest and in transit
- [ ] Data masking for non-production
- [ ] PII minimization
- [ ] Right to erasure supported
- [ ] Data retention policies enforced

#### Compliance
- [ ] Compliance framework identified (GDPR, HIPAA, etc.)
- [ ] DPA with vendors
- [ ] Privacy policy aligned with practice
- [ ] Consent management
- [ ] DSAR workflow
- [ ] Breach notification process

#### Data Lineage
- [ ] Lineage tools in use
- [ ] Column-level lineage for PII
- [ ] Impact analysis for schema changes
- [ ] Data quality metrics tracked
- [ ] Data catalog maintained
- [ ] Ownership assigned to datasets

#### Audit Logging
- [ ] Data access logs captured
- [ ] Anomaly detection for access patterns
- [ ] Alerts for bulk exports or PII access
- [ ] Immutable audit trail
- [ ] Log retention meets compliance
- [ ] Regular review of logs

---

## Common Issues & Solutions

### Pipeline Reliability

#### Issue: Non-idempotent pipelines cause duplicate data
**Symptoms:** Re-running pipeline creates duplicate records, inconsistent counts
**Root Cause:** INSERT without DELETE, no deduplication logic
**Solution:**
```sql
-- Bad: Non-idempotent
INSERT INTO fact_orders SELECT * FROM staging_orders;

-- Good: Idempotent with MERGE
MERGE INTO fact_orders AS target
USING staging_orders AS source
ON target.order_id = source.order_id
WHEN MATCHED THEN UPDATE SET ...
WHEN NOT MATCHED THEN INSERT ...;

-- Alternative: Delete then insert
DELETE FROM fact_orders WHERE order_date = '{{ ds }}';
INSERT INTO fact_orders SELECT * FROM staging_orders WHERE order_date = '{{ ds }}';
```

#### Issue: Pipelines fail silently, no alerts
**Symptoms:** Data stale, users report missing data
**Root Cause:** No monitoring or alerting configured
**Solution:**
```python
# Airflow: Add SLA and on_failure_callback
default_args = {
    'sla': timedelta(hours=2),
    'on_failure_callback': send_slack_alert,
}

# dbt: Add row count assertions
models:
  - name: fact_orders
    tests:
      - dbt_utils.recency:
          datepart: day
          field: created_at
          interval: 1
```

#### Issue: Long-running jobs fail near completion
**Symptoms:** 4-hour job fails at 3h 55m, have to restart from beginning
**Root Cause:** No checkpointing, no incremental processing
**Solution:**
```python
# Add checkpointing for Spark jobs
df.write.format("delta") \
    .mode("overwrite") \
    .option("checkpointLocation", "/tmp/checkpoint") \
    .save("/data/output")

# Use incremental processing
SELECT * FROM source
WHERE updated_at > (SELECT MAX(updated_at) FROM target)
```

### Data Quality

#### Issue: Bad data discovered by end users
**Symptoms:** Dashboard shows impossible values, users lose trust
**Root Cause:** No validation at ingestion or transformation
**Solution:**
```yaml
# dbt tests
models:
  - name: fact_orders
    columns:
      - name: revenue
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"
      - name: user_id
        tests:
          - relationships:
              to: ref('users')
              field: id
```

#### Issue: Schema drift breaks downstream pipelines
**Symptoms:** Columns disappear, types change, downstream jobs fail
**Root Cause:** No schema enforcement or change detection
**Solution:**
```python
# Great Expectations: Enforce schema
expectation_suite.expect_table_columns_to_match_ordered_list(
    column_list=["order_id", "user_id", "revenue", "created_at"]
)

# dbt: Use source freshness checks
sources:
  - name: raw
    tables:
      - name: orders
        freshness:
          warn_after: {count: 1, period: hour}
          error_after: {count: 2, period: hour}
```

### Query Performance

#### Issue: Dashboard loads take 2+ minutes
**Symptoms:** Users complain, high warehouse costs
**Root Cause:** Full table scans, missing indexes, SELECT *
**Solution:**
```sql
-- Bad: Full table scan
SELECT * FROM events WHERE user_id = 123;

-- Good: Partition pruning + explicit columns
SELECT event_name, created_at
FROM events
WHERE user_id = 123
  AND event_date >= CURRENT_DATE - 7;  -- Partition filter

-- Add index
CREATE INDEX idx_events_user_id ON events(user_id);
```

#### Issue: Queries scan 100GB but return 1MB
**Symptoms:** High BigQuery on-demand costs, slow queries
**Root Cause:** No partition filters, inefficient query structure
**Solution:**
```sql
-- Bad: Scans all partitions
SELECT COUNT(*) FROM events WHERE event_name = 'purchase';

-- Good: Partition pruning
SELECT COUNT(*) FROM events
WHERE event_date BETWEEN '2024-01-01' AND '2024-01-31'
  AND event_name = 'purchase';

-- Use clustering for common filters
CREATE TABLE events
PARTITION BY DATE(event_date)
CLUSTER BY user_id, event_name;
```

#### Issue: Aggregation spills to disk
**Symptoms:** 3x slower than expected, I/O bottleneck
**Root Cause:** Insufficient memory, large GROUP BY cardinality
**Solution:**
```sql
-- Bad: High-cardinality GROUP BY
SELECT user_id, COUNT(*) FROM events GROUP BY user_id;

-- Good: Pre-aggregate in stages
WITH daily_rollup AS (
  SELECT DATE(event_date) as day, user_id, COUNT(*) as cnt
  FROM events
  WHERE event_date >= CURRENT_DATE - 30
  GROUP BY 1, 2
)
SELECT user_id, SUM(cnt) FROM daily_rollup GROUP BY user_id;
```

### Cost Optimization

#### Issue: Warehouse costs doubled this quarter
**Symptoms:** Budget alerts, no clear driver
**Root Cause:** No cost attribution, abandoned workloads running
**Solution:**
```sql
-- BigQuery: Identify top cost queries
SELECT
  user_email,
  query,
  total_bytes_processed / POW(10, 12) as TB_processed,
  total_bytes_processed / POW(10, 12) * 5 as estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_processed DESC
LIMIT 20;

-- Snowflake: Identify expensive warehouses
SELECT
  warehouse_name,
  SUM(credits_used) as total_credits,
  SUM(credits_used) * 3 as estimated_cost_usd  -- Adjust for your rate
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(day, -30, CURRENT_TIMESTAMP())
GROUP BY warehouse_name
ORDER BY total_credits DESC;
```

#### Issue: 40% of storage is rarely accessed
**Symptoms:** High storage costs for old data
**Root Cause:** No lifecycle policy, everything on hot tier
**Solution:**
```python
# AWS S3 Lifecycle Policy
{
  "Rules": [{
    "Id": "Move old data to cold storage",
    "Status": "Enabled",
    "Transitions": [
      {"Days": 90, "StorageClass": "STANDARD_IA"},
      {"Days": 365, "StorageClass": "GLACIER"}
    ]
  }]
}

# BigQuery: Set table expiration
ALTER TABLE dataset.old_events
SET OPTIONS (expiration_timestamp=TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 365 DAY));
```

### Security & Compliance

#### Issue: PII not encrypted at rest
**Symptoms:** Compliance violation, audit finding
**Root Cause:** Default settings, no encryption configured
**Solution:**
```sql
-- Snowflake: Enable encryption (automatic for most clouds)
CREATE TABLE users (
  user_id NUMBER,
  email VARCHAR ENCRYPT USING 'SNOWFLAKE_SSE'  -- Server-side encryption
);

-- BigQuery: Enable CMEK
bq mk --table \
  --encryption_kms_key=projects/my-project/locations/us/keyRings/my-ring/cryptoKeys/my-key \
  my_dataset.users
```

#### Issue: Production data copied to staging without masking
**Symptoms:** Developers have access to real PII
**Root Cause:** No data masking pipeline
**Solution:**
```python
# dbt macro for email masking
{% macro mask_email(column_name) %}
  CONCAT(
    LEFT({{ column_name }}, 3),
    '***@',
    SPLIT_PART({{ column_name }}, '@', 2)
  )
{% endmacro %}

# Use in staging model
SELECT
  user_id,
  {{ mask_email('email') }} as email,
  {{ mask_phone('phone') }} as phone
FROM {{ source('prod', 'users') }}
```

#### Issue: No audit trail for data access
**Symptoms:** Cannot answer "who accessed this table?"
**Root Cause:** Audit logging not enabled
**Solution:**
```sql
-- BigQuery: Query audit logs
SELECT
  principal_email,
  resource.labels.table_id,
  timestamp
FROM `my-project.region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE statement_type = 'SELECT'
  AND DATE(creation_time) = CURRENT_DATE()
ORDER BY timestamp DESC;

-- Snowflake: Enable query logging
ALTER ACCOUNT SET QUERY_LOG = TRUE;

SELECT
  user_name,
  query_text,
  start_time
FROM snowflake.account_usage.query_history
WHERE query_type = 'SELECT'
  AND start_time >= DATEADD(day, -1, CURRENT_TIMESTAMP())
ORDER BY start_time DESC;
```

---

## Platform-Specific Guides

### dbt (Data Build Tool)

**Quick Wins:**
- Add `dbt test` to CI/CD (blocks merge if tests fail)
- Use `dbt-utils.recency` to catch stale data
- Enable `dbt docs generate` for auto-documentation

**Performance:**
- Use incremental models for large tables: `{{ config(materialized='incremental') }}`
- Add partition filters to incremental logic
- Use `dbt-utils.star()` instead of `SELECT *`

**Quality:**
```yaml
models:
  - name: fact_orders
    meta:
      owner: data-team@company.com
      contains_pii: true
    tests:
      - dbt_utils.equal_rowcount:
          compare_model: ref('staging_orders')
    columns:
      - name: user_id
        tests:
          - not_null
          - relationships:
              to: ref('users')
              field: id
```

### Apache Airflow

**Quick Wins:**
- Add `retries=3` to all tasks
- Use `depends_on_past=False` unless explicitly needed
- Set `sla=timedelta(hours=X)` for monitoring

**Reliability:**
```python
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'sla': timedelta(hours=2),
    'on_failure_callback': send_alert,
}

# Use sensors for upstream dependencies
wait_for_upstream = ExternalTaskSensor(
    task_id='wait_for_upstream',
    external_dag_id='upstream_dag',
    external_task_id='final_task',
    timeout=3600,
)
```

**Monitoring:**
- Install airflow-exporter for Prometheus metrics
- Use `airflow dags test` for local validation
- Enable `dag_run_timeout` to catch stuck DAGs

### BigQuery

**Quick Wins:**
- Add `WHERE _PARTITIONTIME` filters to all queries
- Use `APPROX_COUNT_DISTINCT` instead of `COUNT(DISTINCT ...)`
- Enable BI Engine for dashboard queries

**Performance:**
```sql
-- Partitioning
CREATE TABLE events
PARTITION BY DATE(event_date)
CLUSTER BY user_id, event_name
AS SELECT ...;

-- Cost control
CREATE TABLE expensive_aggregation
OPTIONS(
  expiration_timestamp=TIMESTAMP_ADD(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
)
AS SELECT ...;

-- Query optimization
SELECT  -- Explicit columns, not SELECT *
  user_id,
  COUNT(*) as event_count
FROM events
WHERE DATE(event_date) BETWEEN '2024-01-01' AND '2024-01-31'  -- Partition filter
  AND event_name = 'purchase'  -- Clustering column
GROUP BY user_id;
```

### Snowflake

**Quick Wins:**
- Use `AUTO_SUSPEND = 60` on warehouses
- Enable `AUTO_RESUME = TRUE`
- Use `COPY INTO` for bulk loads (not INSERT)

**Performance:**
```sql
-- Clustering
CREATE TABLE orders
CLUSTER BY (order_date, customer_id);

-- Materialized views for common aggregations
CREATE MATERIALIZED VIEW daily_revenue AS
SELECT DATE(order_date) as day, SUM(revenue) as total
FROM orders
GROUP BY 1;

-- Result caching (automatic, but use same query text)
-- Cache valid for 24 hours or until underlying data changes

-- Cost monitoring
SELECT
  warehouse_name,
  SUM(credits_used) as credits,
  SUM(credits_used) * 3 as est_cost_usd
FROM snowflake.account_usage.warehouse_metering_history
WHERE start_time >= DATEADD(month, -1, CURRENT_TIMESTAMP())
GROUP BY 1
ORDER BY 2 DESC;
```

### Databricks

**Quick Wins:**
- Use Delta Lake for ACID transactions
- Enable auto-optimize: `spark.databricks.delta.autoOptimize.optimizeWrite = true`
- Use Photon for faster queries

**Performance:**
```python
# Delta Lake optimization
spark.sql("""
  OPTIMIZE delta.`/path/to/table`
  ZORDER BY (user_id, event_date)
""")

# Auto-optimize on write
spark.conf.set("spark.databricks.delta.autoOptimize.optimizeWrite", "true")
spark.conf.set("spark.databricks.delta.autoOptimize.autoCompact", "true")

# Partition pruning
df = spark.read.format("delta").load("/path/to/table")
df.filter("event_date >= '2024-01-01'").count()  # Uses partition pruning
```

---

## Health Metrics

### Pipeline Health
- **Success Rate**: >99% (weekly)
- **Mean Time to Recovery (MTTR)**: <1 hour
- **Data Freshness**: Within SLA (typically <1 hour)
- **Test Coverage**: >80% of models have tests
- **Incident Frequency**: <2 per month

### Performance Health
- **Dashboard p95 Latency**: <5 seconds
- **Batch Pipeline Runtime**: Within 2x of baseline
- **Query Cost**: <$X per TB scanned (set based on budget)
- **Cache Hit Rate**: >50% for BI queries
- **Resource Utilization**: 60-80% during peak

### Security Health
- **Access Reviews**: Quarterly
- **Orphaned Account TTL**: <30 days
- **PII Encryption**: 100% of identified columns
- **Audit Log Retention**: Meets compliance (GDPR: 3 years)
- **DSAR Completion Time**: <30 days (GDPR requirement)

### Cost Health
- **Month-over-Month Growth**: <20% without business justification
- **Cost per Query**: Trending down or stable
- **Unused Resources**: <10% of total spend
- **Reserved Capacity Utilization**: >80%

---

## Report Template

Use this template for the final synthesized report:

```markdown
# Data Platform Health Report

**Date**: YYYY-MM-DD
**Reviewed By**: [Agent Team]
**Platform**: [Description]

## Executive Summary

[3-5 sentences: overall health, critical issues, major opportunities, recommended next steps]

## Overall Health Score: X.X / 5.0

| Domain | Score | Status | Priority |
|--------|-------|--------|----------|
| Infrastructure & Reliability | X/5 | 🟢 🟡 🔴 | Critical/High/Medium/Low |
| Data Quality & Analytics | X/5 | 🟢 🟡 🔴 | Critical/High/Medium/Low |
| Performance & Cost | X/5 | 🟢 🟡 🔴 | Critical/High/Medium/Low |
| Security & Governance | X/5 | 🟢 🟡 🔴 | Critical/High/Medium/Low |

**Legend**: 🟢 Good (4-5) | 🟡 Needs Attention (3) | 🔴 Critical (1-2)

## Critical Issues (Fix Immediately)

1. **[Issue Title]** (Impact: [business/technical])
   - **Current State**: [description]
   - **Risk**: [what happens if not fixed]
   - **Fix**: [specific solution]
   - **Effort**: [S/M/L] | **Timeline**: [days/weeks]

[Repeat for each critical issue]

## High Priority Recommendations (This Sprint)

1. **[Recommendation Title]** (Impact: [cost savings/performance gain/risk reduction])
   - **Rationale**: [why this matters]
   - **Implementation**: [how to do it]
   - **Effort**: [S/M/L] | **Timeline**: [days/weeks]

[Repeat for each high-priority item]

## Medium Priority (Next Quarter)

- [List of recommendations with brief description]

## Low Priority / Nice-to-Have

- [List of nice-to-have improvements]

## Domain Deep Dives

### Infrastructure & Reliability (X/5)

**Summary**: [paragraph on overall state]

**Strengths**:
- [What's working well]

**Gaps**:
- [What needs improvement]

**Key Findings**:
1. [Finding with file:line reference and fix]

[Repeat for: Data Quality, Performance, Security]

## Architecture Trade-Offs

[Summary of agent debate on conflicting recommendations]

**Example**:
- **Performance vs. Cost**: Materialized views improve dashboard latency by 10x but add $500/month in storage
  - **Recommendation**: Implement for top 5 dashboards only, measure ROI

## Cost Breakdown & Optimization

| Category | Current/Month | Waste | Optimized | Savings |
|----------|---------------|-------|-----------|---------|
| Compute | $X,XXX | $X | $X,XXX | X% |
| Storage | $X,XXX | $X | $X,XXX | X% |
| **Total** | **$X,XXX** | **$X** | **$X,XXX** | **X%** |

**Quick Wins**: [Top 3 cost optimizations with minimal effort]

## Compliance & Security Status

| Requirement | Status | Gap | Timeline |
|-------------|--------|-----|----------|
| GDPR Art. 32 (Encryption) | ❌ | PII not encrypted | 2 weeks |
| GDPR Art. 15 (DSAR) | ⚠️ | No workflow | 1 month |
| SOC2 CC6.1 (Access Control) | ✅ | Compliant | N/A |

## Success Metrics (30/60/90 Days)

**30 Days**:
- [ ] Critical issues resolved
- [ ] Monitoring and alerting in place
- [ ] PII encryption enabled

**60 Days**:
- [ ] High-priority optimizations complete
- [ ] Cost savings realized (target: X%)
- [ ] Compliance gaps closed

**90 Days**:
- [ ] Pipeline success rate >99%
- [ ] Dashboard latency <5s p95
- [ ] Security posture score >4/5

## Appendices

### A. Detailed Findings by Agent
[Links to individual agent reports]

### B. Platform Inventory
[From discovery phase]

### C. Debate Transcript
[Architecture trade-off discussions]

### D. References
[Links to documentation, best practices, compliance frameworks]
```

---

## Usage Guidelines

### For Agents

1. **Load this reference** at the start of your audit
2. **Use the checklist** for your domain to ensure comprehensive coverage
3. **Apply the scoring rubric** consistently (1-5 scale)
4. **Reference common issues** to provide specific, actionable fixes
5. **Cite file:line numbers** for all findings
6. **Quantify impact** (cost, latency, risk) wherever possible

### For Coordinators

1. **Share discovery.md** with all agents
2. **Provide this REFERENCE.md** to all agents
3. **Collect individual reports** and identify overlaps/conflicts
4. **Facilitate debate** on architecture trade-offs
5. **Use report template** for final synthesis
6. **Present actionable recommendations** prioritized by impact/effort

### For Users

1. **Focus on critical findings** first (score ≤ 2)
2. **Prioritize by business impact**, not technical complexity
3. **Start with quick wins** to build momentum
4. **Set realistic timelines** based on team size
5. **Re-run review quarterly** to track progress

---

## Best Practices

### Writing Findings

**Good**:
```
❌ CRITICAL: PII columns (email, phone) not encrypted in users table (schema.sql:15)
   Impact: Violates GDPR Art. 32, potential €20M fine, high breach risk
   Fix: Enable column-level encryption (ALTER TABLE users ENCRYPT COLUMN email, phone)
   Effort: Small (1 day) | Cost: Negligible | Risk: Low (backward compatible)
```

**Bad**:
```
⚠️  Security issue: some data not protected properly
   Fix: add encryption
```

### Prioritization Framework

**Critical** = High impact × High urgency × High risk
- Compliance violations
- Production outages
- Data loss risks
- Security breaches

**High** = High impact × Medium urgency
- Performance degradation
- Cost inefficiencies >20%
- Quality issues affecting users
- Moderate security gaps

**Medium** = Medium impact × Low urgency
- Technical debt
- Missing documentation
- Monitoring gaps
- Process improvements

**Low** = Low impact (nice-to-have)
- Code style
- Minor optimizations
- Future-proofing
- Tooling upgrades

### Small Team Optimizations

For 2-5 person data teams, prioritize:
1. **Automation over manual processes** (highest ROI)
2. **Monitoring over after-the-fact debugging**
3. **Idempotency over complex error handling**
4. **Managed services over self-hosted** (dbt Cloud > Airflow)
5. **Simple solutions over perfect architectures**
6. **Incremental improvements over big rewrites**

---

**End of Reference**
