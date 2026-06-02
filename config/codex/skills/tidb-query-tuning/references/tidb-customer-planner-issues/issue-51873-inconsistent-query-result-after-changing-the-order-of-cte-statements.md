# Issue #51873: Inconsistent query result after changing the order of cte statements

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/51873
- Status: closed
- Type: type/bug
- Created At: 2024-03-19T02:27:22Z
- Closed At: 2024-03-19T13:38:14Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.0, report/customer, severity/critical, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- Query A: Empty set, 1 warning (0.00 sec) Query B: +---------------+

## Linked PRs
- Fix PR #51903: planner: apply rule_partition_pruning when optimizing CTE under static mode
  URL: https://github.com/pingcap/tidb/pull/51903
  State: closed
  Merged At: 2024-03-19T13:38:13Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/BUILD.bazel
  - pkg/planner/core/casetest/integration_test.go
  - pkg/planner/core/optimizer.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #52058: planner: apply rule_partition_pruning when optimizing CTE under static mode (#51903)
  URL: https://github.com/pingcap/tidb/pull/52058
  State: closed
  Merged At: 2024-04-01T06:24:16Z
  Changed Files Count: 3
  Main Modules: planner/core, executor/sample_test.go
  Sample Changed Files:
  - executor/sample_test.go
  - planner/core/integration_test.go
  - planner/core/optimizer.go
  PR Summary: This is an automated cherry-pick of #51903 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #52148: planner: apply rule_partition_pruning when optimizing CTE under static mode (#51903)
  URL: https://github.com/pingcap/tidb/pull/52148
  State: closed
  Merged At: 2024-03-27T09:32:18Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/BUILD.bazel
  - pkg/planner/core/casetest/integration_test.go
  - pkg/planner/core/optimizer.go
  PR Summary: This is an automated cherry-pick of #51903 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #52269: planner: apply rule_partition_pruning when optimizing CTE under static mode (#51903)
  URL: https://github.com/pingcap/tidb/pull/52269
  State: closed
  Merged At: 2024-04-18T13:36:08Z
  Changed Files Count: 3
  Main Modules: planner/core, executor/sample_test.go
  Sample Changed Files:
  - executor/sample_test.go
  - planner/core/integration_test.go
  - planner/core/optimizer.go
  PR Summary: This is an automated cherry-pick of #51903 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #52270: planner: apply rule_partition_pruning when optimizing CTE under static mode (#51903)
  URL: https://github.com/pingcap/tidb/pull/52270
  State: closed
  Merged At: 2024-05-21T07:58:17Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/executor
  Sample Changed Files:
  - pkg/executor/sample_test.go
  - pkg/planner/core/casetest/BUILD.bazel
  - pkg/planner/core/casetest/integration_test.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/optimizer.go
  PR Summary: This is an automated cherry-pick of #51903 What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
