# Issue #59652: Rewrite exprs like `a = 10 or a = 20 or a = 30 ...` to `a in (10,20,30)` for better expr evaluation performance in the execution engine

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59652
- Status: open
- Type: type/enhancement
- Created At: 2025-02-19T16:56:59Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Currently, if conditions are not converted to index ranges, they will be evaluated in the operator unchanged. However, for expressions like , it's better to convert it to , especially when there are lots of values. It's because: 1. The structure of the first expression is more complicated. Each expression is an independent expression, and they are connected by expressions, which can connect two expressions at once. The expression has a more compact structure. 2. We have implemented more optimizations for the expression, like According to members of the execution engine team, the performance of is better than connected by in tidb, tikv, and tiflash.

## Linked PRs
- Fix PR #63141: planner: Fix issue #59652: convert OR to IN predicate. 
  URL: https://github.com/pingcap/tidb/pull/63141
  State: closed
  Merged At: not merged
  Changed Files Count: 4
  Main Modules: tests/integrationtest, pkg/ddl, pkg/planner/core
  Sample Changed Files:
  - pkg/ddl/ingest/BUILD.bazel
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - tests/integrationtest/r/planner/core/casetest/predicate_simplification.result
  - tests/integrationtest/t/planner/core/casetest/predicate_simplification.test
  PR Summary: What problem does this PR solve? Problem Summary: Initial motivation in  is that IN list equivalent to OR list produce better outcomes with index-selection and producing a unified canonical form using IN list produce better plans and make it consistent. What changed and how does it work? Predicate simplification is extended to convert OR list to IN list as the last rewrite. This uncovered other limitations in predicate simplification that does not cover IN list and IR list equally. Additional changes were made: (1) flip flop between OR and IN lists to make sure existing prediate simplification is applied fully. (2) Use equivalance classes to support simplification. For example a1=a2 and a2 in (1,2,3) and a1 > 2 should simplify to a1=a2 and a1=3 and a2=3.
- Fix PR #63162: planner: Convert OR to IN predicate | tidb-test=pr/2588
  URL: https://github.com/pingcap/tidb/pull/63162
  State: open
  Merged At: not merged
  Changed Files Count: 29
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/executor
  Sample Changed Files:
  - pkg/executor/explainfor_test.go
  - pkg/executor/sortexec/parallel_sort_test.go
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_out.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - pkg/planner/core/testdata/index_merge_suite_out.json
  - pkg/planner/core/testdata/index_merge_suite_xut.json
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - tests/integrationtest/r/executor/explainfor.result
  - tests/integrationtest/r/executor/partition/partition_boundaries.result
  - tests/integrationtest/r/executor/partition/partition_with_expression.result
  - tests/integrationtest/r/explain_cte.result
  - tests/integrationtest/r/explain_shard_index.result
  - tests/integrationtest/r/expression/issues.result
  PR Summary: What problem does this PR solve? Problem Summary: Initial motivation in  is that IN list equivalent to OR list produce better outcomes with index-selection and producing a unified canonical form using IN list produce better plans and make it consistent. What changed and how does it work? Predicate simplification is extended to convert OR list to IN list as the last rewrite. This uncovered other limitations in predicate simplification that does not cover IN list and IR list equally. Additional changes were made: (1) flip flop between OR and IN lists to make sure existing prediate simplification is applied fully. (2) Use equivalence classes to support simplification. For example a1=a2 and a2 in (1,2,3) and a1 > 2 should simplify to a1=a2 and a1=3 and a2=3.
- Related PR #63317: planner : merge index scan ranges | tidb-test=pr/2591
  URL: https://github.com/pingcap/tidb/pull/63317
  State: open
  Merged At: not merged
  Changed Files Count: 21
  Main Modules: tests/integrationtest, pkg/planner/core, pkg/util, pkg/executor
  Sample Changed Files:
  - pkg/executor/test/indexmergereadtest/index_merge_reader_test.go
  - pkg/planner/core/casetest/index/testdata/index_range_out.json
  - pkg/planner/core/casetest/index/testdata/index_range_xut.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_out.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/util/ranger/detacher.go
  - pkg/util/ranger/ranger_test.go
  - tests/integrationtest/r/black_list.result
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/r/explain_complex_stats.result
  - tests/integrationtest/r/explain_generate_column_substitute.result
  - tests/integrationtest/r/expression/vitess_hash.result
  - tests/integrationtest/r/generated_columns.result
  - tests/integrationtest/r/planner/core/casetest/index/index.result
  - tests/integrationtest/r/planner/core/casetest/partition/partition_pruner.result
  - tests/integrationtest/r/planner/core/casetest/physicalplantest/physical_plan.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_result_reorder.result
  - tests/integrationtest/r/util/ranger.result
  PR Summary: What problem does this PR solve? Problem Summary: This is a an enhancement for the planner range derivation logic for IN list which produces more ranges than the equivalent OR predicate. See example below. The ranges [1,1] [2,2] for the IN predicate compared to [1,2] for the equivalent OR predicate. Both forms scan the same data but less ranges could perform better especially if the number of ranges is high.  This issue addresses of on the potential side effect of issue  that aims to produce one canonical form for IN and irs equivalent OR list. What changed and how does it work?
- Fix PR #67125: planner: merge OR and IN predicates into IN lists | tidb-test=pr/2714
  URL: https://github.com/pingcap/tidb/pull/67125
  State: open
  Merged At: not merged
  Changed Files Count: 27
  Main Modules: pkg/planner/core, tests/integrationtest, pkg/executor
  Sample Changed Files:
  - pkg/executor/explainfor_test.go
  - pkg/planner/core/casetest/indexmerge/testdata/index_merge_suite_out.json
  - pkg/planner/core/casetest/indexmerge/testdata/index_merge_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_out.json
  - pkg/planner/core/casetest/partition/testdata/integration_partition_suite_xut.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_out.json
  - pkg/planner/core/casetest/partition/testdata/partition_pruner_xut.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_xut.json
  - pkg/planner/core/casetest/plancache/plan_cache_partition_table_test.go
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_in.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_out.json
  - pkg/planner/core/casetest/rule/testdata/predicate_simplification_xut.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_xut.json
  - pkg/planner/core/casetest/tpcds/testdata/tpcds_suite_out.json
  - pkg/planner/core/casetest/tpcds/testdata/tpcds_suite_xut.json
  - pkg/planner/core/rule/rule_predicate_simplification.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - tests/integrationtest/r/executor/partition/partition_boundaries.result
  PR Summary: What problem does this PR solve? Problem Summary: Predicate simplification can already remove duplicated branches from expressions such as , but it still keeps many same-column disjunctions in non-normalized forms, for example: This means logically equivalent predicates may reach later optimization stages in different shapes, which makes plan output and related test expectations less consistent than they need to be. What changed and how does it work?

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
