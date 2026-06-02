# Issue #50507: planner: set_var(fix_control) is incompatible with binding

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/50507
- Status: closed
- Type: type/bug
- Created At: 2024-01-17T08:44:55Z
- Closed At: 2024-01-18T03:52:48Z
- Labels: affects-7.5, epic/sql-plan-management, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #50515: parser: restore set_var value to string instead of plain text
  URL: https://github.com/pingcap/tidb/pull/50515
  State: closed
  Merged At: 2024-01-18T03:52:47Z
  Changed Files Count: 3
  Main Modules: pkg/parser, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/global_handle_test.go
  - pkg/parser/ast/misc.go
  - pkg/parser/parser_test.go
  PR Summary: What problem does this PR solve? Problem Summary: parser: restore set_var value to string instead of plain text What changed and how does it work?
- Fix PR #50536: parser: restore set_var value to string instead of plain text (#50515)
  URL: https://github.com/pingcap/tidb/pull/50536
  State: closed
  Merged At: 2024-02-20T13:03:56Z
  Changed Files Count: 5
  Main Modules: pkg/bindinfo, pkg/parser
  Sample Changed Files:
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/handle_test.go
  - pkg/bindinfo/tests/bind_test.go
  - pkg/parser/ast/misc.go
  - pkg/parser/parser_test.go
  PR Summary: This is an automated cherry-pick of #50515 What problem does this PR solve? Problem Summary: parser: restore set_var value to string instead of plain text What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
