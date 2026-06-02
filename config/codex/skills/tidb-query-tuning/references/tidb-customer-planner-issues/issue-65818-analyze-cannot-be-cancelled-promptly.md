# Issue #65818: Analyze cannot be cancelled promptly

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65818
- Status: closed
- Type: type/bug
- Created At: 2026-01-26T11:27:23Z
- Closed At: 2026-03-18T04:31:31Z
- Labels: affects-8.5, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- The analyze worker blocks on RPC/NextRaw; the job does not exit promptly after kill, and the analyze execution can hang.

## Linked PRs
- Fix PR #65249: executor: fix analyze cannot be killed
  URL: https://github.com/pingcap/tidb/pull/65249
  State: closed
  Merged At: 2026-03-18T04:31:29Z
  Changed Files Count: 11
  Main Modules: pkg/executor, pkg/distsql
  Sample Changed Files:
  - pkg/distsql/distsql.go
  - pkg/executor/analyze.go
  - pkg/executor/analyze_col.go
  - pkg/executor/analyze_col_sampling.go
  - pkg/executor/analyze_idx.go
  - pkg/executor/analyze_test.go
  - pkg/executor/analyze_utils.go
  - pkg/executor/table_reader.go
  - pkg/executor/test/analyzetest/BUILD.bazel
  - pkg/executor/test/analyzetest/analyze_test.go
  - pkg/executor/test/analyzetest/memorycontrol/memory_control_test.go
  PR Summary: What problem does this PR solve? Problem Summary: After #63067 removed the coprocessor-side periodic kill polling fallback in ,  started depending on the caller-provided context to stop blocked  / DistSQL work promptly. Several analyze paths still used  or did not propagate the same kill-aware context consistently through workers, merge loops, and result handling. As a result, a kill or cancellation could be observed before the RPC started, but some blocked analyze paths still could not exit promptly once they entered  / DistSQL. What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
