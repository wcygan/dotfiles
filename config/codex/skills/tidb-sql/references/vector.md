---
title: TiDB Vector SQL (Types, Functions, Indexes)
---

# TiDB Vector SQL (Types, Functions, Indexes)

## Feature gate

- Vector data types and functions require TiDB v8.4.0+ (v8.5.0+ recommended for self-managed/dedicated deployments).
- Confirm with `SELECT VERSION();`.

## Data types

- `VECTOR`: variable dimension (cannot build a vector index on it)
- `VECTOR(D)`: fixed dimension `D` (required for vector index)

Example:

```sql
CREATE TABLE embedded_documents (
  id INT PRIMARY KEY,
  document TEXT,
  embedding VECTOR(3)
);
```

Insert vector literals as strings:

```sql
INSERT INTO embedded_documents VALUES (1, 'dog', '[1,2,1]');
```

## Distance functions (common)

- `VEC_COSINE_DISTANCE(v1, v2)`
- `VEC_L2_DISTANCE(v1, v2)`
- (Also exists: `VEC_L1_DISTANCE`, `VEC_NEGATIVE_INNER_PRODUCT`)

Example query (exact scan):

```sql
SELECT id, document, VEC_COSINE_DISTANCE(embedding, '[1,2,3]') AS distance
FROM embedded_documents
ORDER BY distance
LIMIT 10;
```

## Cast / parsing helpers

- `VEC_FROM_TEXT('[...]')` - string -> vector
- `VEC_AS_TEXT(vec)` - vector -> string
- `CAST('[...]' AS VECTOR)` - string -> vector

Tip: If you compare vector constants, cast explicitly to avoid string-based comparisons.

## Vector index (HNSW) essentials

Prerequisites / constraints:

- Requires TiFlash nodes (and TiFlash replica for the table).
- Cannot be `PRIMARY KEY` or `UNIQUE`.
- Single vector column only (no composite vector+other-column index).
- Must use the same distance function in both index definition and query ordering.

Create index at table creation time:

```sql
CREATE TABLE foo (
  id INT PRIMARY KEY,
  embedding VECTOR(3),
  VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding)))
);
```

Create index on an existing table:

```sql
CREATE VECTOR INDEX idx_embedding ON foo ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
-- or:
ALTER TABLE foo ADD VECTOR INDEX idx_embedding ((VEC_COSINE_DISTANCE(embedding))) USING HNSW;
```

Query pattern to use the ANN index:

- Use `ORDER BY VEC_COSINE_DISTANCE(...) ASC LIMIT <K>` (Top-K must be present)
- Desc order or mismatched distance function prevents index usage

Validate index usage:

```sql
EXPLAIN SELECT * FROM foo
ORDER BY VEC_COSINE_DISTANCE(embedding, '[1,2,3]')
LIMIT 10;
SHOW WARNINGS;
```
