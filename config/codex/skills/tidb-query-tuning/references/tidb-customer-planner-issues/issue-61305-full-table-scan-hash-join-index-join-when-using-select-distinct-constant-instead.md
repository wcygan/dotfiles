# Issue #61305: Full table scan / Hash Join+Index Join when using select distinct constant, instead of column

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61305
- Status: closed
- Type: type/bug
- Created At: 2025-05-24T19:41:48Z
- Closed At: 2025-09-01T06:55:26Z
- Labels: affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, planner/cascades, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Added Hash Join and Index Join (to do non-needed left outer join?) When it should been more similar to:

## Linked PRs
- Fix PR #61478: planner: outer join pruning for constants
  URL: https://github.com/pingcap/tidb/pull/61478
  State: closed
  Merged At: 2025-06-06T14:23:46Z
  Changed Files Count: 4
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/rule/util/misc.go
  - pkg/planner/core/rule_join_elimination.go
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Issue 61305 exposed limitations in the outer join pruning if constants are in the select list. If a constant is in the select list, then we don't recognize that this column is irrelvant - and thus if you ONLY otherwise have columns from the left side, we don't prune right side tables due to the constant. Enhanced outer join pruning to cover these cases.
- Fix PR #62166: planner: outer join pruning for constants (#61478)
  URL: https://github.com/pingcap/tidb/pull/62166
  State: closed
  Merged At: 2025-07-03T17:46:42Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/bindinfo, tests/integrationtest
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/planner/core/casetest/BUILD.bazel
  - pkg/planner/core/casetest/plan_test.go
  - pkg/planner/core/rule_join_elimination.go
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  PR Summary: This is an automated cherry-pick of #61478 What problem does this PR solve? Problem Summary: What changed and how does it work? Issue 61305 exposed limitations in the outer join pruning if constants are in the select list. If a constant is in the select list, then we don't recognize that this column is irrelvant - and thus if you ONLY otherwise have columns from the left side, we don't prune right side tables due to the constant.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
