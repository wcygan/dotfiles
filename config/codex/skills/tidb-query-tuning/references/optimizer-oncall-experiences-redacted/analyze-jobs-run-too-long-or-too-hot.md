# Analyze Jobs Run Too Long or Too Hot

## User Symptom
- Auto analyze keeps timing out, gets killed, or causes visible CPU pressure on TiDB or TiKV.
- Partitioned tables and very large tables are especially problematic.

## Investigation Signals
- Analyze stacks show lock-heavy functions such as `mergeglobaltopn` or `queryLockedTables`.
- Large partition counts or many concurrent analyze jobs amplify the problem.
- Some tables have not completed a successful analyze for a very long time.
- TiKV CPU is already high before any attempt to raise scan concurrency.

## Workaround
- Reduce analyze concurrency, especially for partitioned tables.
- Lower sample rate for the specific table if the business can tolerate it.
- Increase `tidb_max_auto_analyze_time` only when the job is fundamentally correct but too large for the current limit.
- Be careful with `tidb_sysproc_scan_concurrency`; it can worsen hot TiKV nodes.

## Fixed Version
- Some sub-cases were improved in later releases such as `v7.5`, but this remains a mixed operational and product area rather than one single bug.
