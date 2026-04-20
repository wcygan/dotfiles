---
title: AWS CLI against SeaweedFS
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/AWS-CLI-with-SeaweedFS
fetch-when: User needs a working aws-cli config for SeaweedFS or is hitting 400/403 SignatureDoesNotMatch.
---

# AWS CLI against a SeaweedFS S3 endpoint

`aws` works unchanged as long as you override the endpoint and pin SigV4.

## One-time config

```sh
aws configure
# Access key ID: anything (real value if IAM on)
# Secret key: anything
# Default region: us-east-1
# Output: json
aws configure set default.s3.signature_version s3v4
```

## Running commands

Always pass `--endpoint-url`:

```sh
S3=http://<seaweed-s3>:8333

aws --endpoint-url $S3 s3 mb s3://bucket
aws --endpoint-url $S3 s3 ls
aws --endpoint-url $S3 s3 cp ./local s3://bucket/key
aws --endpoint-url $S3 s3 cp s3://bucket/key - > dl
aws --endpoint-url $S3 s3 rm s3://bucket/key
aws --endpoint-url $S3 s3 cp s3://b/k1 s3://b/k2  # server-side copy
```

Presigned URL:
```sh
aws --endpoint-url $S3 s3 presign s3://bucket/key --expires-in 900
```

Multipart is automatic for large uploads; override threshold with `aws configure set default.s3.multipart_threshold 64MB`.

## Common errors

- **400 SignatureDoesNotMatch** → wrong region or `signature_version` not `s3v4`.
- **301 MovedPermanently** → you hit the gateway over HTTP when an HTTPS route redirects (S3 clients don't follow redirects on signed requests). Use `https://` directly.
- **InvalidBucketName (longhorn flagged)** → path-style is required; host-style via a virtual-bucket subdomain isn't supported.
- **AccessDenied from anonymous** → IAM is enabled, seed identities in `configSecret` (or set `iam: false` if appropriate).

## Reverse proxy with X-Forwarded-Prefix

If you sit behind Caddy/Nginx that mounts SeaweedFS at a subpath, add:

```
header_up X-Forwarded-Prefix /seaweed/
```

so SigV4 signatures match.

## Other CLIs

- `s3cmd` — supports SeaweedFS, use `--host-bucket=s3.example.com` + `signature_v2 = False`
- `rclone` — uses `s3` backend with `--s3-endpoint-url`
- `restic` — `s3:http://host:8333/bucket/`

Each has its own wiki page — see SKILL.md's topic router.
