# Issue #52294: wrong singleflight implementation for stats' syncload

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52294
- Status: closed
- Type: type/bug
- Created At: 2024-04-01T13:03:40Z
- Closed At: 2024-04-03T10:16:56Z
- Labels: affects-6.5, affects-7.1, affects-7.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- ![image]() We use the for sync load's duplicate task detection. ![image]() It will return a boolean value directly after it finds duplicates. ![image]() And we can see that the also returns directly by writing an ok result to the .

## Linked PRs
- Fix PR #52301: statistics: fix wrong singleflight implementation for stats' syncload
  URL: https://github.com/pingcap/tidb/pull/52301
  State: closed
  Merged At: 2024-04-03T10:16:55Z
  Changed Files Count: 5
  Main Modules: pkg/statistics, pkg/parser
  Sample Changed Files:
  - pkg/parser/model/model.go
  - pkg/statistics/handle/syncload/stats_syncload.go
  - pkg/statistics/handle/syncload/stats_syncload_test.go
  - pkg/statistics/handle/types/BUILD.bazel
  - pkg/statistics/handle/types/interfaces.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? the problem has been described in the issue. we refactor the singleflight using the golang official library.
- Fix PR #52374: statistics: fix wrong singleflight implementation for stats' syncload (#52301)
  URL: https://github.com/pingcap/tidb/pull/52374
  State: closed
  Merged At: 2024-04-07T08:51:20Z
  Changed Files Count: 5
  Main Modules: pkg/statistics, pkg/parser
  Sample Changed Files:
  - pkg/parser/model/model.go
  - pkg/statistics/handle/BUILD.bazel
  - pkg/statistics/handle/handle.go
  - pkg/statistics/handle/handle_hist.go
  - pkg/statistics/handle/handle_hist_test.go
  PR Summary: This is an automated cherry-pick of #52301 What problem does this PR solve? Problem Summary: What changed and how does it work? the problem has been described in the issue. we refactor the singleflight using the golang official library.
- Fix PR #52382: statistics: fix wrong singleflight implementation for stats' syncload (#52301)
  URL: https://github.com/pingcap/tidb/pull/52382
  State: closed
  Merged At: 2024-08-27T13:48:17Z
  Changed Files Count: 5
  Main Modules: statistics/handle, parser/model
  Sample Changed Files:
  - parser/model/model.go
  - statistics/handle/BUILD.bazel
  - statistics/handle/handle.go
  - statistics/handle/handle_hist.go
  - statistics/handle/handle_hist_test.go
  PR Summary: This is an automated cherry-pick of #52301 What problem does this PR solve? Problem Summary: What changed and how does it work? the problem has been described in the issue. we refactor the singleflight using the golang official library.
- Fix PR #52383: statistics: fix wrong singleflight implementation for stats' syncload (#52301)
  URL: https://github.com/pingcap/tidb/pull/52383
  State: closed
  Merged At: 2024-06-04T14:10:28Z
  Changed Files Count: 5
  Main Modules: statistics/handle, parser/model
  Sample Changed Files:
  - parser/model/model.go
  - statistics/handle/BUILD.bazel
  - statistics/handle/handle.go
  - statistics/handle/handle_hist.go
  - statistics/handle/handle_hist_test.go
  PR Summary: This is an automated cherry-pick of #52301 What problem does this PR solve? Problem Summary: What changed and how does it work? the problem has been described in the issue. we refactor the singleflight using the golang official library.
- Related PR #54339: statistics: fix wrong singleflight implementation for stats' syncload
  URL: https://github.com/pingcap/tidb/pull/54339
  State: closed
  Merged At: 2024-07-01T06:10:26Z
  Changed Files Count: 5
  Main Modules: statistics/handle, parser/model
  Sample Changed Files:
  - parser/model/model.go
  - statistics/handle/BUILD.bazel
  - statistics/handle/handle.go
  - statistics/handle/handle_hist.go
  - statistics/handle/handle_hist_test.go
  PR Summary: close pingcap/tidb#52294 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Related PR #55726: statistics: fix wrong singleflight implementation for stats' syncload(#52301) (#52382)
  URL: https://github.com/pingcap/tidb/pull/55726
  State: closed
  Merged At: 2024-08-28T12:27:18Z
  Changed Files Count: 5
  Main Modules: statistics/handle, parser/model
  Sample Changed Files:
  - parser/model/model.go
  - statistics/handle/BUILD.bazel
  - statistics/handle/handle.go
  - statistics/handle/handle_hist.go
  - statistics/handle/handle_hist_test.go
  PR Summary: cherry pick #52382  close pingcap/tidb#52294 What problem does this PR solve? Problem Summary:

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
