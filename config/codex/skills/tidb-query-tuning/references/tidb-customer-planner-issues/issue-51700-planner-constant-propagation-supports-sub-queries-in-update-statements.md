# Issue #51700: planner: constant propagation supports sub-queries in update statements

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/51700
- Status: closed
- Type: type/bug
- Created At: 2024-03-12T08:28:46Z
- Closed At: 2025-07-18T10:27:50Z
- Labels: affects-7.5, affects-8.1, affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The constant  is only propagated to t2 side for select sql

## Linked PRs
- Fix PR #61909: planner: constant propagation supports more join type in the logical plan builder
  URL: https://github.com/pingcap/tidb/pull/61909
  State: closed
  Merged At: 2025-07-18T10:27:49Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  - tests/integrationtest/t/planner/core/rule_constant_propagation.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? The flag for the constant propagation rule was set too conservatively before, which led to the inability to execute constant propagation in some places.
- Fix PR #62518: planner: constant propagation supports more join type in the logical plan builder (#61909)
  URL: https://github.com/pingcap/tidb/pull/62518
  State: closed
  Merged At: 2025-07-21T16:07:30Z
  Changed Files Count: 6
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  - tests/integrationtest/t/planner/core/rule_constant_propagation.test
  PR Summary: This is an automated cherry-pick of #61909 What problem does this PR solve? Problem Summary: What changed and how does it work? The flag for the constant propagation rule was set too conservatively before, which led to the inability to execute constant propagation in some places.
- Fix PR #62534: planner: constant propagation supports more join type in the logical plan builder (#61909)
  URL: https://github.com/pingcap/tidb/pull/62534
  State: closed
  Merged At: 2025-07-24T16:28:20Z
  Changed Files Count: 4
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/logical_plan_builder.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  - tests/integrationtest/t/planner/core/rule_constant_propagation.test
  PR Summary: This is an automated cherry-pick of #61909 What problem does this PR solve? Problem Summary: What changed and how does it work? The flag for the constant propagation rule was set too conservatively before, which led to the inability to execute constant propagation in some places.
- Fix PR #62535: planner: constant propagation supports more join type in the logical plan builder (#61909)
  URL: https://github.com/pingcap/tidb/pull/62535
  State: closed
  Merged At: 2025-07-21T15:07:27Z
  Changed Files Count: 4
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/logical_plan_builder.go
  - tests/integrationtest/r/cte.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  - tests/integrationtest/t/planner/core/rule_constant_propagation.test
  PR Summary: This is an automated cherry-pick of #61909 What problem does this PR solve? Problem Summary: What changed and how does it work? The flag for the constant propagation rule was set too conservatively before, which led to the inability to execute constant propagation in some places.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
