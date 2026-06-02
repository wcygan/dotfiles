# Issue #64274: Async load may panic when processing dropped indexes

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64274
- Status: closed
- Type: type/bug
- Created At: 2025-11-04T21:20:24Z
- Closed At: 2025-11-08T22:42:47Z
- Labels: affects-6.5, affects-7.5, component/statistics, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- It directly accesses the IsLoadNeeded func.

## Linked PRs
- Related PR #64292: statistics: remove the unnecessary log
  URL: https://github.com/pingcap/tidb/pull/64292
  State: closed
  Merged At: 2025-11-07T18:59:59Z
  Changed Files Count: 5
  Main Modules: pkg/statistics, tests/realtikvtest
  Sample Changed Files:
  - pkg/statistics/handle/storage/BUILD.bazel
  - pkg/statistics/handle/storage/read.go
  - pkg/statistics/handle/storage/read_test.go
  - tests/realtikvtest/statisticstest/BUILD.bazel
  - tests/realtikvtest/statisticstest/statistics_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? IsLoadNeeded doesn’t check for nil internally. We should explicitly verify that it’s safe to use. The real use case the users may have is as follows:

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
