# Binding Cache Quota Blocks Baselines

## User Symptom
- A binding exists, but the query sometimes behaves as if the binding does not exist.
- Regressed plans appear after upgrade or restart even though the expected bindings were already created.

## Investigation Signals
- Search TiDB logs for `category=sql-bind`.
- A representative log pattern is the error saying available bindings exceed `tidb_mem_quota_binding_cache`.
- Binding load is not synchronous like stats load. A manual reload may still be required.

## Workaround
- Increase `tidb_mem_quota_binding_cache`.
- Run `ADMIN RELOAD BINDINGS` after increasing the quota.
- Treat binding reload as a separate recovery step after restart or migration.

## Fixed Version
- No product fix was recorded in the handbook.
