# Issue #67467: enable semi_join_rewrite in multi alternative implementation

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67467
- Status: open
- Type: type/enhancement
- Created At: 2026-03-31T12:41:16Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- bad plan In real customer env, the final result is zero(IndexJoin_181 output 0 rows), most of time is spent to compute the outer side of , because will keep all rows from , and is a very large table(almost 3,000,000 rows after the filter of .

## Linked PRs
- Fix PR #67497: pkg/planner: support semi join rewrite as an alternative logical plan
  URL: https://github.com/pingcap/tidb/pull/67497
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core, pkg/planner, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/rule_outer_to_semi_join_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/optimize.go
  - pkg/sessionctx/stmtctx/stmtctx.go
  PR Summary: What problem does this PR solve? Problem Summary:   The alternative logical plan framework introduced by #66995 can explore a non-decorrelated path and compare physical costs, but it cannot explore the semi-join rewrite path unless the query explicitly uses  or the session variable  is enabled. That means the optimizer may still miss a cheaper plan shape for  /  subqueries when semi-join rewrite is beneficial but not explicitly requested. What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
