# /context-load-go-web

Load comprehensive documentation context for Go web development frameworks and HTTP patterns.

## Instructions for Claude

When this command is executed, you MUST:

1. **Use the Context7 MCP server** (if available) to fetch and load context from the URLs below
2. **Use WebFetch tool** to gather information from these key sources:
   - **Chi Router**: `https://github.com/go-chi/chi`
     - Focus on: routing, middleware, sub-routers, URL parameters
   - **Gin Framework**: `https://gin-gonic.com/docs/`
     - Focus on: routing, middleware, JSON binding, rendering
   - **Fiber Framework**: `https://docs.gofiber.io/`
     - Focus on: routing, middleware, context handling, performance
   - **Go HTTP Package**: `https://pkg.go.dev/net/http`
     - Focus on: handlers, middleware, client, server configuration
   - **Gorilla Mux**: `https://github.com/gorilla/mux`
     - Focus on: advanced routing, middleware, testing

3. **Key documentation sections to prioritize**:
   - HTTP routing patterns
   - Middleware implementation
   - Request/response handling
   - JSON processing and validation
   - Error handling strategies
   - Testing HTTP handlers

4. **Focus areas for this stack**:
   - RESTful API design
   - Middleware chains
   - Request context handling
   - JSON marshaling/unmarshaling
   - Error handling and status codes
   - HTTP client usage
   - Testing web applications
   - Performance optimization

## Expected Outcome

After loading this context, you should be able to provide expert guidance on:

- Building REST APIs with Go
- Implementing custom middleware
- Handling HTTP requests and responses
- JSON API development patterns
- Error handling in web applications
- HTTP client best practices
- Testing web services
- Performance optimization techniques

## Usage Example

```
/context-load-go-web
```
