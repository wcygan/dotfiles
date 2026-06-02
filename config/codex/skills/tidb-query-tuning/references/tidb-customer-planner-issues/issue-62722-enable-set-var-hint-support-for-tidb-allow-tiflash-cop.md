# Issue #62722: Enable `set_var` Hint Support for `tidb_allow_tiflash_cop`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/62722
- Status: closed
- Type: type/enhancement
- Created At: 2025-07-30T13:32:01Z
- Closed At: 2025-09-17T15:27:07Z
- Labels: epic/hint, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Currently, has a default value of . This is because in most cases, we only want TiFlash to use the MPP protocol for execution, as MPP is almost always superior to the cop protocol. However, there is an exception: using the cop protocol allows for execution in "keep order" mode, meaning that queries like can be executed with the cop protocol and terminate early, similar to when using TiKV.

## Linked PRs
- Fix PR #63570: sessionctx: disable warning when setting tidb_allow_tiflash_cop in set_var hint
  URL: https://github.com/pingcap/tidb/pull/63570
  State: closed
  Merged At: 2025-09-17T15:27:06Z
  Changed Files Count: 3
  Main Modules: pkg/executor, pkg/session
  Sample Changed Files:
  - pkg/executor/test/tiflashtest/BUILD.bazel
  - pkg/executor/test/tiflashtest/tiflash_test.go
  - pkg/sessionctx/variable/setvar_affect.go
  PR Summary: What problem does this PR solve? Problem Summary: check What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
