# Plan Cache Skipped by Short-Circuit Predicates

## User Symptom
- Prepared statements do not hit the plan cache even though plan cache is enabled.

## Investigation Signals
- The query contains short-circuit predicate patterns such as:
  `c = ? OR ISNULL(?) OR LENGTH(TRIM(?)) < 1`
- Predicate simplification can skip plan cache admission for this shape.

## Workaround
- Rewrite the predicate to avoid the short-circuit pattern when practical.
- If stable caching is more important than SQL shape preservation, simplify the application-side query builder.
- For known unstable patterns, use `/*+ ignore_plan_cache() */` and treat them as uncached queries.

## Fixed Version
- The handbook points to a public issue for this pattern but does not record a fixed release.

## Public References
- https://github.com/pingcap/tidb/issues/63754
