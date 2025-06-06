Help debug issue: $ARGUMENTS

Steps:
1. Understand the problem:
   - Parse error messages and stack traces
   - **Java**: Analyze full stack trace, check caused-by chains
   - **Go**: Read panic output, trace goroutine dumps
   - **Rust**: Interpret panic messages and backtraces
   - Locate the exact file and line where error occurs
   - Check logs at INFO/DEBUG/TRACE levels
   - Review monitoring/APM data if available

2. Analyze the code path:
   - Trace execution flow leading to the error
   - Identify all variables and their states
   - Check function/method signatures and calls
   - Review recent changes that might have introduced the bug

3. Suggest debugging strategies:
   **Java:**
   - Remote debugging with JDWP
   - Conditional breakpoints in IDE
   - JVM flags: -XX:+PrintGCDetails, -XX:+HeapDumpOnOutOfMemoryError
   - Thread dumps and heap analysis
   
   **Go:**
   - Delve debugger usage
   - pprof for runtime analysis
   - race detector: go run -race
   - Structured logging with context
   
   **Rust:**
   - RUST_BACKTRACE=full for detailed traces
   - gdb/lldb integration
   - println! debugging with dbg! macro
   - cargo-expand for macro debugging
   
   **General:**
   - Distributed tracing for microservices
   - tcpdump/Wireshark for network issues
   - strace/dtrace for system calls

4. Identify common pitfalls:
   **Java:**
   - NullPointerException causes
   - Concurrency issues (deadlocks, race conditions)
   - Memory leaks and GC pressure
   - ClassLoader problems
   - Resource leaks (connections, files)
   
   **Go:**
   - Nil pointer dereferences
   - Goroutine leaks
   - Channel deadlocks
   - Interface{} type assertions
   - Slice capacity vs length issues
   
   **Rust:**
   - Borrow checker violations
   - Lifetime issues
   - Move semantics confusion
   - Unsafe code problems
   - Panic in production code
   
   **Common:**
   - Race conditions in concurrent code
   - Resource exhaustion
   - Network timeouts and retries
   - Database connection pool exhaustion

5. Create minimal reproduction:
   - Isolate the problem code
   - Remove unnecessary dependencies
   - Create simple test case that reproduces the issue
   - Document steps to reproduce

6. Propose solutions:
   - Provide specific code fixes with examples
   - Defensive programming techniques:
     - **Java**: Optional usage, try-with-resources
     - **Go**: Error wrapping, defer cleanup
     - **Rust**: Result<T,E> handling, match exhaustiveness
   - Add comprehensive error handling
   - Circuit breakers for external services
   - Implement proper timeout handling
   - Add observability (metrics, logs, traces)
   - Include unit tests to prevent regression
   - Consider integration tests for complex issues

Output format:
- Root cause analysis
- Step-by-step debugging plan
- Specific code changes needed
- Test cases to verify the fix
- Prevention strategies:
  - Code review checklist items
  - Static analysis rules to add
  - Monitoring alerts to implement
  - Documentation updates needed