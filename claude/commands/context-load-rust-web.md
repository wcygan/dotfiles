# /context-load-rust-web

Load comprehensive documentation context for Rust web development with Axum, Tokio, and related frameworks.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from:
   - `https://context7.com/api/upload` with the URLs below
   - This will provide the most recent documentation

2. **Use WebFetch tool** to gather information from these key sources:
   - **Axum Framework**: `https://docs.rs/axum/latest/axum/`
     - Focus on: routing, handlers, extractors, middleware, response types
   - **Tokio Runtime**: `https://docs.rs/tokio/latest/tokio/`
     - Focus on: async runtime, tasks, I/O, timers, synchronization
   - **Serde Serialization**: `https://docs.rs/serde/latest/serde/`
     - Focus on: derive macros, JSON handling, custom serializers
   - **SQLx Database**: `https://docs.rs/sqlx/latest/sqlx/`
     - Focus on: async queries, connection pools, migrations, type safety
   - **Tower Services**: `https://docs.rs/tower/latest/tower/`
     - Focus on: middleware, service trait, layers, timeouts
   - **Tracing**: `https://docs.rs/tracing/latest/tracing/`
     - Focus on: structured logging, spans, events, subscribers

3. **Key documentation sections to prioritize**:
   - Getting started guides and examples
   - Common patterns and best practices
   - Error handling strategies
   - Performance considerations
   - Integration examples

4. **Focus areas for this stack**:
   - HTTP server setup with Axum
   - Async request handling patterns
   - JSON API development
   - Database integration with SQLx
   - Middleware implementation
   - Error handling and response types
   - Testing strategies for async code
   - Structured logging with tracing

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building REST APIs with Axum
- Async/await patterns in web services
- Database operations with SQLx
- Middleware and request/response handling
- Error handling and custom error types
- Performance optimization
- Testing async web applications
- Logging and observability setup

## Usage Example

```
/context-load-rust-web
```

This will load all relevant Rust web development documentation into the current chat context for immediate use.
