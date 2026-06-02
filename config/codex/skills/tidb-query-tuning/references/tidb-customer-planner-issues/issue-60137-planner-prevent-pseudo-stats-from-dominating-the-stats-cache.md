# Issue #60137: planner: prevent pseudo-stats from dominating the Stats Cache

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60137
- Status: closed
- Type: type/enhancement
- Created At: 2025-03-18T04:35:37Z
- Closed At: 2025-09-09T20:29:04Z
- Labels: component/statistics, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- In a customer case below, pseudo-stats costs 1.8GB (40%) memory: ![Image]()

## Linked PRs
- Fix PR #63160: stats: optimize memory footprint of pseudo stats table
  URL: https://github.com/pingcap/tidb/pull/63160
  State: closed
  Merged At: 2025-09-09T20:29:03Z
  Changed Files Count: 6
  Main Modules: pkg/statistics, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/planbuilder.go
  - pkg/statistics/BUILD.bazel
  - pkg/statistics/handle/handle.go
  - pkg/statistics/histogram.go
  - pkg/statistics/histogram_test.go
  - pkg/statistics/table.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? A significant part of memory consumption of pseudo table is creating new chunk for every pseudo table creation. These new chunks are read only and only to provide compatibility to the code of using real stats table struct. We can make it a static object and shared by all pseudo tables to reduce memory usage.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
