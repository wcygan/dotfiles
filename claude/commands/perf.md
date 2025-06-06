Analyze and optimize performance for $ARGUMENTS.

Steps:
1. Profile current performance:
   - Measure execution time of key operations
   - Identify memory usage patterns
   - Check for CPU-intensive operations
   - Monitor I/O operations (disk, network)
   - Use appropriate profiling tools for the language

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
   - Check for missing indexes
   - Optimize JOIN operations
   - Use query explanation plans
   - Consider caching frequently accessed data

5. Async/Parallel processing:
   - Identify blocking operations that can be async
   - Find independent operations for parallelization
   - Use Promise.all() for concurrent operations
   - Consider worker threads/processes for CPU-intensive tasks
   - Implement proper batching strategies

6. Caching strategies:
   - Identify cacheable computations
   - Implement appropriate cache invalidation
   - Use memoization for pure functions
   - Consider Redis/in-memory caching for hot data
   - Set proper TTLs

7. Resource optimization:
   - Lazy loading for large datasets
   - Pagination for list operations
   - Streaming for large file operations
   - Connection pooling for databases
   - Proper resource cleanup

Output:
- Performance bottlenecks ranked by impact
- Specific optimization recommendations
- Before/after performance metrics
- Implementation plan with effort estimates