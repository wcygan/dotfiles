---
title: File operations (HTTP cheat sheet)
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/File-Operations-Quick-Reference
fetch-when: Quick HTTP-API recall for upload/download/delete against the filer.
---

# File operations cheat sheet (filer HTTP API)

Two paths exist. **Blob-store path** (assign via master, POST to volume — see [architecture](architecture.md)) and **filer path** (everything below), which is the 99% case.

## Upload

```sh
# raw body
curl -X PUT "http://filer:8888/path/to/file.txt" -d "content"
# multipart
curl -X POST "http://filer:8888/path/to/file.txt" -F "file=@local.txt"
```

## Download

```sh
curl "http://filer:8888/path/to/file.txt"
curl "http://filer:8888/path/to/file.txt" -o local.txt
```

## Delete

```sh
curl -X DELETE "http://filer:8888/path/to/file.txt"
curl -X DELETE "http://filer:8888/path/?recursive=true"     # directory
```

## Move / rename

```sh
curl -X POST "http://filer:8888/new/path/file.txt?mv.from=/old/path/file.txt"
```

## Copy (server-side)

```sh
curl -X POST "http://filer:8888/backup/file.txt?cp.from=/original/file.txt"
```

Fast — no upload/download round-trip.

## List directory

```sh
curl -H "Accept: application/json" "http://filer:8888/path/?pretty=y"
# Paginate with limit + lastFileName
curl -H "Accept: application/json" \
     "http://filer:8888/path/?limit=10&lastFileName=file-abc.txt"
```

## Create directory

```sh
curl -X POST "http://filer:8888/path/to/new/dir/"
```

## Metadata ops

```sh
# HEAD — returns size, mtime, etc in headers
curl -I "http://filer:8888/path/to/file.txt"

# Custom xattr on upload
curl -X PUT "http://filer:8888/path/to/file.txt" \
     -H "Seaweed-Custom-Attribute: value" \
     -F "file=@local.txt"

# Per-file TTL
curl -X POST "http://filer:8888/path/to/file.txt?ttl=3600" -F file=@local.txt
```

## HTTP status codes

| Code | Ops | Meaning |
|------|-----|---------|
| 200 | GET | Success |
| 201 | POST/PUT | Created |
| 204 | DELETE / COPY / MOVE | Success, no body |
| 400 | Any | Bad request |
| 404 | GET / DELETE | Not found |

## Tips

- Use `mv.from` for rename/reorganize — metadata-only, instant.
- Use `cp.from` for server-side backup — avoids transferring bytes through your client.
- For very large files, the filer auto-chunks — see [large-files](large-files.md).
- For S3-shaped access, hit the S3 gateway instead (port 8333) — see [s3-api](s3-api.md).
