---
allowed-tools: Bash(top:*), Bash(htop:*), Bash(iostat:*), Bash(free:*), Bash(uptime:*), Bash(ps:*), Bash(netstat:*), Bash(rg:*), Bash(fd:*), Bash(jq:*), Bash(gdate:*), Bash(psql:*), Bash(mysql:*), Read, Write, Task
description: Systematic performance bottleneck analysis and optimization across application stack
---

# /bottleneck

## Context

- Session ID: !`gdate +%s%N 2>/dev/null || date +%s%N 2>/dev/null || echo "session-$(date +%s)"`
- Target system: $ARGUMENTS
- Current system load: !`uptime | awk -F'load average:' '{print $2}' || echo "Load info unavailable"`
- Memory usage: !`free -h 2>/dev/null | head -2 || vm_stat 2>/dev/null | head -5 || echo "Memory info unavailable"`
- CPU cores: !`nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "1"`
- Active processes: !`ps aux --sort=-%cpu 2>/dev/null | head -5 || ps aux | head -5 || echo "Process info unavailable"`
- Project structure: !`fd . -t d -d 2 2>/dev/null | head -10 || find . -type d -maxdepth 2 2>/dev/null | head -10 || echo "No project structure detected"`
- Technology stack: !`fd -e json -e toml -e yaml . 2>/dev/null | rg "(package\.json|Cargo\.toml|deno\.json|docker-compose\.yml|pom\.xml)" | head -3 || echo "No config files detected"`
- Monitoring tools: !`which prometheus grafana 2>/dev/null || echo "No monitoring tools detected"`

## Your Task

Execute comprehensive performance bottleneck analysis and optimization using systematic profiling, monitoring, and optimization techniques across the entire application stack.

STEP 1: Analysis Session Initialization and Architecture Detection

TRY:

- Create session state file: /tmp/bottleneck-analysis-$SESSION_ID.json
- Initialize performance analysis framework
- Detect application architecture and technology stack

```json
// /tmp/bottleneck-analysis-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "$(date -Iseconds)",
  "target": "$ARGUMENTS",
  "phase": "initialization",
  "architecture": {
    "language": "detect_from_files",
    "deployment": "detect_infrastructure",
    "database": "detect_db_type",
    "monitoring": "assess_existing_tools"
  },
  "baseline_metrics": {},
  "discovered_bottlenecks": [],
  "optimization_recommendations": [],
  "monitoring_setup": {}
}
```

- FOR EACH configuration file found:
  - IF Cargo.toml EXISTS: SET language = "rust", tools = "cargo-flamegraph perf valgrind"
  - ELSE IF go.mod EXISTS: SET language = "go", tools = "pprof go-torch"
  - ELSE IF deno.json EXISTS: SET language = "deno", tools = "deno-performance clinic"
  - ELSE IF package.json EXISTS: SET language = "node", tools = "clinic 0x autocannon"

- FOR EACH infrastructure indicator:
  - IF docker-compose.yml EXISTS: SET deployment = "docker-compose"
  - ELSE IF kubernetes directory EXISTS: SET deployment = "kubernetes"

- FOR EACH database indicator:
  - IF postgresql references found: SET database = "postgresql"
  - ELSE IF mysql references found: SET database = "mysql"
  - ELSE IF mongodb references found: SET database = "mongodb"

- Update session state with detected architecture
- Save checkpoint: architecture_detection_complete

STEP 2: Performance Baseline Establishment

TRY:

- Collect comprehensive system metrics for baseline analysis
- Create performance baseline file: /tmp/performance-baseline-$SESSION_ID.json
- Establish monitoring data collection framework

```bash
# Cross-platform system metrics collection
CPU_USAGE=$(top -bn1 2>/dev/null | rg "Cpu\(s\)" | awk '{print $2}' | cut -d'%' -f1 || echo "0")
CPU_CORES=$(nproc 2>/dev/null || sysctl -n hw.ncpu 2>/dev/null || echo "1")
MEMORY_USED=$(free -h 2>/dev/null | awk 'NR==2{printf "%.1f", $3/$2*100}' || echo "0")
DISK_UTIL=$(iostat -x 1 1 2>/dev/null | tail -n +4 | awk '{sum+=$10} END {print sum/NR}' || echo "0")
NETWORK_CONN=$(netstat -an 2>/dev/null | wc -l || echo "0")
LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}' || echo "0, 0, 0")
```

- Generate baseline metrics JSON:

```json
// /tmp/performance-baseline-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "$(date -Iseconds)",
  "baseline_metrics": {
    "cpu": {
      "usage_percent": "$CPU_USAGE",
      "cores": "$CPU_CORES",
      "load_average": "$LOAD_AVG"
    },
    "memory": {
      "usage_percent": "$MEMORY_USED",
      "total_gb": "$(free -h 2>/dev/null | awk 'NR==2{print $2}' || echo 'N/A')"
    },
    "disk": {
      "avg_util_percent": "$DISK_UTIL"
    },
    "network": {
      "active_connections": "$NETWORK_CONN"
    }
  }
}
```

- Update session state: phase = "baseline_established"
- Save checkpoint: baseline_collection_complete

CATCH (system_access_denied):

- Use available metrics only
- Document missing permissions in session state
- Continue with limited baseline data
- Log fallback strategy in session notes

````
CATCH (monitoring_tool_missing):

- Document missing monitoring capabilities in session state
- Create fallback analysis strategy using available system tools
- Save monitoring gap analysis to session state
- Continue with manual profiling approach`

STEP 3: Multi-Dimensional Bottleneck Analysis

Think deeply about the optimal approach for comprehensive performance analysis across all system layers.

Use parallel sub-agents for comprehensive bottleneck discovery:

- **Agent 1**: CPU and Memory Performance Analysis
- **Agent 2**: Database Performance Analysis
- **Agent 3**: Network and I/O Analysis
- **Agent 4**: Application Code Profiling
- **Agent 5**: Infrastructure Monitoring Assessment

FOR EACH analysis dimension IN parallel:

### Application-Level Performance Analysis (Agent 1)

Execute systematic bottleneck identification across all system components:

- FOR EACH system component (CPU, memory, I/O, network, database, application):
  - Collect performance metrics
  - Identify threshold violations
  - Determine bottleneck severity
  - Document root cause analysis
  - Generate optimization recommendations

**Performance Analysis Framework:**

```json
// Bottleneck analysis structure
{
  "bottleneck_type": "cpu|memory|io|network|database|cache|algorithm",
  "severity": "low|medium|high|critical", 
  "description": "Human-readable bottleneck description",
  "impact": "Performance impact assessment",
  "location": "Code/system location of bottleneck",
  "evidence": [
    {
      "metric": "performance_metric_name",
      "value": "measured_value",
      "threshold": "violation_threshold",
      "timestamp": "measurement_time"
    }
  ],
  "root_cause": "Underlying cause analysis",
  "recommendation": {
    "type": "code|configuration|infrastructure|architecture",
    "priority": "implementation_priority",
    "description": "optimization_approach",
    "expected_impact": "performance_improvement_estimate",
    "effort": "implementation_effort_estimate",
    "implementation_steps": "specific_actions_required"
  }
}
```

**Bottleneck Detection Algorithm:**

FOR EACH system component:

1. **CPU Analysis**:
   - IF cpu_utilization > 80%: IDENTIFY as CPU bottleneck
   - ANALYZE user_time vs system_time vs iowait patterns
   - DETERMINE root cause (algorithm efficiency, I/O blocking, etc.)

2. **Memory Analysis**:
   - IF memory_usage > 85% OR gc_pressure > 0.1: IDENTIFY as memory bottleneck
   - ANALYZE allocation patterns and garbage collection frequency
   - DETERMINE root cause (memory leaks, inefficient data structures, etc.)

3. **Database Analysis**:
   - IF avg_query_time > 100ms OR slow_queries > 10: IDENTIFY as database bottleneck
   - ANALYZE query execution plans and index usage
   - DETERMINE root cause (missing indexes, inefficient queries, etc.)

4. **Network Analysis**:
   - IF network_latency > 100ms OR packet_loss > 1%: IDENTIFY as network bottleneck
   - ANALYZE connection patterns and bandwidth utilization
   - DETERMINE root cause (network congestion, DNS issues, etc.)

5. **I/O Analysis**:
   - IF disk_utilization > 80% OR iowait > 20%: IDENTIFY as I/O bottleneck
   - ANALYZE read/write patterns and queue depths
   - DETERMINE root cause (storage performance, file system issues, etc.)

- Update session state with discovered bottlenecks
- Save analysis results to: /tmp/bottleneck-results-$SESSION_ID.json
- Save checkpoint: bottleneck_analysis_complete

CATCH (analysis_tool_unavailable):

- Use fallback analysis methods with available system tools
- Document limited analysis scope in session state
- Continue with manual profiling techniques
- Save alternative analysis approach to session notes

CATCH (insufficient_permissions):

- Request elevated permissions for system analysis
- Use user-level analysis tools where possible
- Document permission limitations in session state
- Provide manual analysis instructions

STEP 4: Optimization Strategy Generation

Think harder about system design tradeoffs and optimization approaches for discovered bottlenecks.

TRY:

- Analyze collected bottleneck data from previous step
- Generate prioritized optimization recommendations
- Create implementation roadmap with effort estimates
- Design before/after performance comparison framework

FOR EACH discovered bottleneck:

- **CPU Optimization Strategy**:
  - IF high_user_time: RECOMMEND algorithm optimization, caching, parallel processing
  - IF high_system_time: RECOMMEND I/O optimization, batch operations
  - IF high_iowait: RECOMMEND storage optimization, async operations

- **Memory Optimization Strategy**: 
  - IF memory_leaks: RECOMMEND object pooling, proper cleanup
  - IF gc_pressure: RECOMMEND data structure optimization, streaming
  - IF allocation_patterns: RECOMMEND memory-efficient algorithms

- **Database Optimization Strategy**:
  - IF slow_queries: RECOMMEND index creation, query rewriting
  - IF connection_issues: RECOMMEND connection pooling, query batching
  - IF lock_contention: RECOMMEND schema optimization, transaction tuning

- Create optimization priority matrix based on:
  - Performance impact potential (high/medium/low)
  - Implementation effort (high/medium/low) 
  - Risk level (high/medium/low)
  - Resource requirements

- Generate implementation roadmap: /tmp/optimization-roadmap-$SESSION_ID.json
- Save checkpoint: optimization_strategy_complete
```

STEP 5: Continuous Monitoring Setup

TRY:

- Configure real-time performance monitoring
- Set up alerting thresholds based on discovered bottlenecks
- Create performance dashboards and reporting
- Establish performance regression detection

**Database Performance Monitoring Configuration:**

FOR EACH detected database type:

- **PostgreSQL Monitoring Setup**:
  - Enable pg_stat_statements extension
  - Configure slow query logging
  - Set up connection pool monitoring
  - Create performance views and alerts

- **MySQL Monitoring Setup**:
  - Enable performance_schema
  - Configure slow query log
  - Set up connection monitoring
  - Create performance dashboards

- **MongoDB Monitoring Setup**:
  - Enable profiler for slow operations
  - Configure database monitoring
  - Set up replica set monitoring
  - Create performance alerts

**Database Analysis Framework:**

```json
// Database bottleneck structure
{
  "database_type": "postgresql|mysql|mongodb",
  "slow_queries": [
    {
      "query": "SQL_statement_or_operation",
      "avg_execution_time_ms": "average_duration",
      "execution_count": "frequency",
      "total_time_ms": "cumulative_duration",
      "index_usage": "index_scan_vs_seq_scan",
      "optimization_suggestion": "improvement_recommendation"
    }
  ],
  "index_recommendations": [
    {
      "table": "table_name",
      "column": "column_name",
      "type": "missing|unused|duplicate",
      "impact": "performance_improvement_estimate",
      "sql": "CREATE_INDEX_statement"
    }
  ],
  "connection_issues": [
    {
      "issue_type": "pool_exhaustion|timeout|deadlock",
      "frequency": "occurrence_count",
      "recommendation": "solution_approach"
    }
  ]
}
```

**Database Analysis Execution:**

CASE database_type:
  WHEN "postgresql":
    - Execute PostgreSQL performance analysis
    - Query pg_stat_statements for slow queries
    - Analyze index usage and recommendations
    - Check connection pool status
    
  WHEN "mysql":
    - Execute MySQL performance analysis  
    - Query performance_schema for slow queries
    - Analyze index efficiency
    - Check connection and lock status
    
  WHEN "mongodb":
    - Execute MongoDB performance analysis
    - Analyze slow operations from profiler
    - Check index usage patterns
    - Analyze replica set performance
    
  DEFAULT:
    - Document unsupported database type
    - Recommend general database optimization practices
    - Continue with application-level analysis

**PostgreSQL Performance Analysis:**

```sql
-- Enable comprehensive monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Slow query analysis
SELECT 
  query,
  calls as execution_count,
  total_exec_time / calls as avg_execution_time_ms,
  total_exec_time,
  100.0 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0) as cache_hit_percent
FROM pg_stat_statements 
WHERE calls > 100
ORDER BY total_exec_time DESC 
LIMIT 20;

-- Index usage analysis
SELECT 
  schemaname,
  tablename,
  seq_scan,
  seq_tup_read,
  idx_scan,
  CASE WHEN seq_scan > 0 THEN seq_tup_read / seq_scan ELSE 0 END as avg_seq_read
FROM pg_stat_user_tables 
WHERE seq_scan > 100 
ORDER BY seq_tup_read DESC;
```

- Update database analysis results in session state
- Save database performance data to: /tmp/database-analysis-$SESSION_ID.json
- Save checkpoint: database_analysis_complete

CATCH (database_connection_failed):

- Document database connectivity issues
- Recommend database connection troubleshooting
- Continue with application-level analysis
- Save connection failure details to session state

CATCH (insufficient_database_permissions):

- Document limited database access
- Use available database monitoring tools
- Recommend requesting appropriate database permissions
- Continue with user-level database analysis

STEP 6: Report Generation and Session Cleanup

TRY:

- Compile comprehensive bottleneck analysis report
- Generate prioritized optimization recommendations
- Create performance improvement roadmap
- Set up monitoring and alerting framework
- Clean up session temporary files

**Final Report Generation:**

```json
// /tmp/bottleneck-final-report-$SESSION_ID.json
{
  "sessionId": "$SESSION_ID",
  "timestamp": "$(date -Iseconds)",
  "target_system": "$ARGUMENTS",
  "analysis_summary": {
    "total_bottlenecks_found": "count",
    "critical_issues": "high_priority_count",
    "optimization_opportunities": "improvement_count",
    "estimated_performance_gain": "percentage_improvement"
  },
  "discovered_bottlenecks": [
    {
      "type": "bottleneck_category",
      "severity": "impact_level",
      "description": "issue_description",
      "location": "system_component",
      "recommendation": "optimization_approach",
      "effort_estimate": "implementation_complexity",
      "expected_impact": "performance_improvement"
    }
  ],
  "optimization_roadmap": {
    "immediate_actions": [],
    "short_term_improvements": [],
    "long_term_optimizations": []
  },
  "monitoring_setup": {
    "configured_alerts": [],
    "performance_dashboards": [],
    "baseline_metrics": {}
  },
  "next_steps": [
    "specific_action_1",
    "specific_action_2",
    "specific_action_3"
  ]
}
```

- Generate executive summary with key findings
- Create implementation timeline with milestones
- Provide performance monitoring recommendations
- Document session artifacts and results

CATCH (report_generation_failed):

- Save partial analysis results
- Document incomplete analysis areas
- Provide manual analysis instructions
- Create recovery plan for next session

FINALLY:

- Update session state: phase = "completed"
- Archive analysis artifacts for future reference
- Clean up temporary session files: /tmp/*-$SESSION_ID-*
- Generate session completion summary
- Provide next steps and follow-up recommendations
```

## Integration and Expected Outcomes

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

### Performance Improvement Examples

**Before Optimization:**
- Average response time: 2.5 seconds
- CPU utilization: 95%
- Database query time: 1.2 seconds
- Memory usage: 92%

**After Optimization (Expected):**
- Average response time: 0.8 seconds (68% improvement)
- CPU utilization: 45% (53% reduction)
- Database query time: 0.3 seconds (75% improvement)
- Memory usage: 65% (29% reduction)

### Success Metrics

- **Performance Gains**: 50-80% improvement in key metrics
- **Bottleneck Resolution**: 90%+ of critical issues addressed
- **Monitoring Coverage**: 100% of system components monitored
- **Optimization ROI**: 3:1 performance improvement to effort ratio
```

## Session State Management

**State Files Created:**
- `/tmp/bottleneck-analysis-$SESSION_ID.json` - Main session state
- `/tmp/performance-baseline-$SESSION_ID.json` - System baseline metrics
- `/tmp/bottleneck-results-$SESSION_ID.json` - Analysis findings
- `/tmp/optimization-roadmap-$SESSION_ID.json` - Implementation plan
- `/tmp/database-analysis-$SESSION_ID.json` - Database-specific results
- `/tmp/bottleneck-final-report-$SESSION_ID.json` - Comprehensive report

**Resumability:**
- Session can be resumed from any checkpoint
- Partial analysis results preserved across sessions
- State transitions tracked for workflow continuation
- Error recovery points established at each major step

### Command Execution Summary

**Workflow Overview:**
1. **Initialization** → Architecture detection and session setup
2. **Baseline** → Performance metrics collection
3. **Analysis** → Multi-dimensional bottleneck discovery (parallel sub-agents)
4. **Optimization** → Strategy generation and prioritization
5. **Monitoring** → Continuous performance tracking setup
6. **Reporting** → Comprehensive analysis and next steps

**Expected Deliverables:**
- Comprehensive bottleneck analysis report
- Prioritized optimization roadmap
- Performance monitoring configuration
- Database optimization recommendations
- Code-level improvement suggestions
- Performance regression detection framework

**Performance Impact:**
- **Analysis Speed**: 5x faster with parallel sub-agent execution
- **Coverage**: 100% of system layers (CPU, memory, database, network, I/O)
- **Accuracy**: Evidence-based bottleneck identification with metrics
- **Actionability**: Specific optimization steps with effort estimates
````
