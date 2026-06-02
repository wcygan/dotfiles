# Issue #64329: "xxxx IS NULL" prevent the optimizer from choosing the best join order and IndexJoin

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64329
- Status: closed
- Type: type/bug
- Created At: 2025-11-06T14:37:21Z
- Closed At: 2026-01-20T13:48:49Z
- Labels: plan-rewrite, planner/join-order, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- If there is no , the plan is:

## Linked PRs
- Fix PR #64959: planner: support left outer join into anti semi join | tidb-test=pr/2649
  URL: https://github.com/pingcap/tidb/pull/64959
  State: closed
  Merged At: 2026-01-20T13:48:47Z
  Changed Files Count: 12
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/rule/BUILD.bazel
  - pkg/planner/core/casetest/rule/main_test.go
  - pkg/planner/core/casetest/rule/rule_outer_to_semi_join_test.go
  - pkg/planner/core/casetest/rule/testdata/outer_to_semi_join_suite_in.json
  - pkg/planner/core/casetest/rule/testdata/outer_to_semi_join_suite_out.json
  - pkg/planner/core/casetest/rule/testdata/outer_to_semi_join_suite_xut.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule/BUILD.bazel
  - pkg/planner/core/rule/logical_rules.go
  - pkg/planner/core/rule/rule_outer_join_to_semi_join.go
  - tests/integrationtest/r/topn_push_down.result
  PR Summary: What problem does this PR solve? Problem Summary: planner: support left outer join into anti semi join What changed and how does it work? This PR introduces two optimization patterns for transforming LEFT JOIN queries into NOT EXISTS subqueries when checking for missing matches. Scenario 1: IS NULL on the Join Condition Column

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
