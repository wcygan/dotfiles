# Issue #65059: TiFlash plan returns `No access path` error in RC isolation level

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65059
- Status: closed
- Type: type/question
- Created At: 2025-12-16T03:37:35Z
- Closed At: 2025-12-29T07:23:42Z
- Labels: affects-8.5, component/tiflash, report/customer, sig/planner, type/question

## Customer-Facing Phenomenon
- ERROR 1815 (HY000): Internal : No access path for table 't1' is found with 'tidb_isolation_read_engines' = 'tidb,tiflash', valid values can be 'tikv'.

## Linked PRs
- Fix PR #65127: planner: fix no access path when TiKV read is disabled under RC isolation
  URL: https://github.com/pingcap/tidb/pull/65127
  State: closed
  Merged At: 2025-12-29T07:23:41Z
  Changed Files Count: 11
  Main Modules: pkg/planner/core, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/enforcempp/BUILD.bazel
  - pkg/planner/core/casetest/enforcempp/enforce_mpp_test.go
  - pkg/planner/core/casetest/tpch/BUILD.bazel
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_in.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_out.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_xut.json
  - pkg/planner/core/casetest/tpch/tpch_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/integration_test.go
  - pkg/planner/util/misc.go
  - tests/integrationtest/r/planner/core/integration.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Because we use RC isolation, so  is true. Here will not remove the tikv path.
- Fix PR #66951: planner: fix no access path when TiKV read is disabled under RC isolation (#65127)
  URL: https://github.com/pingcap/tidb/pull/66951
  State: closed
  Merged At: 2026-03-17T19:37:48Z
  Changed Files Count: 5
  Main Modules: pkg/planner/core, Makefile
  Sample Changed Files:
  - Makefile
  - pkg/planner/core/casetest/enforcempp/BUILD.bazel
  - pkg/planner/core/casetest/enforcempp/enforce_mpp_test.go
  - pkg/planner/core/find_best_task.go
  - pkg/planner/core/integration_test.go
  PR Summary: This is an automated cherry-pick of #65127 What problem does this PR solve? Problem Summary: What changed and how does it work? Because we use RC isolation, so  is true.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
