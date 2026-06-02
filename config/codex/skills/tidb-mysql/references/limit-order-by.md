---
title: LIMIT and ORDER BY Optimization
---

# LIMIT and ORDER BY Optimization

Use `LIMIT` with a deterministic `ORDER BY` to control result size and order. Make sure the `ORDER BY` can use an index to avoid extra sorting.

## LIMIT basics

- `LIMIT` can restrict result size so the server does not need to return all rows.
- If `ORDER BY` is used with `LIMIT`, the server must order rows before applying the limit.

## ORDER BY optimization

- MySQL can use an index to satisfy `ORDER BY` and avoid a separate sort when the ordering matches the index.
- If the order cannot be satisfied by an index, MySQL performs a filesort.
- `EXPLAIN` shows `Using filesort` in `Extra` when a filesort is required.

## Deterministic ordering

- Without a deterministic `ORDER BY`, the order of rows is not guaranteed.
- When ordering by non-unique columns, include a unique tie-breaker column to keep pagination stable.
