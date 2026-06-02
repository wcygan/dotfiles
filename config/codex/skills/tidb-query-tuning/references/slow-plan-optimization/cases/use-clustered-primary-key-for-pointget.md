# Case: Use Clustered Primary Key to Reduce PointGet or BatchPointGet RPC

## Symptom

- Query plan shows `Point_Get` or `Batch_Point_Get`, but latency is still higher than expected.
- `EXPLAIN ANALYZE` shows `Get:{num_rpc:2,...}` for primary-key lookup.

## Required Inputs

- Original SQL.
- `EXPLAIN ANALYZE` output.
- Related table schema (`SHOW CREATE TABLE`), especially whether the primary key is `CLUSTERED` or `NONCLUSTERED`.

## Plan Signature

- Bottleneck operator is `Point_Get` or `Batch_Point_Get`.
- Access object looks like `table:..., index:PRIMARY(...)` on a non-clustered primary-key table.
- Runtime shows double-read behavior (`Get:{num_rpc:2,...}`), indicating one read for primary-key index lookup and one read for table row fetch.

## Diagnosis

- This is usually a schema layout issue rather than a bad operator choice.
- For non-clustered primary-key tables, point lookup by primary key may require 2 RPCs.
- For clustered primary-key tables, the same lookup can be completed in 1 RPC.
- The same principle applies to both `PointGet` and `BatchPointGet`.

## Suggestions (Strict Order)

1. Binding or hints first.
   - Usually not effective for reducing this specific `PointGet`/`BatchPointGet` double-read pattern when the root cause is non-clustered storage layout.
2. Add new index.
   - Usually not the right fix for this pattern.
3. Rewrite query or schema.
   - If workload is dominated by primary-key point lookups, prefer clustered primary key table design.
   - For existing non-clustered tables, consider schema migration (rebuild into a clustered primary-key table) when benefit justifies migration cost.

## Example

```sql
create table t_non_clustered (a int, b int, c int, primary key(a) nonclustered);
create table t_clustered (a int, b int, c int, primary key(a) clustered);
insert into t_non_clustered values (1, 1, 1);
insert into t_clustered values (1, 1, 1);
```

```sql
mysql> explain analyze select * from t_non_clustered where a=1;
+-------------+---------+---------+------+-----------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object                           | execution info                                                                                                                                                                                                                                                                                                                                                                                                                        | operator info | memory | disk |
+-------------+---------+---------+------+-----------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t_non_clustered, index:PRIMARY(a) | time:347.3µs, open:792ns, close:3.79µs, loops:2, RU:0.96, Get:{num_rpc:2, total_time:312.4µs}, time_detail: {total_process_time: 34.9µs, total_wait_time: 55.1µs, total_kv_read_wall_time: 95.6µs, tikv_grpc_process_time: 3.96µs, tikv_grpc_wait_time: 26.5µs, tikv_wall_time: 130.8µs}, scan_detail: {total_process_keys: 2, total_process_keys_size: 89, total_keys: 2, get_snapshot_time: 28.4µs, rocksdb: {block: {}}}           |               | N/A    | N/A  |
+-------------+---------+---------+------+-----------------------------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
```

```sql
mysql> explain analyze select * from t_clustered where a=1;
+-------------+---------+---------+------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
| id          | estRows | actRows | task | access object     | execution info                                                                                                                                                                                                                                                                                                                                                                                                                   | operator info | memory | disk |
+-------------+---------+---------+------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
| Point_Get_1 | 1.00    | 1       | root | table:t_clustered | time:187µs, open:625ns, close:5.96µs, loops:2, RU:0.48, Get:{num_rpc:1, total_time:168.3µs}, time_detail: {total_process_time: 14.8µs, total_wait_time: 36.8µs, total_kv_read_wall_time: 53.7µs, tikv_grpc_process_time: 1.96µs, tikv_grpc_wait_time: 8.79µs, tikv_wall_time: 64.2µs}, scan_detail: {total_process_keys: 1, total_process_keys_size: 41, total_keys: 1, get_snapshot_time: 12µs, rocksdb: {block: {}}}           | handle:1      | N/A    | N/A  |
+-------------+---------+---------+------+-------------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+---------------+--------+------+
```

## Verification

- Re-run `EXPLAIN ANALYZE`.
- Confirm `Get:{num_rpc:...}` decreases (for example, from `2` to `1`).
- Confirm total latency and RU for `Point_Get`/`Batch_Point_Get` improve.
