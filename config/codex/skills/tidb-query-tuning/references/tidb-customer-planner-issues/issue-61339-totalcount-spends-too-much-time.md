# Issue #61339: TotalCount spends too much time

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61339
- Status: closed
- Type: type/enhancement
- Created At: 2025-05-27T03:06:40Z
- Closed At: 2025-05-28T02:10:56Z
- Labels: affects-8.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- The issue is as shown in this flame graph.

## Linked PRs
- Fix PR #61340: statistics: the totalCount/minCount of TopN is calculated only once
  URL: https://github.com/pingcap/tidb/pull/61340
  State: closed
  Merged At: 2025-05-28T02:10:55Z
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/builder.go
  - pkg/statistics/cmsketch.go
  - pkg/statistics/cmsketch_test.go
  PR Summary: What problem does this PR solve? Problem Summary: The issue is as shown in this flame graph. You can see that calculating the total for topn takes a lot of time, because it needs to traverse topn each time to compute the total count. This is very time-consuming. Moreover, the result of each calculation is the same, so you can cache this result to avoid performance issues. What changed and how does it work?
- Fix PR #61371: statistics: the totalCount/minCount of TopN is calculated only once (#61340)
  URL: https://github.com/pingcap/tidb/pull/61371
  State: closed
  Merged At: 2025-07-01T06:17:57Z
  Changed Files Count: 3
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/builder.go
  - pkg/statistics/cmsketch.go
  - pkg/statistics/cmsketch_test.go
  PR Summary: This is an automated cherry-pick of #61340 What problem does this PR solve? Problem Summary: The issue is as shown in this flame graph. You can see that calculating the total for topn takes a lot of time, because it needs to traverse topn each time to compute the total count. This is very time-consuming. Moreover, the result of each calculation is the same, so you can cache this result to avoid performance issues.
- Fix PR #61421: planner: Only count all topn when necessary
  URL: https://github.com/pingcap/tidb/pull/61421
  State: closed
  Merged At: 2025-06-03T18:11:35Z
  Changed Files Count: 1
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/builder.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? This PR does the following in addition to a prior PR targeted at this issue: 1) It removes the need to accumulate the count of all topN for the purposes of determining if we have all rows in the TopN.
- Fix PR #61996: planner: Only count all topn when necessary (#61421)
  URL: https://github.com/pingcap/tidb/pull/61996
  State: closed
  Merged At: 2025-07-02T17:06:03Z
  Changed Files Count: 1
  Main Modules: pkg/statistics
  Sample Changed Files:
  - pkg/statistics/builder.go
  PR Summary: This is an automated cherry-pick of #61421 What problem does this PR solve? Problem Summary: What changed and how does it work? This PR does the following in addition to a prior PR targeted at this issue:

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
