---
title: S3 Object Versioning
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/S3-Object-Versioning
fetch-when: Enabling versioning on a bucket, debugging delete markers, or restoring a prior version.
---

# S3 Object Versioning

Standard S3 versioning is implemented — enable per bucket, delete creates tombstones, restore by version ID.

## Enabling

```sh
aws s3api put-bucket-versioning \
  --bucket my-bucket \
  --versioning-configuration Status=Enabled
```

Also supports `Status=Suspended` (versions retained, new writes unversioned).

## Version storage

Each version gets an ID of form `v_<32-hex>`. The layout in the filer:

```
/buckets/my-bucket/path/to/object    (current)
/buckets/my-bucket/path/to/object/.versions/
  v_abc123…  (old version)
  v_def456…  (older version)
```

## Delete markers

Deleting a versioned object creates a delete marker (soft delete). To actually remove a version:
```sh
aws s3api delete-object --bucket my-bucket --key path/to/object --version-id v_xxx
```

With versioning **Suspended**, deletes are permanent (like classic S3).

## List versions

```sh
aws s3api list-object-versions --bucket my-bucket --prefix path/
```

Returns both `Versions` and `DeleteMarkers`.

## Known limitations

- **Restore API**: partial support.
- **Version-specific lifecycle rules**: not fully implemented.
- **MFA Delete**: unsupported.

## Best practices

- Enable before real data lands — retrofitting is disruptive.
- Budget for storage growth; add a `NoncurrentVersionExpiration` lifecycle rule early (see [s3-lifecycle](s3-lifecycle.md)).
- Use version-specific operations when restoring historical data — the "current" pointer moves to the most recent non-deleted version on marker removal.
