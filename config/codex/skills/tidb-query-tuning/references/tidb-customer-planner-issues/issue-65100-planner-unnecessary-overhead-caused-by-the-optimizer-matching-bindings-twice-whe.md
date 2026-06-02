# Issue #65100: planner: unnecessary overhead caused by the optimizer matching bindings twice when plan cache miss

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65100
- Status: closed
- Type: type/enhancement
- Created At: 2025-12-17T12:46:23Z
- Closed At: 2026-01-13T19:55:09Z
- Labels: affects-8.5, epic/plan-cache, report/customer, sig/planner, type/enhancement, type/performance

## Customer-Facing Phenomenon
- See the picture below, the optimizer calls twice when getting the cached plan, which could bring us some unnecessary overhead:

## Linked PRs
- Fix PR #65104: planner: plan cache performance optimization | tidb-test=86a1cff755f507d127f0bca7ff18e2f3b9537124
  URL: https://github.com/pingcap/tidb/pull/65104
  State: closed
  Merged At: 2025-12-18T01:46:34Z
  Changed Files Count: 7
  Main Modules: pkg/session, pkg/planner/core, pkg/bindinfo, pkg/executor
  Sample Changed Files:
  - pkg/bindinfo/binding_match.go
  - pkg/executor/select.go
  - pkg/planner/core/plan_cache_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/sessionctx/stmtctx/stmtctx.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #65484: bindinfo: save bindinfo into stmtctx to avoid calling NormalizeStmtForBinding and getbindcache repeatedly
  URL: https://github.com/pingcap/tidb/pull/65484
  State: closed
  Merged At: 2026-01-13T19:55:08Z
  Changed Files Count: 11
  Main Modules: pkg/bindinfo, pkg/planner/core, .bazelrc, pkg/executor, pkg/session
  Sample Changed Files:
  - .bazelrc
  - pkg/bindinfo/binding.go
  - pkg/bindinfo/binding_cache_test.go
  - pkg/bindinfo/session_handle_test.go
  - pkg/bindinfo/tests/cross_db_binding_test.go
  - pkg/executor/select.go
  - pkg/planner/core/casetest/plancache/BUILD.bazel
  - pkg/planner/core/casetest/plancache/plan_cache_test.go
  - pkg/planner/core/integration_partition_test.go
  - pkg/planner/core/plan_cache_utils.go
  - pkg/sessionctx/stmtctx/stmtctx.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? save bindinfo into stmtctx to avoid calling NormalizeStmtForBinding and getbindcache repeatedly. This PR is an improvement for
- Related PR #65524: planner: add some plan cache benchmark into bench daily
  URL: https://github.com/pingcap/tidb/pull/65524
  State: closed
  Merged At: 2026-01-12T05:58:56Z
  Changed Files Count: 1
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/integration_partition_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? planner: add some plan cache benchmark into bench daily

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
