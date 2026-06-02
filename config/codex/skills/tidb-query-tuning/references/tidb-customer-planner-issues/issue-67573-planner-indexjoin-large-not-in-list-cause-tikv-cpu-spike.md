# Issue #67573: planner: IndexJoin + large not-in list cause TiKV CPU spike

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/67573
- Status: open
- Type: type/enhancement
- Created At: 2026-04-06T03:12:26Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Below is the TiKV CPU Profile, a large amount of CPU is spent on decoding requests and building executors, because the not-in list is too large.

## Linked PRs
- Related PR #67475: planner: simplify grouped max/min having on constant args
  URL: https://github.com/pingcap/tidb/pull/67475
  State: closed
  Merged At: 2026-04-04T10:57:57Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/resourcegroup
  Sample Changed Files:
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/operator/logicalop/logical_aggregation.go
  - pkg/resourcegroup/tests/BUILD.bazel
  PR Summary: What problem does this PR solve? Problem Summary: Some generated queries can end up with grouped , for example when a generic aggregation template wraps an expression that no longer depends on input rows after parameterization or simplification. For grouped non-empty results,  of such an expression
- Fix PR #67574: planner: compress large not-in filters for index join probe
  URL: https://github.com/pingcap/tidb/pull/67574
  State: open
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, pkg/resourcegroup
  Sample Changed Files:
  - pkg/planner/core/casetest/cbotest/cbo_test.go
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_in.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/operator/logicalop/logical_aggregation.go
  - pkg/resourcegroup/tests/BUILD.bazel
  PR Summary: What problem does this PR solve? Problem Summary: can amplify the cost of a large  list on the probe side. In the problematic shape from , the join key still uses point lookups on , but the probe-side keeps a very large  expression on another column such as . That
- Fix PR #67597: planner/core: keep large IN-list probe predicates on root for IndexJoin
  URL: https://github.com/pingcap/tidb/pull/67597
  State: closed
  Merged At: 2026-04-16T19:36:22Z
  Changed Files Count: 3
  Main Modules: pkg/planner/core
  Sample Changed Files:
  - pkg/planner/core/casetest/join/join_test.go
  - pkg/planner/core/exhaust_physical_plans.go
  - pkg/planner/core/find_best_task.go
  PR Summary: What problem does this PR solve? Problem Summary: pkg/planner/core: keep large IN-list probe predicates on root for IndexJoin What changed and how does it work? Add a fixed guardrail () for IndexJoin probe-side residual predicates. When a probe-side predicate contains a large  list and does not affect access range construction, do not push it to coprocessor; keep it in TiDB root task.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
