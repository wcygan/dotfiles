---
title: S3 Lifecycle
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/S3-Lifecycle
fetch-when: Configuring bucket expiration, stuck lifecycle rules, or wondering why objects aren't being deleted.
---

# S3 Lifecycle

SeaweedFS supports the S3 bucket-lifecycle configuration subset that maps naturally to its volume-TTL + filer-scan model.

## Supported rule actions

- `Expiration.Days` / `Expiration.Date` — delete objects after N days or at a specific date.
- `NoncurrentVersionExpiration` — delete old versions on versioned buckets.
- `AbortIncompleteMultipartUpload` — clean up stuck uploads after N days.
- `ExpiredObjectDeleteMarker` — remove tombstone markers once underlying versions are gone.

## Filters supported

- Prefix match
- Object tags
- Size greater-than / less-than

## Not supported

- `Transition` / `NoncurrentVersionTransition` — no storage-class tiers in SeaweedFS to move objects into.
- Cross-region replication rules.

## Two evaluation paths

1. **Fast path (TTL)**: prefix-only expiration rules are translated to a per-volume TTL (see [ttl](ttl.md)), so expired volumes are reclaimed at ~10% of TTL / max 10 min. Zero-cost.
2. **Slow path (worker scan)**: rules with tags, sizes, dates, or version management are evaluated by a lifecycle worker that scans the bucket on an interval (default ~5 min).

## Configuring

Standard S3 API — PUT/GET/DELETE `/{bucket}?lifecycle`. Works with:
- AWS CLI: `aws s3api put-bucket-lifecycle-configuration`
- Terraform `aws_s3_bucket_lifecycle_configuration`
- aws-sdk in any language

## Behavior on versioned buckets

Expiration rules create **delete markers**, not permanent deletes. Use `NoncurrentVersionExpiration` to actually reclaim space. `NoncurrentVersions` parameter lets you retain N most-recent non-current versions.

## Gotchas

- Detection is scan-based, so objects can persist slightly beyond the configured expiry.
- The TTL fast path only applies to prefix-filtered expiration rules — adding a tag filter pushes into the slow path.
- Large buckets scan slowly; budget lifecycle worker capacity accordingly.
