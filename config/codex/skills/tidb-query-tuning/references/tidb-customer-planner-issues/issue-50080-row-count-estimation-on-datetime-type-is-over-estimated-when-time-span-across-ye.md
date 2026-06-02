# Issue #50080: row count estimation on DATETIME type is over-estimated when time span across years/months

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/50080
- Status: open
- Type: type/bug
- Created At: 2024-01-04T08:53:30Z
- Labels: affects-6.5, affects-7.1, affects-7.5, affects-8.1, affects-8.5, epic/cardinality-estimation, found/gs, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. Minimal reproduce step (Required) [test.zip]()

## Linked PRs
- Fix PR #58661: planner: fix wrong count when is out of range with datetime
  URL: https://github.com/pingcap/tidb/pull/58661
  State: closed
  Merged At: not merged
  Changed Files Count: 8
  Main Modules: pkg/planner/core, pkg/planner, pkg/statistics, build/nogo_config.json
  Sample Changed Files:
  - build/nogo_config.json
  - pkg/planner/cardinality/row_count_column.go
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/core/issuetest/BUILD.bazel
  - pkg/planner/core/issuetest/planner_issue_test.go
  - pkg/planner/core/issuetest/testdata/test.json
  - pkg/statistics/histogram.go
  - pkg/statistics/scalar.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? First, we found that this issue shows a significant difference between datetime with an index and without an index. Therefore, one of the goals of this PR is to reduce the error between them. The issue actually occurs at this point: we found that datetime is first specially encoded into a uint64, and this uint64 is different from a timestamp — it cannot be directly subtracted.
- Fix PR #55600: Planner: Single col out of range use original type
  URL: https://github.com/pingcap/tidb/pull/55600
  State: closed
  Merged At: 2025-04-29T16:41:17Z
  Changed Files Count: 5
  Main Modules: tests/integrationtest, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - tests/integrationtest/r/explain_complex.result
  - tests/integrationtest/s.zip
  - tests/integrationtest/t/explain_complex.test
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.
- Fix PR #61364: Planner: Single col out of range use original type (#55600)
  URL: https://github.com/pingcap/tidb/pull/61364
  State: closed
  Merged At: not merged
  Changed Files Count: 5
  Main Modules: cmd/explaintest, pkg/planner, tests/integrationtest
  Sample Changed Files:
  - cmd/explaintest/r/explain_complex.result
  - cmd/explaintest/t/explain_complex.test
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - tests/integrationtest/s.zip
  PR Summary: This is an automated cherry-pick of #55600 What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.
- Fix PR #61365: Planner: Single col out of range use original type (#55600)
  URL: https://github.com/pingcap/tidb/pull/61365
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: cmd/explaintest, statistics/testdata, statistics/index.go
  Sample Changed Files:
  - cmd/explaintest/r/explain_complex_update_date.result
  - cmd/explaintest/s.zip
  - cmd/explaintest/t/explain_complex_update_date.test
  - statistics/index.go
  - statistics/testdata/stats_suite_out.json
  - statistics/testdata/trace_suite_out.json
  PR Summary: This is an automated cherry-pick of #55600 What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.
- Fix PR #62156: Planner: Single col out of range use original type (#55600)
  URL: https://github.com/pingcap/tidb/pull/62156
  State: closed
  Merged At: 2025-07-07T21:51:27Z
  Changed Files Count: 2
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  PR Summary: This is an automated cherry-pick of #55600 What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.
- Fix PR #62259: Planner: Single col out of range use original type (#55600)
  URL: https://github.com/pingcap/tidb/pull/62259
  State: closed
  Merged At: 2025-07-08T16:08:24Z
  Changed Files Count: 2
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  PR Summary: This is an automated cherry-pick of #55600 What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.
- Fix PR #62260: Planner: Single col out of range use original type (#55600)
  URL: https://github.com/pingcap/tidb/pull/62260
  State: closed
  Merged At: 2025-07-08T23:45:36Z
  Changed Files Count: 2
  Main Modules: pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  PR Summary: This is an automated cherry-pick of #55600 What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.
- Fix PR #65667: Planner: Single col out of range use original type (#55600)
  URL: https://github.com/pingcap/tidb/pull/65667
  State: closed
  Merged At: 2026-01-20T09:46:14Z
  Changed Files Count: 5
  Main Modules: pkg/privilege, pkg/planner
  Sample Changed Files:
  - pkg/planner/cardinality/row_count_index.go
  - pkg/planner/cardinality/testdata/cardinality_suite_out.json
  - pkg/privilege/privileges/ldap/test/ca.crt
  - pkg/privilege/privileges/ldap/test/ldap.crt
  - pkg/privilege/privileges/ldap/test/ldap.key
  PR Summary: Manual cherry-pick of #62259 What problem does this PR solve? Problem Summary: What changed and how does it work? Index histograms are stored as type string to support the potential for multiple columns with different types to have their histograms combined into a consistent type. This conversion to string can result in a loss of precision when comparing out of range estimation. This fix will use the original column histogram data for out of range estimation.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
