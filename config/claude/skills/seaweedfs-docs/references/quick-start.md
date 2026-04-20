---
title: Quick Start
canonical-url: https://github.com/seaweedfs/seaweedfs
fetch-when: User asks for current CLI flags, default ports, or a command you don't have memorized. Wiki page `Quick-Start-with-weed-mini` has the same content in wiki form.
---

# Quick Start

SeaweedFS ships as a single `weed` binary that embeds every component.

## Three install paths

**1. `weed mini` — all-in-one, auto-configures.** Best for development and learning.
```sh
./weed mini -dir=/data
```
Brings up master (UI 9333), volume (9340), filer (8888), S3 (8333), WebDAV (7333), admin UI (23646) in one process.

**2. Docker single-container S3.** Fast smoke test.
```sh
docker run -p 8333:8333 chrislusf/seaweedfs server -s3
```

**3. `weed server` — production, manual configuration.** Starts one master + one volume + one filer + S3 gateway. Still single-node but requires explicit layout.
```sh
export AWS_ACCESS_KEY_ID=admin
export AWS_SECRET_ACCESS_KEY=key
weed server -dir=/some/data/dir -s3
```

## Adding capacity

Add volume servers (same or different machine):
```sh
weed volume -dir="/some/data2" -master="<master>:9333" -port=8081
```

Volumes register themselves with master on heartbeat; no rebalancing triggered.

## Binary install

- Release tarballs: https://github.com/seaweedfs/seaweedfs/releases (unzip → single binary)
- Go install: `go install github.com/seaweedfs/seaweedfs/weed@latest`
- macOS quarantine: `xattr -d com.apple.quarantine ./weed` after download

## Key gotchas

- `weed mini` is **not** production-safe — defaults favor easy startup, not durability.
- Default volume size is 30 GB and max-volumes default is 8. Override with `-volumeSizeLimitMB` (master) and `-max` (volume).
- Images run as non-root UID/GID 1000:1000 — bind-mounted dirs need matching ownership.
- gRPC port = HTTP port + 10000 unless you use explicit `<host>:<port>.<grpcPort>` syntax.

## Adjacent topics

- Production multi-node layout → [production-setup](production-setup.md)
- Per-component ports and HA → [components](components.md)
- Weed shell for cluster ops → [weed-shell](weed-shell.md)
