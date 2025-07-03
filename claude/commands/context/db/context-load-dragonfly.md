# /context-load-dragonfly

Load comprehensive documentation context for DragonflyDB development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **DragonflyDB Documentation**: `https://dragonflydb.io/docs/`
     - Focus on: installation, configuration, Redis compatibility
   - **Getting Started**: `https://dragonflydb.io/docs/getting-started`
     - Focus on: installation, basic configuration, Redis compatibility
   - **Managing Dragonfly**: `https://dragonflydb.io/docs/managing-dragonfly/`
     - Focus on: cluster setup, performance tuning, monitoring
   - **Configuration Reference**: `https://dragonflydb.io/docs/managing-dragonfly/`
     - Focus on: cluster setup, persistence, security
   - **Client Libraries**: `https://dragonflydb.io/docs/integrations/`
     - Focus on: driver usage, connection patterns

3. **Key documentation sections to prioritize**:
   - Redis API compatibility
   - Performance characteristics
   - Clustering configuration
   - Memory optimization
   - Persistence options
   - Monitoring and metrics

4. **Focus areas for this stack**:
   - Redis command compatibility
   - Memory-efficient data structures
   - Multi-threading architecture
   - Cluster deployment
   - Performance monitoring
   - Migration from Redis
   - Client connection patterns
   - Security configuration

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Migrating from Redis to DragonflyDB
- Optimizing memory usage
- Configuring high-performance clusters
- Monitoring DragonflyDB instances
- Using Redis clients with DragonflyDB
- Performance tuning strategies
- Security best practices
- Troubleshooting common issues

## Usage Example

```
/context-load-dragonfly
```
