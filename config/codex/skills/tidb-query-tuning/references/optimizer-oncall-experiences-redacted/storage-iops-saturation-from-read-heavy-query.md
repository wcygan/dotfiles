# Storage IOPS Saturation From a Read-Heavy Query

## User Symptom
- Query latency jumps sharply and the storage device reaches its IOPS ceiling.
- TiKV CPU is not proportionally high, so the usual CPU-first workflow misses the culprit.

## Investigation Signals
- Volume or EBS IOPS becomes saturated.
- `rocksdb` read metrics such as read size or `block_read_bytes` are abnormal.
- TopSQL is often not enough; the decisive clue usually comes from slow query logs and storage metrics together.

## Workaround
- Temporarily raise the storage IOPS limit if the platform allows it.
- Manually inspect the slow query log to find the read-heavy query.
- Reduce query frequency or change the query shape after the culprit is found.

## Fixed Version
- No product fix was recorded. The immediate mitigation is workload reduction or capacity adjustment.
