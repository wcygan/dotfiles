# TiDB Query Tuning: Investigation & Reproduction

Once clues are collected, use these methods to investigate the root cause and attempt reproduction.

## 1. Plan Analysis (`estRows` vs `actRows`)
Run `EXPLAIN ANALYZE` on the query.

```sql
EXPLAIN ANALYZE SELECT ...;
```
Look at these columns:
- **estRows**: The number of rows the optimizer *thinks* it will process.
- **actRows**: The number of rows actually processed.
- **Large Difference?** If `estRows` is 100 but `actRows` is 1,000,000, the optimizer will likely choose a bad join order or access path. **Solution**: Run `ANALYZE TABLE <table_name>;` (or with `ALL COLUMNS` if `@@tidb_analyze_column_options` is not `ALL`).

## 2. Check Version-Specific Known Issues
Known performance issues often exist in older versions.
- **Check TiDB version**: `SELECT tidb_version();`
- **Release Notes Search**: Look for "Performance" or "Fixes" in the TiDB [Release Notes](https://docs.pingcap.com/tidb/stable/release-notes).
- **Common version-related bugs**:
  - Partitioned table performance (v5.x vs v6.x vs v7.x).
  - Optimizer rule bugs for `IndexJoin` or `MPP` mode in early 6.x releases.
  - Resource control overhead in 7.x.

## 3. Reproduction Steps
- **Use `EXPLAIN` with plan reuse**: `EXPLAIN FOR CONNECTION <conn_id>;` if the query is currently running.
- **Duplicate Schema & Sample Data**:
  1. Export schema: `SHOW CREATE TABLE`.
  2. Sample data or use `SELECT * INTO OUTFILE` (if permitted).
  3. Load into a test cluster and check the plan.
- **Check System State**:
  - Check `SHOW PROCESSLIST` to see if the query is blocked by MDL (Metadata Lock) or GC (Garbage Collection).
  - Use `information_schema.tidb_hot_regions` to check if a single TiKV node is handling all the load (write/read hotspot).

## 4. Diagnostic Checklist
- [ ] Are stats healthy? (`SHOW STATS_HEALTHY`)
- [ ] Is the plan using the expected index?
- [ ] Is TiFlash being used for analytical queries? (`READ_FROM_STORAGE(TIFLASH[t])`)
- [ ] Is the bottleneck in `cop` tasks (TiKV) or the `root` task (TiDB)?
- [ ] Are there concurrent `ADD INDEX` or `ANALYZE` jobs? (`SHOW DDL JOBS`, `SHOW ANALYZE STATUS`)
