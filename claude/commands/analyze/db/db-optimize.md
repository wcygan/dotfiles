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

IF PostgreSQL detected:

- Analyze pg_stat_statements for slow queries
- Examine index usage with pg_stat_user_indexes
- Check configuration parameters vs. best practices
- Identify vacuum and analyze issues

ELSE IF MySQL detected:

- Analyze performance_schema for slow queries
- Check InnoDB buffer pool efficiency
- Examine index usage statistics
- Review configuration variables

ELSE IF MongoDB detected:

- Enable profiling and analyze slow operations
- Examine index usage per collection
- Check connection and memory metrics
- Analyze query execution patterns

ELSE IF SQLite detected:

- Analyze query execution with EXPLAIN QUERY PLAN
- Check for missing indexes
- Examine file size and vacuum status

STEP 3: Risk Assessment and Optimization Planning

- Categorize identified issues by risk level (low/medium/high)
- Prioritize optimizations by impact vs. implementation complexity
- Create rollback procedures for configuration changes
- Generate specific SQL statements for index modifications
- Estimate performance improvement potential

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

- Generate database-specific monitoring queries
- Create alerting thresholds for key performance metrics
- Provide maintenance schedules (vacuum, analyze, etc.)
- Document ongoing optimization procedures

STEP 7: State Management and Cleanup

```json
// /tmp/db-optimize-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "ISO_8601_TIMESTAMP",
  "target": "$ARGUMENTS",
  "discoveredDatabases": ["postgresql", "mysql"],
  "optimizationResults": {
    "indexesCreated": 3,
    "configChanges": 5,
    "performanceImprovement": "45%",
    "riskLevel": "low"
  },
  "recommendations": {
    "immediate": ["Create index on users.email", "Increase shared_buffers"],
    "scheduled": ["VACUUM ANALYZE", "Update table statistics"],
    "monitoring": ["Track slow query log", "Monitor connection usage"]
  },
  "rollbackProcedures": {
    "indexDrops": ["DROP INDEX CONCURRENTLY idx_users_email"],
    "configRollback": "shared_buffers = 128MB"
  }
}
```

FINALLY:

- Clean up temporary analysis files
- Archive optimization session data
- Update project documentation with performance improvements
