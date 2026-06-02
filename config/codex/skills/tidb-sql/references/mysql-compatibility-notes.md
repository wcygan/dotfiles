---
title: MySQL to TiDB SQL Compatibility Notes (Common Breaks)
---

# MySQL to TiDB SQL Compatibility Notes (Common Breaks)

Use this as a quick "lint list" when adapting MySQL SQL to TiDB.

## Detect TiDB vs MySQL quickly

```sql
SELECT VERSION();
```

If the returned string contains `TiDB`, you are connected to TiDB and can infer the TiDB version from that string.

## Unsupported or commonly unavailable features (avoid generating by default)

Always confirm your TiDB version and deployment mode before relying on borderline features.

- Stored procedures and stored functions
- Triggers
- Events (event scheduler)
- User-defined functions (UDF)
- `SPATIAL` / `GEOMETRY` functions, data types, and indexes
- XML functions
- `XA` syntax (TiDB uses 2PC internally but does not expose XA over SQL)
- `CREATE TABLE ... AS SELECT ...` (CTAS)
- `CHECK TABLE`, `CHECKSUM TABLE`, `REPAIR TABLE`, `OPTIMIZE TABLE`
- `HANDLER`, `CREATE TABLESPACE`
- Some advanced query syntaxes might be unsupported depending on TiDB version (examples seen in TiDB docs include `SKIP LOCKED`, lateral derived tables, and `JOIN ... ON (subquery)` patterns)

## FULLTEXT: clarify intent

- Do not assume MySQL `FULLTEXT` indexes work everywhere on TiDB.
- If the user needs keyword search, prefer TiDB full-text search when their deployment supports it (see `references/full-text-search.md`).

## Views

- Views are not updatable: do not emit `UPDATE/INSERT/DELETE` against views.

## SELECT syntax edge cases

- Do not emit `SELECT ... INTO @variable` (unsupported).
- In TiDB, `SELECT ... GROUP BY expr` does not imply `ORDER BY expr` (MySQL 5.7 behavior differs). If ordering matters, add an explicit `ORDER BY`.

## Built-in functions (be defensive)

- TiDB supports most MySQL built-ins, but not all. When porting SQL that uses non-trivial built-ins, validate availability with:

```sql
SHOW BUILTINS;
```

## Charset/collation pitfalls

- TiDB supports a limited set of character sets. If you see errors around charset/collation, stick to commonly supported sets like `utf8mb4` (and avoid exotic charsets).
- Default charset/collation can differ from MySQL: TiDB defaults are typically `utf8mb4` and `utf8mb4_bin`. If you depend on case-insensitive comparisons, set the collation explicitly.

## Name casing pitfalls

- TiDB supports `lower_case_table_names = 2` only (case-insensitive lookup behavior). Do not rely on two objects whose names differ only by letter case.

## AUTO_INCREMENT pitfalls (and why AUTO_RANDOM is common on TiDB)

- AUTO_INCREMENT IDs are globally unique in TiDB, but not necessarily sequential across nodes. Avoid mixing implicit IDs with custom explicit values.
- Removing `AUTO_INCREMENT` is possible (guarded by `tidb_allow_remove_auto_inc`), but adding it later is not supported.
- If you do not define a primary key, TiDB uses `_tidb_rowid`. Its allocator can interact with AUTO_INCREMENT in ways that surprise MySQL users.
- If you are designing a write-heavy schema, prefer `AUTO_RANDOM` for BIGINT PKs when it fits (see `references/auto-random.md`).

## DDL / schema changes (be conservative, TiDB has extra restrictions)

- Avoid "multi-change" `ALTER TABLE` that references the same column/index more than once in one statement.
- Avoid packing multiple TiDB-specific schema changes into one `ALTER TABLE` when possible (split them).
- Not all type changes are supported via `ALTER TABLE` (for unsupported changes, plan a backfill/migration).
- `ALGORITHM={INSTANT,INPLACE,COPY}` is treated as an assertion, not as an algorithm selector.
- Adding/dropping a clustered primary key can be unsupported; in practice, treat PK changes as "new table + backfill + swap".
- Index type decorations like `USING HASH|BTREE|RTREE|FULLTEXT` can be parsed but ignored. Do not rely on them to change behavior.

## Partitioning notes (avoid fancy operations unless you know TiDB supports them)

- Supported partitioning types include `HASH`, `RANGE`, `LIST`, and `KEY`.
- Some partition DDL operations are ignored, and `SUBPARTITION` is not supported. If you need advanced partition DDL, confirm support on your TiDB version first.

## Optimizer / plan differences

- `optimizer_switch` is read-only and does not affect TiDB plans.
- Optimizer hints are not a drop-in replacement for MySQL hints. Use `EXPLAIN` on TiDB to validate critical queries.
  - For structured plans, use `EXPLAIN FORMAT = "tidb_json"` (see `references/explain.md`).

## Timezone and timestamp defaults

- TiDB supports named timezones based on system timezone rules; MySQL often requires timezone tables for named timezones.
- TiDB only supports `explicit_defaults_for_timestamp = ON`. If you are porting MySQL 5.7-era SQL that relies on implicit TIMESTAMP defaults, test carefully and set defaults explicitly.

## Deprecated MySQL features you should avoid porting

- Floating-point type precision specifiers (prefer `DECIMAL` when you need fixed precision).
- `ZEROFILL` (pad in the application layer instead).
