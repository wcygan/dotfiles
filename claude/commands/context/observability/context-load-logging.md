# /context-load-logging

Load comprehensive documentation context for logging and tracing with Loki and structured logging patterns.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Loki Documentation**: `https://grafana.com/docs/loki/`
     - Focus on: log aggregation, querying, configuration, storage
   - **Structured Logging Guide**: `https://12factor.net/logs`
     - Focus on: twelve-factor app logging principles
   - **OpenTelemetry Logging**: `https://opentelemetry.io/docs/concepts/signals/logs/`
     - Focus on: trace correlation, log collection, exporters
   - **Grafana Log Management**: `https://grafana.com/docs/grafana/latest/explore/logs-integration/`
     - Focus on: log visualization, correlation, querying
   - **Best Practices**: `https://grafana.com/docs/loki/latest/best-practices/`
     - Focus on: label design, performance, retention

3. **Key documentation sections to prioritize**:
   - Log aggregation and storage
   - Structured logging patterns
   - Log correlation with traces
   - Query language and analysis
   - Retention and performance
   - Alert integration

4. **Focus areas for this stack**:
   - Centralized log collection
   - Structured log format design
   - Log correlation strategies
   - Query optimization
   - Retention policy management
   - Performance monitoring
   - Security and compliance
   - Integration with tracing

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Implementing centralized logging
- Designing structured log formats
- Setting up log correlation
- Optimizing log queries
- Managing log retention
- Integrating logs with traces
- Securing log pipelines
- Troubleshooting log issues

## Usage Example

```
/context-load-logging
```
