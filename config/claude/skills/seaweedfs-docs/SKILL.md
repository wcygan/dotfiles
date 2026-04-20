---
name: seaweedfs-docs
description: Reference knowledge for upstream SeaweedFS and the seaweedfs-operator Kubernetes operator. Covers architecture (master/volume/filer split, blob-id format, O(1) read path), components and their ports, replication codes (000/001/010/100/110/200), TTL semantics, filer metadata store choice (leveldb/sqlite/postgres/mysql/redis/cassandra), the S3-compatible API (supported ops, lifecycle, versioning, table buckets, Iceberg REST catalog), the `weed shell` CLI, cloud-tiering, erasure coding, the Seaweed CRD shape, operator IAM and topology support, and release-notes triage. Load when the user mentions seaweedfs, weed, seaweedfs-operator, Seaweed CRD, weed shell, filer, volume server, master server, blob store, erasure coding, WebDAV on seaweedfs, CSI seaweedfs, Iceberg on seaweedfs, S3 table bucket, or when working in code that uses the SeaweedFS S3 endpoint. Do NOT load on generic mentions of "S3" alone. Keywords — seaweedfs, seaweed-fs, weed, seaweedfs-operator, Seaweed CRD, weed shell, weed mini, filer, volume server, master server, blob store, erasure coding, Iceberg catalog, S3 table bucket, chrislusf/seaweedfs.
---

# SeaweedFS Documentation Reference

Upstream knowledge for SeaweedFS and its Kubernetes operator. Scope: **upstream concepts only**. Anton-specific deployment decisions live in `context/plans/0005-*.md`, ADR 0019, and `kubernetes/apps/storage/CLAUDE.md` — consult those for how *this* cluster uses SeaweedFS.

## Fetch strategy

Each reference file holds a local summary plus a canonical URL. For quick answers, read the local summary. Before giving definitive guidance on API shapes, CLI flags, CRD fields, or release behavior, **WebFetch the canonical URL** — SeaweedFS releases often and wiki pages drift.

## Topic router

### Fundamentals
| Topic | Reference | Canonical URL |
|---|---|---|
| Install and first cluster | [quick-start](references/quick-start.md) | https://github.com/seaweedfs/seaweedfs |
| Multi-component production layout | [production-setup](references/production-setup.md) | https://github.com/seaweedfs/seaweedfs/wiki/Production-Setup |
| Component roles and default ports | [components](references/components.md) | https://github.com/seaweedfs/seaweedfs/wiki/Components |
| Blob-store model, O(1) reads, blob-id format | [architecture](references/architecture.md) | https://github.com/seaweedfs/seaweedfs |
| Cross-filesystem comparisons | [comparison](references/comparison.md) | https://github.com/seaweedfs/seaweedfs |
| Frequently-hit pitfalls | [faq](references/faq.md) | https://github.com/seaweedfs/seaweedfs/wiki/FAQ |

### Filer and file ops
| Topic | Reference | Canonical URL |
|---|---|---|
| Filer abstraction and metadata stores | [directories-and-files](references/directories-and-files.md) | https://github.com/seaweedfs/seaweedfs/wiki/Directories-and-Files |
| Picking a filer metadata backend | [filer-store-backends](references/filer-store-backends.md) | https://github.com/seaweedfs/seaweedfs/wiki/Choosing-a-Filer-Store |
| HTTP file operations cheat sheet | [file-operations](references/file-operations.md) | https://github.com/seaweedfs/seaweedfs/wiki/File-Operations-Quick-Reference |
| Chunking for very large files | [large-files](references/large-files.md) | https://github.com/seaweedfs/seaweedfs/wiki/Data-Structure-for-Large-Files |

### Storage policy
| Topic | Reference | Canonical URL |
|---|---|---|
| Volume replication codes (000..200) | [replication](references/replication.md) | https://github.com/seaweedfs/seaweedfs/wiki/Replication |
| TTL on volumes and files | [ttl](references/ttl.md) | https://github.com/seaweedfs/seaweedfs/wiki/Store-file-with-a-Time-To-Live |
| Erasure coding for warm data | [erasure-coding](references/erasure-coding.md) | https://github.com/seaweedfs/seaweedfs/wiki/Erasure-Coding-for-warm-storage |
| Cloud-drive / remote-mount tiering | [cloud-tiering](references/cloud-tiering.md) | https://github.com/seaweedfs/seaweedfs/wiki/Cloud-Drive-Quick-Setup |

### S3 API surface
| Topic | Reference | Canonical URL |
|---|---|---|
| Supported S3 operations and gaps | [s3-api](references/s3-api.md) | https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API |
| Bucket lifecycle rules | [s3-lifecycle](references/s3-lifecycle.md) | https://github.com/seaweedfs/seaweedfs/wiki/S3-Lifecycle |
| Object versioning | [s3-versioning](references/s3-versioning.md) | https://github.com/seaweedfs/seaweedfs/wiki/S3-Object-Versioning |
| Table buckets (Iceberg REST catalog) | [s3-table-bucket](references/s3-table-bucket.md) | https://github.com/seaweedfs/seaweedfs/wiki/S3-Table-Bucket |
| Spark + Trino against Iceberg tables | [s3-iceberg](references/s3-iceberg.md) | https://github.com/seaweedfs/seaweedfs/wiki/Spark-Iceberg-Integration |
| AWS CLI against a SeaweedFS endpoint | [aws-cli](references/aws-cli.md) | https://github.com/seaweedfs/seaweedfs/wiki/AWS-CLI-with-SeaweedFS |

### Operations
| Topic | Reference | Canonical URL |
|---|---|---|
| `weed shell` interactive CLI | [weed-shell](references/weed-shell.md) | https://github.com/seaweedfs/seaweedfs/wiki/weed-shell |

### Kubernetes
| Topic | Reference | Canonical URL |
|---|---|---|
| CSI driver (pure block mount, not S3) | [k8s-csi](references/k8s-csi.md) | https://github.com/seaweedfs/seaweedfs-csi-driver |
| Operator overview and Seaweed CRD | [operator-overview](references/operator-overview.md) | https://github.com/seaweedfs/seaweedfs-operator |
| Seaweed CRD field reference | [operator-crd-schema](references/operator-crd-schema.md) | https://github.com/seaweedfs/seaweedfs-operator |
| Operator IAM / embedded S3 identities | [operator-iam](references/operator-iam.md) | https://github.com/seaweedfs/seaweedfs-operator/blob/master/IAM_SUPPORT.md |
| Operator rack/DC topology | [operator-topology](references/operator-topology.md) | https://github.com/seaweedfs/seaweedfs-operator/blob/master/TOPOLOGY_SUPPORT.md |
| Operator release triage | [operator-releases](references/operator-releases.md) | https://github.com/seaweedfs/seaweedfs-operator/releases |

## When to skip this skill

- Generic "how do I use S3 with the AWS SDK" questions — load the AWS SDK docs instead.
- Anton cluster config (HelmRelease values, HTTPRoute, ExternalSecret shape) — that lives in `kubernetes/apps/storage/` and `context/plans/0005-*.md`.
- Longhorn block-storage questions (SeaweedFS volume servers consume Longhorn PVCs *as clients*, they don't manage them) — use the `longhorn-*` skill pack.
