# Secondary Indexes

Use this when a system needs lookup by a field that is not the primary storage key.

## Mental Model

A secondary index is derived data that maps an alternate key to one or more primary records. It speeds reads while adding write amplification and consistency work. The design must define uniqueness, covering data, stale entries, and how index updates are coordinated with base-row updates.

## Key Invariants

- Each committed base-row change has matching index effects.
- Non-unique secondary keys can address multiple records.
- Index entries can be verified against base records.

## Implementation Exercise

Add a secondary index from email to user ID in a toy storage engine. Support update and delete.

## Tests And Failure Cases

Crash between base-row update and index update. Verify whether recovery repairs or rolls back the mismatch.

## Online References

- [PostgreSQL Indexes](https://www.postgresql.org/docs/current/indexes.html)
- [SQLite Query Planner](https://www.sqlite.org/queryplanner.html)
- [CockroachDB Secondary Index Best Practices](https://www.cockroachlabs.com/docs/stable/schema-design-indexes)
