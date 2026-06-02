# Issue #56724: use_toja can not be applied to a named query block & leading hint can not be applied to join children

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56724
- Status: open
- Type: type/enhancement
- Created At: 2024-10-18T08:50:31Z
- Labels: affects-7.5, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- * use_toja should be able to be applied to a named query block * when we build a join, we will set the preferred join hint, we could see when join child are already a join with merged schema(different table name inside), it couldn't pass the extract alias check

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
