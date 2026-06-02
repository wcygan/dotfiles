---
title: MySQL SQL Mode Essentials
---

# MySQL SQL Mode Essentials

SQL modes define supported SQL syntax and data validation behavior. They affect how MySQL handles invalid or ambiguous data.

## Check current modes

```sql
SELECT @@GLOBAL.sql_mode AS global_sql_mode;
SELECT @@SESSION.sql_mode AS session_sql_mode;
```

## Set modes

```sql
SET GLOBAL sql_mode = 'STRICT_TRANS_TABLES,ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION';
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,ONLY_FULL_GROUP_BY,NO_ENGINE_SUBSTITUTION';
```

## MySQL 8.0 default mode

The default SQL mode includes:
`ONLY_FULL_GROUP_BY`, `STRICT_TRANS_TABLES`, `NO_ZERO_IN_DATE`, `NO_ZERO_DATE`,
`ERROR_FOR_DIVISION_BY_ZERO`, and `NO_ENGINE_SUBSTITUTION`.

## Strict mode impact

Strict SQL mode causes invalid or out-of-range values to produce errors instead of warnings and makes data validation stricter.
