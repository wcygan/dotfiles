---
title: MySQL EXPLAIN and EXPLAIN ANALYZE
---

# MySQL EXPLAIN and EXPLAIN ANALYZE

Use `EXPLAIN` to inspect the optimizer plan. Use `EXPLAIN ANALYZE` to execute the statement and compare estimated vs actual behavior.

## Key facts

- `EXPLAIN ANALYZE` was introduced in MySQL 8.0.18 and runs the statement, producing iterator timing and row counts. It always uses the `TREE` output format.
- `EXPLAIN ANALYZE` can be used with `SELECT`, multi-table `UPDATE` and `DELETE`, and (since 8.0.19) `TABLE` statements.

## Minimal usage

```sql
EXPLAIN SELECT ...;
EXPLAIN FORMAT=TREE SELECT ...;
EXPLAIN ANALYZE SELECT ...;
```

## Reading the output

- Compare estimated rows/cost vs actual rows/time from `EXPLAIN ANALYZE` to spot cardinality or selectivity issues.
