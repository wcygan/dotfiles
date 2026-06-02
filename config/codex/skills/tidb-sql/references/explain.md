---
title: TiDB EXPLAIN and EXPLAIN ANALYZE (Troubleshooting)
---

# TiDB EXPLAIN and EXPLAIN ANALYZE (Troubleshooting)

Use `EXPLAIN` to see the plan without executing the query, and `EXPLAIN ANALYZE` to execute it and capture runtime stats.

## Quick rules

- If `EXPLAIN` looks "obviously wrong", run `ANALYZE TABLE <table>` on involved tables and re-check.
- Prefer `EXPLAIN FORMAT = "tidb_json"` when you need to programmatically inspect the operator tree.
- Prefer `EXPLAIN FORMAT = "dot"` when you need a visual operator graph (Graphviz).
- `EXPLAIN ANALYZE` executes the statement. Use carefully on production / heavy queries.
- TiDB does not support MySQL `FORMAT=JSON` or `FORMAT=TREE`. Use `FORMAT="tidb_json"` instead.

## Default EXPLAIN columns (row format)

TiDB `EXPLAIN` outputs these columns by default: `id`, `estRows`, `task`, `access object`, `operator info`.

## Structured plan: FORMAT = "tidb_json"

```sql
EXPLAIN FORMAT = "tidb_json"
SELECT /* your query */ 1;
```

The output is a JSON array. Each object can include:

- `id`, `estRows`, `taskType`, `accessObject`, `operatorInfo`
- `subOperators`: array of child operators (tree structure)

Tip: If a field is missing, it is empty.

## Visual plan: FORMAT = "dot" (Graphviz)

```sql
EXPLAIN FORMAT = "dot"
SELECT /* your query */ 1;
```

This returns a DOT graph string (starting with `digraph ... {`).

### Render DOT to an image (optional)

If `dot` (Graphviz) is installed locally:

```bash
dot plan.dot -T png -O
```

If you want a helper script, see `scripts/render_dot_png.sh`.

## EXPLAIN ANALYZE

```sql
EXPLAIN ANALYZE
SELECT /* your query */ 1;
```

Compared to `EXPLAIN`, `EXPLAIN ANALYZE` adds runtime columns such as:

- `actRows`
- `execution info` (time, loops, etc.)
- `memory`, `disk`

Use it to compare `estRows` vs `actRows`. Large gaps usually indicate stale or missing statistics, skewed data, or predicates the optimizer cannot estimate well.

Note: When you use `EXPLAIN ANALYZE` to execute DML statements, the data modifications are normally executed, and the execution plan for DML statements cannot be shown yet.

## EXPLAIN FOR CONNECTION (advanced)

TiDB supports:

```sql
EXPLAIN FOR CONNECTION <connection_id>;
```

Privilege note: in TiDB, to explain another connection you typically need `SUPER` (or be the same user/session).
