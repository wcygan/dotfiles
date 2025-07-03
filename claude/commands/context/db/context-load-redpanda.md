# /context-load-redpanda

Load comprehensive documentation context for Redpanda streaming platform development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Redpanda Documentation**: `https://docs.redpanda.com/`
     - Focus on: architecture, deployment, administration
   - **Kafka Compatibility**: `https://docs.redpanda.com/current/reference/kafka-compatibility/`
     - Focus on: API compatibility, migration strategies
   - **Getting Started**: `https://docs.redpanda.com/current/get-started/`
     - Focus on: installation, configuration, basic usage
   - **Performance Tuning**: `https://docs.redpanda.com/current/manage/cluster-maintenance/`
     - Focus on: optimization, monitoring, troubleshooting
   - **Schema Registry**: `https://docs.redpanda.com/current/manage/schema-registry/`
     - Focus on: schema management, compatibility, evolution

3. **Key documentation sections to prioritize**:
   - Kafka API compatibility
   - Topic and partition management
   - Producer and consumer patterns
   - Schema registry usage
   - Performance optimization
   - Cluster management

4. **Focus areas for this stack**:
   - High-throughput streaming
   - Low-latency message processing
   - Schema evolution strategies
   - Consumer group management
   - Transaction support
   - Monitoring and observability
   - Client library usage
   - Migration from Kafka

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building streaming applications
- Optimizing message throughput
- Managing schemas effectively
- Implementing consumer patterns
- Performance tuning strategies
- Monitoring streaming pipelines
- Migrating from Apache Kafka
- Troubleshooting streaming issues

## Usage Example

```
/context-load-redpanda
```
