# Issue #61785: Analyze's analyzeColumnsPushDownV2 create too much concurrency

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61785
- Status: closed
- Type: type/bug
- Created At: 2025-06-17T20:15:49Z
- Closed At: 2025-06-18T14:59:31Z
- Labels: affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The issue is that customers have observed higher I/O consumption when the   analyze   operation reaches the index, compared to when it analyzes regular tables. (The   analyze   status contains sensitive information, so it will not be included here.) ![Image]() The root cause of the issue lies in improper coding practices. When we perform the   analyze   operation, we create multiple concurrent tasks to execute it. However, within these concurrently spawned goroutines, we further create additional concurrency. This nested concurrency results in an actual level of parallelism that is significantly higher than we anticipated. You will see that it will create two task about .

## Linked PRs
- Fix PR #61786: planner: avoid exceeding the configured concurrency limit
  URL: https://github.com/pingcap/tidb/pull/61786
  State: closed
  Merged At: 2025-06-18T14:59:30Z
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  PR Summary: What problem does this PR solve? Problem Summary: The issue is that customers have observed higher I/O consumption when the   analyze   operation reaches the index, compared to when it analyzes regular tables. (The   analyze   status contains sensitive information, so it will not be included here.) ![Image]() The root cause of the issue lies in improper coding practices. When we perform the   analyze   operation, we create multiple concurrent tasks to execute it. However, within these concurrently spawned goroutines, we further create additional concurrency. This nested concurrency results in an actual level of parallelism that is significantly higher than we anticipated.
- Fix PR #61813: planner: avoid exceeding the configured concurrency limit (#61786)
  URL: https://github.com/pingcap/tidb/pull/61813
  State: closed
  Merged At: 2025-07-09T00:43:15Z
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #61786 What problem does this PR solve? Problem Summary: The issue is that customers have observed higher I/O consumption when the   analyze   operation reaches the index, compared to when it analyzes regular tables. (The   analyze   status contains sensitive information, so it will not be included here.) ![Image]()
- Fix PR #61814: planner: avoid exceeding the configured concurrency limit (#61786)
  URL: https://github.com/pingcap/tidb/pull/61814
  State: open
  Merged At: not merged
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #61786 What problem does this PR solve? Problem Summary: The issue is that customers have observed higher I/O consumption when the   analyze   operation reaches the index, compared to when it analyzes regular tables. (The   analyze   status contains sensitive information, so it will not be included here.) ![Image]()
- Fix PR #61815: planner: avoid exceeding the configured concurrency limit (#61786)
  URL: https://github.com/pingcap/tidb/pull/61815
  State: closed
  Merged At: 2025-06-25T11:09:54Z
  Changed Files Count: 1
  Main Modules: pkg/executor
  Sample Changed Files:
  - pkg/executor/analyze_col_v2.go
  PR Summary: This is an automated cherry-pick of #61786 What problem does this PR solve? Problem Summary: The issue is that customers have observed higher I/O consumption when the   analyze   operation reaches the index, compared to when it analyzes regular tables. (The   analyze   status contains sensitive information, so it will not be included here.) ![Image]()

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
