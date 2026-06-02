---
name: "Bug Report Template & Workflow"
description: Standard template and deterministic workflow for reporting TiDB bugs identified during query tuning.
---

# Bug Reporting Workflow

Follow these steps to produce a high-quality bug report:

1. **Information Synthesis**:
   - Collect the problematic SQL and the expected vs. actual behavior (execution plan or result).
   - Gather execution metadata (Query_time, Mem_max, etc.) from `INFORMATION_SCHEMA.SLOW_QUERY`.
   - Identify the TiDB version and any relevant session variables.

2. **Minimal Reproduction & Anonymization**:
   - **MANDATORY**: Anonymize all sensitive information (table names, column names, data values) unless the user explicitly consents to sharing raw logs.
   - Use `SHOW CREATE TABLE` and reduce it to the minimal set of columns and indexes required to trigger the issue.
   - Provide a self-contained SQL script that includes `CREATE TABLE`, `INSERT` (if data-dependent), and the `SELECT` query.

3. **Root-Cause Analysis**:
   - Perform a concise analysis (1–3 likely causes).
   - Provide evidence from `EXPLAIN ANALYZE` (e.g., plan signature differences, `estRows` vs `actRows` mismatches).

4. **Fill Template**: Use the template below to format the GitHub issue.

---

## Bug Report Template

### 1. Minimal reproduce step (Required)

<!-- 
A step-by-step guide for reproducing the bug. 
If a PLAN REPLAYER ZIP is available (and anonymized/authorized), mention it here.
Include the minimal, anonymized SQL script.
-->

### 2. What did you expect to see? (Required)

<!-- Description of the correct plan or correct result -->

### 3. What did you see instead (Required)

<!-- Description of the suboptimal plan or the error message -->

### 4. What is your TiDB version? (Required)

<!-- Paste the output of SELECT tidb_version() -->

---

## Analysis (Internal/Diagnostic)

<!-- 
1-3 likely causes based on the local reproduction.
Evidence from SQL or plan signature differences.
-->

## Labeling Guidelines

When filing the issue on GitHub, use the following labels:

- **Type**: `type/bug`
- **Sig**: `sig/planner` (for most tuning issues) or `sig/executor`
- **Severity**:
  - `severity/major`: Wrong-result bugs or queries that fail to execute (internal error).
  - `severity/moderate`: Planner/performance issues that are not confirmed wrong-result and not execution-blocking.
