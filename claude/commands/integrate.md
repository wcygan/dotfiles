# /integrate

Connect services, APIs, databases, and tools to create seamless integrations with proper error handling and monitoring.

## Usage

```
/integrate [source system] with [target system] for [purpose]
```

## Integration Process

### 1. Integration Analysis

```bash
# Identify existing integrations
rg "http|https|api|client|sdk" --type-add 'config:*.{json,yaml,toml}'
fd "client|connector|adapter|integration" --type f

# Check for existing API keys/configs
rg "API_KEY|CLIENT_ID|SECRET" .env* --no-ignore
rg "endpoint|baseUrl|host" -t config

# Find current data flows
rg "fetch|axios|request|WebClient" -A 3 -B 1
```

### 2. Integration Patterns

#### REST API Integration

```typescript
// api-integration.ts
interface APIConfig {
  baseUrl: string;
  apiKey?: string;
  timeout?: number;
  retryAttempts?: number;
}

class APIIntegration {
  constructor(private config: APIConfig) {}

  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.config.baseUrl}${endpoint}`;
    const headers = {
      "Content-Type": "application/json",
      ...(this.config.apiKey && { "Authorization": `Bearer ${this.config.apiKey}` }),
      ...options.headers,
    };

    let lastError: Error | null = null;

    for (let attempt = 0; attempt < (this.config.retryAttempts || 3); attempt++) {
      try {
        const response = await fetch(url, {
          ...options,
          headers,
          signal: AbortSignal.timeout(this.config.timeout || 30000),
        });

        if (!response.ok) {
          throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }

        return await response.json();
      } catch (error) {
        lastError = error as Error;
        if (attempt < (this.config.retryAttempts || 3) - 1) {
          await new Promise((resolve) => setTimeout(resolve, Math.pow(2, attempt) * 1000));
        }
      }
    }

    throw lastError;
  }
}
```

#### Database Integration

```typescript
// database-integration.ts
import { Client } from "https://deno.land/x/postgres/mod.ts";
import { connect } from "https://deno.land/x/redis/mod.ts";

class DatabaseIntegration {
  private pgClient: Client;
  private redisClient: Redis;

  async initialize() {
    // PostgreSQL connection
    this.pgClient = new Client({
      hostname: Deno.env.get("PG_HOST") || "localhost",
      port: parseInt(Deno.env.get("PG_PORT") || "5432"),
      user: Deno.env.get("PG_USER"),
      password: Deno.env.get("PG_PASSWORD"),
      database: Deno.env.get("PG_DATABASE"),
    });

    // Redis connection for caching
    this.redisClient = await connect({
      hostname: Deno.env.get("REDIS_HOST") || "localhost",
      port: parseInt(Deno.env.get("REDIS_PORT") || "6379"),
    });

    await this.pgClient.connect();
  }

  async query<T>(sql: string, params?: any[]): Promise<T[]> {
    const cacheKey = `query:${sql}:${JSON.stringify(params)}`;

    // Check cache first
    const cached = await this.redisClient.get(cacheKey);
    if (cached) {
      return JSON.parse(cached);
    }

    // Execute query
    const result = await this.pgClient.queryObject<T>(sql, params);

    // Cache result
    await this.redisClient.setex(cacheKey, 300, JSON.stringify(result.rows));

    return result.rows;
  }
}
```

#### Message Queue Integration

```go
// queue-integration.go
package integration

import (
    "github.com/rabbitmq/amqp091-go"
    "encoding/json"
    "time"
)

type QueueIntegration struct {
    conn    *amqp091.Connection
    channel *amqp091.Channel
}

func NewQueueIntegration(url string) (*QueueIntegration, error) {
    conn, err := amqp091.Dial(url)
    if err != nil {
        return nil, err
    }
    
    ch, err := conn.Channel()
    if err != nil {
        return nil, err
    }
    
    return &QueueIntegration{
        conn:    conn,
        channel: ch,
    }, nil
}

func (q *QueueIntegration) Publish(queue string, message interface{}) error {
    body, err := json.Marshal(message)
    if err != nil {
        return err
    }
    
    return q.channel.Publish(
        "",    // exchange
        queue, // routing key
        false, // mandatory
        false, // immediate
        amqp091.Publishing{
            ContentType: "application/json",
            Body:        body,
            Timestamp:   time.Now(),
        },
    )
}

func (q *QueueIntegration) Subscribe(queue string, handler func([]byte) error) error {
    msgs, err := q.channel.Consume(
        queue,
        "",    // consumer
        false, // auto-ack
        false, // exclusive
        false, // no-local
        false, // no-wait
        nil,   // args
    )
    if err != nil {
        return err
    }
    
    go func() {
        for msg := range msgs {
            if err := handler(msg.Body); err != nil {
                msg.Nack(false, true) // requeue on error
            } else {
                msg.Ack(false)
            }
        }
    }()
    
    return nil
}
```

#### Webhook Integration

```typescript
// webhook-integration.ts
interface WebhookConfig {
  secret: string;
  endpoint: string;
  events: string[];
}

class WebhookIntegration {
  private handlers = new Map<string, Function[]>();

  constructor(private config: WebhookConfig) {}

  on(event: string, handler: Function) {
    if (!this.handlers.has(event)) {
      this.handlers.set(event, []);
    }
    this.handlers.get(event)!.push(handler);
  }

  async handleWebhook(req: Request): Promise<Response> {
    // Verify signature
    const signature = req.headers.get("X-Webhook-Signature");
    if (!this.verifySignature(await req.text(), signature)) {
      return new Response("Invalid signature", { status: 401 });
    }

    const payload = await req.json();
    const event = payload.event || req.headers.get("X-Event-Type");

    // Process event
    const handlers = this.handlers.get(event) || [];
    await Promise.all(handlers.map((h) => h(payload)));

    return new Response("OK", { status: 200 });
  }

  private verifySignature(body: string, signature: string | null): boolean {
    if (!signature) return false;

    const encoder = new TextEncoder();
    const key = encoder.encode(this.config.secret);
    const data = encoder.encode(body);

    // HMAC verification
    return crypto.subtle.verify(
      "HMAC",
      key,
      signature,
      data,
    );
  }
}
```

### 3. Service Orchestration

```typescript
// orchestration.ts
class ServiceOrchestrator {
  private services: Map<string, any> = new Map();

  register(name: string, service: any) {
    this.services.set(name, service);
  }

  async executeWorkflow(workflow: WorkflowDefinition) {
    const context: WorkflowContext = {
      data: {},
      errors: [],
    };

    for (const step of workflow.steps) {
      try {
        const service = this.services.get(step.service);
        if (!service) {
          throw new Error(`Service ${step.service} not found`);
        }

        const result = await service[step.method](...step.args);
        context.data[step.outputKey] = result;

        // Handle conditional branching
        if (step.condition && !step.condition(context)) {
          continue;
        }
      } catch (error) {
        context.errors.push({ step: step.name, error });

        if (step.onError === "fail") {
          throw error;
        } else if (step.onError === "skip") {
          continue;
        }
        // retry logic here
      }
    }

    return context;
  }
}
```

### 4. Authentication Integration

```typescript
// auth-integration.ts
class AuthIntegration {
  async integrateOAuth(provider: string) {
    const config = {
      google: {
        authUrl: "https://accounts.google.com/o/oauth2/v2/auth",
        tokenUrl: "https://oauth2.googleapis.com/token",
        scope: "openid email profile",
      },
      github: {
        authUrl: "https://github.com/login/oauth/authorize",
        tokenUrl: "https://github.com/login/oauth/access_token",
        scope: "read:user user:email",
      },
    };

    return {
      getAuthUrl(clientId: string, redirectUri: string) {
        const params = new URLSearchParams({
          client_id: clientId,
          redirect_uri: redirectUri,
          response_type: "code",
          scope: config[provider].scope,
        });

        return `${config[provider].authUrl}?${params}`;
      },

      async exchangeToken(code: string, clientId: string, clientSecret: string) {
        const response = await fetch(config[provider].tokenUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            code,
            client_id: clientId,
            client_secret: clientSecret,
            grant_type: "authorization_code",
          }),
        });

        return response.json();
      },
    };
  }
}
```

### 5. Monitoring & Logging

```typescript
// monitoring-integration.ts
class MonitoringIntegration {
  constructor(
    private metrics: MetricsClient,
    private logger: Logger,
  ) {}

  wrapIntegration<T extends Function>(name: string, fn: T): T {
    return (async (...args: any[]) => {
      const start = Date.now();
      const labels = { integration: name };

      try {
        this.metrics.increment("integration.calls", labels);
        const result = await fn(...args);

        this.metrics.histogram("integration.duration", Date.now() - start, labels);
        this.metrics.increment("integration.success", labels);

        return result;
      } catch (error) {
        this.metrics.increment("integration.errors", labels);
        this.logger.error(`Integration ${name} failed`, { error, args });
        throw error;
      }
    }) as any;
  }
}
```

## Output Format

````markdown
# Integration: ${Source} ↔ ${Target}

## Overview

- **Purpose**: ${Integration purpose}
- **Type**: ${REST API | Database | Queue | Webhook}
- **Direction**: ${Unidirectional | Bidirectional}

## Configuration

```yaml
integration:
  source:
    type: ${source_type}
    endpoint: ${source_endpoint}
    auth: ${auth_method}
  target:
    type: ${target_type}
    endpoint: ${target_endpoint}
    auth: ${auth_method}
  sync:
    frequency: ${cron_expression}
    batch_size: ${number}
```
````

## Implementation

### Connection Setup

[Code for establishing connections]

### Data Mapping

[Source fields → Target fields mapping]

### Error Handling

- Retry strategy: ${exponential backoff}
- Dead letter queue: ${enabled/disabled}
- Alerting: ${conditions}

### Monitoring

- Success rate metric: `integration.${name}.success`
- Error rate metric: `integration.${name}.errors`
- Latency metric: `integration.${name}.duration`

## Testing

```bash
# Test connection
deno task test:integration

# Verify data flow
curl -X POST localhost:8000/webhook/test

# Check metrics
curl localhost:9090/metrics | grep integration
```

## Deployment

1. Set environment variables
2. Deploy integration service
3. Configure monitoring alerts
4. Test in staging
5. Enable in production

```
## Integration Types

1. **API → Database**: Sync external data
2. **Database → API**: Push updates
3. **Queue → Service**: Event processing
4. **Service → Service**: Microservice communication
5. **File → System**: Batch imports
6. **System → Webhook**: Real-time notifications

## Guidelines

- Always implement retry logic
- Use circuit breakers for external services
- Log all integration events
- Monitor success/failure rates
- Document data transformations
- Test error scenarios
```
