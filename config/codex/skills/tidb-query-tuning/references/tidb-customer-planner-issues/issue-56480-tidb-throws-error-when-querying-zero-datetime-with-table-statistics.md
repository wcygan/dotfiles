# Issue #56480: tidb throws error when querying zero datetime with table statistics

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56480
- Status: closed
- Type: type/bug
- Created At: 2024-10-08T14:49:08Z
- Closed At: 2024-10-08T14:52:04Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- lots of following errors in tidb log:

## Linked PRs
- Fix PR #52615: statistics: reduce allocation of types.Context
  URL: https://github.com/pingcap/tidb/pull/52615
  State: closed
  Merged At: 2024-04-28T19:26:59Z
  Changed Files Count: 8
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/BUILD.bazel
  - pkg/statistics/handle/BUILD.bazel
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/storage/BUILD.bazel
  - pkg/statistics/handle/storage/json.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/histogram.go
  - pkg/statistics/scalar.go
  PR Summary: What problem does this PR solve? Problem Summary: We still have  but we can reduce the allocations first. What changed and how does it work?
- Fix PR #57300: statistics: avoid throw error when data contains invalid date value
  URL: https://github.com/pingcap/tidb/pull/57300
  State: closed
  Merged At: 2024-11-11T14:14:09Z
  Changed Files Count: 1
  Main Modules: statistics/scalar.go
  Sample Changed Files:
  - statistics/scalar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Mannuly solve it in released branch.
- Related PR #58218: statistics: avoid throw error when data contains invalid date value
  URL: https://github.com/pingcap/tidb/pull/58218
  State: closed
  Merged At: 2024-12-12T16:50:01Z
  Changed Files Count: 1
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/scalar.go
  PR Summary: Same as ref What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #59375: statistics: avoid throw error when data contains invalid date value
  URL: https://github.com/pingcap/tidb/pull/59375
  State: closed
  Merged At: 2025-02-13T09:06:11Z
  Changed Files Count: 1
  Main Modules: statistics/scalar.go
  Sample Changed Files:
  - statistics/scalar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Mannuly solve it in released branch.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
