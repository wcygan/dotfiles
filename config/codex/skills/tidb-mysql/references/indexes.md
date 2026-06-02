---
title: MySQL Indexing Essentials
---

# MySQL Indexing Essentials

Use indexes to make `WHERE` and `ORDER BY` efficient, but avoid over-indexing write-heavy tables.

## Core rules

- Indexes improve lookup speed for queries that filter by indexed columns. They also add write overhead because indexes must be maintained on `INSERT/UPDATE/DELETE`.
- Use composite (multi-column) indexes when queries filter on multiple columns; they are used based on the leftmost prefix of the index definition.

## InnoDB specifics

- InnoDB stores table data in the clustered index (the primary key). If no primary key exists, InnoDB uses the first unique NOT NULL index; otherwise it creates a hidden row ID.
- Secondary indexes store the primary key value for each row, so a very wide primary key increases secondary index size.

## Practical tips

- Always define a primary key. Keep it short and stable.
- For composite indexes, order columns to match query predicates and ordering so the leftmost prefix can be used.
- Limit index count on write-heavy tables; each additional index adds write cost.
