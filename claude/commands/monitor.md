# /monitor

Set up comprehensive monitoring, observability, and alerting systems for $ARGUMENT with modern tooling and intelligent metric collection.

## Monitoring Strategy Framework

### Phase 1: Observability Foundation

**The Three Pillars**

- **Metrics**: Quantitative measurements over time
- **Logs**: Discrete events with timestamps and context
- **Traces**: Request flows through distributed systems

**Modern Stack (Preferred)**

```yaml
# Observability Stack
metrics:
  collection: Prometheus + OpenTelemetry
  storage: Prometheus + Thanos (long-term)
  visualization: Grafana

logs:
  collection: Vector + OpenTelemetry
  storage: Loki + S3
  visualization: Grafana

traces:
  collection: OpenTelemetry Collector
  storage: Jaeger + S3
  visualization: Jaeger UI + Grafana

# Alternative: All-in-one solutions
observability:
  - Grafana Cloud (SaaS)
  - DataDog (SaaS)
  - New Relic (SaaS)
  - Honeycomb (SaaS)
```

### Phase 2: Application Monitoring

**Golden Signals (SRE)**

```yaml
# The Four Golden Signals
latency:
  description: "Time to serve requests"
  metrics:
    - response_time_p50
    - response_time_p95
    - response_time_p99
  alerts:
    - p95 > 500ms for 5 minutes
    - p99 > 2s for 2 minutes

traffic:
  description: "Demand on the system"
  metrics:
    - requests_per_second
    - concurrent_users
    - throughput
  alerts:
    - RPS drops 50% below baseline
    - Traffic spike >200% of capacity

errors:
  description: "Rate of failed requests"
  metrics:
    - error_rate_percentage
    - 4xx_error_rate
    - 5xx_error_rate
  alerts:
    - Error rate >1% for 5 minutes
    - 5xx errors >0.1% for 2 minutes

saturation:
  description: "How full the service is"
  metrics:
    - cpu_utilization
    - memory_utilization
    - disk_utilization
    - connection_pool_usage
  alerts:
    - CPU >80% for 10 minutes
    - Memory >85% for 5 minutes
```

**Application-Specific Metrics**

```bash
# Business Logic Metrics
user_registrations_total
orders_processed_total
payment_failures_total
user_session_duration_seconds

# Performance Metrics
database_query_duration_seconds
cache_hit_ratio
queue_size_current
background_job_duration_seconds

# Resource Metrics
goroutines_current  # Go
heap_size_bytes     # Memory usage
gc_duration_seconds # Garbage collection
```

### Phase 3: Infrastructure Monitoring

**System Metrics (USE Method)**

- **Utilization**: Percentage of time the resource is busy
- **Saturation**: Amount of queued work
- **Errors**: Count of error events

```yaml
# Infrastructure Monitoring
compute:
  cpu:
    - cpu_utilization_percent
    - load_average_1m
    - context_switches_per_second
  memory:
    - memory_utilization_percent
    - memory_available_bytes
    - swap_usage_percent
  disk:
    - disk_utilization_percent
    - disk_io_read_bytes_per_second
    - disk_io_write_bytes_per_second

network:
  - network_io_bytes_per_second
  - network_connections_active
  - network_errors_per_second

containers:
  - container_cpu_usage_percent
  - container_memory_usage_bytes
  - container_restart_count

kubernetes:
  - pod_status
  - node_ready_status
  - persistent_volume_usage_percent
```

**Service Discovery Integration**

```yaml
# Prometheus Service Discovery
prometheus_config:
  scrape_configs:
    - job_name: "kubernetes-pods"
      kubernetes_sd_configs:
        - role: pod
      relabel_configs:
        - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
          action: keep
          regex: true
```

### Phase 4: Distributed Tracing

**OpenTelemetry Implementation**

```rust
// Rust example with axum + tracing
use opentelemetry::trace::TraceContextExt;
use tracing_opentelemetry::OpenTelemetrySpanExt;

#[tracing::instrument(skip(db))]
async fn handle_user_request(
    user_id: String,
    db: Arc<Database>
) -> Result<UserResponse> {
    let span = tracing::Span::current();
    span.set_attribute("user.id", user_id.clone());
    
    // Trace database query
    let user = db.get_user(&user_id).await?;
    
    // Trace external API call
    let profile = external_api::get_profile(&user_id).await?;
    
    Ok(UserResponse { user, profile })
}
```

```go
// Go example with ConnectRPC + OpenTelemetry
func (s *UserService) GetUser(ctx context.Context, req *pb.GetUserRequest) (*pb.GetUserResponse, error) {
    ctx, span := otel.Tracer("user-service").Start(ctx, "GetUser")
    defer span.End()
    
    span.SetAttributes(
        attribute.String("user.id", req.UserId),
        attribute.String("operation", "get_user"),
    )
    
    // Trace database operation
    user, err := s.db.GetUser(ctx, req.UserId)
    if err != nil {
        span.RecordError(err)
        return nil, err
    }
    
    return &pb.GetUserResponse{User: user}, nil
}
```

### Phase 5: Alerting Strategy

**Alert Levels and Escalation**

```yaml
alert_levels:
  P1_CRITICAL:
    description: "System down or critical business impact"
    response_time: "< 15 minutes"
    escalation: "Immediate PagerDuty + Phone"
    examples:
      - "Service completely unavailable"
      - "Database down"
      - "Security breach detected"

  P2_HIGH:
    description: "Significant degradation or risk"
    response_time: "< 1 hour"
    escalation: "PagerDuty during business hours"
    examples:
      - "Error rate >5%"
      - "Response time >2s"
      - "High memory usage >90%"

  P3_MEDIUM:
    description: "Performance issues or warnings"
    response_time: "< 4 hours"
    escalation: "Slack notification"
    examples:
      - "Disk usage >80%"
      - "Unusual traffic patterns"
      - "Certificate expiring in 7 days"

  P4_LOW:
    description: "Informational or minor issues"
    response_time: "Next business day"
    escalation: "Email or dashboard"
    examples:
      - "Scheduled maintenance reminder"
      - "Resource optimization opportunity"
```

**Smart Alerting Rules**

```yaml
# Prometheus Alert Rules
groups:
  - name: application.rules
    rules:
      - alert: HighErrorRate
        expr: (rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m])) > 0.01
        for: 5m
        labels:
          severity: P2_HIGH
        annotations:
          summary: "High error rate detected"
          description: "{{ $labels.service }} has error rate of {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
        for: 10m
        labels:
          severity: P2_HIGH
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is {{ $value }}s"

      # Alert fatigue prevention
      - alert: DatabaseConnectionPool
        expr: database_connections_active / database_connections_max > 0.8
        for: 15m # Longer duration to avoid flapping
        labels:
          severity: P3_MEDIUM
        annotations:
          runbook_url: "https://docs.company.com/runbooks/database-connections"
```

### Phase 6: Dashboard Strategy

**Hierarchical Dashboard Design**

```yaml
dashboard_hierarchy:
  L1_EXECUTIVE:
    purpose: "Business overview and SLA compliance"
    metrics:
      - system_availability_percent
      - customer_impact_incidents
      - business_kpi_dashboard
    audience: "Leadership, business stakeholders"

  L2_OPERATIONAL:
    purpose: "Service health and operational metrics"
    metrics:
      - golden_signals_dashboard
      - infrastructure_overview
      - deployment_status
    audience: "SRE, DevOps, on-call engineers"

  L3_DEBUGGING:
    purpose: "Detailed troubleshooting and investigation"
    metrics:
      - detailed_service_metrics
      - distributed_tracing_views
      - log_correlation_dashboard
    audience: "Engineers debugging issues"
```

**Grafana Dashboard Examples**

```json
{
  "dashboard": {
    "title": "Service Golden Signals",
    "panels": [
      {
        "title": "Request Rate",
        "type": "graph",
        "targets": [
          {
            "expr": "rate(http_requests_total[5m])",
            "legendFormat": "{{ method }} {{ status }}"
          }
        ]
      },
      {
        "title": "Error Rate",
        "type": "singlestat",
        "targets": [
          {
            "expr": "rate(http_requests_total{status=~\"5..\"}[5m]) / rate(http_requests_total[5m])",
            "format": "percentunit"
          }
        ],
        "thresholds": "0.01,0.05"
      }
    ]
  }
}
```

### Phase 7: Log Management

**Structured Logging Best Practices**

```rust
// Rust structured logging with tracing
use tracing::{info, warn, error, instrument};

#[instrument(fields(user_id = %user_id, order_id = %order_id))]
async fn process_order(user_id: String, order_id: String) {
    info!("Processing order started");
    
    match validate_order(&order_id).await {
        Ok(_) => info!("Order validation successful"),
        Err(e) => {
            error!(error = %e, "Order validation failed");
            return;
        }
    }
    
    info!(
        duration_ms = 150,
        items_count = 3,
        "Order processing completed"
    );
}
```

**Log Aggregation Pipeline**

```yaml
# Vector configuration for log collection
sources:
  app_logs:
    type: file
    include:
      - /var/log/app/*.log

transforms:
  parse_json:
    type: remap
    inputs: [app_logs]
    source: |
      . = parse_json!(string!(.message))
      .timestamp = parse_timestamp!(string!(.timestamp), "%Y-%m-%dT%H:%M:%S%.fZ")

sinks:
  loki:
    type: loki
    inputs: [parse_json]
    endpoint: http://loki:3100
    labels:
      service: "{{ service }}"
      level: "{{ level }}"
```

### Phase 8: Business Metrics Monitoring

**Key Business Indicators**

```yaml
business_metrics:
  revenue:
    - daily_revenue_usd
    - monthly_recurring_revenue
    - average_order_value

  user_engagement:
    - daily_active_users
    - user_retention_rate_7d
    - session_duration_minutes

  conversion:
    - signup_conversion_rate
    - trial_to_paid_conversion
    - checkout_abandonment_rate

  operational:
    - customer_support_tickets
    - deployment_frequency
    - mean_time_to_recovery
```

### Phase 9: Security Monitoring

**Security Event Detection**

```yaml
security_monitoring:
  authentication:
    - failed_login_attempts
    - unusual_login_locations
    - privilege_escalation_attempts

  application:
    - sql_injection_attempts
    - suspicious_user_agents
    - rate_limiting_triggers

  infrastructure:
    - unauthorized_access_attempts
    - configuration_changes
    - network_anomalies
```

## Implementation Checklist

### Phase 1: Foundation (Week 1-2)

- [ ] Set up metrics collection (Prometheus/OpenTelemetry)
- [ ] Configure log aggregation (Vector/Loki)
- [ ] Install visualization platform (Grafana)
- [ ] Implement basic health checks

### Phase 2: Application Monitoring (Week 3-4)

- [ ] Instrument Golden Signals metrics
- [ ] Add business logic metrics
- [ ] Create service dashboards
- [ ] Set up basic alerting rules

### Phase 3: Infrastructure Monitoring (Week 5-6)

- [ ] Deploy infrastructure monitoring agents
- [ ] Configure Kubernetes monitoring
- [ ] Set up network and storage monitoring
- [ ] Create infrastructure dashboards

### Phase 4: Advanced Observability (Week 7-8)

- [ ] Implement distributed tracing
- [ ] Set up log correlation
- [ ] Create debugging dashboards
- [ ] Fine-tune alert thresholds

### Phase 5: Operations (Week 9-10)

- [ ] Document runbooks and procedures
- [ ] Train team on monitoring tools
- [ ] Establish on-call rotation
- [ ] Conduct monitoring review and optimization

## Integration with Other Commands

- Use with `/deep-dive` to analyze monitoring requirements thoroughly
- Combine with `/dependencies` to monitor critical service dependencies
- Follow with `/plan` to organize monitoring implementation
- Use with `/investigate` to research best monitoring practices
- Apply `/refactor` to improve application observability

The goal is to achieve comprehensive observability that enables proactive issue detection, efficient troubleshooting, and data-driven operational decisions.
