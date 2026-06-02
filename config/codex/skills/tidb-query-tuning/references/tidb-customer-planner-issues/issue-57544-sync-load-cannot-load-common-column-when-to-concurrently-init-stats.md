# Issue #57544: sync load cannot load common column when to concurrently init stats

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/57544
- Status: closed
- Type: type/bug
- Created At: 2024-11-20T06:53:46Z
- Closed At: 2024-11-27T18:32:42Z
- Labels: affects-7.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- we can see a pseudo stats

## Linked PRs
- Fix PR #57548: statstics: fix cannot load non-index column with concurrently init stats
  URL: https://github.com/pingcap/tidb/pull/57548
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #57664: statistics: add more tests for init stats
  URL: https://github.com/pingcap/tidb/pull/57664
  State: closed
  Merged At: 2024-11-28T11:33:52Z
  Changed Files Count: 4
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/initstats/BUILD.bazel
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  - pkg/statistics/handle/handletest/initstats/main_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #57665: statistics: fix sync load cannot load common column with concurrently init stats
  URL: https://github.com/pingcap/tidb/pull/57665
  State: closed
  Merged At: 2024-11-27T06:45:17Z
  Changed Files Count: 7
  Main Modules: pkg/statistics, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_stats.go
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handle_hist.go
  - pkg/statistics/handle/handletest/initstats/BUILD.bazel
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  - pkg/statistics/handle/handletest/initstats/main_test.go
  - pkg/statistics/handle/storage/read.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #57800: statistics: add more tests for init stats (#57664)
  URL: https://github.com/pingcap/tidb/pull/57800
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/initstats/BUILD.bazel
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  PR Summary: This is an automated cherry-pick of #57664 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
