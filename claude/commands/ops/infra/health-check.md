---
allowed-tools: Bash(kubectl:*), Bash(docker:*), Bash(curl:*), Bash(jq:*), Bash(systemctl:*)
description: Implement comprehensive health monitoring with real-time system assessment
---

# /health-check

Implement comprehensive health monitoring for $ARGUMENT with automated alerting and status reporting. Think harder about complex distributed system health patterns and monitoring strategies when dealing with microservices architectures.

## Live System Context

- **Cluster Status**: !`kubectl get nodes -o json | jq '.items[] | {name: .metadata.name, status: .status.conditions[-1].type}'`
- **Container Health**: !`docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -10`
- **System Services**: !`systemctl --failed --no-legend | wc -l`
- **Resource Usage**: !`free -h && df -h / | tail -1`
- **Active Health Endpoints**: !`curl -s http://localhost:8080/health || echo "Health endpoint unreachable"`

## Configuration Analysis

Analyze existing configuration files for current health check setup:

- System architecture: @docker-compose.yml @k8s/*.yaml
- Application configs: @package.json @deno.json @Cargo.toml
- Monitoring setup: @prometheus.yml @grafana-dashboards/*.json
- Health check implementations: @**/_health_.{ts,js,go,rs,java}

## Health Check Implementation

### 1. System Analysis

```bash
# Identify services and dependencies
fd "docker-compose|k8s|deployment" --type f
rg "port:|expose:|listen" -t yaml -t json

# Find existing health endpoints
rg "health|status|ping|ready|live" --type-add 'code:*.{ts,js,go,rs,java}'
rg "@Get.*health|router.*health|/health" -A 2

# Check for monitoring tools
fd "prometheus|grafana|datadog|newrelic" --type f
```

### 2. Health Check Patterns

#### Basic HTTP Health Check

```typescript
// health-check.ts
interface HealthStatus {
  status: "healthy" | "degraded" | "unhealthy";
  timestamp: string;
  version: string;
  uptime: number;
  checks: Record<string, CheckResult>;
}

interface CheckResult {
  status: "pass" | "fail" | "warn";
  message?: string;
  responseTime?: number;
  details?: Record<string, any>;
}

class HealthCheckService {
  private startTime = Date.now();
  private checks = new Map<string, () => Promise<CheckResult>>();

  register(name: string, check: () => Promise<CheckResult>) {
    this.checks.set(name, check);
  }

  async getHealth(): Promise<HealthStatus> {
    const results: Record<string, CheckResult> = {};
    let overallStatus: "healthy" | "degraded" | "unhealthy" = "healthy";

    // Execute all checks in parallel
    await Promise.all(
      Array.from(this.checks.entries()).map(async ([name, check]) => {
        const start = Date.now();
        try {
          results[name] = await check();
          results[name].responseTime = Date.now() - start;

          if (results[name].status === "fail") {
            overallStatus = "unhealthy";
          } else if (results[name].status === "warn" && overallStatus === "healthy") {
            overallStatus = "degraded";
          }
        } catch (error) {
          results[name] = {
            status: "fail",
            message: error.message,
            responseTime: Date.now() - start,
          };
          overallStatus = "unhealthy";
        }
      }),
    );

    return {
      status: overallStatus,
      timestamp: new Date().toISOString(),
      version: Deno.env.get("APP_VERSION") || "unknown",
      uptime: Date.now() - this.startTime,
      checks: results,
    };
  }
}

// Register checks
const healthService = new HealthCheckService();

// Database check
healthService.register("database", async () => {
  try {
    const start = Date.now();
    await db.query("SELECT 1");
    const latency = Date.now() - start;

    return {
      status: latency < 100 ? "pass" : "warn",
      details: { latency },
    };
  } catch (error) {
    return { status: "fail", message: error.message };
  }
});

// Redis check
healthService.register("cache", async () => {
  try {
    await redis.ping();
    const info = await redis.info();
    const memory = parseInt(info.match(/used_memory:(\d+)/)?.[1] || "0");

    return {
      status: memory < 1_000_000_000 ? "pass" : "warn", // Warn if > 1GB
      details: { memory },
    };
  } catch (error) {
    return { status: "fail", message: error.message };
  }
});

// External API check
healthService.register("external_api", async () => {
  try {
    const response = await fetch("https://api.example.com/health", {
      signal: AbortSignal.timeout(5000),
    });

    return {
      status: response.ok ? "pass" : "warn",
      details: { statusCode: response.status },
    };
  } catch (error) {
    return { status: "fail", message: "API unreachable" };
  }
});
```

#### Kubernetes Probes

```yaml
# k8s-health-probes.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-service
spec:
  template:
    spec:
      containers:
        - name: api
          image: api:latest
          ports:
            - containerPort: 8080

            # Liveness probe - restart if fails
          livenessProbe:
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 30
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 3

          # Readiness probe - remove from load balancer if fails
          readinessProbe:
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 5
            timeoutSeconds: 3
            failureThreshold: 2

          # Startup probe - for slow starting containers
          startupProbe:
            httpGet:
              path: /health/startup
              port: 8080
            initialDelaySeconds: 0
            periodSeconds: 10
            timeoutSeconds: 5
            failureThreshold: 30
```

#### Comprehensive System Check

```rust
// health_check.rs
use std::time::{Duration, Instant};
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct HealthCheck {
    pub status: HealthStatus,
    pub timestamp: String,
    pub checks: Vec<ComponentCheck>,
    pub system: SystemInfo,
}

#[derive(Serialize, Deserialize)]
pub struct ComponentCheck {
    pub name: String,
    pub status: CheckStatus,
    pub response_time_ms: u64,
    pub message: Option<String>,
    pub metadata: Option<serde_json::Value>,
}

#[derive(Serialize, Deserialize)]
pub struct SystemInfo {
    pub cpu_usage: f32,
    pub memory_usage: f32,
    pub disk_usage: f32,
    pub open_connections: u32,
}

pub async fn perform_health_check() -> HealthCheck {
    let start = Instant::now();
    let mut checks = vec![];
    let mut overall_status = HealthStatus::Healthy;
    
    // Database check
    let db_check = check_database().await;
    if db_check.status == CheckStatus::Unhealthy {
        overall_status = HealthStatus::Unhealthy;
    }
    checks.push(db_check);
    
    // Message queue check
    let mq_check = check_message_queue().await;
    if mq_check.status == CheckStatus::Degraded && overall_status == HealthStatus::Healthy {
        overall_status = HealthStatus::Degraded;
    }
    checks.push(mq_check);
    
    // Disk space check
    let disk_check = check_disk_space();
    checks.push(disk_check);
    
    // Memory check
    let memory_check = check_memory();
    checks.push(memory_check);
    
    HealthCheck {
        status: overall_status,
        timestamp: chrono::Utc::now().to_rfc3339(),
        checks,
        system: get_system_info(),
    }
}

async fn check_database() -> ComponentCheck {
    let start = Instant::now();
    
    match sqlx::query("SELECT 1").fetch_one(&*DB_POOL).await {
        Ok(_) => ComponentCheck {
            name: "database".to_string(),
            status: CheckStatus::Healthy,
            response_time_ms: start.elapsed().as_millis() as u64,
            message: None,
            metadata: None,
        },
        Err(e) => ComponentCheck {
            name: "database".to_string(),
            status: CheckStatus::Unhealthy,
            response_time_ms: start.elapsed().as_millis() as u64,
            message: Some(e.to_string()),
            metadata: None,
        },
    }
}
```

### 3. Monitoring Integration

#### Prometheus Metrics

```go
// health_metrics.go
package health

import (
    "github.com/prometheus/client_golang/prometheus"
    "github.com/prometheus/client_golang/prometheus/promauto"
)

var (
    healthCheckDuration = promauto.NewHistogramVec(prometheus.HistogramOpts{
        Name: "health_check_duration_seconds",
        Help: "Duration of health checks",
    }, []string{"check_name"})
    
    healthCheckStatus = promauto.NewGaugeVec(prometheus.GaugeOpts{
        Name: "health_check_status",
        Help: "Status of health checks (1=healthy, 0=unhealthy)",
    }, []string{"check_name"})
    
    systemMetrics = promauto.NewGaugeVec(prometheus.GaugeOpts{
        Name: "system_resource_usage",
        Help: "System resource usage",
    }, []string{"resource"})
)

func RecordHealthCheck(name string, duration float64, healthy bool) {
    healthCheckDuration.WithLabelValues(name).Observe(duration)
    if healthy {
        healthCheckStatus.WithLabelValues(name).Set(1)
    } else {
        healthCheckStatus.WithLabelValues(name).Set(0)
    }
}
```

### 4. Status Page Generator

```html
<!-- health-status.html -->
<!DOCTYPE html>
<html>
  <head>
    <title>Service Health Status</title>
    <style>
      .healthy {
        color: green;
      }
      .degraded {
        color: orange;
      }
      .unhealthy {
        color: red;
      }
      .check-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px;
      }
      .check-card {
        border: 1px solid #ddd;
        padding: 15px;
        border-radius: 8px;
      }
    </style>
  </head>
  <body>
    <h1>System Health Status</h1>
    <div id="overall-status"></div>
    <div class="check-grid" id="checks"></div>

    <script>
      async function updateHealth() {
        const response = await fetch("/health");
        const health = await response.json();

        // Update overall status
        const statusEl = document.getElementById("overall-status");
        statusEl.className = health.status;
        statusEl.innerHTML = `
                <h2>Status: ${health.status.toUpperCase()}</h2>
                <p>Last updated: ${new Date(health.timestamp).toLocaleString()}</p>
                <p>Uptime: ${formatUptime(health.uptime)}</p>
            `;

        // Update individual checks
        const checksEl = document.getElementById("checks");
        checksEl.innerHTML = Object.entries(health.checks).map(([name, check]) => `
                <div class="check-card ${check.status}">
                    <h3>${name}</h3>
                    <p>Status: ${check.status}</p>
                    <p>Response time: ${check.responseTime}ms</p>
                    ${check.message ? `<p>Message: ${check.message}</p>` : ""}
                </div>
            `).join("");
      }

      function formatUptime(ms) {
        const seconds = Math.floor(ms / 1000);
        const days = Math.floor(seconds / 86400);
        const hours = Math.floor((seconds % 86400) / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        return `${days}d ${hours}h ${minutes}m`;
      }

      // Update every 10 seconds
      updateHealth();
      setInterval(updateHealth, 10000);
    </script>
  </body>
</html>
```

### 5. Alerting Configuration

```yaml
# alerting-rules.yaml
groups:
  - name: health_checks
    interval: 30s
    rules:
      - alert: ServiceUnhealthy
        expr: health_check_status == 0
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Service {{ $labels.check_name }} is unhealthy"
          description: "{{ $labels.check_name }} has been failing for 5 minutes"

      - alert: HighResponseTime
        expr: health_check_duration_seconds > 1
        for: 5m
        labels:
          severity: warning
        annotations:
          summary: "High response time for {{ $labels.check_name }}"
          description: "Response time > 1s for 5 minutes"

      - alert: HighMemoryUsage
        expr: system_resource_usage{resource="memory"} > 0.9
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High memory usage detected"
          description: "Memory usage above 90% for 5 minutes"
```

## Output Format

````markdown
# Health Check Configuration

## Endpoints

- **Liveness**: `/health/live` - Basic aliveness check
- **Readiness**: `/health/ready` - Ready to serve traffic
- **Detailed**: `/health` - Comprehensive status

## Checks Implemented

### Critical Checks

- ✅ Database connectivity
- ✅ Cache availability
- ✅ Message queue status

### Non-Critical Checks

- ⚠️ External API availability
- ⚠️ Disk space (warning at 80%)
- ⚠️ Memory usage (warning at 75%)

## Response Format

```json
{
  "status": "healthy|degraded|unhealthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "version": "1.2.3",
  "uptime": 3600000,
  "checks": {
    "database": {
      "status": "pass",
      "responseTime": 15
    }
  }
}
```
````

## Monitoring Setup

```bash
# Prometheus endpoint
curl http://localhost:9090/metrics | grep health

# Status page
open http://localhost:8080/health/status

# CLI check
curl -s http://localhost:8080/health | jq .status
```

## Alert Configuration

- **Critical**: Service down, database unreachable
- **Warning**: High latency, resource usage
- **Info**: Version changes, restarts

```
## Guidelines

- Keep health checks lightweight
- Set appropriate timeouts
- Include dependency checks
- Monitor trends, not just current state
- Document what each check validates
- Test failure scenarios
```
