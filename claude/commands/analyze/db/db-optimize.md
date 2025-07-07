---
allowed-tools: Bash(psql:*), Bash(mysql:*), Bash(mongosh:*), Bash(sqlite3:*), Read, Write, Task
description: Comprehensive database performance optimization with intelligent analysis and automated improvements
---

## Context

- Session ID: !`gdate +%s%N`
- Current directory: !`pwd`
- Database systems detected: !`(command -v psql >/dev/null && echo "PostgreSQL") || true; (command -v mysql >/dev/null && echo "MySQL") || true; (command -v mongosh >/dev/null && echo "MongoDB") || true; fd "\.(sqlite|db)$" . -t f | head -1 >/dev/null && echo "SQLite" || true`
- Docker services: !`docker-compose ps 2>/dev/null | rg "(postgres|mysql|mongo)" | head -5 || echo "No database containers running"`
- Database configs: !`fd "(\.env|docker-compose\.yml|database\.yml)" . -t f | head -5 || echo "No database config files found"`
- Environment variables: !`env | rg "DATABASE_URL|DB_" | cut -d'=' -f1 || echo "No database env vars"`
- Project type: !`fd "(package\.json|Cargo\.toml|go\.mod|pom\.xml)" . -t f -d 1 | head -1 | xargs basename 2>/dev/null || echo "Unknown"`

## Your Task

Perform comprehensive database performance optimization for $ARGUMENTS using intelligent analysis and automated improvements.

STEP 1: Database Discovery and Environment Analysis

- Initialize session state: /tmp/db-optimize-!`gdate +%s%N`.json
- Detect available database systems (PostgreSQL, MySQL, MongoDB, SQLite)
- Test connectivity and gather connection status
- Identify configuration files and environment setup
- Create performance baseline snapshot

STEP 2: Performance Analysis and Bottleneck Identification

IF multiple database systems detected:

- Use Task tool to delegate parallel analysis:
  - **PostgreSQL Agent**: Analyze pg_stat_statements, index usage, vacuum optimization
  - **MySQL Agent**: Analyze performance_schema, InnoDB efficiency, buffer pool metrics
  - **MongoDB Agent**: Enable profiling, analyze collections, query patterns, connection metrics
  - **SQLite Agent**: Run EXPLAIN QUERY PLAN, check indexes, analyze file performance
- Think deeply about cross-database optimization strategies and workload coordination
- Coordinate findings and identify common bottleneck patterns across systems

ELSE IF single database system:

- Perform focused analysis on detected database type
- Think hard about database-specific optimization opportunities and configuration tuning
- Consider workload characteristics, usage patterns, and performance requirements

**Database-Specific Analysis Execution:**

- **PostgreSQL**: pg_stat_statements analysis, index usage examination, vacuum optimization, configuration tuning
- **MySQL**: performance_schema queries, InnoDB tuning, connection pool analysis, buffer pool optimization
- **MongoDB**: Collection profiling, index effectiveness analysis, query pattern optimization, replica set tuning
- **SQLite**: Query plan analysis, index recommendations, file-based optimization, VACUUM operations

STEP 3: Risk Assessment and Optimization Planning

- Think deeply about optimization risks, trade-offs, and production impact considerations
- Categorize identified issues by risk level (low/medium/high)
- Prioritize optimizations by impact vs. implementation complexity
- Create rollback procedures for configuration changes
- Generate specific SQL statements for index modifications
- Estimate performance improvement potential and maintenance requirements
- Consider production downtime, maintenance windows, and business impact

STEP 4: Implementation with Safeguards

TRY:

- Apply low-risk optimizations first (index creation, statistics updates)
- Create configuration backups before parameter changes
- Implement changes with proper online operations (CONCURRENTLY, etc.)
- Monitor performance metrics during implementation

CATCH (database_connection_failure):

- Document connection issues and requirements
- Provide offline analysis based on available configuration files
- Generate recommendations for when database is accessible

CATCH (insufficient_permissions):

- Document required database permissions
- Provide read-only analysis alternatives
- Generate scripts for database administrator execution

STEP 5: Validation and Performance Measurement

- Compare performance metrics before/after optimization
- Validate that indexes are being used effectively
- Check for any negative side effects (increased write times, etc.)
- Generate comprehensive optimization report with metrics

STEP 6: Monitoring and Maintenance Setup

TRY:

- Generate database-specific monitoring queries and performance dashboards
- Create intelligent alerting thresholds based on baseline metrics
- Provide automated maintenance schedules (vacuum, analyze, statistics updates)
- Document ongoing optimization procedures and performance regression detection
- Set up performance trending and capacity planning metrics
- Save checkpoint: monitoring_setup_complete

CATCH (monitoring_tool_unavailable):

- Document monitoring requirements and recommended tools
- Create manual monitoring procedures and scripts
- Provide performance baseline documentation for future comparison
- Generate monitoring tool installation and configuration guide

STEP 7: State Management and Session Completion

```json
// /tmp/db-optimize-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "target": "$ARGUMENTS",
  "phase": "discovery|analysis|optimization|validation|monitoring|complete",
  "discoveredDatabases": ["postgresql", "mysql", "mongodb", "sqlite"],
  "analysisStrategy": {
    "approach": "single|multi-database|parallel-agents",
    "subAgentsUsed": ["postgresql", "mysql", "mongodb", "sqlite"],
    "complexityLevel": "simple|moderate|complex"
  },
  "optimizationResults": {
    "indexesCreated": 3,
    "configChanges": 5,
    "performanceImprovement": "45%",
    "riskLevel": "low",
    "estimatedDowntime": "minimal",
    "rollbackTested": true
  },
  "recommendations": {
    "immediate": ["Create index on users.email", "Increase shared_buffers"],
    "scheduled": ["VACUUM ANALYZE", "Update table statistics"],
    "monitoring": ["Track slow query log", "Monitor connection usage"],
    "longTerm": ["Consider read replicas", "Implement connection pooling"]
  },
  "rollbackProcedures": {
    "indexDrops": ["DROP INDEX CONCURRENTLY idx_users_email"],
    "configRollback": "shared_buffers = 128MB",
    "validationSteps": ["Check query performance", "Monitor error logs"]
  },
  "checkpoints": {
    "discovery_complete": true,
    "analysis_complete": true,
    "optimization_applied": true,
    "validation_passed": true,
    "monitoring_configured": true
  }
}
```

FINALLY:

- Update session state: phase = "complete"
- Generate comprehensive optimization report with before/after metrics
- Archive optimization session data for future reference
- Clean up temporary analysis files: /tmp/db-optimize-temp-$SESSION_ID-*
- Create follow-up recommendations and maintenance schedule
- Update project documentation with performance improvements and monitoring setup
