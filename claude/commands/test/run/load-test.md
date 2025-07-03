# /load-test

Generate comprehensive load testing suites for $ARGUMENT with intelligent test scenario creation, performance baselines, and automated analysis.

## Usage

```
/load-test [endpoint-url]
/load-test [api-spec-file]
/load-test
```

## Context Detection

**When no argument provided:**

- Analyzes project structure for API endpoints and services
- Detects OpenAPI/Swagger specifications
- Identifies docker-compose services with exposed ports
- Provides interactive endpoint selection

**When endpoint provided:**

- Creates targeted load tests for specific URL
- Auto-detects authentication requirements
- Analyzes response patterns for realistic scenarios

**When API spec provided:**

- Generates comprehensive test suite from OpenAPI/Swagger
- Creates weighted scenario distributions
- Includes all endpoint combinations

## Framework Detection

**Load Testing Tools:**

```bash
# Detect existing tools
fd "package.json" | xargs jq -r '.devDependencies | keys[]' | rg "(k6|artillery|wrk|autocannon)"

# Check for load testing configs
fd "(k6|artillery|wrk).(js|yml|yaml|json)$" --max-depth 2

# Analyze project language preferences
case $DETECTED_TECH in
  "node"|"deno") echo "k6 or Artillery recommended" ;;
  "go") echo "wrk or hey recommended" ;;
  "rust") echo "drill or wrk recommended" ;;
  "python") echo "locust recommended" ;;
esac
```

## Load Test Generation Strategies

### 1. API Endpoint Analysis

**Endpoint Discovery:**

```bash
# Extract API routes from common frameworks
case $FRAMEWORK in
  "express"|"fastify")
    rg "(app|router)\.(get|post|put|delete|patch)" --type js --type ts -A 2
    ;;
  "axum"|"actix")
    rg "Router::new\(\)|\.route\(" --type rust -A 2
    ;;
  "spring"|"quarkus")
    rg "@(GetMapping|PostMapping|PutMapping|DeleteMapping|RequestMapping)" --type java -A 2
    ;;
  "gin"|"echo"|"connectrpc")
    rg "router\.(GET|POST|PUT|DELETE)|connect\." --type go -A 2
    ;;
  "fresh"|"oak")
    rg "handler|GET|POST" --type ts -A 2
    ;;
esac
```

**OpenAPI/Swagger Analysis:**

```typescript
// Parse OpenAPI spec for comprehensive testing
interface OpenAPISpec {
  paths: Record<string, {
    get?: OperationObject;
    post?: OperationObject;
    put?: OperationObject;
    delete?: OperationObject;
  }>;
  components?: {
    schemas?: Record<string, SchemaObject>;
    securitySchemes?: Record<string, SecuritySchemeObject>;
  };
}

function generateLoadTestScenarios(spec: OpenAPISpec) {
  const scenarios = [];

  for (const [path, methods] of Object.entries(spec.paths)) {
    for (const [method, operation] of Object.entries(methods)) {
      scenarios.push({
        name: operation.operationId || `${method.toUpperCase()} ${path}`,
        path: path,
        method: method.toUpperCase(),
        weight: calculateWeight(operation),
        auth: detectAuthRequirements(operation),
        parameters: extractParameters(operation),
        requestBody: generateRequestBody(operation),
      });
    }
  }

  return scenarios;
}
```

### 2. K6 Load Test Generation

**Basic Load Test Template:**

```javascript
// Generated K6 load test for API endpoints
import http from "k6/http";
import { check, sleep } from "k6";
import { Rate } from "k6/metrics";

// Custom metrics
const errorRate = new Rate("errors");

// Test configuration
export const options = {
  stages: [
    { duration: "2m", target: 10 }, // Ramp up
    { duration: "5m", target: 10 }, // Stay at 10 users
    { duration: "2m", target: 20 }, // Ramp up to 20 users
    { duration: "5m", target: 20 }, // Stay at 20 users
    { duration: "2m", target: 0 }, // Ramp down
  ],
  thresholds: {
    http_req_duration: ["p(95)<500"], // 95% of requests must complete below 500ms
    http_req_failed: ["rate<0.1"], // Error rate must be below 10%
    errors: ["rate<0.1"],
  },
};

// Base URL configuration
const BASE_URL = __ENV.BASE_URL || "http://localhost:3000";

// Authentication setup
let authHeaders = {};
if (__ENV.API_KEY) {
  authHeaders["Authorization"] = `Bearer ${__ENV.API_KEY}`;
}

// Test data
const testUsers = [
  { email: "test1@example.com", name: "Test User 1" },
  { email: "test2@example.com", name: "Test User 2" },
  { email: "test3@example.com", name: "Test User 3" },
];

export default function () {
  // Test scenario selection based on weights
  const scenario = selectScenario();

  switch (scenario) {
    case "getUsers":
      testGetUsers();
      break;
    case "createUser":
      testCreateUser();
      break;
    case "getUserById":
      testGetUserById();
      break;
    case "updateUser":
      testUpdateUser();
      break;
    case "deleteUser":
      testDeleteUser();
      break;
  }

  sleep(1); // Think time between requests
}

function selectScenario() {
  const scenarios = [
    { name: "getUsers", weight: 40 },
    { name: "createUser", weight: 20 },
    { name: "getUserById", weight: 25 },
    { name: "updateUser", weight: 10 },
    { name: "deleteUser", weight: 5 },
  ];

  const random = Math.random() * 100;
  let cumulative = 0;

  for (const scenario of scenarios) {
    cumulative += scenario.weight;
    if (random <= cumulative) {
      return scenario.name;
    }
  }

  return scenarios[0].name;
}

function testGetUsers() {
  const response = http.get(`${BASE_URL}/api/users`, {
    headers: authHeaders,
  });

  check(response, {
    "GET /api/users status is 200": (r) => r.status === 200,
    "GET /api/users response time < 500ms": (r) => r.timings.duration < 500,
    "GET /api/users has users array": (r) => {
      try {
        const body = JSON.parse(r.body);
        return Array.isArray(body.users);
      } catch {
        return false;
      }
    },
  }) || errorRate.add(1);
}

function testCreateUser() {
  const user = testUsers[Math.floor(Math.random() * testUsers.length)];
  const payload = {
    ...user,
    email: `${Date.now()}_${user.email}`, // Ensure unique email
  };

  const response = http.post(
    `${BASE_URL}/api/users`,
    JSON.stringify(payload),
    {
      headers: {
        ...authHeaders,
        "Content-Type": "application/json",
      },
    },
  );

  check(response, {
    "POST /api/users status is 201": (r) => r.status === 201,
    "POST /api/users response time < 1000ms": (r) => r.timings.duration < 1000,
    "POST /api/users returns user ID": (r) => {
      try {
        const body = JSON.parse(r.body);
        return body.id !== undefined;
      } catch {
        return false;
      }
    },
  }) || errorRate.add(1);
}

function testGetUserById() {
  // Simulate getting a user by ID (using a range of likely IDs)
  const userId = Math.floor(Math.random() * 1000) + 1;

  const response = http.get(`${BASE_URL}/api/users/${userId}`, {
    headers: authHeaders,
  });

  check(response, {
    "GET /api/users/:id response time < 300ms": (r) => r.timings.duration < 300,
    "GET /api/users/:id status is 200 or 404": (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);
}

function testUpdateUser() {
  const userId = Math.floor(Math.random() * 100) + 1;
  const updateData = {
    name: `Updated User ${Date.now()}`,
  };

  const response = http.put(
    `${BASE_URL}/api/users/${userId}`,
    JSON.stringify(updateData),
    {
      headers: {
        ...authHeaders,
        "Content-Type": "application/json",
      },
    },
  );

  check(response, {
    "PUT /api/users/:id response time < 800ms": (r) => r.timings.duration < 800,
    "PUT /api/users/:id status is 200 or 404": (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);
}

function testDeleteUser() {
  const userId = Math.floor(Math.random() * 100) + 1;

  const response = http.del(`${BASE_URL}/api/users/${userId}`, null, {
    headers: authHeaders,
  });

  check(response, {
    "DELETE /api/users/:id response time < 500ms": (r) => r.timings.duration < 500,
    "DELETE /api/users/:id status is 200 or 404": (r) => r.status === 200 || r.status === 404,
  }) || errorRate.add(1);
}
```

### 3. Artillery Load Test Generation

**Artillery Configuration:**

```yaml
# Generated Artillery load test configuration
config:
  target: '{{ $environment.BASE_URL | default("http://localhost:3000") }}'
  phases:
    - duration: 60
      arrivalRate: 5
      name: "Warm up"
    - duration: 120
      arrivalRate: 10
      name: "Steady load"
    - duration: 60
      arrivalRate: 20
      name: "Peak load"
    - duration: 60
      arrivalRate: 5
      name: "Cool down"
  variables:
    userEmail:
      - "test1@example.com"
      - "test2@example.com"
      - "test3@example.com"
  plugins:
    - artillery-plugin-metrics-by-endpoint
    - artillery-plugin-statsd
  processor: "./processor.js"

scenarios:
  - name: "User Management Flow"
    weight: 60
    flow:
      - get:
          url: "/api/health"
          capture:
            - json: "$.status"
              as: "healthStatus"
      - think: 1
      - get:
          url: "/api/users"
          headers:
            Authorization: "Bearer {{ $environment.API_KEY }}"
          capture:
            - json: "$.users[0].id"
              as: "userId"
      - think: 2
      - get:
          url: "/api/users/{{ userId }}"
          headers:
            Authorization: "Bearer {{ $environment.API_KEY }}"

  - name: "Create and Update User"
    weight: 30
    flow:
      - post:
          url: "/api/users"
          headers:
            Authorization: "Bearer {{ $environment.API_KEY }}"
            Content-Type: "application/json"
          json:
            email: "{{ userEmail }}_{{ $timestamp }}"
            name: "Load Test User"
          capture:
            - json: "$.id"
              as: "newUserId"
      - think: 1
      - put:
          url: "/api/users/{{ newUserId }}"
          headers:
            Authorization: "Bearer {{ $environment.API_KEY }}"
            Content-Type: "application/json"
          json:
            name: "Updated Load Test User"

  - name: "High Frequency Reads"
    weight: 10
    flow:
      - loop:
          - get:
              url: "/api/users/{{ $randomInt(1, 1000) }}"
              headers:
                Authorization: "Bearer {{ $environment.API_KEY }}"
          - think: 0.5
        count: 5
```

### 4. Performance Baseline Generation

**Automated Baseline Creation:**

```typescript
// Performance baseline generator
interface PerformanceBaseline {
  endpoint: string;
  method: string;
  p50ResponseTime: number;
  p95ResponseTime: number;
  p99ResponseTime: number;
  throughputRps: number;
  errorRate: number;
  timestamp: string;
}

async function generateBaseline(endpoint: string): Promise<PerformanceBaseline> {
  // Run lightweight baseline test
  const results = await runBaselineTest(endpoint);

  return {
    endpoint,
    method: detectHttpMethod(endpoint),
    p50ResponseTime: results.responseTime.p50,
    p95ResponseTime: results.responseTime.p95,
    p99ResponseTime: results.responseTime.p99,
    throughputRps: results.throughput.rps,
    errorRate: results.errors.rate,
    timestamp: new Date().toISOString(),
  };
}

// Baseline comparison for regression detection
function compareWithBaseline(
  current: PerformanceBaseline,
  baseline: PerformanceBaseline,
): PerformanceReport {
  const regressions = [];

  if (current.p95ResponseTime > baseline.p95ResponseTime * 1.2) {
    regressions.push({
      metric: "p95ResponseTime",
      current: current.p95ResponseTime,
      baseline: baseline.p95ResponseTime,
      degradation: ((current.p95ResponseTime / baseline.p95ResponseTime) - 1) * 100,
    });
  }

  if (current.errorRate > baseline.errorRate * 1.5) {
    regressions.push({
      metric: "errorRate",
      current: current.errorRate,
      baseline: baseline.errorRate,
      degradation: ((current.errorRate / baseline.errorRate) - 1) * 100,
    });
  }

  return {
    status: regressions.length > 0 ? "REGRESSION_DETECTED" : "PERFORMANCE_STABLE",
    regressions,
    summary: generatePerformanceSummary(current, baseline),
  };
}
```

### 5. CI/CD Integration

**GitHub Actions Integration:**

```yaml
# Generated performance testing workflow
name: Load Testing

on:
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 2 * * *" # Daily at 2 AM

jobs:
  load-test:
    runs-on: ubuntu-latest

    services:
      app:
        image: ${{ env.APP_IMAGE }}
        ports:
          - 3000:3000
        env:
          DATABASE_URL: ${{ secrets.TEST_DATABASE_URL }}

    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Install k6
        run: |
          curl https://github.com/grafana/k6/releases/download/v0.47.0/k6-v0.47.0-linux-amd64.tar.gz -L | tar xvz --strip-components 1
          sudo mv k6 /usr/local/bin/

      - name: Wait for service
        run: |
          timeout 60 bash -c 'until curl -f http://localhost:3000/health; do sleep 2; done'

      - name: Run load tests
        run: |
          k6 run --out json=results.json load-test.js
        env:
          BASE_URL: http://localhost:3000
          API_KEY: ${{ secrets.TEST_API_KEY }}

      - name: Analyze results
        run: |
          node analyze-performance.js results.json

      - name: Upload results
        uses: actions/upload-artifact@v4
        with:
          name: load-test-results
          path: |
            results.json
            performance-report.html

      - name: Comment PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('performance-summary.md', 'utf8');

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

## Deno Task Integration

**Generated deno.json tasks:**

```json
{
  "tasks": {
    "load-test": "k6 run load-test.js",
    "load-test:watch": "k6 run --watch load-test.js",
    "load-test:smoke": "k6 run --vus 1 --duration 30s load-test.js",
    "load-test:stress": "k6 run --vus 100 --duration 10m load-test.js",
    "load-test:spike": "k6 run --stage 0:0,1m:100,2m:100,3m:0 load-test.js",
    "baseline": "k6 run --vus 10 --duration 2m load-test.js --out json=baseline.json",
    "perf-report": "node analyze-performance.js results.json"
  }
}
```

## Output

The command generates:

1. **Load Test Scripts**: K6, Artillery, or tool-specific test configurations
2. **Test Scenarios**: Realistic user behavior patterns and weighted distributions
3. **Performance Baselines**: Automated baseline capture and regression detection
4. **CI Integration**: GitHub Actions workflows for automated testing
5. **Analysis Tools**: Result parsing and performance report generation
6. **Monitoring Setup**: Grafana dashboards and alert configurations

## Integration with Other Commands

- Use with `/monitor` for ongoing performance tracking
- Combine with `/deploy` for staging environment testing
- Integrate with `/ci-gen` for automated pipeline setup
- Follow with `/bottleneck` for performance optimization
- Use with `/health-check` for comprehensive monitoring

The load testing setup adapts to detected technology stacks and provides comprehensive performance validation with automated regression detection and CI/CD integration.
