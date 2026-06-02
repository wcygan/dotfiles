# Issue #62917: planner: MergeJoin cost formula should consider OtherCond

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62917
- Status: closed
- Type: type/bug
- Created At: 2025-08-11T07:36:12Z
- Closed At: 2025-08-15T18:35:31Z
- Labels: affects-7.5, affects-8.5, epic/cost-model, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- They have the same cost.

## Linked PRs
- Fix PR #63010: planner: consider OtherConds in MergeJoin cost formula
  URL: https://github.com/pingcap/tidb/pull/63010
  State: closed
  Merged At: 2025-08-15T18:35:30Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Please see the case below, the first plan's cost should be larger than the second one, but now they are the same. The reason is that we forget to consider the cost of  in our MergeJoin cost formula, this PR is going to fix this problem.
- Fix PR #63112: planner: consider OtherConds in MergeJoin cost formula (#63010)
  URL: https://github.com/pingcap/tidb/pull/63112
  State: closed
  Merged At: 2025-09-22T10:14:37Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  PR Summary: This is an automated cherry-pick of #63010 What problem does this PR solve? Problem Summary: What changed and how does it work? Please see the case below, the first plan's cost should be larger than the second one, but now they are the same.
- Fix PR #63113: planner: consider OtherConds in MergeJoin cost formula (#63010)
  URL: https://github.com/pingcap/tidb/pull/63113
  State: open
  Merged At: not merged
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  PR Summary: This is an automated cherry-pick of #63010 What problem does this PR solve? Problem Summary: What changed and how does it work? Please see the case below, the first plan's cost should be larger than the second one, but now they are the same.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
