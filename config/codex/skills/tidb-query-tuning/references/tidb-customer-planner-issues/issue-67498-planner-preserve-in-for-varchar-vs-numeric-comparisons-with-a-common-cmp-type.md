# Issue #67498: planner: preserve IN for varchar-vs-numeric comparisons with a common cmp type

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67498
- Status: open
- Type: type/bug
- Created At: 2026-04-01T13:36:46Z
- Labels: component/expression, may-affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- TiDB rewrites the  predicate into a DNF of equality predicates: For long  lists this produces a very large expression tree in the planner, even though every element uses the same comparison type. Warning: even after this planner fix,  is still a non-ideal SQL shape for index usage. The comparison has to follow MySQL's mixed-type semantics and usually cannot use the string index as efficiently as a type-aligned predicate. Users should still align the literal type with the column type whenever possible, for example compare  columns with string literals instead of numeric literals. The root cause is that  is only preserved when the comparison type is exactly the left operand's eval type. In this case the comparison type is consistently , but the left operand is , so TiDB unnecessarily expands it to OR-of-EQ.

## Linked PRs
- Fix PR #67499: planner: preserve IN for common mixed-type comparisons | tidb-test=pr/2723
  URL: https://github.com/pingcap/tidb/pull/67499
  State: open
  Merged At: not merged
  Changed Files Count: 9
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/executor, pkg/util
  Sample Changed Files:
  - pkg/executor/prepared_test.go
  - pkg/planner/core/casetest/integration_test.go
  - pkg/planner/core/casetest/plancache/plan_cache_suite_test.go
  - pkg/planner/core/expression_rewriter.go
  - pkg/util/ranger/ranger_test.go
  - tests/integrationtest/r/executor/executor.result
  - tests/integrationtest/r/planner/core/casetest/point_get_plan.result
  - tests/integrationtest/t/executor/executor.test
  - tests/integrationtest/t/planner/core/casetest/point_get_plan.test
  PR Summary: What problem does this PR solve? Problem Summary: For mixed-type predicates such as , TiDB currently expands  into a large DNF of  even when every element shares the same comparison type with the left operand. This is semantically unnecessary and makes generated SQL with long  lists much harder for the planner to process. What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
