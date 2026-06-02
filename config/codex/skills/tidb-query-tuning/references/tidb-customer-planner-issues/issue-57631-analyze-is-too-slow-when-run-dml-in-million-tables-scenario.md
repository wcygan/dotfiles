# Issue #57631: Analyze is too slow when run dml in million tables scenario

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57631
- Status: closed
- Type: type/bug
- Created At: 2024-11-22T07:46:47Z
- Closed At: 2024-12-03T05:55:22Z
- Labels: affects-7.5, affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Edition: Community Git Commit Hash: eb871f862e059832533f1abc6b9b1b3f0957a780 Git Branch: heads/refs/tags/v8.5.0 UTC Build Time: 2024-11-22 03:01:24

## Linked PRs
- Related PR #57638: statistics: debug the update
  URL: https://github.com/pingcap/tidb/pull/57638
  State: closed
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/cache/statscache.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #57756: statistics: avoid stats meta full load after table analysis
  URL: https://github.com/pingcap/tidb/pull/57756
  State: closed
  Merged At: 2024-12-03T05:55:20Z
  Changed Files Count: 12
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze.go
  - pkg/statistics/handle/cache/bench_test.go
  - pkg/statistics/handle/cache/statscache.go
  - pkg/statistics/handle/cache/statscacheinner.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/types/interfaces.go
  PR Summary: What problem does this PR solve? Problem Summary: See more at We need to support updating the stats of only a few tables within the update function. This will help reduce the function's duration after the table analysis is completed. The analysis duration is stable:
- Related PR #57911: statistics: avoid stats meta full load after table analysis (#57756)
  URL: https://github.com/pingcap/tidb/pull/57911
  State: closed
  Merged At: 2024-12-03T10:04:23Z
  Changed Files Count: 12
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze.go
  - pkg/statistics/handle/cache/bench_test.go
  - pkg/statistics/handle/cache/statscache.go
  - pkg/statistics/handle/cache/statscacheinner.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/types/interfaces.go
  PR Summary: This is an automated cherry-pick of #57756 What problem does this PR solve? Problem Summary: See more at We need to support updating the stats of only a few tables within the update function. This will help reduce the function's duration after the table analysis is completed.
- Related PR #61732: statistics: avoid stats meta full load after table analysis (#57756)
  URL: https://github.com/pingcap/tidb/pull/61732
  State: closed
  Merged At: 2025-06-24T14:47:00Z
  Changed Files Count: 12
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze.go
  - pkg/statistics/handle/cache/bench_test.go
  - pkg/statistics/handle/cache/statscache.go
  - pkg/statistics/handle/cache/statscacheinner.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/handle_hist.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  - pkg/statistics/handle/util/interfaces.go
  PR Summary: This is an automated cherry-pick of #57756 What problem does this PR solve? Problem Summary: See more at We need to support updating the stats of only a few tables within the update function. This will help reduce the function's duration after the table analysis is completed.
- Related PR #61944: statistics: avoid stats meta full load after table analysis (#57756)
  URL: https://github.com/pingcap/tidb/pull/61944
  State: open
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/statistics, pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze.go
  - pkg/statistics/handle/cache/bench_test.go
  - pkg/statistics/handle/cache/statscache.go
  - pkg/statistics/handle/cache/statscacheinner.go
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/stats_read_writer.go
  - pkg/statistics/handle/storage/update.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/types/interfaces.go
  PR Summary: This is an automated cherry-pick of #57756 What problem does this PR solve? Problem Summary: See more at We need to support updating the stats of only a few tables within the update function. This will help reduce the function's duration after the table analysis is completed.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
