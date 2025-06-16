# /db-optimize

Comprehensive database performance optimization with intelligent query analysis, index recommendations, configuration tuning, and automated optimization strategies.

## Usage

```
/db-optimize [analyze|indexes|queries|config|monitor] [--database=auto] [--impact=medium]
```

## Parameters

- `analyze` - Comprehensive database performance analysis (default)
- `indexes` - Index optimization and recommendations
- `queries` - Query performance analysis and optimization
- `config` - Database configuration tuning
- `monitor` - Set up ongoing database performance monitoring
- `--database` - Target database: postgresql, mysql, mongodb, sqlite (auto-detect by default)
- `--impact` - Optimization impact level: low, medium, high (affects aggressiveness of changes)

## Context Intelligence

### Database Detection and Analysis

**Database System Discovery:**

```bash
# Detect database systems and gather connection information
detect_database_systems() {
  echo "🔍 Detecting database systems..."
  
  # PostgreSQL detection
  if command -v psql &> /dev/null || rg -q "postgresql|postgres" .; then
    POSTGRES_DETECTED=true
    
    # Check for connection details
    if [ -f ".env" ]; then
      POSTGRES_URL=$(rg "DATABASE_URL|POSTGRES_URL" .env | head -1 | cut -d'=' -f2)
    fi
    
    if [ -f "docker-compose.yml" ]; then
      POSTGRES_COMPOSE=$(yq '.services[] | select(.image | contains("postgres"))' docker-compose.yml)
    fi
    
    echo "✅ PostgreSQL detected"
  fi
  
  # MySQL detection
  if command -v mysql &> /dev/null || rg -q "mysql|mariadb" .; then
    MYSQL_DETECTED=true
    echo "✅ MySQL/MariaDB detected"
  fi
  
  # MongoDB detection
  if command -v mongosh &> /dev/null || rg -q "mongodb" .; then
    MONGODB_DETECTED=true
    echo "✅ MongoDB detected"
  fi
  
  # SQLite detection
  if fd "\.sqlite$|\.db$" > /dev/null || rg -q "sqlite" .; then
    SQLITE_DETECTED=true
    echo "✅ SQLite detected"
  fi
}

# Analyze current database configuration
analyze_current_config() {
  echo "⚙️ Analyzing current database configuration..."
  
  if [ "$POSTGRES_DETECTED" = true ]; then
    echo "Analyzing PostgreSQL configuration..."
    
    # Get current PostgreSQL settings
    psql -c "
    SELECT name, setting, unit, context, source
    FROM pg_settings 
    WHERE name IN (
      'shared_buffers', 'effective_cache_size', 'maintenance_work_mem',
      'checkpoint_completion_target', 'wal_buffers', 'default_statistics_target',
      'random_page_cost', 'effective_io_concurrency', 'work_mem', 'max_connections'
    )
    ORDER BY name;" > postgres_config.txt 2>/dev/null || echo "❌ Could not connect to PostgreSQL"
    
    # Get database size information
    psql -c "
    SELECT 
      datname as database_name,
      pg_size_pretty(pg_database_size(datname)) as size,
      pg_database_size(datname) as size_bytes
    FROM pg_database 
    WHERE datistemplate = false;" > postgres_db_sizes.txt 2>/dev/null
  fi
  
  if [ "$MYSQL_DETECTED" = true ]; then
    echo "Analyzing MySQL configuration..."
    
    # Get MySQL configuration
    mysql -e "
    SELECT VARIABLE_NAME, VARIABLE_VALUE 
    FROM information_schema.GLOBAL_VARIABLES 
    WHERE VARIABLE_NAME IN (
      'innodb_buffer_pool_size', 'innodb_log_file_size', 'innodb_log_buffer_size',
      'max_connections', 'query_cache_size', 'tmp_table_size', 'max_heap_table_size'
    )
    ORDER BY VARIABLE_NAME;" > mysql_config.txt 2>/dev/null || echo "❌ Could not connect to MySQL"
  fi
}
```

### Performance Metrics Collection

**Database Performance Analysis:**

```bash
# Collect comprehensive database performance metrics
collect_performance_metrics() {
  echo "📊 Collecting database performance metrics..."
  
  if [ "$POSTGRES_DETECTED" = true ]; then
    collect_postgres_metrics
  fi
  
  if [ "$MYSQL_DETECTED" = true ]; then
    collect_mysql_metrics
  fi
  
  if [ "$MONGODB_DETECTED" = true ]; then
    collect_mongodb_metrics
  fi
}

collect_postgres_metrics() {
  echo "🐘 Collecting PostgreSQL performance metrics..."
  
  # Query performance statistics
  psql -c "
  SELECT 
    query,
    calls,
    total_exec_time,
    mean_exec_time,
    rows,
    100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) as hit_percent
  FROM pg_stat_statements 
  WHERE calls > 10
  ORDER BY total_exec_time DESC 
  LIMIT 20;" > postgres_slow_queries.txt 2>/dev/null
  
  # Index usage statistics
  psql -c "
  SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
  FROM pg_stat_user_indexes 
  ORDER BY idx_scan DESC;" > postgres_index_usage.txt 2>/dev/null
  
  # Table statistics
  psql -c "
  SELECT 
    schemaname,
    tablename,
    n_tup_ins + n_tup_upd + n_tup_del as total_writes,
    seq_scan,
    seq_tup_read,
    idx_scan,
    idx_tup_fetch,
    n_dead_tup,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
  FROM pg_stat_user_tables 
  ORDER BY total_writes DESC;" > postgres_table_stats.txt 2>/dev/null
  
  # Connection and activity statistics
  psql -c "
  SELECT 
    datname,
    numbackends,
    xact_commit,
    xact_rollback,
    blks_read,
    blks_hit,
    tup_returned,
    tup_fetched,
    tup_inserted,
    tup_updated,
    tup_deleted,
    conflicts,
    temp_files,
    temp_bytes,
    deadlocks
  FROM pg_stat_database;" > postgres_db_stats.txt 2>/dev/null
}
```

## Database-Specific Optimization Strategies

### 1. PostgreSQL Optimization

**Comprehensive PostgreSQL Performance Analysis:**

```typescript
// Generated PostgreSQL optimizer
interface PostgreSQLOptimizer {
  analyzePerformance(): Promise<PostgreSQLAnalysis>;
  generateIndexRecommendations(): Promise<IndexRecommendation[]>;
  optimizeQueries(): Promise<QueryOptimization[]>;
  tuneConfiguration(): Promise<ConfigurationTuning>;
}

interface PostgreSQLAnalysis {
  slowQueries: SlowQuery[];
  indexIssues: IndexIssue[];
  vacuumIssues: VacuumIssue[];
  connectionIssues: ConnectionIssue[];
  configIssues: ConfigurationIssue[];
}

interface SlowQuery {
  query: string;
  totalTime: number;
  meanTime: number;
  calls: number;
  hitPercent: number;
  recommendation: string;
  explainPlan?: any;
}

export class PostgreSQLOptimizer implements PostgreSQLOptimizer {
  async analyzePerformance(): Promise<PostgreSQLAnalysis> {
    console.log("🐘 Analyzing PostgreSQL performance...");

    const slowQueries = await this.analyzeSlowQueries();
    const indexIssues = await this.analyzeIndexIssues();
    const vacuumIssues = await this.analyzeVacuumIssues();
    const connectionIssues = await this.analyzeConnectionIssues();
    const configIssues = await this.analyzeConfigurationIssues();

    return {
      slowQueries,
      indexIssues,
      vacuumIssues,
      connectionIssues,
      configIssues,
    };
  }

  async generateIndexRecommendations(): Promise<IndexRecommendation[]> {
    const recommendations: IndexRecommendation[] = [];

    // Analyze missing indexes based on pg_stat_statements
    const missingIndexes = await this.findMissingIndexes();

    for (const missing of missingIndexes) {
      recommendations.push({
        type: "create",
        table: missing.table,
        columns: missing.columns,
        indexType: missing.suggestedType,
        reason: missing.reason,
        impact: missing.estimatedImpact,
        sql: this.generateCreateIndexSQL(missing),
        priority: this.calculateIndexPriority(missing),
      });
    }

    // Analyze unused indexes
    const unusedIndexes = await this.findUnusedIndexes();

    for (const unused of unusedIndexes) {
      recommendations.push({
        type: "drop",
        table: unused.table,
        indexName: unused.indexName,
        reason: `Index not used (${unused.scanCount} scans)`,
        impact: "Reduced storage and faster writes",
        sql: `DROP INDEX CONCURRENTLY ${unused.indexName};`,
        priority: unused.size > 100 * 1024 * 1024 ? "medium" : "low", // 100MB threshold
      });
    }

    return recommendations;
  }

  private async findMissingIndexes(): Promise<MissingIndex[]> {
    // Analyze queries for potential index opportunities
    const queries = await this.getSlowQueries();
    const missingIndexes: MissingIndex[] = [];

    for (const query of queries) {
      if (query.hitPercent < 80) { // Low cache hit ratio
        const analysis = await this.analyzeQueryForIndexes(query);

        if (analysis.suggestedIndexes.length > 0) {
          missingIndexes.push(...analysis.suggestedIndexes);
        }
      }
    }

    return missingIndexes;
  }

  private generateCreateIndexSQL(missing: MissingIndex): string {
    const indexName = `idx_${missing.table}_${missing.columns.join("_")}`;

    switch (missing.suggestedType) {
      case "btree":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} (${
          missing.columns.join(", ")
        });`;
      case "partial":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} (${
          missing.columns.join(", ")
        }) WHERE ${missing.condition};`;
      case "gin":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} USING GIN (${
          missing.columns.join(", ")
        });`;
      case "gist":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} USING GIST (${
          missing.columns.join(", ")
        });`;
      default:
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} (${
          missing.columns.join(", ")
        });`;
    }
  }

  async optimizeQueries(): Promise<QueryOptimization[]> {
    const optimizations: QueryOptimization[] = [];
    const slowQueries = await this.getSlowQueries();

    for (const query of slowQueries) {
      const optimization = await this.optimizeQuery(query);
      if (optimization) {
        optimizations.push(optimization);
      }
    }

    return optimizations;
  }

  private async optimizeQuery(query: SlowQuery): Promise<QueryOptimization | null> {
    // Analyze query structure and suggest optimizations
    const analysis = await this.analyzeQueryStructure(query.query);

    if (analysis.issues.length > 0) {
      return {
        originalQuery: query.query,
        optimizedQuery: analysis.optimizedQuery,
        issues: analysis.issues,
        improvements: analysis.improvements,
        estimatedSpeedup: analysis.estimatedSpeedup,
        explanation: analysis.explanation,
      };
    }

    return null;
  }
}
```

**PostgreSQL Configuration Tuning:**

```sql
-- Generated PostgreSQL configuration optimizations

-- Memory Configuration
-- Calculate based on available system memory
DO $$
DECLARE
    total_memory_gb numeric;
    shared_buffers_size text;
    effective_cache_size_size text;
    work_mem_size text;
    maintenance_work_mem_size text;
BEGIN
    -- Get total system memory (assuming 8GB for example)
    total_memory_gb := 8;
    
    -- Shared buffers: 25% of total memory (but not more than 8GB)
    shared_buffers_size := LEAST(total_memory_gb * 0.25, 8) || 'GB';
    
    -- Effective cache size: 75% of total memory
    effective_cache_size_size := (total_memory_gb * 0.75) || 'GB';
    
    -- Work mem: Start with 4MB per connection
    work_mem_size := '4MB';
    
    -- Maintenance work mem: 256MB to 1GB
    maintenance_work_mem_size := LEAST(total_memory_gb * 0.05, 1) || 'GB';
    
    RAISE NOTICE 'Recommended PostgreSQL memory settings:';
    RAISE NOTICE 'shared_buffers = %', shared_buffers_size;
    RAISE NOTICE 'effective_cache_size = %', effective_cache_size_size;
    RAISE NOTICE 'work_mem = %', work_mem_size;
    RAISE NOTICE 'maintenance_work_mem = %', maintenance_work_mem_size;
END $$;

-- Checkpoint and WAL Configuration
-- For write-heavy workloads
ALTER SYSTEM SET checkpoint_completion_target = 0.9;
ALTER SYSTEM SET wal_buffers = '16MB';
ALTER SYSTEM SET checkpoint_segments = 32;  -- PostgreSQL < 9.5
ALTER SYSTEM SET max_wal_size = '2GB';      -- PostgreSQL >= 9.5

-- Query Planner Configuration
ALTER SYSTEM SET default_statistics_target = 100;
ALTER SYSTEM SET random_page_cost = 1.1;  -- For SSD storage
ALTER SYSTEM SET effective_io_concurrency = 200;  -- For SSD storage

-- Connection Configuration
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET shared_preload_libraries = 'pg_stat_statements';

-- Apply changes
SELECT pg_reload_conf();

-- Create optimized indexes for common query patterns
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Index for email lookups
CREATE INDEX CONCURRENTLY idx_users_email_hash ON users USING hash (email);

-- Partial index for active users
CREATE INDEX CONCURRENTLY idx_users_active ON users (created_at) WHERE active = true;

-- Composite index for common query patterns
CREATE INDEX CONCURRENTLY idx_orders_user_date ON orders (user_id, created_at DESC);

-- GIN index for JSON/array columns
CREATE INDEX CONCURRENTLY idx_products_tags ON products USING GIN (tags);

-- Expression index for case-insensitive searches
CREATE INDEX CONCURRENTLY idx_users_name_lower ON users (LOWER(name));
```

### 2. MySQL/MariaDB Optimization

**MySQL Performance Analysis and Optimization:**

```sql
-- Generated MySQL optimization queries

-- Analyze slow queries
SELECT 
  ROUND(SUM(total_latency)/1000000) as exec_time_ms,
  sql_text,
  exec_count,
  ROUND(avg_latency/1000000) as avg_latency_ms,
  ROUND(lock_latency/1000000) as lock_latency_ms,
  rows_sent_avg,
  rows_examined_avg,
  first_seen,
  last_seen
FROM performance_schema.events_statements_summary_by_digest 
WHERE digest_text NOT LIKE '%performance_schema%'
ORDER BY SUM(total_latency) DESC
LIMIT 20;

-- Find tables without primary keys
SELECT 
  table_schema,
  table_name
FROM information_schema.tables t
LEFT JOIN information_schema.table_constraints tc 
  ON t.table_schema = tc.table_schema 
  AND t.table_name = tc.table_name 
  AND tc.constraint_type = 'PRIMARY KEY'
WHERE t.table_schema NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
  AND tc.constraint_name IS NULL
  AND t.table_type = 'BASE TABLE';

-- Analyze index efficiency
SELECT 
  OBJECT_SCHEMA as db,
  OBJECT_NAME as table_name,
  INDEX_NAME as index_name,
  COUNT_FETCH,
  COUNT_INSERT,
  COUNT_UPDATE,
  COUNT_DELETE,
  COUNT_FETCH / (COUNT_INSERT + COUNT_UPDATE + COUNT_DELETE + 1) as efficiency_ratio
FROM performance_schema.table_io_waits_summary_by_index_usage
WHERE OBJECT_SCHEMA NOT IN ('mysql', 'performance_schema', 'information_schema', 'sys')
  AND INDEX_NAME IS NOT NULL
ORDER BY efficiency_ratio ASC;

-- Find duplicate indexes
SELECT 
  a.table_schema,
  a.table_name,
  a.index_name as index1,
  b.index_name as index2,
  a.column_name,
  a.seq_in_index
FROM information_schema.statistics a
JOIN information_schema.statistics b 
  ON a.table_schema = b.table_schema
  AND a.table_name = b.table_name
  AND a.column_name = b.column_name
  AND a.seq_in_index = b.seq_in_index
  AND a.index_name != b.index_name
WHERE a.table_schema NOT IN ('information_schema', 'performance_schema', 'mysql', 'sys')
ORDER BY a.table_schema, a.table_name, a.seq_in_index;

-- MySQL configuration recommendations
SET @total_memory_gb = 8; -- Adjust based on system memory

-- InnoDB Buffer Pool: 70-80% of total memory
SELECT CONCAT('innodb_buffer_pool_size = ', FLOOR(@total_memory_gb * 0.75), 'G') as recommendation
UNION ALL
-- InnoDB Log File Size: 25% of buffer pool size
SELECT CONCAT('innodb_log_file_size = ', FLOOR(@total_memory_gb * 0.75 * 0.25), 'G')
UNION ALL
-- Query Cache (if using MySQL < 8.0)
SELECT 'query_cache_type = 1'
UNION ALL
SELECT CONCAT('query_cache_size = ', LEAST(FLOOR(@total_memory_gb * 0.1), 1), 'G')
UNION ALL
-- Connection limits
SELECT 'max_connections = 200'
UNION ALL
-- Temporary table settings
SELECT 'tmp_table_size = 256M'
UNION ALL
SELECT 'max_heap_table_size = 256M';
```

### 3. MongoDB Optimization

**MongoDB Performance Analysis:**

```javascript
// Generated MongoDB optimization scripts

// Analyze slow operations
db.setProfilingLevel(2, { slowms: 100 });

// Find slow queries
db.system.profile.find().limit(20).sort({ ts: -1 }).pretty();

// Index analysis
db.runCommand({ listCollections: 1 }).cursor.firstBatch.forEach(
  function (collection) {
    print("Collection: " + collection.name);
    db[collection.name].getIndexes().forEach(function (index) {
      print("  Index: " + JSON.stringify(index.key) + " - " + index.name);
    });
  },
);

// Find collections without indexes
db.runCommand({ listCollections: 1 }).cursor.firstBatch.forEach(
  function (collection) {
    var indexes = db[collection.name].getIndexes();
    if (indexes.length === 1 && indexes[0].name === "_id_") {
      print("Collection with only _id index: " + collection.name);
    }
  },
);

// Query performance analysis
function analyzeQuery(collection, query) {
  print("Analyzing query on " + collection + ":");
  print("Query: " + JSON.stringify(query));

  var explain = db[collection].find(query).explain("executionStats");
  print("Execution time: " + explain.executionStats.executionTimeMillis + "ms");
  print("Documents examined: " + explain.executionStats.totalDocsExamined);
  print("Documents returned: " + explain.executionStats.totalDocsReturned);
  print("Index used: " + (explain.executionStats.indexesUsed ? "Yes" : "No"));

  if (explain.executionStats.totalDocsExamined > explain.executionStats.totalDocsReturned * 10) {
    print("⚠️ Warning: High document examination ratio - consider adding an index");
  }
}

// Index recommendations
function recommendIndexes() {
  // Analyze most common query patterns
  var profile = db.system.profile.aggregate([
    { $match: { "command.find": { $exists: true } } },
    {
      $group: {
        _id: {
          collection: "$command.find",
          filter: "$command.filter",
        },
        count: { $sum: 1 },
        avgDuration: { $avg: "$millis" },
      },
    },
    { $sort: { count: -1 } },
    { $limit: 10 },
  ]).toArray();

  profile.forEach(function (op) {
    print("Frequent query on " + op._id.collection + ":");
    print("  Filter: " + JSON.stringify(op._id.filter));
    print("  Count: " + op.count + ", Avg duration: " + op.avgDuration + "ms");

    // Suggest indexes based on filter fields
    var filterFields = Object.keys(op._id.filter || {});
    if (filterFields.length > 0) {
      var indexSpec = {};
      filterFields.forEach(function (field) {
        indexSpec[field] = 1;
      });
      print("  Suggested index: " + JSON.stringify(indexSpec));
    }
  });
}

// Connection and performance metrics
function getPerformanceMetrics() {
  var serverStatus = db.serverStatus();

  print("=== MongoDB Performance Metrics ===");
  print(
    "Connections: " + serverStatus.connections.current + "/" + serverStatus.connections.available,
  );
  print(
    "Memory usage: " + Math.round(serverStatus.mem.resident) + "MB resident, " +
      Math.round(serverStatus.mem.virtual) + "MB virtual",
  );
  print("Operations per second:");
  print("  Insert: " + serverStatus.opcounters.insert);
  print("  Query: " + serverStatus.opcounters.query);
  print("  Update: " + serverStatus.opcounters.update);
  print("  Delete: " + serverStatus.opcounters.delete);

  if (serverStatus.wiredTiger) {
    var cache = serverStatus.wiredTiger.cache;
    print("WiredTiger cache:");
    print("  Cache size: " + Math.round(cache["maximum bytes configured"] / 1024 / 1024) + "MB");
    print(
      "  Cache used: " + Math.round(cache["bytes currently in the cache"] / 1024 / 1024) + "MB",
    );
    print(
      "  Cache hit ratio: " +
        Math.round(
          cache["pages read into cache"] /
            (cache["pages read into cache"] + cache["pages requested from the cache"]) * 100,
        ) + "%",
    );
  }
}

// Run analysis
recommendIndexes();
getPerformanceMetrics();
```

## Query Optimization Engine

### 1. Automated Query Analysis

**Intelligent Query Optimization:**

```typescript
// Generated query optimization engine
interface QueryOptimizer {
  analyzeQuery(query: string, database: DatabaseType): Promise<QueryAnalysis>;
  optimizeQuery(query: string, schema: DatabaseSchema): Promise<OptimizedQuery>;
  generateExplainPlan(query: string): Promise<ExplainPlan>;
}

interface QueryAnalysis {
  performance: PerformanceMetrics;
  issues: QueryIssue[];
  suggestions: OptimizationSuggestion[];
  complexity: QueryComplexity;
}

interface OptimizedQuery {
  originalQuery: string;
  optimizedQuery: string;
  changes: QueryChange[];
  expectedImprovement: number; // percentage
  riskLevel: "low" | "medium" | "high";
}

export class SmartQueryOptimizer implements QueryOptimizer {
  async analyzeQuery(query: string, database: DatabaseType): Promise<QueryAnalysis> {
    const ast = this.parseQuery(query);
    const performance = await this.measureQueryPerformance(query);
    const issues = this.identifyQueryIssues(ast, performance);
    const suggestions = this.generateOptimizationSuggestions(issues, ast);
    const complexity = this.calculateQueryComplexity(ast);

    return {
      performance,
      issues,
      suggestions,
      complexity,
    };
  }

  async optimizeQuery(query: string, schema: DatabaseSchema): Promise<OptimizedQuery> {
    const analysis = await this.analyzeQuery(query, schema.type);
    const optimizations = this.prioritizeOptimizations(analysis.suggestions);

    let optimizedQuery = query;
    const changes: QueryChange[] = [];

    for (const optimization of optimizations) {
      const result = this.applyOptimization(optimizedQuery, optimization, schema);
      if (result.success) {
        optimizedQuery = result.query;
        changes.push(result.change);
      }
    }

    const expectedImprovement = this.estimateImprovement(changes);
    const riskLevel = this.assessOptimizationRisk(changes);

    return {
      originalQuery: query,
      optimizedQuery,
      changes,
      expectedImprovement,
      riskLevel,
    };
  }

  private identifyQueryIssues(ast: QueryAST, performance: PerformanceMetrics): QueryIssue[] {
    const issues: QueryIssue[] = [];

    // Check for SELECT * queries
    if (ast.select.includes("*")) {
      issues.push({
        type: "select_star",
        severity: "medium",
        description: "Using SELECT * returns unnecessary columns",
        recommendation: "Specify only needed columns in SELECT clause",
        impact: "Reduced network transfer and memory usage",
      });
    }

    // Check for missing WHERE clauses on large tables
    if (!ast.where && performance.rowsExamined > 10000) {
      issues.push({
        type: "missing_where",
        severity: "high",
        description: "Query without WHERE clause on large table",
        recommendation: "Add appropriate WHERE conditions to limit rows",
        impact: "Dramatically reduced query execution time",
      });
    }

    // Check for inefficient JOINs
    if (ast.joins && ast.joins.length > 0) {
      for (const join of ast.joins) {
        if (!this.hasIndexOnJoinColumn(join.condition)) {
          issues.push({
            type: "unindexed_join",
            severity: "high",
            description: `JOIN without index on ${join.condition}`,
            recommendation: `Create index on ${join.condition}`,
            impact: "Faster JOIN operations",
          });
        }
      }
    }

    // Check for ORDER BY without indexes
    if (ast.orderBy && !this.hasIndexOnOrderByColumns(ast.orderBy)) {
      issues.push({
        type: "unindexed_order_by",
        severity: "medium",
        description: "ORDER BY without supporting index",
        recommendation: "Create index on ORDER BY columns",
        impact: "Eliminates expensive sorting operations",
      });
    }

    // Check for subqueries that could be JOINs
    if (ast.subqueries && ast.subqueries.length > 0) {
      issues.push({
        type: "subquery_to_join",
        severity: "medium",
        description: "Correlated subqueries can often be rewritten as JOINs",
        recommendation: "Consider rewriting as JOIN for better performance",
        impact: "Improved query execution plan",
      });
    }

    return issues;
  }

  private generateOptimizationSuggestions(
    issues: QueryIssue[],
    ast: QueryAST,
  ): OptimizationSuggestion[] {
    const suggestions: OptimizationSuggestion[] = [];

    for (const issue of issues) {
      switch (issue.type) {
        case "select_star":
          suggestions.push({
            type: "rewrite_select",
            priority: "medium",
            description: "Replace SELECT * with specific column names",
            implementation: this.generateSelectColumnList(ast),
            estimatedImprovement: 15,
          });
          break;

        case "missing_where":
          suggestions.push({
            type: "add_where_clause",
            priority: "high",
            description: "Add WHERE clause to limit results",
            implementation: "Add appropriate filtering conditions",
            estimatedImprovement: 70,
          });
          break;

        case "unindexed_join":
          suggestions.push({
            type: "create_index",
            priority: "high",
            description: "Create index on JOIN columns",
            implementation: this.generateIndexSQL(issue),
            estimatedImprovement: 60,
          });
          break;

        case "subquery_to_join":
          suggestions.push({
            type: "rewrite_subquery",
            priority: "medium",
            description: "Rewrite correlated subquery as JOIN",
            implementation: this.convertSubqueryToJoin(ast),
            estimatedImprovement: 40,
          });
          break;
      }
    }

    return suggestions;
  }
}
```

### 2. Automated Index Management

**Smart Index Recommendations:**

```typescript
// Generated index management system
interface IndexManager {
  analyzeIndexUsage(): Promise<IndexUsageAnalysis>;
  recommendIndexes(): Promise<IndexRecommendation[]>;
  validateIndexes(): Promise<IndexValidation[]>;
  optimizeIndexes(): Promise<IndexOptimization[]>;
}

interface IndexRecommendation {
  type: "create" | "drop" | "modify";
  table: string;
  columns: string[];
  indexType: "btree" | "hash" | "gin" | "gist" | "partial";
  reason: string;
  priority: "low" | "medium" | "high" | "critical";
  impact: string;
  sql: string;
  size?: number;
  maintenance?: string;
}

export class SmartIndexManager implements IndexManager {
  async analyzeIndexUsage(): Promise<IndexUsageAnalysis> {
    const indexStats = await this.getIndexStatistics();
    const queryPatterns = await this.analyzeQueryPatterns();
    const tableStats = await this.getTableStatistics();

    return {
      totalIndexes: indexStats.length,
      unusedIndexes: indexStats.filter((idx) => idx.scans === 0),
      underusedIndexes: indexStats.filter((idx) => idx.scans > 0 && idx.scans < 10),
      efficientIndexes: indexStats.filter((idx) => idx.efficiency > 0.8),
      missingIndexes: await this.identifyMissingIndexes(queryPatterns, tableStats),
      duplicateIndexes: await this.findDuplicateIndexes(indexStats),
    };
  }

  async recommendIndexes(): Promise<IndexRecommendation[]> {
    const recommendations: IndexRecommendation[] = [];
    const analysis = await this.analyzeIndexUsage();

    // Recommend dropping unused indexes
    for (const unused of analysis.unusedIndexes) {
      if (unused.size > 50 * 1024 * 1024) { // 50MB threshold
        recommendations.push({
          type: "drop",
          table: unused.table,
          columns: [],
          indexType: "btree",
          reason: `Unused index consuming ${this.formatBytes(unused.size)}`,
          priority: "medium",
          impact: "Reduced storage usage and faster writes",
          sql: `DROP INDEX CONCURRENTLY ${unused.name};`,
          size: unused.size,
          maintenance: "Monitor for any performance impact after dropping",
        });
      }
    }

    // Recommend creating missing indexes
    for (const missing of analysis.missingIndexes) {
      recommendations.push({
        type: "create",
        table: missing.table,
        columns: missing.columns,
        indexType: missing.type,
        reason: missing.reason,
        priority: this.calculatePriority(missing.impact),
        impact: missing.impact,
        sql: this.generateCreateIndexSQL(missing),
        maintenance: "Monitor index size and usage after creation",
      });
    }

    // Recommend composite indexes for common query patterns
    const compositeRecommendations = await this.analyzeCompositeIndexOpportunities();
    recommendations.push(...compositeRecommendations);

    return recommendations.sort((a, b) => {
      const priorityOrder = { critical: 4, high: 3, medium: 2, low: 1 };
      return priorityOrder[b.priority] - priorityOrder[a.priority];
    });
  }

  private async identifyMissingIndexes(
    queryPatterns: QueryPattern[],
    tableStats: TableStatistic[],
  ): Promise<MissingIndex[]> {
    const missingIndexes: MissingIndex[] = [];

    for (const pattern of queryPatterns) {
      if (pattern.frequency > 100 && pattern.avgExecutionTime > 100) {
        const analysis = this.analyzeQueryForIndexNeeds(pattern);

        if (analysis.recommendedIndexes.length > 0) {
          for (const recommended of analysis.recommendedIndexes) {
            const tableSize = tableStats.find((t) => t.name === recommended.table)?.rowCount || 0;

            if (tableSize > 1000) { // Only recommend for tables with significant size
              missingIndexes.push({
                table: recommended.table,
                columns: recommended.columns,
                type: recommended.type,
                reason:
                  `Query pattern executed ${pattern.frequency} times with avg ${pattern.avgExecutionTime}ms`,
                impact: this.estimateIndexImpact(recommended, pattern, tableSize),
                queryPattern: pattern.pattern,
              });
            }
          }
        }
      }
    }

    return missingIndexes;
  }

  private generateCreateIndexSQL(missing: MissingIndex): string {
    const indexName = `idx_${missing.table}_${missing.columns.join("_")}`;
    const columns = missing.columns.join(", ");

    switch (missing.type) {
      case "partial":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} (${columns}) WHERE ${missing.condition};`;
      case "gin":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} USING GIN (${columns});`;
      case "gist":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} USING GIST (${columns});`;
      case "hash":
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} USING HASH (${columns});`;
      default:
        return `CREATE INDEX CONCURRENTLY ${indexName} ON ${missing.table} (${columns});`;
    }
  }

  private async analyzeCompositeIndexOpportunities(): Promise<IndexRecommendation[]> {
    const recommendations: IndexRecommendation[] = [];

    // Analyze queries that could benefit from composite indexes
    const multiColumnQueries = await this.findMultiColumnQueries();

    for (const query of multiColumnQueries) {
      if (query.frequency > 50 && query.columns.length > 1) {
        const existingIndexes = await this.getTableIndexes(query.table);
        const hasCompositeIndex = existingIndexes.some((idx) =>
          idx.columns.length > 1 &&
          query.columns.every((col) => idx.columns.includes(col))
        );

        if (!hasCompositeIndex) {
          recommendations.push({
            type: "create",
            table: query.table,
            columns: query.columns,
            indexType: "btree",
            reason: `Multi-column query executed ${query.frequency} times`,
            priority: "medium",
            impact: `Potential ${
              this.estimateCompositeIndexImpact(query)
            }% performance improvement`,
            sql: this.generateCreateIndexSQL({
              table: query.table,
              columns: query.columns,
              type: "btree",
            } as MissingIndex),
          });
        }
      }
    }

    return recommendations;
  }
}
```

## Monitoring and Alerting

### 1. Performance Monitoring Setup

**Database Performance Dashboard:**

```yaml
# Generated Grafana dashboard configuration for database monitoring
apiVersion: 1

datasources:
  - name: Prometheus
    type: prometheus
    url: http://prometheus:9090

dashboards:
  - title: "Database Performance Overview"
    panels:
      - title: "Query Response Time"
        type: stat
        targets:
          - expr: avg(mysql_global_status_queries) by (instance)
            legendFormat: "{{instance}}"
        fieldConfig:
          defaults:
            unit: ms
            thresholds:
              steps:
                - color: green
                  value: 0
                - color: yellow
                  value: 100
                - color: red
                  value: 500

      - title: "Slow Queries per Second"
        type: graph
        targets:
          - expr: rate(mysql_global_status_slow_queries[5m])
            legendFormat: "Slow Queries/sec"
        yAxes:
          - label: "Queries/sec"
            min: 0

      - title: "Database Connections"
        type: graph
        targets:
          - expr: mysql_global_status_threads_connected
            legendFormat: "Active Connections"
          - expr: mysql_global_variables_max_connections
            legendFormat: "Max Connections"

      - title: "Index Usage Efficiency"
        type: table
        targets:
          - expr: |
              (mysql_info_schema_table_statistics_index_length /
               mysql_info_schema_table_statistics_data_length) * 100
            legendFormat: "Index Ratio %"
        transformations:
          - id: organize
            options:
              excludeByName:
                __name__: true

      - title: "Buffer Pool Hit Ratio"
        type: stat
        targets:
          - expr: |
              (mysql_global_status_innodb_buffer_pool_read_requests -
               mysql_global_status_innodb_buffer_pool_reads) /
               mysql_global_status_innodb_buffer_pool_read_requests * 100
            legendFormat: "Hit Ratio %"
        fieldConfig:
          defaults:
            unit: percent
            thresholds:
              steps:
                - color: red
                  value: 0
                - color: yellow
                  value: 90
                - color: green
                  value: 95

alerts:
  - alert: DatabaseHighResponseTime
    expr: avg_over_time(mysql_global_status_queries[5m]) > 500
    for: 2m
    labels:
      severity: warning
    annotations:
      summary: "Database response time is high"
      description: "Average query response time is {{ $value }}ms"

  - alert: SlowQueriesHigh
    expr: rate(mysql_global_status_slow_queries[5m]) > 10
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "High number of slow queries"
      description: "{{ $value }} slow queries per second"

  - alert: DatabaseConnectionsHigh
    expr: |
      mysql_global_status_threads_connected /
      mysql_global_variables_max_connections > 0.8
    for: 1m
    labels:
      severity: warning
    annotations:
      summary: "Database connection usage high"
      description: "{{ $value | humanizePercentage }} of connections in use"
```

### 2. Automated Performance Alerts

**Intelligent Alert System:**

```typescript
// Generated database alert system
interface DatabaseAlertManager {
  monitorPerformance(): Promise<void>;
  evaluateThresholds(metrics: DatabaseMetrics): Alert[];
  sendAlert(alert: Alert): Promise<void>;
}

interface Alert {
  id: string;
  severity: "info" | "warning" | "critical";
  metric: string;
  currentValue: number;
  threshold: number;
  message: string;
  recommendations: string[];
  timestamp: Date;
}

export class SmartDatabaseAlerts implements DatabaseAlertManager {
  private thresholds: AlertThreshold[] = [
    {
      metric: "avg_query_time",
      warning: 100,
      critical: 500,
      window: "5m",
    },
    {
      metric: "connection_utilization",
      warning: 0.7,
      critical: 0.9,
      window: "1m",
    },
    {
      metric: "slow_queries_rate",
      warning: 5,
      critical: 20,
      window: "5m",
    },
    {
      metric: "buffer_pool_hit_ratio",
      warning: 0.95,
      critical: 0.90,
      window: "5m",
      invert: true, // Alert when value is BELOW threshold
    },
  ];

  async monitorPerformance(): Promise<void> {
    setInterval(async () => {
      try {
        const metrics = await this.collectMetrics();
        const alerts = this.evaluateThresholds(metrics);

        for (const alert of alerts) {
          await this.sendAlert(alert);
        }
      } catch (error) {
        console.error("Error in performance monitoring:", error);
      }
    }, 30000); // Check every 30 seconds
  }

  evaluateThresholds(metrics: DatabaseMetrics): Alert[] {
    const alerts: Alert[] = [];

    for (const threshold of this.thresholds) {
      const value = this.getMetricValue(metrics, threshold.metric);
      const severity = this.calculateSeverity(value, threshold);

      if (severity) {
        alerts.push({
          id: `${threshold.metric}_${Date.now()}`,
          severity,
          metric: threshold.metric,
          currentValue: value,
          threshold: severity === "critical" ? threshold.critical : threshold.warning,
          message: this.generateAlertMessage(threshold.metric, value, severity),
          recommendations: this.generateRecommendations(threshold.metric, value, severity),
          timestamp: new Date(),
        });
      }
    }

    return alerts;
  }

  private generateRecommendations(metric: string, value: number, severity: string): string[] {
    const recommendations: string[] = [];

    switch (metric) {
      case "avg_query_time":
        recommendations.push("Analyze slow query log for optimization opportunities");
        recommendations.push("Check for missing indexes on frequently queried columns");
        recommendations.push("Consider query rewriting or caching for expensive operations");
        if (severity === "critical") {
          recommendations.push("Consider adding read replicas to distribute load");
        }
        break;

      case "connection_utilization":
        recommendations.push("Implement connection pooling if not already in use");
        recommendations.push("Review application connection management");
        recommendations.push("Consider increasing max_connections if hardware allows");
        if (severity === "critical") {
          recommendations.push("Investigate potential connection leaks");
        }
        break;

      case "slow_queries_rate":
        recommendations.push("Enable slow query log analysis");
        recommendations.push("Review and optimize queries exceeding slow_query_log_time");
        recommendations.push("Add appropriate indexes for slow queries");
        break;

      case "buffer_pool_hit_ratio":
        recommendations.push("Consider increasing innodb_buffer_pool_size");
        recommendations.push("Analyze memory usage and available system resources");
        recommendations.push("Review query patterns for unnecessary full table scans");
        break;
    }

    return recommendations;
  }

  async sendAlert(alert: Alert): Promise<void> {
    // Prevent alert spam with deduplication
    if (await this.isDuplicateAlert(alert)) {
      return;
    }

    const message = this.formatAlertMessage(alert);

    // Send to multiple channels
    await Promise.all([
      this.sendSlackAlert(message),
      this.sendEmailAlert(alert),
      this.logAlert(alert),
    ]);

    // Store alert for deduplication
    await this.storeAlert(alert);
  }

  private formatAlertMessage(alert: Alert): string {
    const emoji = alert.severity === "critical" ? "🚨" : alert.severity === "warning" ? "⚠️" : "ℹ️";

    return `
${emoji} **Database Performance Alert**

**Metric:** ${alert.metric}
**Severity:** ${alert.severity.toUpperCase()}
**Current Value:** ${alert.currentValue}
**Threshold:** ${alert.threshold}
**Time:** ${alert.timestamp.toISOString()}

**Message:** ${alert.message}

**Recommendations:**
${alert.recommendations.map((r) => `• ${r}`).join("\n")}

**Investigation Steps:**
1. Check database performance dashboard
2. Review recent query patterns
3. Analyze system resource usage
4. Consider immediate mitigation if critical
`;
  }
}
```

## Integration and Output

### Integration with Other Commands

- Use with `/bottleneck` for comprehensive performance analysis
- Combine with `/monitor` for ongoing database health tracking
- Integrate with `/benchmark` for performance regression testing
- Use with `/harden` for security-focused database optimization

### Generated Outputs

1. **Performance Analysis Report**: Comprehensive database performance assessment with specific bottleneck identification
2. **Index Optimization Plan**: Detailed index recommendations with priority and impact analysis
3. **Query Optimization Guide**: Specific query improvements with before/after comparisons
4. **Configuration Tuning**: Database parameter optimization based on workload analysis
5. **Monitoring Dashboard**: Real-time database performance monitoring with intelligent alerting
6. **Maintenance Schedule**: Automated database maintenance tasks and optimization routines

<function_calls>
<invoke name="TodoWrite">
<parameter name="todos">[{"id": "1", "content": "Create /test-gen command file", "status": "completed", "priority": "high"}, {"id": "2", "content": "Create /flaky-fix command file", "status": "completed", "priority": "high"}, {"id": "3", "content": "Create /coverage command file", "status": "completed", "priority": "high"}, {"id": "4", "content": "Create /threat-model command file", "status": "completed", "priority": "high"}, {"id": "5", "content": "Create /bottleneck command file", "status": "completed", "priority": "high"}, {"id": "6", "content": "Create /db-optimize command file", "status": "completed", "priority": "high"}]
