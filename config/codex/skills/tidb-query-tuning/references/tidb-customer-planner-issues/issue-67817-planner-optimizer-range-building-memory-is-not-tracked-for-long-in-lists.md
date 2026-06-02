# Issue #67817: planner: optimizer range building memory is not tracked for long IN lists

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67817
- Status: open
- Type: type/bug
- Created At: 2026-04-16T08:45:01Z
- Labels: report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The memory used during optimizer range-point/range construction is not consistently recorded by the SQL/session . As a result, when a long  list causes high transient memory usage during optimization, OOM alarm/top SQL diagnostics can miss or underreport the SQL responsible.  may prevent some range explosion cases by falling back, but that is separate from memory attribution, and the cached-plan range rebuild path currently bypasses that limit by passing .

## Linked PRs
- Fix PR #67834: session, ranger: attribute range-build memory to stmt tracker
  URL: https://github.com/pingcap/tidb/pull/67834
  State: open
  Merged At: not merged
  Changed Files Count: 12
  Main Modules: pkg/util, pkg/session, pkg/executor, tests/integrationtest
  Sample Changed Files:
  - pkg/executor/partition_table_test.go
  - pkg/session/session.go
  - pkg/session/test/variable/variable_test.go
  - pkg/util/ranger/BUILD.bazel
  - pkg/util/ranger/context/BUILD.bazel
  - pkg/util/ranger/context/context.go
  - pkg/util/ranger/context/context_test.go
  - pkg/util/ranger/memory_test.go
  - pkg/util/ranger/points.go
  - pkg/util/ranger/ranger.go
  - pkg/util/ranger/ranger_test.go
  - tests/integrationtest/r/executor/executor.result
  PR Summary: What problem does this PR solve? Problem Summary: Long  lists can allocate a large amount of memory while the optimizer builds ranger points and ranges, but that memory is not attributed to the statement tracker today. On fresh , a focused probe still showed large planner-side allocations for  while  stayed at . What changed and how does it work? Pass  into  from .

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
