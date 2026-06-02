---
title: MySQL Slow Query Log
---

# MySQL Slow Query Log

Use the slow query log to capture statements that exceed a time threshold and optionally include queries that do not use indexes.

## Enable and configure

- Enable at startup with `--slow_query_log` or at runtime with `SET GLOBAL slow_query_log = ON`.
- Control the threshold with `long_query_time` (seconds; can be fractional).
- Optionally log queries that do not use indexes with `log_queries_not_using_indexes`.

## Log destination

- Use `log_output` to select `FILE`, `TABLE`, or `NONE`.
- When logging to `TABLE`, use `mysql.slow_log` for inspection.

## Analyze

- Use `mysqldumpslow` to summarize and group slow queries from the log file.
