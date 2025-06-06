# /observe

Instruments applications for production-grade observability.

## Usage
```
/observe <service>
/observe <service> --metrics-only
/observe <service> --logging-only
/observe <service> --tracing
```

## Description
This command transforms "black box" services into fully observable systems by automatically adding metrics, structured logging, distributed tracing, and monitoring dashboards. It makes production systems transparent and debuggable.

### What it adds:

#### 1. Metrics Instrumentation
Injects comprehensive Prometheus metrics for key operations:

**HTTP/API Metrics:**
- Request duration histograms with percentiles (p50, p95, p99)
- Request rate counters by endpoint and method
- Error rate counters by status code and error type
- Active connections and concurrent requests

**Application Metrics:**
- Business logic counters (user registrations, orders, etc.)
- Resource utilization (memory, CPU, database connections)
- Queue depths and processing times
- Cache hit/miss ratios

**Framework-Specific Implementation:**

**Go (with Prometheus client):**
```go
var (
    httpDuration = prometheus.NewHistogramVec(
        prometheus.HistogramOpts{
            Name: "http_request_duration_seconds",
            Help: "Duration of HTTP requests",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint", "status_code"},
    )
    
    requestsTotal = prometheus.NewCounterVec(
        prometheus.CounterOpts{
            Name: "http_requests_total", 
            Help: "Total number of HTTP requests",
        },
        []string{"method", "endpoint", "status_code"},
    )
)

// Middleware injection
func MetricsMiddleware(next http.Handler) http.Handler {
    return promhttp.InstrumentHandlerDuration(httpDuration,
        promhttp.InstrumentHandlerCounter(requestsTotal, next))
}
```

**Rust (with metrics crate):**
```rust
use metrics::{counter, histogram, gauge};

#[instrument]
async fn handle_request(req: Request<Body>) -> Result<Response<Body>, Error> {
    let start = Instant::now();
    let method = req.method().as_str();
    let path = req.uri().path();
    
    let result = process_request(req).await;
    
    let duration = start.elapsed().as_secs_f64();
    histogram!("http_request_duration_seconds")
        .with_tag("method", method)
        .with_tag("path", path)
        .record(duration);
        
    counter!("http_requests_total")
        .with_tag("method", method)
        .with_tag("status", result.status().as_str())
        .increment(1);
        
    result
}
```

#### 2. Structured Logging
Refactors logging to use structured, machine-readable formats:

**Log Structure Enhancement:**
- JSON format for log aggregation systems
- Consistent field naming and data types
- Request correlation IDs for tracing
- Structured error context and stack traces

**Framework Integration:**

**Go (with slog):**
```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))

func handleUser(w http.ResponseWriter, r *http.Request) {
    requestID := r.Header.Get("X-Request-ID")
    
    logger.InfoContext(r.Context(), "processing user request",
        slog.String("request_id", requestID),
        slog.String("user_id", getUserID(r)),
        slog.String("endpoint", r.URL.Path),
        slog.Duration("processing_time", time.Since(start)),
    )
}
```

**Rust (with tracing):**
```rust
use tracing::{info, error, instrument};

#[instrument(fields(user_id = %user.id, request_id = %req_id))]
async fn process_user_order(user: &User, order: Order, req_id: String) -> Result<OrderResponse, OrderError> {
    info!("processing order for user");
    
    match create_order(&order).await {
        Ok(response) => {
            info!(order_id = %response.id, "order created successfully");
            Ok(response)
        },
        Err(e) => {
            error!(error = %e, "failed to create order");
            Err(e)
        }
    }
}
```

#### 3. Distributed Tracing
Implements OpenTelemetry for request flow visibility:

**Trace Context Propagation:**
- Automatic span creation for HTTP requests
- Database query tracing with SQL statements
- External service call instrumentation
- Custom business logic spans

**Integration Examples:**

**Java (with OpenTelemetry):**
```java
@RestController
public class UserController {
    
    @GetMapping("/users/{id}")
    @WithSpan("get_user_by_id")
    public ResponseEntity<User> getUser(@SpanAttribute("user.id") @PathVariable Long id) {
        Span currentSpan = Span.current();
        currentSpan.addEvent("starting user lookup");
        
        User user = userService.findById(id);
        currentSpan.setAllAttributes(Attributes.of(
            AttributeKey.stringKey("user.email"), user.getEmail(),
            AttributeKey.longKey("user.created_timestamp"), user.getCreatedAt().toEpochMilli()
        ));
        
        return ResponseEntity.ok(user);
    }
}
```

#### 4. Health Checks and Readiness Probes
Creates comprehensive health monitoring endpoints:

**Health Check Implementation:**
```go
type HealthCheck struct {
    database    DatabaseChecker
    redis       RedisChecker
    externalAPI ExternalAPIChecker
}

func (h *HealthCheck) CheckHealth(ctx context.Context) HealthStatus {
    checks := map[string]ComponentHealth{
        "database":     h.database.Check(ctx),
        "redis":        h.redis.Check(ctx),
        "external_api": h.externalAPI.Check(ctx),
    }
    
    overall := "healthy"
    for _, check := range checks {
        if check.Status != "healthy" {
            overall = "unhealthy"
            break
        }
    }
    
    return HealthStatus{
        Status:     overall,
        Timestamp:  time.Now(),
        Components: checks,
        Version:    buildInfo.Version,
        Uptime:     time.Since(startTime),
    }
}
```

### 5. Monitoring Dashboards
Generates Grafana dashboard configurations:

**Dashboard Features:**
- Service overview with golden signals (latency, traffic, errors, saturation)
- Detailed breakdowns by endpoint and error type
- Resource utilization and capacity planning
- SLA/SLO tracking with burn rate alerts

**Generated Dashboard JSON:**
```json
{
  "dashboard": {
    "title": "User Service Monitoring",
    "panels": [
      {
        "title": "Request Rate",
        "type": "stat",
        "targets": [
          {
            "expr": "sum(rate(http_requests_total{service=\"user-service\"}[5m]))",
            "legendFormat": "Requests/sec"
          }
        ]
      },
      {
        "title": "Response Time Percentiles", 
        "type": "graph",
        "targets": [
          {
            "expr": "histogram_quantile(0.50, http_request_duration_seconds_bucket{service=\"user-service\"})",
            "legendFormat": "p50"
          },
          {
            "expr": "histogram_quantile(0.95, http_request_duration_seconds_bucket{service=\"user-service\"})",
            "legendFormat": "p95"
          }
        ]
      }
    ]
  }
}
```

### 6. Alerting Rules
Creates Prometheus alerting rules for common failure modes:

**Generated Alert Rules:**
```yaml
groups:
  - name: user-service-alerts
    rules:
      - alert: HighErrorRate
        expr: |
          (
            sum(rate(http_requests_total{service="user-service",status_code=~"5.."}[5m])) /
            sum(rate(http_requests_total{service="user-service"}[5m]))
          ) > 0.05
        for: 2m
        labels:
          severity: critical
          service: user-service
        annotations:
          summary: "High error rate detected"
          description: "Service {{ $labels.service }} has error rate above 5% for 2 minutes"
          
      - alert: HighLatency
        expr: |
          histogram_quantile(0.95, 
            sum(rate(http_request_duration_seconds_bucket{service="user-service"}[5m])) by (le)
          ) > 0.5
        for: 3m
        labels:
          severity: warning
          service: user-service
        annotations:
          summary: "High latency detected"
          description: "95th percentile latency is above 500ms"
```

## Examples

### Add full observability to a service:
```
/observe user-service
```

### Add only metrics instrumentation:
```
/observe api-gateway --metrics-only
```

### Add distributed tracing:
```
/observe payment-service --tracing
```

## Generated File Structure
```
observability/
├── metrics/
│   ├── prometheus.yml      # Scrape configuration
│   └── metrics.go|rs|java  # Application metrics code
├── dashboards/
│   ├── service-overview.json
│   └── detailed-metrics.json
├── alerts/
│   └── service-alerts.yml
└── tracing/
    └── otel-config.yml
```

## Technology Support

**Metrics Libraries:**
- **Go**: Prometheus client, expvar
- **Rust**: metrics, prometheus crate
- **Java**: Micrometer, Prometheus JVM client
- **Node/Deno**: prom-client, @opentelemetry/metrics

**Logging Frameworks:**
- **Go**: slog, logrus, zap
- **Rust**: tracing, log + env_logger
- **Java**: Logback, Log4j2 with JSON encoders
- **Node/Deno**: winston, pino

**Tracing Systems:**
- OpenTelemetry (all languages)
- Jaeger and Zipkin compatible
- Cloud provider tracing (AWS X-Ray, Google Cloud Trace)

## Integration with Other Commands
- Use with `/deploy` to add monitoring to Kubernetes deployments
- Combine with `/harden` for security-aware logging (no sensitive data)
- Use after `/containerize` to add observability to Docker images
- Integrate with `/ci-gen` to test observability endpoints in CI