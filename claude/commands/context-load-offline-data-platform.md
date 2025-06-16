# /context-load-offline-data-platform

Load comprehensive context about the modern lakehouse architecture stack including Trino, Apache Iceberg, Nessie, Spark, and Airflow.

## Instructions

When this command is executed, you MUST:

1. First attempt to use the Context7 MCP server if available to load documentation for Trino, Apache Iceberg, Nessie, Apache Spark, Apache Airflow, and Rook Ceph

2. If Context7 is not available, use the WebFetch tool to load documentation from these key sources:
   - **Trino Documentation**: `https://trino.io/docs/current/`
     - Focus on: cluster configuration, query optimization, connector setup, performance tuning
   - **Apache Iceberg**: `https://iceberg.apache.org/docs/latest/`
     - Focus on: table format, partitioning, schema evolution, catalog management
   - **Nessie**: `https://projectnessie.org/docs/`
     - Focus on: version control concepts, branching strategies, catalog integration
   - **Apache Spark on K8s**: `https://spark.apache.org/docs/latest/running-on-kubernetes.html`
     - Focus on: operator deployment, job submission, resource management
   - **Apache Airflow**: `https://airflow.apache.org/docs/apache-airflow/stable/`
     - Focus on: KubernetesExecutor, DAG design, operator usage, monitoring
   - **Rook Ceph**: `https://rook.io/docs/rook/latest-release/Storage-Configuration/Object-Storage-RGW/object-storage/`
     - Focus on: S3-compatible object storage, bucket policies, performance tuning, multi-site replication

3. Prioritize loading documentation sections on:
   - Distributed SQL query patterns and optimization techniques
   - Iceberg table management and maintenance operations
   - Data versioning workflows with Nessie branches and tags
   - Spark job orchestration on Kubernetes
   - Airflow DAG design for data pipeline workflows
   - S3-compatible object storage integration patterns with Rook Ceph
   - Ceph RGW configuration for lakehouse workloads
   - Performance tuning for analytical workloads
   - Multi-cluster coordination and federation

4. Focus on lakehouse-specific areas:
   - **Query Optimization**: Trino cost-based optimization, partition pruning, predicate pushdown
   - **Table Management**: Iceberg snapshots, time travel, compaction strategies
   - **Version Control**: Nessie branching for experimentation and rollback
   - **Processing Patterns**: Spark structured streaming with Iceberg sinks
   - **Orchestration**: Airflow operators for Trino queries and Spark jobs
   - **Storage Layer**: Rook Ceph S3 configuration, bucket lifecycle policies, storage classes
   - **Storage Layout**: Parquet file optimization, Z-ordering, bloom filters
   - **Catalog Integration**: Unified metadata across Trino, Spark, and Nessie
   - **Monitoring**: Query performance metrics, Ceph cluster health, storage utilization

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building production-ready lakehouse architectures on Kubernetes
- Implementing ACID transactions with Iceberg tables
- Managing data versioning workflows with Nessie branches
- Optimizing Trino queries for large-scale analytics
- Designing resilient Airflow DAGs with KubernetesExecutor
- Configuring Rook Ceph for S3-compatible lakehouse storage
- Integrating S3-compatible storage with analytical engines
- Troubleshooting distributed query performance and storage issues
- Migrating from traditional data warehouses to lakehouse architecture

## Usage

```
/context-load-offline-data-platform
```
