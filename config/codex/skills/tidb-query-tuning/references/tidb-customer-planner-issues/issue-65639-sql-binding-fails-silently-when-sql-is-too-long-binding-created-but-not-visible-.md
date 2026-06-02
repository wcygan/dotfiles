# Issue #65639: SQL Binding fails silently when SQL is too long - binding created but not visible in SHOW GLOBAL BINDINGS

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/65639
- Status: open
- Type: type/bug
- Created At: 2026-01-19T09:00:50Z
- Labels: contribution, may-affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- Actual behavior observed: 1. **Silent failure**:  executed **without any error**, appearing to succeed 2. **Data inconsistency**: **does NOT show** the binding

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
