# Plan Cache Memory Growth From Varying Parameter Shapes

## User Symptom
- TiDB memory keeps growing while the business workload appears stable.
- In worse cases the node eventually OOMs.

## Investigation Signals
- Grafana shows plan-cache memory growing together with TiDB heap memory.
- The application uses prepared statements, but the number of `IN` values or placeholder shapes varies widely.
- Prepare statement count or session count also jumps during the same window.

## Workaround
- Add `/*+ ignore_plan_cache() */` for this unstable query pattern.
- Avoid prepared statements for highly variable `IN` list shapes.
- Audit session lifecycle because plan cache is session-local on each node.

## Fixed Version
- No universal fix was recorded for this workload pattern.
