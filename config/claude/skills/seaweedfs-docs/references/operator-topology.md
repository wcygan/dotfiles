---
title: Operator topology (rack / DC)
canonical-url: https://github.com/seaweedfs/seaweedfs-operator/blob/master/TOPOLOGY_SUPPORT.md
fetch-when: Planning replication like "210", distributing volume servers across racks or zones, or debugging why placement isn't matching.
---

# Rack / DC topology via the operator

SeaweedFS needs volume servers to advertise `-rack=...` and `-dataCenter=...` so the master can satisfy replication codes like `001` (same rack), `010` (different rack), `100` (different DC). The operator exposes this in two shapes.

## Simple topology (flat)

Apply labels to all volume replicas at once:

```yaml
spec:
  volume:
    replicas: 3
    requests:
      storage: 10Gi
    rack: "rack1"
    dataCenter: "dc1"
```

All 3 volume pods start with `-rack=rack1 -dataCenter=dc1`. Good for a single-rack setup.

## Tree topology (recommended for multi-rack/DC)

Define multiple groups, each with its own rack/DC + nodeSelector:

```yaml
spec:
  master:
    replicas: 3
    defaultReplication: "210"
  volumeTopology:
    dc1-rack1:
      replicas: 3
      rack: "rack1"
      dataCenter: "dc1"
      nodeSelector:
        topology.kubernetes.io/zone: us-west-2a
      requests: {storage: 10Gi}
    dc1-rack2:
      replicas: 2
      rack: "rack2"
      dataCenter: "dc1"
      nodeSelector:
        topology.kubernetes.io/zone: us-west-2b
      requests: {storage: 10Gi}
    dc2-rack1:
      replicas: 3
      rack: "rack1"
      dataCenter: "dc2"
      nodeSelector:
        topology.kubernetes.io/zone: us-east-1a
      requests: {storage: 15Gi}
      storageClassName: fast-ssd
```

Each key under `volumeTopology` becomes a separate StatefulSet with its own pod spec, rack/DC labels, and nodeSelector.

## `defaultReplication: "210"` gotchas

`210` means 2 copies in *different* DCs + 1 copy in a *different* rack — 4 total copies. Requires a minimum of 2 DCs with 2 racks each. If the master can't find placement matching the code, volume *creation* fails — symptom is CR stays pending with no new volumes.

## How it lands on the pod

The operator translates these labels into `weed volume -rack=... -dataCenter=...` args. Pods heartbeat their topology to the master, which holds a topology tree used at fid-assignment time.

## Anton note

anton runs in a single-rack, single-DC homelab. Default `replication="000"` (see [replication](replication.md)) — Longhorn provides durability at the block layer. Topology labels aren't set. If you ever split nodes across physical racks, revisit this.
