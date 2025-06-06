Analyze and optimize performance for $ARGUMENTS.

Steps:
1. Profile current performance:
   **Java:**
   - JProfiler, YourKit, or async-profiler
   - JMX metrics and heap dumps
   - GC logs analysis
   
   **Go:**
   - pprof for CPU and memory profiling
   - trace tool for execution tracing
   - benchstat for benchmark comparison
   
   **Rust:**
   - cargo flamegraph
   - perf profiling
   - valgrind for memory analysis
   
   **General:**
   - APM tools (DataDog, New Relic)
   - Distributed tracing (Jaeger, Zipkin)
   - Custom metrics with Prometheus

2. Algorithm analysis:
   - Calculate Big O complexity for loops and recursion
   - Identify O(n²) or worse algorithms
   - Look for unnecessary nested loops
   - Check for redundant calculations
   - Find opportunities for memoization

3. Data structure optimization:
   - Ensure appropriate data structures (Array vs Set vs Map)
   - Check for inefficient lookups (array.includes vs Set.has)
   - Optimize for access patterns (read-heavy vs write-heavy)
   - Consider space-time tradeoffs

4. Database/Query optimization:
   - Identify N+1 query problems
   - Check for missing indexes with EXPLAIN ANALYZE
   - Optimize JOIN operations and query structure
   - **PostgreSQL**: pg_stat_statements, auto_explain
   - **MySQL**: slow query log, performance schema
   - Connection pooling optimization (HikariCP, pgbouncer)
   - Consider read replicas for scaling
   - Implement query result caching

5. Async/Parallel processing:
   **Java:**
   - CompletableFuture for async operations
   - Parallel streams and ForkJoinPool
   - Virtual threads (Java 21+)
   - Reactive frameworks (Project Reactor, RxJava)
   
   **Go:**
   - Goroutines and channels
   - sync.WaitGroup for coordination
   - Worker pool patterns
   - Context for cancellation
   
   **Rust:**
   - Tokio/async-std for async runtime
   - Rayon for data parallelism
   - Crossbeam for concurrent data structures
   
   - Implement proper batching and backpressure

6. Caching strategies:
   - **Application-level**: Caffeine (Java), groupcache (Go), moka (Rust)
   - **Distributed**: Redis/DragonflyDB, Hazelcast
   - **HTTP caching**: ETags, Cache-Control headers
   - **Database query caching**: Prepared statements
   - Cache warming strategies
   - Cache-aside vs write-through patterns
   - Proper TTLs and invalidation strategies

7. Resource optimization:
   - Lazy loading for large datasets
   - Pagination for list operations
   - Streaming for large file operations
   - Connection pooling for databases
   - Proper resource cleanup

Output:
- Performance bottlenecks ranked by impact
- Specific optimization recommendations with code examples
- Before/after performance metrics:
  - Latency percentiles (p50, p95, p99)
  - Throughput (requests/second)
  - Resource utilization (CPU, memory, I/O)
- Implementation plan with effort estimates
- Load testing scripts (k6, Gatling, wrk)
- Monitoring dashboard setup recommendations