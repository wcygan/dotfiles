# Issue #63805: Prepare query with ORDER BY clause does not work with sql binding

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/63805
- Status: open
- Type: type/bug
- Created At: 2025-09-29T10:47:13Z
- Labels: affects-8.5, good first issue, help wanted, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The binding doesn't work.

## Linked PRs
- Fix PR #63903: planner: fix binding usage for prepare query with order by clause
  URL: https://github.com/pingcap/tidb/pull/63903
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/bindinfo, pkg/util
  Sample Changed Files:
  - pkg/bindinfo/binding_operator_test.go
  - pkg/bindinfo/session_handle_test.go
  - pkg/util/parser/ast.go
  PR Summary: What problem does this PR solve? Problem Summary: Using prepare statement with ORDER BY doesn't use bindings What changed and how does it work? Possible bindings are selected by comparing the normalized statement for the binding with the current running statement. Since the prepared statements are stored based on the plan from , there is additional handling in  which changes the  in the AST.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
