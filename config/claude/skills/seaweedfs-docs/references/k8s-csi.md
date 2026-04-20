---
title: Kubernetes CSI driver
canonical-url: https://github.com/seaweedfs/seaweedfs-csi-driver
fetch-when: User asks about mounting SeaweedFS as a PVC via CSI, vs just hitting the S3 endpoint.
---

# SeaweedFS CSI driver

A separate project from the operator: `seaweedfs-csi-driver` lets pods mount a SeaweedFS filer path as a regular Kubernetes PVC via FUSE.

## What it gives you

- `StorageClass` → `PersistentVolumeClaim` → `PersistentVolume` backed by a filer subdirectory.
- FUSE-mounted inside the pod — app sees a regular filesystem, reads/writes go to SeaweedFS filer.
- Supports ReadWriteMany (RWX) because SeaweedFS is a shared filesystem.
- Useful for POSIX-expecting workloads (Postgres wouldn't qualify, but log aggregators, ML training checkpoints, media processing, shared config).

## vs. operator

- The **operator** stands up SeaweedFS components (master/volume/filer/s3) on K8s.
- The **CSI driver** lets K8s workloads *consume* a SeaweedFS filer as a volume.
- You can run both — operator hosts the cluster, CSI driver provides PVCs to other pods.

## vs. S3 endpoint

If your app speaks S3 natively, use the S3 endpoint — lower overhead, no FUSE, HA comes free from multiple S3 pods. Reach for CSI only when:
- App expects a POSIX mount and you can't change that.
- You need RWX across many pods (S3 doesn't have file-locking semantics).
- You want filesystem-level features like quota-per-PVC.

## Install

Separate Helm chart: `https://seaweedfs.github.io/seaweedfs-csi-driver/helm`. Point it at an existing filer endpoint. See the repo's README for current values.

## Anton note

Not in use today. Longhorn already covers block-storage PVC needs via iSCSI/host-fabric (ADR 0005). Adding SeaweedFS CSI would only be worth it for a workload requiring RWX filer semantics that Longhorn can't provide.
