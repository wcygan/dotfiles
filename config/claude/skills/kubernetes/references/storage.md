# Storage

Authoritative deep links:

- <https://kubernetes.io/docs/concepts/storage/volumes/>
- <https://kubernetes.io/docs/concepts/storage/persistent-volumes/>
- <https://kubernetes.io/docs/concepts/storage/storage-classes/>
- <https://kubernetes.io/docs/concepts/storage/dynamic-provisioning/>
- <https://kubernetes.io/docs/concepts/storage/volume-snapshots/>

## Core Concepts

- **Volume** — storage tied to a Pod's lifecycle (emptyDir, configMap, secret, projected, hostPath, CSI inline...).
- **PersistentVolume (PV)** — cluster resource, independent of Pod lifecycle.
- **PersistentVolumeClaim (PVC)** — a user's request for storage. Binds 1:1 with a PV.
- **StorageClass** — template for dynamic PV provisioning (provisioner + parameters).
- **CSI driver** — pluggable storage backend (EBS, GCE PD, Azure Disk, Ceph, Longhorn, etc.).

The typical flow: user creates a PVC referencing a StorageClass → the CSI driver provisions a PV → PVC binds → Pod mounts PVC.

## Access Modes

| Mode | Short | Semantics |
|---|---|---|
| `ReadWriteOnce` | RWO | Single **node** can mount read-write (many pods on that node ok) |
| `ReadWriteOncePod` | RWOP | Single **Pod** can mount read-write (v1.27+ stable) |
| `ReadOnlyMany` | ROX | Many nodes mount read-only |
| `ReadWriteMany` | RWX | Many nodes mount read-write (requires NFS, CephFS, EFS, etc.) |

Most block storage (EBS, GCE PD, Azure Disk) is **RWO only**. RWX needs a filesystem backend.

## Dynamic Provisioning

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: fast
provisioner: ebs.csi.aws.com
parameters:
  type: gp3
  iops: "3000"
  throughput: "125"
reclaimPolicy: Delete          # or Retain
allowVolumeExpansion: true
volumeBindingMode: WaitForFirstConsumer   # preferred
```

- `volumeBindingMode: WaitForFirstConsumer` defers PV creation until a Pod using the PVC is scheduled — critical for zonal storage so the volume lands in the right zone.
- `reclaimPolicy: Retain` preserves the PV (and underlying cloud disk) when the PVC is deleted — use for anything you cannot afford to lose accidentally.
- `allowVolumeExpansion: true` enables `kubectl patch pvc` to grow the volume.

## PVC + Pod Mount

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: fast
  resources:
    requests: { storage: 20Gi }
---
apiVersion: v1
kind: Pod
metadata: { name: app }
spec:
  containers:
    - name: app
      image: app:v1
      volumeMounts:
        - { name: data, mountPath: /var/lib/app }
  volumes:
    - name: data
      persistentVolumeClaim: { claimName: data }
```

## StatefulSet volumeClaimTemplates

Each replica gets its own PVC derived from the template:

```yaml
spec:
  volumeClaimTemplates:
    - metadata: { name: data }
      spec:
        accessModes: [ReadWriteOnce]
        storageClassName: fast
        resources: { requests: { storage: 10Gi } }
```

**Warning**: deleting a StatefulSet does **not** delete its PVCs. Scale down + manual cleanup if you want to reclaim space.

## Volume Expansion

```bash
# 1. Ensure StorageClass allows expansion
kubectl get sc <name> -o jsonpath='{.allowVolumeExpansion}'

# 2. Edit PVC storage request upward (never downward)
kubectl patch pvc <pvc> -p '{"spec":{"resources":{"requests":{"storage":"50Gi"}}}}'

# 3. Some CSI drivers require a Pod restart to see the new size
kubectl rollout restart statefulset/<name>
```

## Ephemeral Volumes

- **emptyDir** — scratch space, deleted with Pod. `emptyDir: { medium: Memory }` uses tmpfs (counts against memory limit).
- **configMap / secret** — inject data as files (read-only).
- **projected** — merge multiple sources (secrets, configMaps, serviceAccountToken, downwardAPI) into one mount.
- **CSI ephemeral** — CSI-backed volume tied to Pod lifecycle (e.g., secrets-store-csi-driver).

```yaml
volumes:
  - name: scratch
    emptyDir:
      sizeLimit: 1Gi
  - name: config
    configMap:
      name: app-config
  - name: sa-token
    projected:
      sources:
        - serviceAccountToken:
            audience: vault
            expirationSeconds: 3600
            path: token
```

## Snapshots (where supported)

```yaml
apiVersion: snapshot.storage.k8s.io/v1
kind: VolumeSnapshot
metadata: { name: data-snap-1 }
spec:
  volumeSnapshotClassName: csi-snap
  source:
    persistentVolumeClaimName: data
```

Restore by creating a new PVC with `dataSource` referencing the VolumeSnapshot. Requires the external-snapshotter controller and a CSI driver that supports snapshots.
