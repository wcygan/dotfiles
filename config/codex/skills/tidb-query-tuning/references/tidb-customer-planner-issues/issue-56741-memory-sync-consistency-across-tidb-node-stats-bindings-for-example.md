# Issue #56741: memory sync consistency across tidb node(stats/bindings/... for example) 

## Metadata
- Issue: https://github.com/pingcap/tidb/issues/56741
- Status: open
- Type: type/enhancement
- Created At: 2024-10-21T06:30:46Z
- Labels: affects-7.5, affects-8.1, report/customer, sig/planner, type/enhancement

## Customer-Facing Phenomenon
- Enhancement for delta stats updates across tidb nodes, the multi writes acorss tidb nodes will finally be converted sequential apply-logs at the stats_meta table via group leader role. so the data consistency is gained in a dependent storage layer, while tidb in-mem stats cache should be notified when the new commits are applied in case of loss of stats renew.As is known to all, tikv component did a great job on consistency guarantee based on raft mechanism, the multi writes at different tikv node will form leader‘s sequential apply-logs and delivered across the raft group members (number basically equal to 3). the consistency can be guaranteed across the group members when one of them is being request because of the apply log is on the same node already. ﻿ for delta stats updates across tidb nodes, the multi writes acorss tidb nodes will finally be converted sequential apply-logs at the stats_meta table via group leader role. so the data consistency is gained in a dependent storage layer, while tidb in-mem stats cache should be notified when the new commits are applied in case of loss of stats renew. So we have the cache consistency problem by now.

## Linked PRs
- No linked PR was found from the issue timeline.

## Notes
- This issue is still open. Use this file as a reminder list for customer-driven gaps that still need a fix or a completed rollout.
