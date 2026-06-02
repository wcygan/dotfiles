# Issue #60692: tidb reports "Can't find column" error from v8.5.0 when there are multiple joins in the query

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/60692
- Status: closed
- Type: type/bug
- Created At: 2025-04-21T14:31:50Z
- Closed At: 2025-04-23T07:54:57Z
- Labels: affects-8.5, affects-9.0, report/customer, severity/major, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #60694: planner: add back children's `Schema` when checking `LogicalJoin`'s used columns in column pruning
  URL: https://github.com/pingcap/tidb/pull/60694
  State: closed
  Merged At: 2025-04-23T07:54:56Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/operator/logicalop/logical_join.go
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: What problem does this PR solve? Problem Summary: As said in the issue, sometimes the  may contain outdated s after the projection elimination. We should have fixed the , but considering the long-standing problems in schema maintenance and column pruning in tidb, we can't make sure we won't introduce any new risk. This PR is likely to be cherry-picked to the LTS version quickly. So it's better to just restore the previous checking logic, i.e., use the  to do the check.
- Fix PR #60738: planner: add back children's `Schema` when checking `LogicalJoin`'s used columns in column pruning (#60694)
  URL: https://github.com/pingcap/tidb/pull/60738
  State: closed
  Merged At: 2025-04-25T03:59:56Z
  Changed Files Count: 3
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/operator/logicalop/logical_join.go
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: This is an automated cherry-pick of #60694 What problem does this PR solve? Problem Summary: As said in the issue, sometimes the  may contain outdated s after the projection elimination. We should have fixed the , but considering the long-standing problems in schema maintenance and column pruning in tidb, we can't make sure we won't introduce any new risk.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
