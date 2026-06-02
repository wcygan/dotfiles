# Issue #50067: planner: leading hint cannot take effect in UNION ALL statements

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/50067
- Status: closed
- Type: type/bug
- Created At: 2024-01-04T05:52:53Z
- Closed At: 2024-01-11T08:11:11Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-7.6, epic/hint, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required)

## Linked PRs
- Fix PR #50145: planner: fix leading hint cannot take effect in UNION ALL statements
  URL: https://github.com/pingcap/tidb/pull/50145
  State: closed
  Merged At: 2024-01-10T07:18:24Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50257: planner: fix leading hint cannot take effect in UNION ALL statements (#50145)
  URL: https://github.com/pingcap/tidb/pull/50257
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/util/hint/hint.go
  - planner/core/logical_plan_builder.go
  - planner/core/planbuilder.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50258: planner: fix leading hint cannot take effect in UNION ALL statements (#50145)
  URL: https://github.com/pingcap/tidb/pull/50258
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/util/hint/hint.go
  - planner/core/logical_plan_builder.go
  - planner/core/planbuilder.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50259: planner: fix leading hint cannot take effect in UNION ALL statements (#50145)
  URL: https://github.com/pingcap/tidb/pull/50259
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50260: Revert "planner: fix leading hint cannot take effect in UNION ALL statements"
  URL: https://github.com/pingcap/tidb/pull/50260
  State: closed
  Merged At: 2024-01-10T08:32:08Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: Reverts pingcap/tidb#50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50268: Revert "planner: fix leading hint cannot take effect in UNION ALL statements" (#50260)
  URL: https://github.com/pingcap/tidb/pull/50268
  State: closed
  Merged At: not merged
  Changed Files Count: 3
  Main Modules: pkg/planner/core, pkg/util
  Sample Changed Files:
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/util/hint/hint.go
  PR Summary: This is an automated cherry-pick of #50260 Reverts pingcap/tidb#50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50270: Revert "planner: fix leading hint cannot take effect in UNION ALL statements" (#50260)
  URL: https://github.com/pingcap/tidb/pull/50270
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/util/hint/hint.go
  - planner/core/logical_plan_builder.go
  - planner/core/planbuilder.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50260 Reverts pingcap/tidb#50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50272: Revert "planner: fix leading hint cannot take effect in UNION ALL statements" (#50260)
  URL: https://github.com/pingcap/tidb/pull/50272
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/util/hint/hint.go
  - planner/core/logical_plan_builder.go
  - planner/core/planbuilder.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50260 Reverts pingcap/tidb#50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50277: planner: fix leading hint cannot take effect in UNION ALL statements
  URL: https://github.com/pingcap/tidb/pull/50277
  State: closed
  Merged At: 2024-01-11T08:11:10Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? the root cause is that the  will be overwritten by push/pop in the
- Fix PR #50320: planner: fix leading hint cannot take effect in UNION ALL statements (#50277)
  URL: https://github.com/pingcap/tidb/pull/50320
  State: closed
  Merged At: 2024-01-16T07:15:16Z
  Changed Files Count: 5
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/logical_plan_builder.go
  - planner/core/planbuilder.go
  - planner/core/rule_join_reorder_greedy.go
  - planner/core/testdata/integration_suite_out.json
  - planner/core/testdata/join_reorder_suite_out.json
  PR Summary: This is an automated cherry-pick of #50277 What problem does this PR solve? Problem Summary: What changed and how does it work? the root cause is that the  will be overwritten by push/pop in the
- Fix PR #50322: planner: fix leading hint cannot take effect in UNION ALL statements (#50277)
  URL: https://github.com/pingcap/tidb/pull/50322
  State: closed
  Merged At: 2024-01-12T04:10:55Z
  Changed Files Count: 5
  Main Modules: planner/core
  Sample Changed Files:
  - planner/core/casetest/testdata/integration_suite_out.json
  - planner/core/casetest/testdata/join_reorder_suite_out.json
  - planner/core/logical_plan_builder.go
  - planner/core/planbuilder.go
  - planner/core/rule_join_reorder_greedy.go
  PR Summary: This is an automated cherry-pick of #50277 What problem does this PR solve? Problem Summary: What changed and how does it work? the root cause is that the  will be overwritten by push/pop in the
- Fix PR #50323: planner: fix leading hint cannot take effect in UNION ALL statements (#50277)
  URL: https://github.com/pingcap/tidb/pull/50323
  State: closed
  Merged At: 2024-01-12T04:06:26Z
  Changed Files Count: 8
  Main Modules: pkg/planner/core, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50277 What problem does this PR solve? Problem Summary: What changed and how does it work? the root cause is that the  will be overwritten by push/pop in the
- Fix PR #50376: planner: fix leading hint cannot take effect in UNION ALL statements (#50277)
  URL: https://github.com/pingcap/tidb/pull/50376
  State: closed
  Merged At: not merged
  Changed Files Count: 9
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50277 What problem does this PR solve? Problem Summary: What changed and how does it work? the root cause is that the  will be overwritten by push/pop in the
- Fix PR #50721: planner: fix leading hint cannot take effect in UNION ALL statements (#50145)
  URL: https://github.com/pingcap/tidb/pull/50721
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50145 What problem does this PR solve? Problem Summary: What changed and how does it work?
- Fix PR #50722: planner: fix leading hint cannot take effect in UNION ALL statements (#50277)
  URL: https://github.com/pingcap/tidb/pull/50722
  State: closed
  Merged At: 2024-01-25T08:37:51Z
  Changed Files Count: 9
  Main Modules: pkg/planner/core, pkg/util, tests/integrationtest
  Sample Changed Files:
  - pkg/planner/core/casetest/hint/BUILD.bazel
  - pkg/planner/core/casetest/hint/hint_test.go
  - pkg/planner/core/casetest/hint/testdata/integration_suite_in.json
  - pkg/planner/core/casetest/hint/testdata/integration_suite_out.json
  - pkg/planner/core/logical_plan_builder.go
  - pkg/planner/core/planbuilder.go
  - pkg/planner/core/rule_join_reorder_greedy.go
  - pkg/util/hint/hint.go
  - tests/integrationtest/r/planner/core/casetest/rule/rule_join_reorder.result
  PR Summary: This is an automated cherry-pick of #50277 What problem does this PR solve? Problem Summary: What changed and how does it work? the root cause is that the  will be overwritten by push/pop in the

## Notes
- At least one merged PR was found. The merge timestamp above can be used as the fix landing time in the main branch.
