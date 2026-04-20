---
title: Seaweed CRD schema
canonical-url: https://github.com/seaweedfs/seaweedfs-operator
fetch-when: Authoring or modifying a Seaweed CR; figuring out which field controls a component's behavior.
---

# Seaweed CRD field reference

CRD: `seaweeds.seaweed.seaweedfs.com/v1`.

## Top-level `spec` fields

| Field | Type | Notes |
|---|---|---|
| `image` | string | Container image, e.g. `chrislusf/seaweedfs:4.21`. Used by all components unless overridden per-component. |
| `imagePullPolicy` | string | Applied to all component StatefulSets/Deployments. |
| `imagePullSecrets` | []LocalRef | |
| `volumeServerDiskCount` | int | Per-volume-server disk count; typically 1 for most homelab deployments. |
| `hostSuffix` | string | DNS suffix appended when exposing services externally. |
| `master` | MasterSpec | See below. Required. |
| `volume` | VolumeSpec | Required. |
| `filer` | FilerSpec | Optional but nearly always set (needed for S3, FUSE, HTTP filer). |
| `s3` | S3Spec | **Canonical** since 1.0.12 — standalone S3 Deployment. Preferred over `filer.s3`. |
| `admin` | AdminSpec | Optional admin server. |
| `worker` | WorkerSpec | Optional worker for EC/vacuum/maintenance. |
| `volumeTopology` | map[string]VolumeSpec | Tree-topology alternative to flat `volume`. See [operator-topology](operator-topology.md). |

## `master`

| Field | Default | Notes |
|---|---|---|
| `replicas` | — | **3** for Raft HA. 1 or 5 also valid. Never 2. |
| `defaultReplication` | `"000"` | Cluster-wide default replication code. See [replication](replication.md). |
| `volumeSizeLimitMB` | 30000 | 30 GB/volume. Larger (e.g. 100000) requires `_large_disk` image variant. |
| `requests` / `limits` | — | Standard resource blocks. |
| `storageClassName` | — | PVC for master data dir. |

## `volume`

| Field | Default | Notes |
|---|---|---|
| `replicas` | — | Total volume-server count. Does NOT spread across nodes automatically — set `topologySpreadConstraints` for that. |
| `requests.storage` | — | PVC size per volume server. |
| `storageClassName` | — | e.g. `longhorn` on anton. |
| `compactionMBps` | — | Rate-limit compaction I/O. |
| `rack` / `dataCenter` | — | Set for topology-aware placement. |
| `topologySpreadConstraints` | — | Kubernetes-native spread. |

## `filer`

| Field | Default | Notes |
|---|---|---|
| `replicas` | 1 | 2+ needs an external (shareable) metadata backend. See [filer-store-backends](filer-store-backends.md). |
| `config` | — | Inline `filer.toml` content. |
| `s3.enabled` | false | **Deprecated** in 1.0.12 — use top-level `spec.s3` instead. Setting both is rejected by the validating webhook. |
| `iam` | true | Old location for the IAM flag; in 1.0.12+ the `iam` field also lives under `spec.s3`. |
| `storage` | — | PVC requests for filer data dir (only relevant if using embedded leveldb). |

## `s3` (canonical, 1.0.12+)

| Field | Default | Notes |
|---|---|---|
| `replicas` | — | Standalone S3 Deployment replica count. |
| `iam` | **true** | Default is on. Set `false` explicitly if you want no-IAM / anonymous access. |
| `configSecret.name` / `configSecret.key` | — | References a Secret whose `<key>` contains the IAM `identities` JSON. See [operator-iam](operator-iam.md). |
| `port` | 8333 | S3 HTTP port. |
| `version` | — | Override S3-specific image. |
| `ingress` | — | Per-component Ingress object. |

## `admin` / `worker`

Opt-in components for management and background EC jobs. Empty unless you need them. See the operator's README for per-field detail; they're newer additions in 1.0.12.

## Common CRD mistakes

- Setting `spec.s3` AND `spec.filer.s3.enabled: true` → rejected by validating webhook.
- Assuming `volume.replicas: 3` spreads across 3 nodes — it doesn't; add topology spread constraints or `volumeTopology`.
- Forgetting `iam: false` — default `iam: true` blocks anonymous clients you might be testing with.
- Using `image: chrislusf/seaweedfs:latest` in production — pin a specific tag.
