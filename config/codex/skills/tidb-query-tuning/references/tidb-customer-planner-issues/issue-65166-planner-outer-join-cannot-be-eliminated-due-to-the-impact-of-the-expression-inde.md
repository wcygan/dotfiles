# Issue #65166: planner: outer join cannot be eliminated due to the impact of the expression index

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65166
- Status: closed
- Type: type/bug
- Created At: 2025-12-22T10:05:56Z
- Closed At: 2026-01-05T18:27:15Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, plan-rewrite, report/customer, severity/moderate, sig/planner, type/bug

## Customer-Facing Phenomenon
- See the example below: See the case above, the outer join  is not eliminated at first place, but after putting the force index hint on , we can eliminate it. The problem is that the expression index affects the  when eliminating outer join and causes us to stop eliminating early (see the picture below): If  is a normal index instead of an expression index, the outer join elimination can also work:

## Linked PRs
- Fix PR #65187: planner: outer join cannot be eliminated due to the impact of the expression index | tidb-test=pr/2657
  URL: https://github.com/pingcap/tidb/pull/65187
  State: closed
  Merged At: 2026-01-05T18:27:14Z
  Changed Files Count: 19
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_out.json
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_xut.json
  - pkg/planner/core/casetest/cascades/testdata/cascades_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_out.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_xut.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/rule_eliminate_projection.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - tests/integrationtest/r/planner/cascades/integration.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_result_reorder.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  PR Summary: What problem does this PR solve? Problem Summary: [65166](planner: outer join cannot be eliminated due to the impact of the expression index) What changed and how does it work? Please see  for more details.
- Fix PR #65425: planner: outer join cannot be eliminated due to the impact of the expression index | tidb-test=pr/2657 (#65187)
  URL: https://github.com/pingcap/tidb/pull/65425
  State: closed
  Merged At: not merged
  Changed Files Count: 19
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_out.json
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_xut.json
  - pkg/planner/core/casetest/cascades/testdata/cascades_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_out.json
  - pkg/planner/core/casetest/cbotest/testdata/analyze_suite_xut.json
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_out.json
  - pkg/planner/core/casetest/tpch/testdata/tpch_suite_xut.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/rule_eliminate_projection.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - tests/integrationtest/r/planner/cascades/integration.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_result_reorder.result
  - tests/integrationtest/r/planner/core/indexjoin.result
  - tests/integrationtest/r/planner/core/plan_cache.result
  - tests/integrationtest/r/planner/core/rule_constant_propagation.result
  PR Summary: This is an automated cherry-pick of #65187 What problem does this PR solve? Problem Summary: [65166](planner: outer join cannot be eliminated due to the impact of the expression index) What changed and how does it work? Please see  for more details.
- Fix PR #65449: planner: outer join cannot be eliminated due to the impact of the expression index
  URL: https://github.com/pingcap/tidb/pull/65449
  State: closed
  Merged At: not merged
  Changed Files Count: 1825
  Main Modules: br/pkg, pkg/executor, pkg/planner/core, pkg/ddl, tests/integrationtest, pkg/statistics
  Sample Changed Files:
  - .bazelrc
  - .bazelversion
  - DEPS.bzl
  - Makefile
  - Makefile.common
  - OWNERS
  - OWNERS_ALIASES
  - WORKSPACE
  - br/cmd/br/BUILD.bazel
  - br/cmd/br/abort.go
  - br/cmd/br/backup.go
  - br/cmd/br/cmd.go
  - br/cmd/br/debug.go
  - br/cmd/br/main.go
  - br/cmd/br/operator.go
  - br/cmd/br/restore.go
  - br/metrics/grafana/br.json
  - br/pkg/backup/BUILD.bazel
  - br/pkg/backup/check.go
  - br/pkg/backup/client.go
  PR Summary: This is an automated cherry-pick of #65187 What problem does this PR solve? Problem Summary: [65166](planner: outer join cannot be eliminated due to the impact of the expression index) What changed and how does it work? Please see  for more details.
- Fix PR #65450: planner: outer join cannot be eliminated due to the impact of the expression index
  URL: https://github.com/pingcap/tidb/pull/65450
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/binaryplan/testdata/binary_plan_suite_out.json
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/rule_eliminate_projection.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/index_merge.result
  PR Summary: This is an automated cherry-pick of #65187 What problem does this PR solve? Problem Summary: [65166](planner: outer join cannot be eliminated due to the impact of the expression index) What changed and how does it work? Please see  for more details.

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
