# Issue #59406: Invalid setting for the variable tidb_record_plan_in_slow_log and the config record-plan-in-slow-log

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/59406
- Status: open
- Type: type/bug
- Created At: 2025-02-11T09:44:52Z
- Labels: may-affects-5.4, may-affects-6.1, may-affects-6.5, may-affects-7.1, may-affects-7.5, may-affects-8.1, may-affects-8.5, report/customer, severity/major, sig/planner, type/bug

## Customer-Facing Phenomenon
- 1. The setting is invalid because tidbOptInt64 but not TiDBOptOn is called to parse the normalizedValue  and fallback to default value due to syntax error. 2. The config setting only works for the part of Plan.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
