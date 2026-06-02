# Issue #65381: planner: the optimizer can't use the latest `tidb_mem_quota_binding_cache` value to initialize binding cache

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65381
- Status: closed
- Type: type/bug
- Created At: 2026-01-02T03:34:13Z
- Closed At: 2026-01-04T07:26:42Z
- Labels: affects-7.5, affects-8.5, component/spm, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Step 1: create massive bindings, and their total memory usage is larger than the default binding cache size 64MB Step 2: restart TiDB and we'll see errors like Step 3: increase the binding cache size through Step 4: restart TiDB again, there should be no binding cache errors.

## Linked PRs
- Fix PR #65382: planner: fix the issue that the optimizer can't use the latest system value to initialize binding cache | tidb-test=86a1cff755f507d127f0bca7ff18e2f3b9537124
  URL: https://github.com/pingcap/tidb/pull/65382
  State: closed
  Merged At: 2026-01-02T05:12:47Z
  Changed Files Count: 1
  Main Modules: pkg/session
  Sample Changed Files:
  - pkg/session/session.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue that the optimizer can't use the latest tidb_mem_quota_binding_cache value to initialize binding cache What changed and how does it work? Just move the initialization of binding cache after the initialization of system variables. This case is hard to add unit tests since it's about Bootstrap.
- Fix PR #65392: planner: fix the issue that the optimizer can't use the latest system value to initialize binding cache
  URL: https://github.com/pingcap/tidb/pull/65392
  State: closed
  Merged At: 2026-01-04T07:26:41Z
  Changed Files Count: 1
  Main Modules: pkg/session
  Sample Changed Files:
  - pkg/session/session.go
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue that the optimizer can't use the latest system value to initialize binding cache What changed and how does it work? We have to initialize Binding Handle after initializing Sysvars, since the optimizer need to use the SQL variable  to set up the binding cache size. In our prior implementation, the optimizer can't get the latest value of this variable when initializing binding cache. This is hard to add unit tests since it's related to TiDB bootstrap. But I tested it locally and this PR can work.
- Fix PR #65397: planner: fix the issue that the optimizer can't use the latest system value to initialize binding cache (#65392)
  URL: https://github.com/pingcap/tidb/pull/65397
  State: closed
  Merged At: 2026-01-06T15:58:32Z
  Changed Files Count: 1
  Main Modules: pkg/session
  Sample Changed Files:
  - pkg/session/session.go
  PR Summary: This is an automated cherry-pick of #65392 What problem does this PR solve? Problem Summary: planner: fix the issue that the optimizer can't use the latest system value to initialize binding cache What changed and how does it work? We have to initialize Binding Handle after initializing Sysvars, since the optimizer need to use the SQL variable  to set up the binding cache size. In our prior implementation, the optimizer can't get the latest value of this variable when initializing binding cache.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
