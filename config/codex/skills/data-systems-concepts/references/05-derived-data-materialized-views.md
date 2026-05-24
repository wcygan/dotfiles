# Derived Data And Materialized Views

Use this when studying caches, indexes, projections, search views, denormalized tables, or stream-maintained read models.

## Mental Model

Derived data is state that can be recomputed from another source of truth. It is valuable because it makes reads faster or more convenient. It is risky because the system now needs a story for lag, divergence, repair, and rebuilds.

## Key Invariants

- The source of truth is identifiable.
- The projection function is deterministic enough to replay.
- Drift can be detected, tolerated, corrected, or rebuilt.

## Implementation Exercise

Build a small event log and two projections: an account balance table and a transaction-count index.

## Tests And Failure Cases

Skip, duplicate, and reorder projection updates. Verify whether replay repairs the view.

## Online References

- [PostgreSQL Materialized Views](https://www.postgresql.org/docs/current/rules-materializedviews.html)
- [Materialize Views](https://materialize.com/docs/concepts/views/)
- [DBSP: Automatic Incremental View Maintenance](https://www.vldb.org/pvldb/vol16/p3142-budiu.pdf)
