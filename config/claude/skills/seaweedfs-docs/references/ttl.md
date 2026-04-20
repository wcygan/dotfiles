---
title: TTL
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Store-file-with-a-Time-To-Live
fetch-when: User asks about expiring files automatically or when setting TTL on a volume vs a file.
---

# TTL (Time To Live)

Files and volumes can carry a TTL so storage is reclaimed automatically at expiry.

## Syntax

`<number><unit>`. Units: `m` (min), `h` (hour), `d` (day), `w` (week), `M` (month), `y` (year). Examples: `3m`, `4h`, `5d`, `6w`, `7M`, `8y`. Note capital `M` for month.

## Two TTLs cooperate

- **Volume TTL** — baked into the volume file at creation. Defines an upper bound for all files in it.
- **File TTL** — written alongside each file on upload.

**Rule:** file TTL must be **≤** volume TTL. They don't need to match.

## Setting TTL

```sh
# Ask the master for a volume with a 5d TTL
curl "http://localhost:9333/dir/assign?ttl=5d"
```

Via filer HTTP upload:
```sh
curl -X POST "http://filer:8888/path/file.txt?ttl=1h" -F file=@local.txt
```

## Expiration

After `volume_ttl`, the volume is entirely expired and **safely deletable**. The master runs a background sweep every `~10% of TTL` (max 10 minutes) to delete expired volumes.

**Per-file:** reading an expired file returns 404; physical reclaim only happens when the *whole volume* expires. So files with very different TTLs belong in different volumes.

## Why volume-level

Per-file GC would require scanning metadata to find expired entries. Volume-level TTL treats the volume as the GC unit — drop the whole file and reclaim 30 GB at once. Same philosophy as TTL-partitioned tables in Cassandra.

## Design tip

Group files with similar lifetimes into the same collection + volume TTL. Mixing `ttl=1h` and `ttl=1y` files in one volume defeats the mechanism — the volume can only be deleted at the 1y mark.
