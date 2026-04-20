---
title: S3 Table Bucket
canonical-url: https://github.com/seaweedfs/seaweedfs/wiki/S3-Table-Bucket
fetch-when: User wants to run Iceberg / Spark / Trino / DuckDB against SeaweedFS natively.
---

# S3 Table Bucket

A special bucket type that implements the Apache Iceberg REST Catalog natively. Unlike a regular bucket (unstructured objects + prefixes), a table bucket enforces Iceberg's directory layout and exposes a catalog API so query engines can discover tables without an external Hive/Glue catalog.

## What it provides

- **Iceberg REST Catalog endpoint** on port 8181 (default).
- Hierarchy: **Bucket → Namespace → Table**. Multi-level namespaces supported.
- Enforced file layouts (metadata/, data/) — rejects misplaced files.
- Native integration targets for Spark, Trino, Flink, DuckDB, RisingWave, Lakekeeper.

## Vs. regular S3 bucket

| | Regular bucket | Table bucket |
|---|---|---|
| Namespace model | Flat + prefixes | Bucket → Namespace → Table |
| API | `S3 API` | `s3tables` API + Iceberg REST catalog |
| Layout validation | None | Iceberg-specific |
| Use case | Arbitrary objects | Analytics tables |

## Enabling

Table-bucket operations go through a separate API namespace (`s3tables`). Creating a table bucket:

```sh
# via weed shell
weed shell
> s3.tablebucket.create <name>
```

The Iceberg REST endpoint runs at `http://<s3-gateway>:8181`.

## Integrations

- Spark → [s3-iceberg](s3-iceberg.md)
- Trino → [s3-iceberg](s3-iceberg.md)
- DuckDB / RisingWave / Lakekeeper — see corresponding wiki pages.

## IAM model

Fine-grained — policies can target bucket, namespace, or table. Different from regular bucket policies which target bucket or prefix.

## When to use

- You're building a data lake and want an Iceberg catalog without running Hive Metastore or Nessie.
- You want Spark/Trino to talk directly to SeaweedFS with no external dependencies.
- You need per-table IAM.

## When not to use

- Plain blob storage — use a regular bucket.
- Non-Iceberg tabular formats (Hudi, Delta) — stick with a regular bucket and a separate catalog service.
