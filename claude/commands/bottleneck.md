# /bottleneck

Identify, analyze, and resolve performance bottlenecks using systematic profiling, monitoring, and optimization techniques across the entire application stack.

## Usage

```
/bottleneck [analyze|profile|optimize|monitor] [--component=all] [--threshold=auto]
```

## Parameters

- `analyze` - Identify performance bottlenecks across the application (default)
- `profile` - Deep performance profiling of specific components
- `optimize` - Apply automated optimization strategies
- `monitor` - Set up continuous bottleneck monitoring
- `--component` - Target specific component: cpu, memory, network, database, cache, all
- `--threshold` - Performance threshold for bottleneck detection (auto-detect by default)

## Context Intelligence

### System Architecture Detection

**Performance Profile Discovery:**

```bash
# Detect application architecture and performance characteristics
detect_performance_context() {
  echo "🔍 Detecting application performance context..."
  
  # Application type detection
  if [ -f "Cargo.toml" ]; then
    LANGUAGE="rust"
    PERF_TOOLS="cargo-flamegraph perf valgrind"
    PROFILE_CMD="cargo build --release && perf record target/release/app"
  elif [ -f "go.mod" ]; then
    LANGUAGE="go" 
    PERF_TOOLS="pprof go-torch"
    PROFILE_CMD="go tool pprof http://localhost:6060/debug/pprof/profile"
  elif [ -f "deno.json" ]; then
    LANGUAGE="deno"
    PERF_TOOLS="deno-performance clinic"
    PROFILE_CMD="deno run --allow-all --v8-flags=--prof app.ts"
  elif [ -f "package.json" ]; then
    LANGUAGE="node"
    PERF_TOOLS="clinic 0x autocannon"
    PROFILE_CMD="clinic doctor -- node app.js"
  fi
  
  # Infrastructure detection
  if [ -f "docker-compose.yml" ]; then
    DEPLOYMENT="docker-compose"
    MONITORING_STACK="prometheus grafana jaeger"
  elif [ -d "k8s" ] || [ -d "kubernetes" ]; then
    DEPLOYMENT="kubernetes"
    MONITORING_STACK="prometheus grafana jaeger istio"
  fi
  
  # Database detection
  if rg -q "postgresql|postgres" .; then
    DATABASE="postgresql"
    DB_TOOLS="pg_stat_statements pgbench explain"
  elif rg -q "mysql|mariadb" .; then
    DATABASE="mysql"
    DB_TOOLS="performance_schema mysqldumpslow"
  elif rg -q "mongodb" .; then
    DATABASE="mongodb"
    DB_TOOLS="mongostat mongotop db.collection.explain"
  fi
  
  echo "Language: $LANGUAGE, Deployment: $DEPLOYMENT, Database: $DATABASE"
}

# Analyze current resource utilization
analyze_resource_baseline() {
  echo "📊 Analyzing current resource utilization..."
  
  # CPU analysis
  CPU_USAGE=$(top -bn1 | rg "Cpu\(s\)" | awk '{print $2}' | cut -d'%' -f1)
  CPU_CORES=$(nproc)
  
  # Memory analysis
  MEMORY_INFO=$(free -h)
  MEMORY_USED=$(echo "$MEMORY_INFO" | awk 'NR==2{printf "%.1f", $3/$2*100}')
  
  # Disk I/O analysis
  DISK_USAGE=$(iostat -x 1 1 | tail -n +4 | awk '{sum+=$10} END {print sum/NR}')
  
  # Network analysis
  NETWORK_CONNECTIONS=$(netstat -an | wc -l)
  
  cat > performance_baseline.json << EOF
{
  "timestamp": "$(date -Iseconds)",
  "cpu": {
    "usage_percent": $CPU_USAGE,
    "cores": $CPU_CORES,
    "load_average": "$(uptime | awk -F'load average:' '{print $2}')"
  },
  "memory": {
    "usage_percent": $MEMORY_USED,
    "details": "$(echo "$MEMORY_INFO" | jq -R -s 'split("\n")')"
  },
  "disk": {
    "avg_util_percent": $DISK_USAGE
  },
  "network": {
    "connections": $NETWORK_CONNECTIONS
  }
}
EOF
}
```

### Application Performance Monitoring Setup

**Instrumentation Detection:**

```bash
# Check for existing monitoring and instrumentation
check_existing_monitoring() {
  echo "🔬 Checking existing performance monitoring..."
  
  # Application metrics endpoints
  if rg -q "metrics|prometheus|/health|/stats" .; then
    echo "✅ Application metrics endpoints detected"
    rg "metrics|prometheus|/health|/stats" --type yaml --type json --type env | head -10
  fi
  
  # Distributed tracing
  if rg -q "jaeger|zipkin|otel|opentelemetry" .; then
    echo "✅ Distributed tracing setup detected"
    rg "jaeger|zipkin|otel|opentelemetry" --type yaml --type json | head -5
  fi
  
  # Database monitoring
  case $DATABASE in
    "postgresql")
      if rg -q "pg_stat_statements|pg_stat_user_tables" .; then
        echo "✅ PostgreSQL monitoring enabled"
      fi
      ;;
    "mysql")
      if rg -q "performance_schema|slow_query_log" .; then
        echo "✅ MySQL performance monitoring enabled"
      fi
      ;;
  esac
  
  # Container monitoring
  if [ -f "docker-compose.yml" ]; then
    if yq '.services[] | select(.image | contains("prometheus"))' docker-compose.yml > /dev/null 2>&1; then
      echo "✅ Prometheus monitoring in docker-compose"
    fi
  fi
}
```

## Multi-Dimensional Bottleneck Analysis

### 1. Application-Level Performance Analysis

**Systematic Performance Profiling:**

```typescript
// Generated performance analyzer
interface PerformanceProfile {
  component: string;
  metrics: PerformanceMetrics;
  bottlenecks: Bottleneck[];
  recommendations: OptimizationRecommendation[];
}

interface PerformanceMetrics {
  cpu: CPUMetrics;
  memory: MemoryMetrics;
  io: IOMetrics;
  network: NetworkMetrics;
  database: DatabaseMetrics;
  cache: CacheMetrics;
}

interface Bottleneck {
  type: "cpu" | "memory" | "io" | "network" | "database" | "cache" | "algorithm";
  severity: "low" | "medium" | "high" | "critical";
  description: string;
  impact: string;
  location: string;
  evidence: PerformanceEvidence[];
  rootCause: string;
}

interface OptimizationRecommendation {
  type: "code" | "configuration" | "infrastructure" | "architecture";
  priority: "low" | "medium" | "high" | "critical";
  description: string;
  expectedImpact: string;
  effort: "low" | "medium" | "high";
  implementation: string;
  codeExample?: string;
}

export class BottleneckAnalyzer {
  async analyzeApplication(): Promise<PerformanceProfile[]> {
    console.log("🔍 Starting comprehensive bottleneck analysis...");

    const profiles: PerformanceProfile[] = [];

    // Analyze different application components
    const components = await this.identifyComponents();

    for (const component of components) {
      const metrics = await this.collectMetrics(component);
      const bottlenecks = await this.identifyBottlenecks(component, metrics);
      const recommendations = await this.generateRecommendations(bottlenecks);

      profiles.push({
        component: component.name,
        metrics,
        bottlenecks,
        recommendations,
      });
    }

    return profiles;
  }

  private async identifyBottlenecks(
    component: any,
    metrics: PerformanceMetrics,
  ): Promise<Bottleneck[]> {
    const bottlenecks: Bottleneck[] = [];

    // CPU bottleneck detection
    if (metrics.cpu.utilization > 80) {
      bottlenecks.push({
        type: "cpu",
        severity: metrics.cpu.utilization > 95 ? "critical" : "high",
        description: `High CPU utilization (${metrics.cpu.utilization}%) in ${component.name}`,
        impact: "Increased response times, potential request timeouts",
        location: component.name,
        evidence: [
          {
            metric: "cpu_utilization",
            value: metrics.cpu.utilization,
            threshold: 80,
            timestamp: new Date().toISOString(),
          },
        ],
        rootCause: await this.analyzeCPUBottleneck(component, metrics.cpu),
      });
    }

    // Memory bottleneck detection
    if (metrics.memory.usage > 85 || metrics.memory.gcPressure > 0.1) {
      bottlenecks.push({
        type: "memory",
        severity: metrics.memory.usage > 95 ? "critical" : "high",
        description:
          `Memory pressure detected: ${metrics.memory.usage}% usage, GC pressure: ${metrics.memory.gcPressure}`,
        impact: "Frequent garbage collection, increased latency, potential OOM",
        location: component.name,
        evidence: [
          {
            metric: "memory_usage",
            value: metrics.memory.usage,
            threshold: 85,
            timestamp: new Date().toISOString(),
          },
        ],
        rootCause: await this.analyzeMemoryBottleneck(component, metrics.memory),
      });
    }

    // Database bottleneck detection
    if (metrics.database.avgQueryTime > 100 || metrics.database.slowQueries > 10) {
      bottlenecks.push({
        type: "database",
        severity: metrics.database.avgQueryTime > 1000 ? "critical" : "high",
        description:
          `Database performance issues: avg query time ${metrics.database.avgQueryTime}ms, ${metrics.database.slowQueries} slow queries`,
        impact: "Increased application response times, potential timeouts",
        location: "database",
        evidence: [
          {
            metric: "avg_query_time",
            value: metrics.database.avgQueryTime,
            threshold: 100,
            timestamp: new Date().toISOString(),
          },
        ],
        rootCause: await this.analyzeDatabaseBottleneck(metrics.database),
      });
    }

    return bottlenecks;
  }

  private async analyzeCPUBottleneck(component: any, cpuMetrics: CPUMetrics): Promise<string> {
    // Analyze CPU usage patterns
    if (cpuMetrics.userTime > cpuMetrics.systemTime * 3) {
      return "High user CPU time suggests application-level performance issues (inefficient algorithms, loops, or computations)";
    } else if (cpuMetrics.systemTime > cpuMetrics.userTime) {
      return "High system CPU time suggests I/O bottlenecks or kernel-level issues";
    } else if (cpuMetrics.iowait > 20) {
      return "High I/O wait time indicates storage or network bottlenecks";
    }

    return "General CPU pressure - consider horizontal scaling or algorithm optimization";
  }
}
```

### 2. Database Performance Analysis

**Comprehensive Database Bottleneck Detection:**

```typescript
// Generated database performance analyzer
interface DatabaseAnalyzer {
  analyzeDatabase(): Promise<DatabaseBottlenecks>;
}

interface DatabaseBottlenecks {
  queries: SlowQuery[];
  indexes: IndexRecommendation[];
  connections: ConnectionIssue[];
  locks: LockContention[];
  schema: SchemaOptimization[];
}

interface SlowQuery {
  query: string;
  avgExecutionTime: number;
  executionCount: number;
  totalTime: number;
  indexUsage: string;
  optimizationSuggestion: string;
  explainPlan?: any;
}

export class DatabasePerformanceAnalyzer implements DatabaseAnalyzer {
  async analyzeDatabase(): Promise<DatabaseBottlenecks> {
    const dbType = await this.detectDatabaseType();

    switch (dbType) {
      case "postgresql":
        return this.analyzePostgreSQL();
      case "mysql":
        return this.analyzeMySQL();
      case "mongodb":
        return this.analyzeMongoDB();
      default:
        throw new Error(`Unsupported database type: ${dbType}`);
    }
  }

  private async analyzePostgreSQL(): Promise<DatabaseBottlenecks> {
    console.log("🐘 Analyzing PostgreSQL performance...");

    // Slow query analysis using pg_stat_statements
    const slowQueries = await this.getPostgreSQLSlowQueries();
    const indexRecommendations = await this.analyzePostgreSQLIndexes();
    const connectionIssues = await this.analyzePostgreSQLConnections();
    const lockContention = await this.analyzePostgreSQLLocks();
    const schemaOptimizations = await this.analyzePostgreSQLSchema();

    return {
      queries: slowQueries,
      indexes: indexRecommendations,
      connections: connectionIssues,
      locks: lockContention,
      schema: schemaOptimizations,
    };
  }

  private async getPostgreSQLSlowQueries(): Promise<SlowQuery[]> {
    // Generate SQL for slow query analysis
    const analysisQueries = `
-- Enable pg_stat_statements if not already enabled
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Find slowest queries by total time
SELECT 
  query,
  calls as execution_count,
  total_exec_time / calls as avg_execution_time,
  total_exec_time,
  rows / calls as avg_rows,
  100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) as hit_percent
FROM pg_stat_statements 
WHERE calls > 100
ORDER BY total_exec_time DESC 
LIMIT 20;

-- Find queries with poor cache hit ratios
SELECT 
  query,
  calls,
  shared_blks_hit,
  shared_blks_read,
  shared_blks_written,
  100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) as hit_percent
FROM pg_stat_statements 
WHERE shared_blks_read > 0
ORDER BY hit_percent ASC, shared_blks_read DESC
LIMIT 10;
`;

    // Return mock data structure - in real implementation, execute queries
    return [
      {
        query: "SELECT * FROM users WHERE email = $1",
        avgExecutionTime: 150.5,
        executionCount: 1250,
        totalTime: 188125,
        indexUsage: "Sequential scan on users table",
        optimizationSuggestion:
          "Add index on email column: CREATE INDEX idx_users_email ON users(email)",
        explainPlan: {
          "Plan": {
            "Node Type": "Seq Scan",
            "Relation Name": "users",
            "Total Cost": 155.42,
            "Rows": 1,
          },
        },
      },
    ];
  }

  private async analyzePostgreSQLIndexes(): Promise<IndexRecommendation[]> {
    // Generate index analysis SQL
    const indexAnalysisSQL = `
-- Find missing indexes (tables with high seq scan ratios)
SELECT 
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  idx_tup_fetch,
  seq_tup_read / seq_scan as avg_seq_read,
  CASE WHEN seq_scan > 0 THEN seq_tup_read / seq_scan ELSE 0 END as seq_scan_ratio
FROM pg_stat_user_tables 
WHERE seq_scan > 100 
  AND (idx_scan IS NULL OR seq_scan > idx_scan)
ORDER BY seq_tup_read DESC;

-- Find unused indexes
SELECT 
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes 
WHERE idx_scan < 10
ORDER BY idx_scan ASC;

-- Find duplicate indexes
SELECT 
  a.tablename,
  a.indexname as index1,
  b.indexname as index2,
  a.indexdef,
  b.indexdef
FROM pg_indexes a
JOIN pg_indexes b ON a.tablename = b.tablename
WHERE a.indexname != b.indexname
  AND a.indexdef SIMILAR TO b.indexdef;
`;

    return [
      {
        type: "missing",
        table: "users",
        column: "email",
        reason: "High sequential scan ratio (95%)",
        suggestion: "CREATE INDEX idx_users_email ON users(email)",
        impact: "Estimated 80% query time reduction",
        priority: "high",
      },
    ];
  }
}
```

### 3. Network and I/O Bottleneck Analysis

**Network Performance Analysis:**

```bash
# Generate network performance analysis script
analyze_network_performance() {
  echo "🌐 Analyzing network performance bottlenecks..."
  
  # Network latency analysis
  ping -c 10 localhost > network_latency.txt
  
  # Connection analysis
  netstat -an | awk '/^tcp/ {++state[$6]} END {for(key in state) print key, state[key]}' > connection_states.txt
  
  # Bandwidth utilization
  if command -v iftop &> /dev/null; then
    timeout 30s iftop -t -s 30 > network_bandwidth.txt 2>&1
  fi
  
  # DNS resolution times
  dig @8.8.8.8 google.com | rg "Query time" > dns_performance.txt
  
  # HTTP response time analysis
  if command -v curl &> /dev/null; then
    for url in "http://localhost:8080/health" "http://localhost:3000/api/status"; do
      if curl -s "$url" > /dev/null; then
        curl -w "@curl-format.txt" -o /dev/null -s "$url" >> http_timing.txt
      fi
    done
  fi
}

# I/O performance analysis
analyze_io_performance() {
  echo "💽 Analyzing I/O performance bottlenecks..."
  
  # Disk I/O statistics
  iostat -x 1 10 > disk_io_stats.txt &
  
  # File system performance
  df -h > disk_usage.txt
  
  # Find I/O intensive processes
  iotop -b -n 3 > io_processes.txt 2>/dev/null || echo "iotop not available"
  
  # Check for disk queue depth issues
  cat /proc/diskstats > diskstats_before.txt
  sleep 5
  cat /proc/diskstats > diskstats_after.txt
  
  # Database I/O analysis (if PostgreSQL)
  if command -v psql &> /dev/null; then
    psql -c "
    SELECT 
      datname,
      blks_read,
      blks_hit,
      blk_read_time,
      blk_write_time,
      100.0 * blks_hit / (blks_hit + blks_read) as cache_hit_ratio
    FROM pg_stat_database 
    WHERE datname NOT IN ('template0', 'template1', 'postgres');" > db_io_stats.txt 2>/dev/null
  fi
}
```

## Automated Optimization Strategies

### 1. Code-Level Optimizations

**Performance Optimization Code Generation:**

```typescript
// Generated optimization engine
interface OptimizationStrategy {
  type: "algorithmic" | "memory" | "io" | "concurrency" | "caching";
  before: string;
  after: string;
  explanation: string;
  expectedImprovement: string;
  tradeoffs: string[];
}

export class CodeOptimizer {
  generateOptimizations(bottlenecks: Bottleneck[]): OptimizationStrategy[] {
    const optimizations: OptimizationStrategy[] = [];

    for (const bottleneck of bottlenecks) {
      switch (bottleneck.type) {
        case "cpu":
          optimizations.push(...this.generateCPUOptimizations(bottleneck));
          break;
        case "memory":
          optimizations.push(...this.generateMemoryOptimizations(bottleneck));
          break;
        case "database":
          optimizations.push(...this.generateDatabaseOptimizations(bottleneck));
          break;
        case "network":
          optimizations.push(...this.generateNetworkOptimizations(bottleneck));
          break;
      }
    }

    return optimizations;
  }

  private generateCPUOptimizations(bottleneck: Bottleneck): OptimizationStrategy[] {
    return [
      {
        type: "algorithmic",
        before: `
// Inefficient O(n²) algorithm
function findDuplicates(arr: number[]): number[] {
  const duplicates: number[] = [];
  for (let i = 0; i < arr.length; i++) {
    for (let j = i + 1; j < arr.length; j++) {
      if (arr[i] === arr[j] && !duplicates.includes(arr[i])) {
        duplicates.push(arr[i]);
      }
    }
  }
  return duplicates;
}`,
        after: `
// Optimized O(n) algorithm using Set
function findDuplicates(arr: number[]): number[] {
  const seen = new Set<number>();
  const duplicates = new Set<number>();
  
  for (const num of arr) {
    if (seen.has(num)) {
      duplicates.add(num);
    } else {
      seen.add(num);
    }
  }
  
  return Array.from(duplicates);
}`,
        explanation: "Replaced O(n²) nested loops with O(n) Set-based algorithm",
        expectedImprovement: "95% reduction in CPU time for large arrays",
        tradeoffs: ["Slightly higher memory usage for Set storage"],
      },
      {
        type: "concurrency",
        before: `
// Sequential processing
async function processItems(items: Item[]): Promise<Result[]> {
  const results: Result[] = [];
  for (const item of items) {
    const result = await processItem(item);
    results.push(result);
  }
  return results;
}`,
        after: `
// Parallel processing with controlled concurrency
async function processItems(items: Item[]): Promise<Result[]> {
  const BATCH_SIZE = Math.min(10, Math.ceil(items.length / 4));
  const results: Result[] = [];
  
  for (let i = 0; i < items.length; i += BATCH_SIZE) {
    const batch = items.slice(i, i + BATCH_SIZE);
    const batchResults = await Promise.all(
      batch.map(item => processItem(item))
    );
    results.push(...batchResults);
  }
  
  return results;
}`,
        explanation: "Added parallel processing with batching to prevent resource exhaustion",
        expectedImprovement: "70-80% reduction in total processing time",
        tradeoffs: ["Higher memory usage", "Potential resource contention"],
      },
    ];
  }

  private generateMemoryOptimizations(bottleneck: Bottleneck): OptimizationStrategy[] {
    return [
      {
        type: "memory",
        before: `
// Memory-inefficient data loading
class DataProcessor {
  async loadAllData(): Promise<DataItem[]> {
    const query = "SELECT * FROM large_table";
    const results = await this.db.query(query);
    return results.map(row => this.transformData(row));
  }
}`,
        after: `
// Streaming data processing
class DataProcessor {
  async* streamData(batchSize = 1000): AsyncGenerator<DataItem[], void, unknown> {
    let offset = 0;
    
    while (true) {
      const query = "SELECT * FROM large_table LIMIT $1 OFFSET $2";
      const results = await this.db.query(query, [batchSize, offset]);
      
      if (results.length === 0) break;
      
      yield results.map(row => this.transformData(row));
      offset += batchSize;
    }
  }
  
  async processData(): Promise<void> {
    for await (const batch of this.streamData()) {
      await this.processBatch(batch);
      // Memory is freed after each batch
    }
  }
}`,
        explanation: "Replaced bulk loading with streaming to reduce memory footprint",
        expectedImprovement: "90% reduction in peak memory usage",
        tradeoffs: ["More complex code", "Slightly higher database load"],
      },
      {
        type: "caching",
        before: `
// No caching - repeated expensive calculations
class Calculator {
  expensiveCalculation(input: number): number {
    // Simulate expensive operation
    let result = 0;
    for (let i = 0; i < 1000000; i++) {
      result += Math.sin(input * i);
    }
    return result;
  }
}`,
        after: `
// LRU cache implementation
class Calculator {
  private cache = new Map<number, number>();
  private readonly maxCacheSize = 1000;
  
  expensiveCalculation(input: number): number {
    // Check cache first
    if (this.cache.has(input)) {
      const value = this.cache.get(input)!;
      // Move to end (LRU)
      this.cache.delete(input);
      this.cache.set(input, value);
      return value;
    }
    
    // Calculate if not cached
    let result = 0;
    for (let i = 0; i < 1000000; i++) {
      result += Math.sin(input * i);
    }
    
    // Add to cache with LRU eviction
    if (this.cache.size >= this.maxCacheSize) {
      const firstKey = this.cache.keys().next().value;
      this.cache.delete(firstKey);
    }
    this.cache.set(input, result);
    
    return result;
  }
}`,
        explanation: "Added LRU cache to avoid recalculating expensive operations",
        expectedImprovement: "99% reduction in computation time for repeated inputs",
        tradeoffs: ["Additional memory usage", "Cache management complexity"],
      },
    ];
  }
}
```

### 2. Database Query Optimization

**Automated Query Optimization:**

```sql
-- Generated database optimization queries

-- Before: Inefficient query without proper indexing
SELECT u.*, p.title, c.name as category_name
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
LEFT JOIN categories c ON p.category_id = c.id
WHERE u.email LIKE '%@company.com'
  AND p.created_at > '2024-01-01'
ORDER BY p.created_at DESC
LIMIT 20;

-- After: Optimized query with proper indexing and structure
-- Step 1: Create necessary indexes
CREATE INDEX CONCURRENTLY idx_users_email_domain ON users (email) WHERE email LIKE '%@company.com';
CREATE INDEX CONCURRENTLY idx_posts_user_created ON posts (user_id, created_at DESC);
CREATE INDEX CONCURRENTLY idx_posts_category_created ON posts (category_id, created_at DESC);

-- Step 2: Rewrite query for better performance
WITH company_users AS (
  SELECT id, email, name 
  FROM users 
  WHERE email LIKE '%@company.com'
),
recent_posts AS (
  SELECT p.*, u.email, u.name as user_name
  FROM posts p
  INNER JOIN company_users u ON p.user_id = u.id
  WHERE p.created_at > '2024-01-01'
  ORDER BY p.created_at DESC
  LIMIT 20
)
SELECT rp.*, c.name as category_name
FROM recent_posts rp
LEFT JOIN categories c ON rp.category_id = c.id
ORDER BY rp.created_at DESC;

-- Query performance analysis
EXPLAIN (ANALYZE, BUFFERS, FORMAT JSON)
[OPTIMIZED_QUERY];
```

## Real-Time Performance Monitoring

### 1. Continuous Bottleneck Detection

**Monitoring Dashboard Setup:**

```typescript
// Generated performance monitoring system
interface PerformanceMonitor {
  startMonitoring(): Promise<void>;
  detectBottlenecks(): Promise<BottleneckAlert[]>;
  generateReport(): Promise<PerformanceReport>;
}

interface BottleneckAlert {
  timestamp: Date;
  type: BottleneckType;
  severity: AlertSeverity;
  metric: string;
  currentValue: number;
  threshold: number;
  component: string;
  suggestion: string;
}

export class RealTimeMonitor implements PerformanceMonitor {
  private metrics: MetricsCollector;
  private alertThresholds: AlertThreshold[];

  async startMonitoring(): Promise<void> {
    console.log("🔄 Starting real-time performance monitoring...");

    // Set up metric collection intervals
    setInterval(() => this.collectCPUMetrics(), 5000);
    setInterval(() => this.collectMemoryMetrics(), 5000);
    setInterval(() => this.collectDatabaseMetrics(), 30000);
    setInterval(() => this.collectNetworkMetrics(), 10000);

    // Set up bottleneck detection
    setInterval(() => this.detectAndAlertBottlenecks(), 15000);

    // Set up report generation
    setInterval(() => this.generateHourlyReport(), 3600000);
  }

  async detectBottlenecks(): Promise<BottleneckAlert[]> {
    const alerts: BottleneckAlert[] = [];
    const currentMetrics = await this.metrics.getCurrentMetrics();

    for (const threshold of this.alertThresholds) {
      const currentValue = this.getMetricValue(currentMetrics, threshold.metric);

      if (this.exceedsThreshold(currentValue, threshold)) {
        alerts.push({
          timestamp: new Date(),
          type: threshold.bottleneckType,
          severity: this.calculateSeverity(currentValue, threshold),
          metric: threshold.metric,
          currentValue,
          threshold: threshold.value,
          component: threshold.component,
          suggestion: this.generateSuggestion(threshold, currentValue),
        });
      }
    }

    return alerts;
  }

  private generateSuggestion(threshold: AlertThreshold, currentValue: number): string {
    const exceededBy = ((currentValue - threshold.value) / threshold.value * 100).toFixed(1);

    switch (threshold.bottleneckType) {
      case "cpu":
        return `CPU usage is ${exceededBy}% above threshold. Consider: 1) Optimizing algorithms, 2) Adding horizontal scaling, 3) Implementing caching`;
      case "memory":
        return `Memory usage is ${exceededBy}% above threshold. Consider: 1) Implementing object pooling, 2) Optimizing data structures, 3) Adding memory-based caching`;
      case "database":
        return `Database performance is degraded. Consider: 1) Adding indexes, 2) Query optimization, 3) Connection pooling`;
      case "network":
        return `Network performance issues detected. Consider: 1) Request batching, 2) Response compression, 3) CDN implementation`;
      default:
        return `Performance threshold exceeded by ${exceededBy}%. Investigation required.`;
    }
  }
}
```

### 2. Automated Alert System

**Intelligent Alert Management:**

```yaml
# Generated alerting configuration for Prometheus/Grafana
groups:
  - name: performance_bottlenecks
    rules:
      - alert: HighCPUUsage
        expr: cpu_usage_percent > 80
        for: 2m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "High CPU usage detected"
          description: "CPU usage is {{ $value }}% for more than 2 minutes"
          runbook_url: "/runbooks/high-cpu"

      - alert: CriticalCPUUsage
        expr: cpu_usage_percent > 95
        for: 30s
        labels:
          severity: critical
          component: application
        annotations:
          summary: "Critical CPU usage detected"
          description: "CPU usage is {{ $value }}% - immediate action required"

      - alert: MemoryPressure
        expr: memory_usage_percent > 85
        for: 1m
        labels:
          severity: warning
          component: application
        annotations:
          summary: "Memory pressure detected"
          description: "Memory usage is {{ $value }}% - potential GC issues"

      - alert: SlowDatabaseQueries
        expr: avg_query_duration_ms > 500
        for: 1m
        labels:
          severity: warning
          component: database
        annotations:
          summary: "Slow database queries detected"
          description: "Average query duration is {{ $value }}ms"

      - alert: DatabaseConnectionExhaustion
        expr: database_active_connections / database_max_connections > 0.9
        for: 30s
        labels:
          severity: critical
          component: database
        annotations:
          summary: "Database connection pool nearly exhausted"
          description: "{{ $value | humanizePercentage }} of connections in use"
```

## Integration and Output

### Integration with Other Commands

- Use with `/benchmark` for before/after performance comparisons
- Combine with `/profile` for detailed component analysis
- Integrate with `/monitor` for ongoing performance tracking
- Use with `/db-optimize` for database-specific optimizations

### Generated Outputs

1. **Bottleneck Analysis Report**: Comprehensive identification of performance issues across all system layers
2. **Optimization Strategies**: Specific code improvements with before/after examples
3. **Database Optimization Plan**: Query improvements, index recommendations, and configuration tuning
4. **Monitoring Setup**: Real-time performance monitoring with automated alerting
5. **Performance Baselines**: Establish performance metrics for regression detection
6. **Remediation Roadmap**: Prioritized list of optimizations with effort estimates and expected impact
