# Issue #53387: outer join reorder will produce unexpected join sequence.

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/53387
- Status: closed
- Type: type/bug
- Created At: 2024-05-20T07:16:29Z
- Closed At: 2024-07-23T06:45:29Z
- Labels: affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, impact/wrong-result, may-affects-5.4, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #52941: Optimizer: Refactor and simplify outer to inner join conversion rule #52941 | tidb-test=pr/2321
  URL: https://github.com/pingcap/tidb/pull/52941
  State: closed
  Merged At: 2024-05-16T03:43:13Z
  Changed Files Count: 15
  Main Modules: pkg/planner/core, pkg/expression
  Sample Changed Files:
  - pkg/expression/schema.go
  - pkg/planner/core/BUILD.bazel
  - pkg/planner/core/base/plan_base.go
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_outer2inner_test.go
  - pkg/planner/core/casetest/rule/testdata/outer2inner_in.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/logical_plans_test.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/physical_plan_trace_test.go
  - pkg/planner/core/rule_outer_to_inner_join.go
  - pkg/planner/core/rule_predicate_push_down.go
  PR Summary: What problem does this PR solve? Problem Summary: Currently, the outer to inner join rewrite is part of the predicate push down. This is causing confusion and difficulty in extending of both rewrites. Also, the current implementation of outer to inner join rewrite has unnecessary special cases. What changed and how does it work? A new logical optimization is added to the list of rules. Also, a simple solution of null filtering (or NF) predicate check is used.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
