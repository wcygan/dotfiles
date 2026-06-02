# Issue #64205: support dump plan replayer for prepare stmt

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/64205
- Status: open
- Type: type/enhancement
- Created At: 2025-10-31T03:19:18Z
- Labels: report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- We can support like the following:

## Linked PRs
- Fix PR #66129: executor: support dump plan replayer for prepare stmt
  URL: https://github.com/pingcap/tidb/pull/66129
  State: open
  Merged At: not merged
  Changed Files Count: 6
  Main Modules: pkg/parser, pkg/executor
  Sample Changed Files:
  - pkg/executor/plan_replayer.go
  - pkg/executor/test/planreplayer/plan_replayer_test.go
  - pkg/parser/ast/misc_test.go
  - pkg/parser/parser.go
  - pkg/parser/parser.y
  - pkg/parser/parser_test.go
  PR Summary: What problem does this PR solve? Problem Summary: What changed and how does it work? support dump plan replayer for prepare stmt

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
