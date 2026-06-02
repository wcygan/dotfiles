# Issue #52772: TiDB panic when new collation is disabled and two expressions use different collation

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/52772
- Status: closed
- Type: type/bug
- Created At: 2024-04-19T11:30:41Z
- Closed At: 2024-04-23T16:45:13Z
- Labels: affects-7.1, affects-7.5, affects-8.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- TiDB reports error: The stack:

## Linked PRs
- Fix PR #52812: expression: don't cast collation for in expression is the new collation is disabled
  URL: https://github.com/pingcap/tidb/pull/52812
  State: closed
  Merged At: 2024-04-23T16:45:12Z
  Changed Files Count: 4
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  - tests/integrationtest/r/collation_misc_disabled.result
  - tests/integrationtest/r/collation_misc_enabled.result
  - tests/integrationtest/t/collation_misc.test
  PR Summary: What problem does this PR solve? Problem Summary: If the new collation is disabled, we should not cast collation for in expression, which may lead to panic in the issue case. What changed and how does it work?
- Fix PR #52863: expression: don't cast collation for in expression is the new collation is disabled (#52812)
  URL: https://github.com/pingcap/tidb/pull/52863
  State: closed
  Merged At: 2024-04-24T18:36:11Z
  Changed Files Count: 4
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  - tests/integrationtest/r/collation_misc_disabled.result
  - tests/integrationtest/r/collation_misc_enabled.result
  - tests/integrationtest/t/collation_misc.test
  PR Summary: This is an automated cherry-pick of #52812 What problem does this PR solve? Problem Summary: If the new collation is disabled, we should not cast collation for in expression, which may lead to panic in the issue case. What changed and how does it work?
- Fix PR #52864: expression: don't cast collation for in expression is the new collation is disabled (#52812)
  URL: https://github.com/pingcap/tidb/pull/52864
  State: closed
  Merged At: 2024-04-24T11:06:12Z
  Changed Files Count: 4
  Main Modules: cmd/explaintest, planner/core
  Sample Changed Files:
  - cmd/explaintest/r/collation_misc_disabled.result
  - cmd/explaintest/r/collation_misc_enabled.result
  - cmd/explaintest/t/collation_misc.test
  - planner/core/expression_rewriter.go
  PR Summary: This is an automated cherry-pick of #52812 What problem does this PR solve? Problem Summary: If the new collation is disabled, we should not cast collation for in expression, which may lead to panic in the issue case. What changed and how does it work?
- Fix PR #53054: expression: don't cast collation for in expression is the new collation is disabled (#52812)
  URL: https://github.com/pingcap/tidb/pull/53054
  State: closed
  Merged At: 2024-05-21T08:31:24Z
  Changed Files Count: 4
  Main Modules: tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/expression_rewriter.go
  - tests/integrationtest/r/collation_misc_disabled.result
  - tests/integrationtest/r/collation_misc_enabled.result
  - tests/integrationtest/t/collation_misc.test
  PR Summary: This is an automated cherry-pick of #52812 What problem does this PR solve? Problem Summary: If the new collation is disabled, we should not cast collation for in expression, which may lead to panic in the issue case. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
