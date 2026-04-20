---
title: S3 Iceberg integration (Spark + Trino)
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/Spark-Iceberg-Integration
fetch-when: User wires Spark, Trino, DuckDB, Flink, RisingWave, or Lakekeeper against SeaweedFS Iceberg tables.
---

# Iceberg on SeaweedFS (Spark + Trino)

SeaweedFS ships a **native Iceberg REST Catalog** (port 8181) alongside an S3 table bucket (see [s3-table-bucket](s3-table-bucket.md)). Query engines talk REST for catalog + S3 for file IO — no Hive Metastore, no Glue, no Nessie.

## Spark 3.5+

Packages:
- `iceberg-spark-runtime-3.5_2.12:1.5.2`
- `iceberg-aws-bundle:1.5.2`

Essential config:
```
spark.sql.extensions = org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions
spark.sql.catalog.iceberg = org.apache.iceberg.spark.SparkCatalog
spark.sql.catalog.iceberg.type = rest
spark.sql.catalog.iceberg.uri = http://<seaweed-s3>:8181
spark.sql.catalog.iceberg.warehouse = s3://my-table-bucket
spark.sql.catalog.iceberg.s3.endpoint = http://<seaweed-s3>:8333
spark.sql.catalog.iceberg.s3.path-style-access = true
# If IAM enabled:
spark.sql.catalog.iceberg.rest.sigv4-enabled = true
spark.sql.catalog.iceberg.rest.signing-region = us-east-1
spark.sql.catalog.iceberg.rest.access-key-id = <AK>
spark.sql.catalog.iceberg.rest.secret-access-key = <SK>
# S3 FileIO creds (often the same, can be different)
spark.sql.catalog.iceberg.s3.access-key-id = <AK>
spark.sql.catalog.iceberg.s3.secret-access-key = <SK>
```

## Trino 4xx+

`etc/catalog/iceberg.properties`:
```
connector.name=iceberg
iceberg.catalog.type=rest
iceberg.rest-catalog.uri=http://<seaweed-s3>:8181
iceberg.rest-catalog.warehouse=s3://my-table-bucket
iceberg.rest-catalog.nested-namespace-enabled=true
fs.native-s3.enabled=true
s3.endpoint=http://<seaweed-s3>:8333
s3.path-style-access=true
s3.signer-type=AwsS3V4Signer
s3.aws-access-key=<AK>
s3.aws-secret-key=<SK>
```

## Common gotchas

- **SigV4 toggling** — if IAM is disabled on the SeaweedFS side, don't enable `sigv4-enabled` or Trino's `AwsS3V4Signer`. Engines insist on signing even when the server ignores it, and some versions mis-handle the unsigned path.
- **Path-style access** — always on. SeaweedFS doesn't do virtual-hosted bucket subdomains.
- **Separate creds for REST vs S3 FileIO** — you can use one set, but they are two config sections.
- **Multi-level namespaces** — enable explicitly (`nested-namespace-enabled=true`) to get `catalog.db.schema`.
- **Iceberg layout enforcement** — the table bucket rejects files outside `metadata/` and `data/`. Don't drop random blobs into a table bucket.

## Features supported

- Time-travel queries (`FOR SYSTEM_TIME AS OF …`)
- ACID UPDATE / DELETE / MERGE via Iceberg v2 spec
- Partition evolution
- Hidden partitioning
- Schema evolution

## Adjacent integrations

- **DuckDB** via `httpfs` + `iceberg` extensions.
- **RisingWave** native REST catalog sink.
- **Lakekeeper** proxies to SeaweedFS's REST catalog for additional policy layers.
