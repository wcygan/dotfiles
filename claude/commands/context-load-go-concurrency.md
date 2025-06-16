# /context-load-go-concurrency

Load comprehensive documentation context for Go concurrency patterns with goroutines and channels.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Go by Example - Concurrency**: `https://gobyexample.com/`
     - Focus on: goroutines, channels, select, worker pools, rate limiting
   - **Effective Go**: `https://go.dev/doc/effective_go`
     - Focus on: concurrency section, channels, goroutines best practices
   - **Go Blog - Concurrency**: `https://go.dev/blog/`
     - Focus on: concurrency patterns, pipelines, cancellation
   - **Go Concurrency Patterns**: `https://go.dev/talks/2012/concurrency.slide`
     - Focus on: advanced patterns, select statement, cancellation
   - **Sync Package**: `https://pkg.go.dev/sync`
     - Focus on: mutexes, wait groups, atomic operations, once

3. **Key documentation sections to prioritize**:
   - Goroutine lifecycle and management
   - Channel types and operations
   - Select statement patterns
   - Synchronization primitives
   - Context package for cancellation
   - Common concurrency patterns

4. **Focus areas for this stack**:
   - Goroutine spawning and management
   - Channel communication patterns
   - Select statement for multiplexing
   - Worker pool implementations
   - Pipeline patterns
   - Context-based cancellation
   - Race condition prevention
   - Performance considerations

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Designing concurrent Go programs
- Using channels effectively
- Implementing worker pools
- Building pipeline architectures
- Handling cancellation and timeouts
- Avoiding race conditions
- Performance tuning concurrent code
- Testing concurrent applications

## Usage Example

```
/context-load-go-concurrency
```
