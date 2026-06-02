# Issue #67701: planner: mismatched integer and varchar value types prevent the optimizer from choosing index range scan

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67701
- Status: open
- Type: type/enhancement
- Created At: 2026-04-11T01:29:42Z
- Labels: plan-rewrite, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Need to also consider Plan Cache:

## Linked PRs
- Fix PR #67702: planner: mismatched integer and varchar value types prevent the optimizer from choosing index range scan
  URL: https://github.com/pingcap/tidb/pull/67702
  State: closed
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/util, pkg/planner/core, tests/realtikvtest
  Sample Changed Files:
  - pkg/planner/core/casetest/integration_test.go
  - pkg/planner/core/casetest/plancache/plan_cache_suite_test.go
  - pkg/util/ranger/checker.go
  - pkg/util/ranger/detacher.go
  - pkg/util/ranger/points.go
  - tests/realtikvtest/addindextest4/BUILD.bazel
  PR Summary: What problem does this PR solve? Problem Summary: planner: mismatched integer and varchar value types prevent the optimizer from choosing index range scan What changed and how does it work?
- Related PR #67470: planner: Implicit cast varchar local (WIP)
  URL: https://github.com/pingcap/tidb/pull/67470
  State: open
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/rule/rule_join_key_type_cast.go
  - tests/integrationtest/r/planner/core/join_key_type_cast.result
  - tests/integrationtest/t/planner/core/join_key_type_cast.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
