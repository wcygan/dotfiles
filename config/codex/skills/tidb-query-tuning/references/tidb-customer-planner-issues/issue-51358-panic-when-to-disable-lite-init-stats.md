# Issue #51358: panic when to disable lite-init-stats

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/51358
- Status: closed
- Type: type/bug
- Created At: 2024-02-27T08:46:01Z
- Closed At: 2024-02-27T10:47:32Z
- Labels: affects-7.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #51357: statistics: fix panic when to enable force-init-stats
  URL: https://github.com/pingcap/tidb/pull/51357
  State: closed
  Merged At: 2024-02-27T10:47:08Z
  Changed Files Count: 5
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/cache/BUILD.bazel
  - pkg/statistics/handle/cache/statscache.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? If we get nil from cache, we shouldn't do anything.
- Fix PR #51369: statistics: fix panic when to enable force-init-stats (#51357)
  URL: https://github.com/pingcap/tidb/pull/51369
  State: closed
  Merged At: 2024-02-27T11:23:02Z
  Changed Files Count: 5
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/cache/BUILD.bazel
  - pkg/statistics/handle/cache/statscache.go
  - pkg/statistics/handle/handletest/statstest/BUILD.bazel
  - pkg/statistics/handle/handletest/statstest/stats_test.go
  PR Summary: This is an automated cherry-pick of #51357 What problem does this PR solve? Problem Summary: What changed and how does it work? If we get nil from cache, we shouldn't do anything.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
