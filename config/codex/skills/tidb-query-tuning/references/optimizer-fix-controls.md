# Optimizer Fix Controls

TiDB provides a fine-grained compatibility control mechanism for the optimizer through the `tidb_opt_fix_control` system variable. Each fix control corresponds to a specific GitHub issue and adjusts a particular optimizer behavior. This feature was introduced to solve three problems: avoiding variable proliferation, handling behavioral incompatibility across scenarios, and maintaining plan stability during upgrades.

Fix controls let you selectively enable or disable specific optimizer behavior changes — especially useful when an upgrade introduces a regression for a particular workload.

## How fix controls work

- Each fix control is identified by a **GitHub issue number** (e.g., `44262` → [github.com/pingcap/tidb/issues/44262](https://github.com/pingcap/tidb/issues/44262)).
- The value is either a **boolean** (`ON`/`OFF`) or an **integer**, depending on the fix.
- Multiple fix controls are set as a single comma-separated string.
- When a fix control is set to its default value, TiDB behaves as if it were not specified.
- Duplicate fix control numbers in the same string produce a warning; only the last value takes effect.

## Setting fix controls

Fix controls can be set at three scopes:

### Global (all new connections)

```sql
SET GLOBAL tidb_opt_fix_control = '44262:ON,44855:ON';
```

Use for cluster-wide tuning when a behavior change should apply to all sessions.

### Session (current connection only)

```sql
SET SESSION tidb_opt_fix_control = '44262:ON,52869:ON';
```

Use when testing a fix control or applying it to a specific workload.

### Per-query via SET_VAR hint

```sql
SELECT /*+ SET_VAR(tidb_opt_fix_control='52869:ON') */ *
FROM orders o JOIN customers c ON o.cust_id = c.id;
```

Use for surgical, per-query tuning — the most precise approach. The variable is set only for the duration of that single statement.

> **Note:** There was a historical bug (Issue #50507, fixed in v7.5+) where `SET_VAR(tidb_opt_fix_control=...)` was incompatible with SQL bindings. This has been resolved.

## Complete fix control catalog

### Plan cache controls

| Fix | Default | Values | Since | Purpose |
|-----|---------|--------|-------|---------|
| `33031` | `OFF` | `ON`, `OFF` | v8.0.0+ | Controls whether plan cache is allowed for partitioned tables (both prepared and non-prepared statement caching) |
| `44823` | `200` | `[0, 2147483647]` | v7.3.0+ | Sets the parameter count limit for plan cache to save memory. `0` removes the limit entirely |
| `44830` | `OFF` | `ON`, `OFF` | v6.5.7, v7.3.0+ | Controls whether plan cache caches execution plans with `PointGet` operators generated from `_tidb_rowid` |
| `45798` | `ON` | `ON`, `OFF` | v7.5.0+ | Controls whether plan cache caches plans that access generated columns |

### Partition and statistics controls

| Fix | Default | Values | Since | Purpose |
|-----|---------|--------|-------|---------|
| `44262` | `OFF` | `ON`, `OFF` | v6.5.3, v7.2.0+ | Controls whether dynamic pruning mode can access partitioned tables when GlobalStats are missing. When `ON`, the optimizer falls back to dynamic pruning even without global statistics |

### Index and scan path controls

| Fix | Default | Values | Since | Purpose |
|-----|---------|--------|-------|---------|
| `44389` | `OFF` | `ON`, `OFF` | v6.5.3, v7.2.0+ | Controls whether to build more comprehensive scan ranges for `IndexRangeScan` with complex OR filters. Can improve plans for queries with `OR`-connected conditions on indexed columns |
| `45132` | `1000` | `[0, 2147483647]` | v7.4.0+ | Sets the heuristic threshold for access path selection. When candidate access paths exceed this threshold, a heuristic strategy prunes less promising paths. `0` disables the heuristic |
| `52592` | `OFF` | `ON`, `OFF` | v8.4.0+ | Disables `Point Get` and `Batch Point Get` operators, forcing the Coprocessor path. Useful for wide tables or tables with large JSON values where Point Get causes excessive memory usage |
| `52869` | `OFF` | `ON`, `OFF` | v8.1.0+ | Removes the limitation that prevents automatic index merge when a single index scan path is available. When `ON`, the optimizer can choose index merge even when a normal index lookup path exists |
| `54337` | `OFF` | `ON`, `OFF` | v8.3.0+ | Enables general range intersection for complex conjunctive (AND) conditions. Can produce tighter scan ranges but may increase optimization time for queries with 10+ conjuncts |

### Join and row estimation controls

| Fix | Default | Values | Since | Purpose |
|-----|---------|--------|-------|---------|
| `44855` | `OFF` | `ON`, `OFF` | v6.5.4, v7.3.0+ | Improves row count estimation for `IndexJoin` scenarios with `Selection` operators on the Probe side. Fixes overestimation that could lead the optimizer to choose suboptimal join strategies |
| `47400` | `ON` | `ON`, `OFF` | v8.4.0+ | Controls the minimum `estRows` limit. When `ON`, the minimum estimated rows for any operator is 1 (Oracle/DB2 compatible behavior). When `OFF`, `estRows` can be less than 1 |

### Optimizer exploration controls

| Fix | Default | Values | Since | Purpose |
|-----|---------|--------|-------|---------|
| `46177` | `ON` (v8.5.0+), `OFF` (before) | `ON`, `OFF` | v6.5.6, v7.1.3, v7.5.0+ | Controls whether the optimizer explores enforced plans (e.g., plans that enforce a specific sort order) after finding unenforced plans. When `ON`, the optimizer may find better plans at the cost of slightly longer optimization time |

### Expression optimization controls

| Fix | Default | Values | Since | Purpose |
|-----|---------|--------|-------|---------|
| `56318` | `ON` | `ON`, `OFF` | Deployment-specific | Controls whether to avoid double calculation of heavy expressions in `ORDER BY` statements. When `ON`, the optimizer rewrites the plan to prevent redundant expression evaluation |

## Practical examples

### Enable improved IndexJoin estimation and index merge

```sql
-- Session-wide: enable better IndexJoin estimation and allow automatic index merge
SET SESSION tidb_opt_fix_control = '44855:ON,52869:ON';
```

### Enable comprehensive OR filter scan ranges

When a query has complex OR conditions on indexed columns and the optimizer isn't building optimal scan ranges:

```sql
SELECT /*+ SET_VAR(tidb_opt_fix_control='44389:ON') */ *
FROM orders
WHERE (status = 'pending' AND region = 'US')
   OR (status = 'active' AND region = 'EU');
```

### Disable Point Get for wide tables

When Point Get causes excessive memory usage on tables with large JSON or BLOB columns:

```sql
SET SESSION tidb_opt_fix_control = '52592:ON';

SELECT * FROM wide_table WHERE id = 12345;
-- Forces Coprocessor path instead of Point Get
```

### Preserve plan stability during upgrade

When upgrading to a new TiDB version and a specific optimizer change causes regression:

```sql
-- Disable the enforced plan exploration that was turned ON by default in v8.5.0
SET GLOBAL tidb_opt_fix_control = '46177:OFF';
```

### Combine multiple fix controls

```sql
-- Enable improved estimation, index merge, and comprehensive scan ranges
SET SESSION tidb_opt_fix_control = '44855:ON,52869:ON,44389:ON,54337:ON';

EXPLAIN ANALYZE
SELECT *
FROM orders o
JOIN items i ON i.order_id = o.id
WHERE (o.status = 'active' OR o.status = 'pending')
  AND o.created_at > '2024-01-01';
```

## Fix controls vs other tuning mechanisms

| Mechanism | Scope | Effect |
|-----------|-------|--------|
| **Optimizer hints** (e.g., `HASH_JOIN`) | Per-query, per-operator | Forces a specific operator or strategy |
| **Cost factors** (`tidb_opt_*_cost_factor`) | Per-query / session / global | Biases the cost model — soft influence |
| **Fix controls** (`tidb_opt_fix_control`) | Per-query / session / global | Toggles specific optimizer behavior changes on/off |
| **Session variables** (e.g., `tidb_opt_prefer_range_scan`) | Session / global | Enables/disables broad optimizer strategies |

**When to use fix controls:**
- An optimizer behavior change introduced in a new version causes a regression in your workload.
- You want to selectively adopt specific optimizer improvements without taking all changes from an upgrade.
- You need to fine-tune estimation or plan exploration behavior beyond what cost factors and hints provide.
- You want to maintain plan stability during upgrades by disabling specific behavior changes.

**When to prefer other mechanisms:**
- Use **hints** when you know exactly which operator to force for a specific query.
- Use **cost factors** when you want to generally bias the optimizer toward or away from certain operators.
- Use **session variables** for broad behavioral switches (e.g., `tidb_opt_prefer_range_scan`).

## Diagnostic workflow

1. Identify the regression: compare `EXPLAIN ANALYZE` output before and after the change (upgrade, config change, etc.).
2. Check the TiDB release notes for optimizer behavior changes introduced in the new version.
3. Match the behavior change to a fix control number from the catalog above.
4. Set the fix control to the previous default at session scope and re-run `EXPLAIN ANALYZE`.
5. If the plan improves, decide the right scope (per-query SET_VAR, session, or global).
6. Document which fix controls are set and why, so they can be re-evaluated in future upgrades.

## Cautions

- **Always test fix controls in a non-production environment first.** Changing optimizer behavior can have unexpected effects on other queries.
- **Prefer per-query SET_VAR for targeted tuning.** It's the safest scope — no side effects on other queries.
- **Fix controls are version-specific.** A fix control number that doesn't exist in your TiDB version will be silently ignored. Always verify the "Since" version.
- **Re-evaluate after upgrades.** Fix controls you set to work around a regression may no longer be necessary (or may conflict with new improvements) in a later version.
- **Document non-default settings.** If you set fix controls at session or global scope, document the reason and the GitHub issue number so future maintainers can understand the intent and re-evaluate.
- **Fix controls don't compose with cost factors.** They control different aspects of the optimizer — fix controls toggle behavior changes, while cost factors adjust the cost model. Both can be used simultaneously.
