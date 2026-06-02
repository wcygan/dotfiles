# Issue #67363: planner: better binding matching mechanism

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67363
- Status: open
- Type: type/enhancement
- Created At: 2026-03-27T08:27:00Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- See the example below, the second query can't hit the binding because is wrapped by , so it has a different SQL digest. It's better to loose the matching mechanism and allow the second query to hit the binding as well:

## Linked PRs
- Fix PR #67532: planner: normalize redundant WHERE parentheses for binding matching
  URL: https://github.com/pingcap/tidb/pull/67532
  State: open
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/session, pkg/parser, tests/integrationtest, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/binding_operator_test.go
  - pkg/parser/digester.go
  - pkg/parser/digester_test.go
  - pkg/session/BUILD.bazel
  - pkg/session/bootstrap_test.go
  - pkg/session/upgrade_def.go
  - tests/integrationtest/r/planner/core/physical_plan.result
  - tests/integrationtest/r/planner/core/rule_join_reorder.result
  PR Summary: What problem does this PR solve? Problem Summary: planner: normalize redundant WHERE parentheses for binding matching What changed and how does it work? Strip redundant outer wrappers in  conditions during binding digest normalization. Example:  ->

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
