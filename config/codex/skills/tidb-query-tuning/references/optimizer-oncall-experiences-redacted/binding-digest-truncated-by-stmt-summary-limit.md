# Binding Digest Truncated by Statement Summary Limit

## User Symptom
- A binding exists but does not take effect for a long SQL statement.

## Investigation Signals
- `tidb_stmt_summary_max_sql_length` is too small.
- The SQL text used for digest calculation is truncated, so the binding digest no longer matches the real statement shape.

## Workaround
- Increase `tidb_stmt_summary_max_sql_length`.
- Keep `tidb_use_plan_baseline` enabled while checking whether the binding itself is valid.
- Re-verify the digest after the length limit is raised.

## Fixed Version
- No product fix was recorded. This is a configuration-side pitfall.
