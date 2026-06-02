# Issue #67815: Optimize Prepared Stmt build process

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67815
- Status: open
- Type: type/enhancement
- Created At: 2026-04-16T08:25:26Z
- Labels: affects-8.5, epic/plan-cache, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- For applications that follow the pattern below(i.e., a 1:1 ratio between prepare and execute). As show from the above image, building prepare statement consume almost 17% of CPU usage. We check whether the prepare-statement has been executed before, if yes, we could skip this execution to save some CPU.

## Linked PRs
- Fix PR #67820: *: support cache prepared statement in plan cache
  URL: https://github.com/pingcap/tidb/pull/67820
  State: open
  Merged At: not merged
  Changed Files Count: 11
  Main Modules: pkg/session, tests/integrationtest, pkg/planner/core, pkg/server
  Sample Changed Files:
  - pkg/planner/core/plan_cache_utils.go
  - pkg/server/internal/testserverclient/server_client.go
  - pkg/session/session.go
  - pkg/session/test/common/BUILD.bazel
  - pkg/session/test/common/prepare_dedup_cache_test.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  - tests/integrationtest/r/sessionctx/setvar.result
  - tests/integrationtest/t/sessionctx/setvar.test
  PR Summary: What problem does this PR solve? Problem Summary:   CPU profiling showed  consuming ~21% of total CPU in workloads using the prepare-per-request pattern (COM_STMT_PREPARE → COM_STMT_EXECUTE → COM_STMT_CLOSE per request with the same SQL). Each Prepare redundantly executed Parse + Preprocess + PlanBuilder.Build for identical SQL text within the same session. What changed and how does it work?
- Fix PR #67857: *: support cache prepared statement in plan cache
  URL: https://github.com/pingcap/tidb/pull/67857
  State: closed
  Merged At: 2026-04-18T09:23:03Z
  Changed Files Count: 11
  Main Modules: pkg/session, tests/integrationtest, pkg/planner/core, pkg/server
  Sample Changed Files:
  - pkg/planner/core/plan_cache_utils.go
  - pkg/server/internal/testserverclient/server_client.go
  - pkg/session/session.go
  - pkg/session/test/common/BUILD.bazel
  - pkg/session/test/common/prepare_dedup_cache_test.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/setvar_affect.go
  - pkg/sessionctx/variable/sysvar.go
  - pkg/sessionctx/variable/tidb_vars.go
  - tests/integrationtest/r/sessionctx/setvar.result
  - tests/integrationtest/t/sessionctx/setvar.test
  PR Summary: What problem does this PR solve? Problem Summary:   CPU profiling showed  consuming ~21% of total CPU in workloads using the prepare-per-request pattern (COM_STMT_PREPARE → COM_STMT_EXECUTE → COM_STMT_CLOSE per request with the same SQL). Each Prepare redundantly executed Parse + Preprocess + PlanBuilder.Build for identical SQL text within the same session. What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
