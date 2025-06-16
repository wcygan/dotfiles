# /context-load-rust-async

Load comprehensive documentation context for Rust async programming patterns and futures.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Tokio Runtime**: `https://docs.rs/tokio/latest/tokio/`
     - Focus on: runtime, tasks, spawn, join handles, select macro
   - **Futures Crate**: `https://docs.rs/futures/latest/futures/`
     - Focus on: Future trait, Stream trait, combinators, utilities
   - **Async-std**: `https://docs.rs/async-std/latest/async_std/`
     - Focus on: async filesystem, networking, task spawning
   - **Async Book**: `https://rust-lang.github.io/async-book/`
     - Focus on: async/await syntax, pinning, executors, wake mechanism
   - **Tokio Tutorial**: `https://tokio.rs/tokio/tutorial`
     - Focus on: practical examples, common patterns

3. **Key documentation sections to prioritize**:
   - async/await fundamentals
   - Future and Stream traits
   - Task spawning and management
   - Async channels and synchronization
   - Error handling in async contexts
   - Performance patterns

4. **Focus areas for this stack**:
   - Understanding async/await syntax
   - Future trait implementation
   - Stream processing patterns
   - Async channels (mpsc, oneshot, broadcast)
   - select! macro for concurrent operations
   - Spawning and managing tasks
   - Async error handling
   - Cancellation and timeouts

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Writing efficient async functions
- Understanding Future and Stream traits
- Implementing custom async types
- Task spawning and lifecycle management
- Async synchronization primitives
- Error propagation in async contexts
- Performance optimization for async code
- Debugging async applications

## Usage Example

```
/context-load-rust-async
```
