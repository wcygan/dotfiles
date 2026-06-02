# Issue #64263: plan cache can't work after update to v8.5.3

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64263
- Status: closed
- Type: type/bug
- Created At: 2025-11-04T10:13:10Z
- Closed At: 2025-11-10T03:15:51Z
- Labels: affects-8.5, impact/upgrade, report/customer, severity/moderate, sig/planner, type/bug, type/regression

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #64265: planner: fix wrongly identify the changes in the expression and skip the plan cache
  URL: https://github.com/pingcap/tidb/pull/64265
  State: closed
  Merged At: 2025-11-10T03:15:50Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, pkg/executor
  Sample Changed Files:
  - pkg/executor/explainfor_test.go
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_xut.json
  - pkg/planner/core/rule/rule_predicate_simplification.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The issue was triggered by  , The original logic would cause any two OR expressions and a scalar function to skip the plan cache, regardless of whether an expression transformation occurs. This PR introduces the correct logic to skip the plan cache only after a transformation has occurred.
- Fix PR #64376: planner: fix wrongly identify the changes in the expression and skip the plan cache (#64265)
  URL: https://github.com/pingcap/tidb/pull/64376
  State: closed
  Merged At: 2025-11-10T07:39:26Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, pkg/executor
  Sample Changed Files:
  - pkg/executor/explainfor_test.go
  - pkg/planner/core/casetest/rule/rule_predicate_simplification_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/rule_predicate_simplification.go
  PR Summary: This is an automated cherry-pick of #64265 What problem does this PR solve? Problem Summary: What changed and how does it work? The issue was triggered by  , The original logic would cause any two OR expressions and a scalar function to skip the plan cache, regardless of whether an expression transformation occurs.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
