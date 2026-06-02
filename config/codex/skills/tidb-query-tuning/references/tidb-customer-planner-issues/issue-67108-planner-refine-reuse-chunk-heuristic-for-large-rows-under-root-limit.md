# Issue #67108: planner: refine reuse chunk heuristic for large rows under root Limit

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67108
- Status: closed
- Type: type/enhancement
- Created At: 2026-03-18T06:30:37Z
- Closed At: 2026-03-27T14:24:49Z
- Labels: affects-8.5, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- This issue came from a customer workload even though the GitHub issue does not carry the `report/customer` label. The planner-side reuse-chunk heuristic was still too conservative for some wide-row queries that were effectively bounded on the TiDB root side, especially under a root `Limit`. TiDB disabled chunk reuse too early for bounded overlong-type plans, which increased per-query allocations, triggered more frequent Go GC, and drove higher CPU usage even when the retained reusable-chunk footprint would still have been small enough to be safe.

## Linked PRs
- Fix PR #67235: planner: refine reuse chunk gating for overlong types
  URL: https://github.com/pingcap/tidb/pull/67235
  State: closed
  Merged At: 2026-03-27T14:24:48Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/physicalplantest/physical_plan_test.go
  - pkg/planner/core/optimizer.go
  - pkg/planner/core/optimizer_test.go
  PR Summary: What problem does this PR solve? Problem Summary: `disableReuseChunkIfNeeded` still disables chunk reuse for some bounded overlong-type queries even when the reusable chunk footprint is small enough to be safe. This causes avoidable allocations, more frequent Go GC, and higher CPU usage. What changed and how does it work? Refine the overlong-type reuse-chunk gate to estimate retained reusable-chunk memory for bounded overlong columns, keep the conservative behavior for unbounded large types, and only take the relaxed path when the row bound and stats are trustworthy.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
- Treat this file as a customer-origin planner case that is intentionally kept in the corpus even though the upstream issue is missing the `report/customer` label.
- Investigation clue: check `@@last_sql_use_alloc` during triage. A value of `0` is a useful signal that chunk reuse was disabled for the last statement. In this workload pattern, that can correlate with higher allocation pressure, slower compile paths, more frequent Go GC, and higher CPU usage.
