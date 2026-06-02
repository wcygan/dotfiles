# Issue #67366: planner: output a warning if implicit join key type conversion happend

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67366
- Status: open
- Type: type/enhancement
- Created At: 2026-03-27T08:35:34Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Enhancement See the example below, MySQL outputs some warnings to notify the user of the implicit type conversion on , but TiDB doesn't have such warnings:

## Linked PRs
- Fix PR #67372: planner: warn on implicit join-key type/collation conversion | tidb-test=pr/2718
  URL: https://github.com/pingcap/tidb/pull/67372
  State: closed
  Merged At: 2026-04-03T16:25:02Z
  Changed Files Count: 2
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/join/join_test.go
  - pkg/planner/core/operator/logicalop/logical_join.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: warn on implicit join-key type/collation conversion What changed and how does it work? TiDB may implicitly cast join keys with different types/collations (for example ), which can make indexes unusable without visible warning. Add planner warning when join key normalization detects implicit cast-based conversion on join keys.
- Fix PR #67433: planner: Implicit cast index join | tidb-test=pr/2721
  URL: https://github.com/pingcap/tidb/pull/67433
  State: closed
  Merged At: 2026-04-07T23:46:42Z
  Changed Files Count: 13
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/dag/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/dag/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/join/join_test.go
  - pkg/planner/core/casetest/rule/testdata/outer2inner_out.json
  - pkg/planner/core/casetest/rule/testdata/outer2inner_xut.json
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/rule/BUILD.bazel
  - pkg/planner/core/rule/logical_rules.go
  - pkg/planner/core/rule/rule_join_key_type_cast.go
  - tests/integrationtest/r/planner/core/join_key_type_cast.result
  - tests/integrationtest/t/planner/core/join_key_type_cast.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #67470: planner: Implicit cast varchar local (WIP)
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
