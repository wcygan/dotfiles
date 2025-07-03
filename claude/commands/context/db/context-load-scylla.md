# /context-load-scylla

Load comprehensive documentation context for ScyllaDB development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **ScyllaDB Documentation**: `https://docs.scylladb.com/`
     - Focus on: architecture, data modeling, performance tuning
   - **CQL Reference**: `https://cassandra.apache.org/doc/latest/cassandra/cql/`
     - Focus on: query language, data types, functions
   - **Data Modeling Guide**: `https://docs.scylladb.com/stable/data-modeling/`
     - Focus on: partition keys, clustering, denormalization
   - **Performance Tuning**: `https://docs.scylladb.com/stable/operating-scylla/`
     - Focus on: configuration, monitoring, optimization
   - **ScyllaDB University**: `https://university.scylladb.com/`
     - Focus on: best practices, advanced topics, case studies

3. **Key documentation sections to prioritize**:
   - Data modeling principles
   - CQL query patterns
   - Performance optimization
   - Cluster management
   - Monitoring and alerting
   - Driver usage

4. **Focus areas for this stack**:
   - Partition key design
   - Clustering column strategies
   - Query pattern optimization
   - Consistency level tuning
   - Compaction strategies
   - Monitoring and metrics
   - Driver integration
   - Migration from Cassandra

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Designing efficient data models
- Writing optimized CQL queries
- Performance tuning strategies
- Cluster configuration and management
- Monitoring ScyllaDB clusters
- Application integration patterns
- Migration strategies
- Troubleshooting performance issues

## Usage Example

```
/context-load-scylla
```
