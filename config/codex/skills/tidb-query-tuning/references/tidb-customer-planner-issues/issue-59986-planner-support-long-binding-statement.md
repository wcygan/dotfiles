# Issue #59986: planner: support long binding statement

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59986
- Status: closed
- Type: type/enhancement
- Created At: 2025-03-10T08:04:29Z
- Closed At: 2025-03-12T10:46:51Z
- Labels: epic/sql-plan-management, impact/upgrade, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- At least we can update its type to , which can support SQL with a maximum length of .

## Linked PRs
- Fix PR #60007: planner: update bind_info binding columns from TEXT to LONGTEXT to support long bindings
  URL: https://github.com/pingcap/tidb/pull/60007
  State: closed
  Merged At: 2025-03-12T10:46:50Z
  Changed Files Count: 4
  Main Modules: pkg/bindinfo, br/pkg, pkg/session
  Sample Changed Files:
  - br/pkg/restore/snap_client/systable_restore_test.go
  - pkg/bindinfo/BUILD.bazel
  - pkg/bindinfo/binding_operator_test.go
  - pkg/session/bootstrap.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: update bind_info binding columns from TEXT to LONGTEXT to support long bindings What changed and how does it work? planner: update bind_info binding columns from TEXT to LONGTEXT to support long bindings

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
