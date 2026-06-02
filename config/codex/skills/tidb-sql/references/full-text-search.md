---
title: TiDB Full-Text Search (SQL)
---

# TiDB Full-Text Search (SQL)

TiDB provides a full-text search feature that can replace MySQL-style keyword search use cases.

## Availability gate (important)

Full-text search availability depends on TiDB version and deployment capabilities. Always confirm the target deployment before relying on it.

## Create a full-text index

Create with table:

```sql
CREATE TABLE stock_items(
  id INT,
  title TEXT,
  FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
);
```

Or add to an existing table:

```sql
ALTER TABLE stock_items
  ADD FULLTEXT INDEX (title) WITH PARSER MULTILINGUAL
  ADD_COLUMNAR_REPLICA_ON_DEMAND;
```

Parsers:

- `STANDARD`: best for space/punctuation-delimited languages (often English)
- `MULTILINGUAL`: supports mixed languages (including CJK)

Note: `ADD_COLUMNAR_REPLICA_ON_DEMAND` is used in the official examples for enabling full-text search indexing. If your TiDB deployment rejects this clause, remove it and follow the deployment-specific guidance.

## Query with ranking

Use `FTS_MATCH_WORD(query, column)` in both `WHERE` and `ORDER BY`:

```sql
SELECT *
FROM stock_items
WHERE FTS_MATCH_WORD('bluetooth earbuds', title)
ORDER BY FTS_MATCH_WORD('bluetooth earbuds', title) DESC
LIMIT 10;
```

Count matches:

```sql
SELECT COUNT(*)
FROM stock_items
WHERE FTS_MATCH_WORD('bluetooth earbuds', title);
```

## Migration note (MySQL FULLTEXT)

Do not assume MySQL `FULLTEXT` behavior/availability carries over to TiDB in all deployments.
If the user says "use FULLTEXT", clarify whether they mean "MySQL FULLTEXT index" or "TiDB full-text search feature".
