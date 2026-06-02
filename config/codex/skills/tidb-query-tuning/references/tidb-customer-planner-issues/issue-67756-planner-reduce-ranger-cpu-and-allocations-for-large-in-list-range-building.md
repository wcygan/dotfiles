# Issue #67756: planner: reduce ranger CPU and allocations for large IN-list range building

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67756
- Status: open
- Type: type/enhancement
- Created At: 2026-04-14T07:41:19Z
- Labels: component/util, planner/performance, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- still spends substantial CPU time and memory building ranges for large predicates, especially on the long- and cartesian-fanout paths.

## Linked PRs
- Fix PR #67757: pkg/util/ranger: reduce allocations for large IN-list range building
  URL: https://github.com/pingcap/tidb/pull/67757
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/util, docs/agents
  Sample Changed Files:
  - docs/agents/notes-guide.md
  - docs/agents/ranger/README.md
  - pkg/util/ranger/bench_test.go
  - pkg/util/ranger/points.go
  - pkg/util/ranger/ranger.go
  - pkg/util/ranger/ranger_test.go
  PR Summary: What problem does this PR solve? Problem Summary: was spending substantial CPU time and memory building ranges for large  predicates. The main pressure came from repeated point/range materialization and per-range small-object allocation on the long- and cartesian-fanout paths. What changed and how does it work? This PR reduces ranger overhead for large  workloads and adds dedicated benchmarks to keep the improvements measurable.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
