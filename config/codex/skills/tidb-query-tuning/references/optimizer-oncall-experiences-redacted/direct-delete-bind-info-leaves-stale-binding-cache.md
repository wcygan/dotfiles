# Direct Delete on `mysql.bind_info` Leaves Stale Binding Cache

## Symptom

- After deleting rows from `mysql.bind_info` directly, `SHOW GLOBAL BINDINGS` still shows the deleted binding.
- Running `ADMIN RELOAD BINDINGS` does not fully clear the stale in-memory binding entry.

## Why this happens

- Direct DML on `mysql.bind_info` bypasses normal binding lifecycle operations.
- Binding cache synchronization can become inconsistent with table state.

## Recovery

- Preferred: always remove bindings with `DROP GLOBAL BINDING ...`.
- If direct delete already happened and reload is ineffective, restart the TiDB server to fully clear and rebuild binding cache state.

## Reproduction Example

```sql
mysql> show global bindings;
+----------------------------+--------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql               | Bind_sql                 | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+----------------------------+--------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t` | SELECT * FROM `test`.`t` | test       | enabled | 2026-04-10 16:29:00.484 | 2026-04-10 16:29:00.484 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
+----------------------------+--------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
1 row in set (0.001 sec)

mysql> delete from mysql.bind_info where source!='builtin';
Query OK, 1 row affected (0.007 sec)

mysql> admin reload bindings;
Query OK, 0 rows affected (0.004 sec)

mysql> show global bindings;
+----------------------------+--------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| Original_sql               | Bind_sql                 | Default_db | Status  | Create_time             | Update_time             | Charset | Collation       | Source | Sql_digest                                                       | Plan_digest |
+----------------------------+--------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
| select * from `test` . `t` | SELECT * FROM `test`.`t` | test       | enabled | 2026-04-10 16:29:00.484 | 2026-04-10 16:29:00.484 | utf8    | utf8_general_ci | manual | 8b193b00413fdb910d39073e0d494c96ebf24d1e30b131ecdd553883d0e29b42 |             |
+----------------------------+--------------------------+------------+---------+-------------------------+-------------------------+---------+-----------------+--------+------------------------------------------------------------------+-------------+
1 row in set (0.001 sec)
```
