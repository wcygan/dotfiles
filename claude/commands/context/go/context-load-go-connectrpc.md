# /context-load-go-connectrpc

Load comprehensive documentation context for Go ConnectRPC development.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **ConnectRPC**: `https://connectrpc.com/docs/`
     - Focus on: protocol definition, code generation, streaming, interceptors
   - **Buf Schema Registry**: `https://buf.build/docs/`
     - Focus on: schema management, code generation, breaking change detection
   - **gRPC-Go**: `https://grpc.io/docs/languages/go/`
     - Focus on: service implementation, client usage, error handling
   - **Protocol Buffers**: `https://protobuf.dev/`
     - Focus on: message definition, field types, best practices
   - **ConnectRPC Examples**: `https://github.com/connectrpc/examples-go`
     - Focus on: practical implementations, patterns

3. **Key documentation sections to prioritize**:
   - Service definition with Protocol Buffers
   - Code generation workflows
   - Server and client implementation
   - Streaming patterns (unary, server, client, bidirectional)
   - Interceptors and middleware
   - Error handling and status codes

4. **Focus areas for this stack**:
   - Protocol Buffer schema design
   - Service implementation patterns
   - Client connection management
   - Streaming RPC patterns
   - Interceptor chains
   - Error handling strategies
   - Testing RPC services
   - Performance optimization

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Designing Protocol Buffer schemas
- Implementing ConnectRPC services
- Building RPC clients
- Handling different streaming patterns
- Implementing custom interceptors
- Error handling and status codes
- Testing RPC applications
- Performance tuning

## Usage Example

```
/context-load-go-connectrpc
```
