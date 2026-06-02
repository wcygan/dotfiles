# Issue #54213: optimizer access table unnecessarily

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/54213
- Status: closed
- Type: type/bug
- Created At: 2024-06-25T21:13:42Z
- Closed At: 2024-07-15T10:35:59Z
- Labels: affects-5.4, affects-6.1, affects-6.5, affects-7.1, affects-7.5, affects-8.1, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #54609: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2362
  URL: https://github.com/pingcap/tidb/pull/54609
  State: closed
  Merged At: 2024-07-15T10:35:58Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_limit.go
  - pkg/planner/core/operator/logicalop/logical_schema_producer.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?
- Fix PR #54636: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2362 (#54609)
  URL: https://github.com/pingcap/tidb/pull/54636
  State: closed
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_limit.go
  - pkg/planner/core/operator/logicalop/logical_schema_producer.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #54609 What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?
- Fix PR #54637: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2362 (#54609)
  URL: https://github.com/pingcap/tidb/pull/54637
  State: closed
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_limit.go
  - pkg/planner/core/operator/logicalop/logical_schema_producer.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #54609 What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?
- Fix PR #54815: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2369
  URL: https://github.com/pingcap/tidb/pull/54815
  State: closed
  Merged At: 2024-07-23T03:10:33Z
  Changed Files Count: 13
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_plan_trace_test.go
  - pkg/planner/core/rule_column_pruning.go
  - pkg/planner/core/testdata/plan_suite_unexported_out.json
  - pkg/planner/core/util.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: This is an automated cherry-pick of #54609 What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?
- Fix PR #54936: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2362 (#54609)
  URL: https://github.com/pingcap/tidb/pull/54936
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_limit.go
  - pkg/planner/core/operator/logicalop/logical_schema_producer.go
  - planner/core/testdata/plan_normalized_suite_out.json
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #54609 What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?
- Fix PR #55161: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2375
  URL: https://github.com/pingcap/tidb/pull/55161
  State: closed
  Merged At: 2024-08-02T12:23:07Z
  Changed Files Count: 12
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/testdata/plan_normalized_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_plan_trace_test.go
  - pkg/planner/core/rule_column_pruning.go
  - pkg/planner/core/util.go
  - tests/integrationtest/r/planner/core/casetest/integration.result
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  - tests/integrationtest/r/planner/core/issuetest/planner_issue.result
  - tests/integrationtest/t/planner/core/issuetest/planner_issue.test
  PR Summary: This is an automated cherry-pick of #54609 What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?
- Fix PR #56900: planner: fix the issue accessing unnecessary table side caused by column pruning | tidb-test=pr/2362 (#54609)
  URL: https://github.com/pingcap/tidb/pull/56900
  State: closed
  Merged At: not merged
  Changed Files Count: 7
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/mpp/testdata/integration_suite_out.json
  - pkg/planner/core/casetest/physicalplantest/testdata/plan_suite_out.json
  - pkg/planner/core/casetest/testdata/integration_suite_out.json
  - pkg/planner/core/integration_test.go
  - pkg/planner/core/logical_limit.go
  - pkg/planner/core/operator/logicalop/logical_schema_producer.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #54609 What problem does this PR solve? Problem Summary: planner: fix the issue accessing unnecessary table side caused by column pruning What changed and how does it work?

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
