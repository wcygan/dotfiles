---
title: S3 API
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Amazon-S3-API
fetch-when: User needs to know whether a specific S3 op is supported; writing or debugging S3 client code against SeaweedFS.
---

# S3 API

SeaweedFS implements a large subset of AWS S3. The gateway runs as `weed s3`, `weed filer -s3`, or `weed server -s3`; by default on port **8333**.

## Supported operations

**Bucket**: CreateBucket, DeleteBucket, HeadBucket, ListBuckets. Each bucket is a *collection* mapped to `/buckets/<name>` in the filer.

**Object**: Get, Put, Delete, Copy, Head. Includes range requests, conditional headers (`If-Match`, `If-None-Match`, `If-Modified-Since`, `If-Unmodified-Since`), user metadata, tagging.

**Multipart**: CreateMultipartUpload, UploadPart, UploadPartCopy, CompleteMultipartUpload, AbortMultipartUpload, ListParts.

**Bucket features**: ACLs, CORS, Lifecycle, Versioning, Object Lock + Retention, Tagging, Encryption (SSE-S3, SSE-KMS, SSE-C), Policies, Conditional Operations.

**IAM**: Access keys, STS (AssumeRole, AssumeRoleWithWebIdentity), OIDC federation, policy variables + conditions, bucket policies.

## Not supported

- S3 Express One Zone
- Bucket analytics / intelligent-tiering / inventory
- Server access logging to a logging bucket
- Bucket-level replication (between S3 buckets)
- Bucket website hosting
- SelectObjectContent, RestoreObject

## Identities and actions (SeaweedFS-specific vocabulary)

The `identities.json` config uses action verbs like `Admin`, `Read`, `Write`, `List`, `Tagging`, `ReadAcp`, `WriteAcp`. `Admin` covers everything. Example:

```json
{
  "identities": [
    {
      "name": "admin",
      "actions": ["Admin"],
      "credentials": [{"accessKey": "AKI…", "secretKey": "…"}]
    },
    {
      "name": "reader",
      "actions": ["Read", "List"],
      "credentials": [{"accessKey": "AKI…", "secretKey": "…"}]
    }
  ]
}
```

## Enabling

- `weed s3` — standalone gateway, stateless, points to an existing filer cluster.
- `weed filer -s3` — filer + S3 in one process (simpler).
- `weed server -s3` — all-in-one dev mode.

Put multiple `weed s3` behind a load balancer for horizontal scaling; they share state through the filer.

## Operator note

In operator 1.0.12+ (via top-level `spec.s3`), S3 runs as a **separate Deployment** from the filer, with independent replica count (`spec.s3.replicas`). The older `FilerSpec.S3` path is deprecated.

## Common client

AWS CLI works out of the box — see [aws-cli](aws-cli.md). Signature v4 and path-style addressing required.
