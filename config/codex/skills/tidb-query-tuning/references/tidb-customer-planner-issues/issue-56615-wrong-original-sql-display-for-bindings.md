# Issue #56615: Wrong Original_sql display for bindings

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56615
- Status: open
- Type: type/enhancement
- Created At: 2024-10-12T08:41:55Z
- Labels: affects-6.5, report/customer, severity/moderate, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- It's better to display Orignal_sql as:

## Linked PRs
- Fix PR #64793: [DNM]bindinfo: fix wrong origin sql
  URL: https://github.com/pingcap/tidb/pull/64793
  State: open
  Merged At: not merged
  Changed Files Count: 17
  Main Modules: pkg/bindinfo, tests/integrationtest, pkg/planner/core
  Sample Changed Files:
  - pkg/bindinfo/binding.go
  - pkg/bindinfo/binding_auto.go
  - pkg/bindinfo/binding_cache.go
  - pkg/bindinfo/binding_cache_test.go
  - pkg/bindinfo/binding_operator_test.go
  - pkg/bindinfo/session_handle.go
  - pkg/bindinfo/session_handle_test.go
  - pkg/bindinfo/tests/bind_test.go
  - pkg/planner/core/issuetest/BUILD.bazel
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/preprocess.go
  - tests/integrationtest/r/bindinfo/bind.result
  - tests/integrationtest/r/executor/executor.result
  - tests/integrationtest/r/planner/core/integration.result
  - tests/integrationtest/r/planner/core/physical_plan.result
  - tests/integrationtest/r/planner/core/rule_join_reorder.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
