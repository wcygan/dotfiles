# Issue #67610: planner: inaccurate cost model for `HashAgg+IndexJoin` vs `HashAgg+HashJoin`

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67610
- Status: open
- Type: type/enhancement
- Created At: 2026-04-08T08:04:01Z
- Labels: affects-8.5, epic/cost-model, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Use the script below to reproduce this case, now see the 2 plans below directly: is 2x faster than , but cost is 5x better than the , the cost model is not working well for this case.

## Linked PRs
- Fix PR #67646: planner/core: discourage degenerate index joins when probe rows approach a full scan
  URL: https://github.com/pingcap/tidb/pull/67646
  State: open
  Merged At: not merged
  Changed Files Count: 11
  Main Modules: pkg/planner/core, pkg/session
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/cbotest/testdata/stats.zip
  - pkg/planner/core/operator/physicalop/physical_utils.go
  - pkg/planner/core/plan_cost_ver2.go
  - pkg/planner/core/plan_cost_ver2_test.go
  - pkg/sessionctx/vardef/tidb_vars.go
  - pkg/sessionctx/variable/session.go
  - pkg/sessionctx/variable/sysvar.go
  PR Summary: What problem does this PR solve? Problem Summary:   When  or  is estimated to probe a large number of inner rows, the optimizer may still prefer it over , even though the index join has already degenerated into a near full-scan pattern and can be slower in practice. What changed and how does it work? This PR introduces a new optimizer sysvar: 

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
