---
title: weed shell
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/weed-shell
fetch-when: User needs an admin CLI command and isn't sure of the exact syntax.
---

# weed shell

Interactive admin console — connects to the master and exposes cluster-maintenance commands.

## Starting it

```sh
weed shell
```

When stdin/stdout is a pipe (scripting), the prompt auto-suppresses. Supply `-master <host:port>` if not the default.

## Command families

### Cluster
- `cluster.status` — quick overview
- `cluster.raft.ps` — Raft peers + leader
- `cluster.ps` — list processes

### Volumes
- `volume.list` — enumerate all volumes
- `volume.fix.replication` — repair under-replicated volumes (use `-doDelete=false` on aging disks)
- `volume.vacuum` — compact volumes where deleted entries exceed a threshold (default 30%)
- `volume.move -source=X -target=Y -volumeId=Z` — relocate a volume
- `volume.balance -force` — balance volume counts across servers (rare; see [replication](replication.md) caveat)

### Collections
- `collection.list` — show all collections
- `collection.delete -collection=<name>` — nuke a whole collection (destructive)

### Filesystem (filer)
- `fs.ls /path` — list filer directory
- `fs.du /path` — disk usage
- `fs.mkdir /path` — create directory
- `fs.rm /path` — delete
- `fs.verify` — check chunk integrity for a file

### Erasure coding
- `ec.encode -volumeId=N` — convert a replicated volume to EC
- `ec.decode -volumeId=N` — reverse
- `ec.rebuild` — reconstruct missing EC shards

### S3 / IAM
- `s3.user.create -user=<name>` — add an S3 identity
- `s3.bucket.create -bucket=<name>` — create bucket
- `s3.bucket.policy` — manage bucket policies

### Locking
- `lock` / `unlock` — take/release a distributed advisory lock. Use before sensitive multi-command operations (e.g. moving volumes during a restore) so two operators don't step on each other.

## When you reach for it

- A volume went under-replicated → `volume.fix.replication`
- Disk usage climbing without deletes reclaiming → `volume.vacuum`
- Moving data off a soon-to-retire node → `volume.move` per volume
- Setting up S3 users without API calls → `s3.user.create` + `s3.policy.*`
- Investigating "which master is the leader?" → `cluster.raft.ps`

## Scripting

```sh
echo "cluster.status" | weed shell -master $M
```

## Operator note

Inside a Kubernetes operator install, `weed shell` must run inside a pod (or you need to port-forward master 9333). Common pattern: `kubectl -n <ns> exec -it <master-0> -- weed shell`.
