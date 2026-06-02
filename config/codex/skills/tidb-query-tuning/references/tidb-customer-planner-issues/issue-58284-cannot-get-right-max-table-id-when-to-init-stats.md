# Issue #58284: cannot get right max table id when to init stats

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/58284
- Status: closed
- Type: type/bug
- Created At: 2024-12-16T06:29:05Z
- Closed At: 2024-12-16T09:32:59Z
- Labels: affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- when we get max table id, we should save it into atomic value. but we save common table id into it. so it is bad max table id and lead to other problem .

## Linked PRs
- Fix PR #58280: statistics: get right max table id when to init stats
  URL: https://github.com/pingcap/tidb/pull/58280
  State: closed
  Merged At: 2024-12-16T09:32:57Z
  Changed Files Count: 2
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? when we get max table id, we should save it into atomic value. but we save common table id into it. so it is bad max table id and lead to other problem .
- Fix PR #58296: statistics: get right max table id when to init stats (#58280)
  URL: https://github.com/pingcap/tidb/pull/58296
  State: closed
  Merged At: 2024-12-16T15:07:45Z
  Changed Files Count: 2
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  PR Summary: This is an automated cherry-pick of #58280 What problem does this PR solve? Problem Summary: What changed and how does it work? when we get max table id, we should save it into atomic value. but we save common table id into it. so it is bad max table id and lead to other problem .
- Fix PR #58297: statistics: get right max table id when to init stats (#58280)
  URL: https://github.com/pingcap/tidb/pull/58297
  State: closed
  Merged At: 2024-12-16T15:54:51Z
  Changed Files Count: 4
  Main Modules: pkg/statistics, .bazelversion
  Sample Changed Files:
  - .bazelversion
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/initstats/BUILD.bazel
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  PR Summary: This is an automated cherry-pick of #58280 What problem does this PR solve? Problem Summary: What changed and how does it work? when we get max table id, we should save it into atomic value. but we save common table id into it. so it is bad max table id and lead to other problem .
- Fix PR #58298: statistics: get right max table id when to init stats (#58280)
  URL: https://github.com/pingcap/tidb/pull/58298
  State: closed
  Merged At: 2024-12-16T14:19:45Z
  Changed Files Count: 4
  Main Modules: pkg/statistics, .bazelversion
  Sample Changed Files:
  - .bazelversion
  - pkg/statistics/handle/bootstrap.go
  - pkg/statistics/handle/handletest/initstats/BUILD.bazel
  - pkg/statistics/handle/handletest/initstats/load_stats_test.go
  PR Summary: This is an automated cherry-pick of #58280 What problem does this PR solve? Problem Summary: What changed and how does it work? when we get max table id, we should save it into atomic value. but we save common table id into it. so it is bad max table id and lead to other problem .

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
