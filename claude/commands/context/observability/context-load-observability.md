# /context-load-observability

Load comprehensive documentation context for observability with Prometheus, Grafana, Jaeger, and OpenTelemetry.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Prometheus Documentation**: `https://prometheus.io/docs/`
     - Focus on: configuration, querying, alerting, federation
   - **Grafana Documentation**: `https://grafana.com/docs/`
     - Focus on: dashboards, data sources, alerting, visualization
   - **Jaeger Documentation**: `https://www.jaegertracing.io/docs/`
     - Focus on: distributed tracing, deployment, configuration
   - **OpenTelemetry Documentation**: `https://opentelemetry.io/docs/`
     - Focus on: instrumentation, collectors, exporters, SDK usage
   - **Best Practices Guide**: `https://prometheus.io/docs/practices/`
     - Focus on: metric naming, instrumentation, performance

3. **Key documentation sections to prioritize**:
   - Metrics collection and storage
   - Dashboard design and visualization
   - Distributed tracing implementation
   - Alerting and notification strategies
   - Performance monitoring
   - SLO/SLI implementation

4. **Focus areas for this stack**:
   - Application instrumentation
   - Metrics aggregation and storage
   - Dashboard creation and management
   - Distributed tracing setup
   - Alert rule configuration
   - Performance monitoring
   - Incident response workflows
   - Observability best practices

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Implementing comprehensive monitoring
- Creating effective dashboards
- Setting up distributed tracing
- Configuring meaningful alerts
- Optimizing observability performance
- Troubleshooting monitoring issues
- Designing SLO/SLI frameworks
- Building incident response processes

## Usage Example

```
/context-load-observability
```
