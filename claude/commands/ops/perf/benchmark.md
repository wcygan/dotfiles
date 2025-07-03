Perform comprehensive performance analysis and optimization for $ARGUMENTS across multiple dimensions.

Steps:

1. **Baseline Performance Measurement:**

   **Language-Specific Benchmarking:**
   ```bash
   # Rust
   if [ -f "Cargo.toml" ]; then
     cargo bench --bench '*'
     cargo build --release
     hyperfine --warmup 3 './target/release/app'
   fi

   # Go
   if [ -f "go.mod" ]; then
     go test -bench=. -benchmem ./...
     go build -o app .
     hyperfine --warmup 3 './app'
   fi

   # Java
   if [ -f "pom.xml" ]; then
     ./mvnw clean compile jmh:run || echo "Add JMH dependency for microbenchmarks"
     java -jar target/*.jar &
     sleep 5 && hyperfine --warmup 3 'curl http://localhost:8080/health'
   fi

   # Deno
   if [ -f "deno.json" ]; then
     deno bench **/*bench*.ts
     deno task build && hyperfine --warmup 3 'deno task start'
   fi
   ```

   **System Resource Monitoring:**
   ```bash
   # CPU and memory profiling during execution
   hyperfine --export-json baseline.json \
     --prepare 'sleep 1' \
     --parameter-list input '1000,10000,100000' \
     './app --input {input}'

   # Memory usage analysis
   valgrind --tool=massif ./app 2>/dev/null || echo "Valgrind not available"
   /usr/bin/time -v ./app 2>&1 | grep -E "Maximum resident|User time|System time"
   ```

2. **Application-Level Benchmarks:**

   **HTTP API Performance:**
   ```bash
   # Start application in background
   ./app &
   APP_PID=$!
   sleep 5

   # Load testing with different patterns
   # Simple load test
   wrk -t4 -c100 -d30s http://localhost:8080/api/health

   # Ramp-up test
   for conns in 10 50 100 200 500; do
     echo "Testing with $conns connections"
     wrk -t4 -c$conns -d10s http://localhost:8080/api/endpoint
   done

   # Complex scenarios with payload
   wrk -t4 -c100 -d30s -s post.lua http://localhost:8080/api/data

   kill $APP_PID
   ```

   **Database Performance:**
   ```bash
   # Connection pool analysis
   echo "Testing database performance..."

   # Query performance with different pool sizes
   for pool_size in 5 10 20 50; do
     echo "Pool size: $pool_size"
     DATABASE_POOL_SIZE=$pool_size ./app benchmark-db
   done

   # Bulk operation benchmarks
   ./app benchmark-insert --count 10000
   ./app benchmark-select --count 10000
   ./app benchmark-update --count 10000
   ```

3. **Profiling and Hotspot Analysis:**

   **CPU Profiling:**
   ```bash
   # Rust
   if [ -f "Cargo.toml" ]; then
     # Install flamegraph tools
     cargo install flamegraph
     sudo cargo flamegraph --bench bench_name
     
     # perf-based profiling
     perf record --call-graph=dwarf ./target/release/app
     perf report
   fi

   # Go
   if [ -f "go.mod" ]; then
     # Built-in pprof
     go tool pprof http://localhost:8080/debug/pprof/profile?seconds=30
     go tool pprof http://localhost:8080/debug/pprof/heap
     
     # CPU profile during execution
     ./app -cpuprofile=cpu.prof
     go tool pprof cpu.prof
   fi

   # Java
   if [ -f "pom.xml" ]; then
     # JProfiler or async-profiler
     java -jar async-profiler.jar -d 30 -e cpu -f profile.html $(pgrep java)
     
     # JVM built-in tools
     jstack $(pgrep java) > thread_dump.txt
     jmap -dump:format=b,file=heap.hprof $(pgrep java)
   fi
   ```

   **Memory Profiling:**
   ```bash
   # Rust memory usage
   if command -v heaptrack &> /dev/null; then
     heaptrack ./target/release/app
     heaptrack_gui heaptrack.app.*.zst
   fi

   # Go memory analysis
   if [ -f "go.mod" ]; then
     go tool pprof http://localhost:8080/debug/pprof/allocs
     go tool pprof http://localhost:8080/debug/pprof/heap
   fi

   # General memory monitoring
   ps aux | grep app | awk '{print $6}' # RSS memory
   cat /proc/$(pgrep app)/status | grep VmRSS
   ```

4. **Performance Regression Detection:**

   **Historical Comparison:**
   ```bash
   # Store current benchmark results
   mkdir -p benchmarks/$(date +%Y-%m-%d)

   # Run benchmarks and store results
   hyperfine --export-json "benchmarks/$(date +%Y-%m-%d)/hyperfine.json" \
     --warmup 3 './app --benchmark'

   # Compare with previous results
   if [ -f "benchmarks/baseline/hyperfine.json" ]; then
     echo "Comparing with baseline..."
     jq -r '.results[0].mean' "benchmarks/$(date +%Y-%m-%d)/hyperfine.json"
     jq -r '.results[0].mean' "benchmarks/baseline/hyperfine.json"
   fi
   ```

   **Continuous Benchmarking Setup:**
   ```bash
   # Create benchmark tracking script
   cat > scripts/track-performance.ts << 'EOF'
   #!/usr/bin/env -S deno run --allow-all

   import { $ } from "jsr:@david/dax@0.42.0";

   interface BenchmarkResult {
     timestamp: string;
     version: string;
     metrics: {
       throughput: number;
       latency: number;
       memory: number;
     };
   }

   const results: BenchmarkResult[] = [];

   // Run benchmarks and collect metrics
   const version = await $`git rev-parse --short HEAD`.text();
   const timestamp = new Date().toISOString();

   console.log(`Running benchmarks for ${version}...`);

   // Add benchmark execution logic here
   const metrics = {
     throughput: 1000, // requests/second
     latency: 50,      // milliseconds
     memory: 128       // MB
   };

   results.push({ timestamp, version, metrics });

   // Store results
   await Deno.writeTextFile(
     `benchmarks/${timestamp.split('T')[0]}/results.json`,
     JSON.stringify(results, null, 2)
   );
   EOF

   chmod +x scripts/track-performance.ts
   ```

5. **Optimization Implementation:**

   **Algorithm Optimization:**
   ```bash
   # Profile algorithmic complexity
   echo "Testing algorithmic performance..."

   for size in 100 1000 10000 100000; do
     echo "Input size: $size"
     time ./app --algorithm-test --size $size
   done

   # Compare different algorithms
   ./app --compare-algorithms --iterations 1000
   ```

   **Concurrency Optimization:**
   ```bash
   # Test different concurrency levels
   for threads in 1 2 4 8 16; do
     echo "Testing with $threads threads"
     THREAD_COUNT=$threads ./app --benchmark-concurrent
   done

   # Async vs sync performance
   ./app --benchmark-sync
   ./app --benchmark-async
   ```

   **Memory Optimization:**
   ```bash
   # Test different allocation strategies
   ./app --benchmark-allocation-strategy=pool
   ./app --benchmark-allocation-strategy=arena
   ./app --benchmark-allocation-strategy=default

   # Cache performance testing
   for cache_size in 1MB 10MB 100MB 1GB; do
     echo "Cache size: $cache_size"
     CACHE_SIZE=$cache_size ./app --benchmark-cache
   done
   ```

6. **Infrastructure Benchmarks:**

   **Database Performance:**
   ```bash
   # PostgreSQL tuning
   echo "Testing database configurations..."

   # Connection pooling
   for pool in 5 10 20 50 100; do
     echo "Pool size: $pool"
     DATABASE_POOL_SIZE=$pool ./app --db-benchmark
   done

   # Query optimization
   psql -d appdb -c "EXPLAIN ANALYZE SELECT * FROM table WHERE condition;"

   # Index performance
   ./app --benchmark-queries --with-indexes
   ./app --benchmark-queries --without-indexes
   ```

   **Network Performance:**
   ```bash
   # Network latency impact
   tc qdisc add dev lo root netem delay 10ms  # Add artificial latency
   ./app --network-benchmark
   tc qdisc del dev lo root  # Remove latency

   # Compression impact
   ./app --benchmark-compression=none
   ./app --benchmark-compression=gzip
   ./app --benchmark-compression=brotli
   ```

   **Caching Performance:**
   ```bash
   # DragonflyDB vs no cache
   echo "Testing cache performance..."
   ./app --benchmark-no-cache
   ./app --benchmark-with-cache

   # Cache hit ratio analysis
   dragonfly-cli --latency-history
   ```

7. **Load Testing Scenarios:**

   **Realistic User Patterns:**
   ```bash
   # Create load testing scenarios
   cat > load-test-scenarios.js << 'EOF'
   import http from 'k6/http';
   import { check, sleep } from 'k6';

   export let options = {
     stages: [
       { duration: '2m', target: 10 },   // Ramp-up
       { duration: '5m', target: 100 },  // Stay at 100 users
       { duration: '2m', target: 200 },  // Ramp to 200 users
       { duration: '5m', target: 200 },  // Stay at 200 users
       { duration: '2m', target: 0 },    // Ramp-down
     ],
   };

   export default function() {
     // Typical user journey
     let response = http.get('http://localhost:8080/api/data');
     check(response, { 'status is 200': (r) => r.status === 200 });
     sleep(1);
     
     response = http.post('http://localhost:8080/api/process', 
       JSON.stringify({data: 'test'}),
       { headers: { 'Content-Type': 'application/json' } }
     );
     check(response, { 'status is 200': (r) => r.status === 200 });
     sleep(2);
   }
   EOF

   # Run load test
   k6 run load-test-scenarios.js
   ```

   **Chaos Engineering:**
   ```bash
   # Network partitions
   iptables -A INPUT -s localhost -j DROP  # Simulate network issues
   ./app --chaos-test
   iptables -D INPUT -s localhost -j DROP  # Restore network

   # Resource exhaustion
   stress --cpu 8 --timeout 60s &  # CPU stress
   ./app --performance-under-stress
   ```

8. **Performance Monitoring Setup:**

   **Metrics Collection:**
   ```bash
   # Prometheus metrics setup
   cat > prometheus.yml << 'EOF'
   global:
     scrape_interval: 15s

   scrape_configs:
     - job_name: 'app'
       static_configs:
         - targets: ['localhost:9090']
   EOF

   # Grafana dashboard config
   echo "Set up Grafana dashboards for:"
   echo "- Request latency (p50, p95, p99)"
   echo "- Throughput (requests/second)"
   echo "- Error rate"
   echo "- Resource utilization (CPU, memory)"
   ```

   **Alerting Setup:**
   ```yaml
   # alerting-rules.yml
   groups:
     - name: performance
       rules:
         - alert: HighLatency
           expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.5
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "High latency detected"

         - alert: LowThroughput
           expr: rate(http_requests_total[5m]) < 10
           for: 5m
           labels:
             severity: warning
           annotations:
             summary: "Low throughput detected"
   ```

9. **Optimization Recommendations:**

   **Performance Tuning Guide:**
   ```markdown
   # Performance Optimization Results

   ## Baseline Metrics

   - Throughput: X requests/second
   - P95 Latency: X milliseconds
   - Memory Usage: X MB
   - CPU Usage: X%

   ## Optimization Opportunities

   1. **Algorithm Improvements**
      - Replace O(n²) with O(n log n) algorithm
      - Implement caching for expensive computations

   2. **Concurrency Optimizations**
      - Increase thread pool size to X
      - Implement connection pooling

   3. **Memory Optimizations**
      - Reduce allocations in hot path
      - Implement object pooling

   4. **Infrastructure Tuning**
      - Database connection pool: X connections
      - Cache size: X MB
      - JVM heap: X GB (if Java)
   ```

10. **Automated Performance Testing:**
    ```bash
    # CI/CD integration script
    cat > .github/workflows/performance.yml << 'EOF'
    name: Performance Tests

    on:
      pull_request:
        branches: [main]

    jobs:
      benchmark:
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v4
        
        - name: Run benchmarks
          run: |
            ./scripts/run-benchmarks.sh
            
        - name: Compare with baseline
          run: |
            ./scripts/compare-performance.sh
            
        - name: Comment PR with results
          uses: actions/github-script@v6
          with:
            script: |
              // Post performance results to PR
    EOF
    ```

**Output Deliverables:**

- Comprehensive performance analysis report
- Baseline metrics and historical trends
- Profiling results with hotspot identification
- Load testing results under various scenarios
- Optimization recommendations with impact estimates
- Performance monitoring and alerting setup
- Automated performance testing pipeline
- Performance regression detection system

**Key Performance Indicators:**

- Throughput (requests/second, transactions/second)
- Latency percentiles (P50, P95, P99)
- Resource utilization (CPU, memory, network, disk)
- Error rates under load
- Scalability characteristics
- Performance degradation thresholds

**Follow-up Actions:**

- Implement top-priority optimizations
- Set up continuous performance monitoring
- Establish performance budgets and SLAs
- Schedule regular performance reviews
- Create performance testing guidelines for new features
