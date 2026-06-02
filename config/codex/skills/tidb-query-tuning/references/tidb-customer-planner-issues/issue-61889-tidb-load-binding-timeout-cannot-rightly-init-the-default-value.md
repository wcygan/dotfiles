# Issue #61889: tidb_load_binding_timeout cannot rightly init the default value

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/61889
- Status: closed
- Type: type/bug
- Created At: 2025-06-20T09:09:06Z
- Closed At: 2025-06-23T04:21:49Z
- Labels: affects-8.1, affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- As the log shows, The duration is . it is not expected. and the user doesn't update this value. so I add a assert into the problem place and CI report the panic at here. This indicates that there indeed is an issue here.

## Linked PRs
- Fix PR #61891: planner: fix uninit timeout for loading bindings
  URL: https://github.com/pingcap/tidb/pull/61891
  State: closed
  Merged At: 2025-06-23T04:21:48Z
  Changed Files Count: 2
  Main Modules: pkg/session
  Sample Changed Files:
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? as the code show, the old code cannot init the right value for Currently,this switch is actually ineffective on the master branch.However,to comply with the process standards,it will still be merged into master first.But please refer to [this PR]() for the tests.
- Fix PR #61926: planner: fix uninit timeout for loading bindings (#61891)
  URL: https://github.com/pingcap/tidb/pull/61926
  State: open
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/session, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/global_handle.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  PR Summary: This is an automated cherry-pick of #61891 What problem does this PR solve? Problem Summary: What changed and how does it work? as the code show, the old code cannot init the right value for
- Fix PR #61928: planner: fix uninit timeout for loading bindings (#61891)
  URL: https://github.com/pingcap/tidb/pull/61928
  State: closed
  Merged At: 2025-07-09T16:05:10Z
  Changed Files Count: 4
  Main Modules: pkg/session, pkg/bindinfo
  Sample Changed Files:
  - pkg/bindinfo/global_handle.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  PR Summary: This is an automated cherry-pick of #61891 What problem does this PR solve? Problem Summary: What changed and how does it work? as the code show, the old code cannot init the right value for

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
