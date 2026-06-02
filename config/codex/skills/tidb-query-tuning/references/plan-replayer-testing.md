# TiDB Query Tuning: Plan Replayer Testing

This guide describes how to use `PLAN REPLAYER` to reproduce and test query plans locally. This is a critical step before recommending upgrades or reporting bugs.

## 1. Local Environment Setup
Use `tiup playground` to spin up a local TiDB cluster that matches the user's environment.

```bash
# Match the user's version
tiup playground v{version} --db 1 --pd 1 --kv 1 --tiflash 0
```

## 2. Loading the Reproduction Package
Once the playground is running, use the `PLAN REPLAYER LOAD` command to restore the schema, statistics, and session variables.

```sql
-- Connect to the local TiDB (usually port 4000)
-- Ensure --local-infile=true is used if loading via mysql client
PLAN REPLAYER LOAD 'path/to/replayer.zip';
```

## 3. Verification & Testing Checkpoints
To ensure a high-quality reproduction, verify these specific checkpoints after loading the ZIP:

1.  **Deterministic Environment**:
    - **Check Timestamp**: Extract the `timestamp` from `variables.toml` inside the ZIP. If the query uses time-sensitive functions (e.g., `NOW()`, `CURRENT_DATE()`), set the session timestamp to match: `SET @@timestamp = <extracted_value>;`.
2.  **TiFlash Replica Readiness**:
    - Check if `table_tiflash_replica.txt` exists in the ZIP. If it does, ensure the local playground has TiFlash enabled and wait for replicas to be ready: `SELECT * FROM information_schema.tiflash_replica;`.
3.  **Plan Consistency**:
    - Run `EXPLAIN FORMAT='plan_tree' <sql>;` or `EXPLAIN <sql>;`.
    - **Checkpoint**: Does the plan match the user's `plan.txt`? If not, check if `tidb_cost_model_version` or other session variables in `variables.toml` were applied correctly.
4.  **SQL Binding Verification**:
    - Check if the loaded plan uses a binding: `SELECT @@last_plan_from_binding;`.
    - **Checkpoint**: If a binding is active, run the query once with it, then delete/disable the binding and run again to see the "raw" optimizer choice.
    - **Disable Binding**: `UPDATE mysql.bind_info SET status = 'deleted' WHERE source != 'builtin'; ADMIN RELOAD BINDINGS;`.
5.  **Alloc Analysis**:
    - For performance issues, check `@@last_sql_use_alloc` to see if memory allocation is a bottleneck.
6.  **Check Statistics**: If the plan is bad due to `estRows` mismatch, verify if the statistics in the ZIP are consistent with the user's environment. (Note: `ANALYZE TABLE` is typically not needed if the replayer ZIP is fresh).

## 4. Cross-Version Testing (Bug vs Enhancement)
If the plan remains suboptimal even after tuning/analyzing:

1.  **Test Newer Stable Version**: Restart playground with the latest stable version.
2.  **Test Nightly Version**:
    - `tiup playground nightly`
    - **Note on updating nightly**: `rm -rf ~/.tiup/components/tidb/v*nightly*` to clear cache.
3.  **Search for Known Issues**: Search [TiDB GitHub Issues](https://github.com/pingcap/tidb/issues) using operator names or plan signatures.
4.  **Determine Bug vs Enhancement**:
    - **Bug**: Objectively wrong plan or execution error.
    - **Enhancement**: Missing feature or optimizer limitation.

## 5. Deep Code Analysis (Advanced)
If local reproduction via `TiUP` is insufficient to pinpoint the issue:

1.  **Clone the Source**: `git clone https://github.com/pingcap/tidb.git`
2.  **Review On-site Agents**: Read `AGENTS.md` and `.agents/skills` in the TiDB repository first.
3.  **Trace the Optimizer**: Trace the implementation of specific operators (e.g., `IndexJoin`) or rules (e.g., `PredicatePushDown`).
