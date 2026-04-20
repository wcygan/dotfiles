---
title: Cloud tiering / remote mount
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Cloud-Drive-Quick-Setup
fetch-when: User wants to tier warm data to S3/GCS/Azure, mount a remote bucket, or set up async replication to cloud.
---

# Cloud tiering

SeaweedFS can mount remote S3-compatible storage as a filer directory with local caching. Useful for cost-tiering, cloud backup, and hybrid architectures.

## Three shapes

1. **Cloud Drive** — remote bucket mounted as a filer path, with local cache and write-back. Reads hit the cache, misses fall through to cloud.
2. **Gateway to Remote Object Store** — every local-bucket mutation is mirrored to a remote bucket. Read-your-writes locally, durable copy in cloud.
3. **Cloud Tier (volume-level)** — older local volumes automatically migrated to cloud after an age/size threshold, keeping pointers locally.

## Cloud Drive setup

```sh
# 1. Register credentials + endpoint
weed shell
> remote.configure -name=s5 \
    -type=s3 \
    -s3.access_key=AK... \
    -s3.secret_key=SK... \
    -s3.region=us-east-1
    # -s3.endpoint=https://... for non-AWS

# 2. Mount the remote bucket at a filer path
> remote.mount -dir=/buckets/bucket1 -remote=s5/bucketxxx
# add -nonempty if the local path isn't empty

# 3. Kick off write-back daemon
# (run outside weed shell, long-lived)
weed filer.remote.sync -dir=/buckets/bucket1
```

## Cache management

```sh
# Preload
remote.cache -dir=/buckets/bucket1/hot/

# Evict based on age / size
remote.uncache -dir=/buckets/bucket1/cold/ -maxAge=30d
```

## Remote providers supported

- AWS S3 (native)
- S3-compatible (Aliyun OSS, Wasabi, Backblaze B2, MinIO, etc.) via `-s3.endpoint`
- Google Cloud Storage
- Azure Blob (via gateway)

## Metadata sync

External cloud writes aren't reflected locally until you run:

```sh
remote.meta.sync -dir=/buckets/bucket1
```

Typically scheduled as a cron-ish job.

## When to reach for cloud tiering

- Hot-local, cold-cloud data pattern.
- Backup seeding — initial upload happens asynchronously.
- Migration path in/out of SeaweedFS (mount remote, copy locally, unmount).

## When not to

- Low-latency requirements on the cold tier — round-trip to cloud will dominate.
- Strict regulatory controls on data egress — the gateway copies data to cloud unless configured carefully.
