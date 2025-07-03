<!--
name: scaffold-go-http-server
description: Scaffold a production-ready Go HTTP server following best practices
tags: go, http, server, scaffold, production
arguments: [project-name] (optional, defaults to current directory name)
-->

# Scaffold Production-Ready Go HTTP Server

Create a minimal, performant Go HTTP server following industry best practices based on comprehensive research from Grafana and other authoritative sources.

## Task

Scaffold a complete Go HTTP server project with the following structure and features:

**Project Structure:**

```
$ARGUMENTS/
├── main.go                 # Minimal main function with run() pattern
├── server.go              # Server constructor and configuration
├── routes.go              # Centralized route definitions
├── handlers.go            # HTTP handlers with factory pattern
├── middleware.go          # Production middleware (logging, security, etc.)
├── health.go              # Health check implementation
├── go.mod                 # Go module with minimal dependencies
├── go.sum                 # Dependency checksums
├── Dockerfile             # Multi-stage Docker build
├── docker-compose.yml     # Local development setup
├── .gitignore             # Go-specific gitignore
└── README.md              # Quick start documentation
```

**Core Features to Implement:**

1. **Server Constructor Pattern (Grafana Standard):**
   - `NewServer()` function taking dependencies as arguments
   - Returns `http.Handler` for composability
   - No global variables or init() functions

2. **Production Server Configuration:**
   - All essential timeouts configured (ReadTimeout, WriteTimeout, IdleTimeout, ReadHeaderTimeout)
   - Proper HTTP/2 support when using HTTPS
   - Connection pooling optimization

3. **Essential Middleware:**
   - Request logging with structured output
   - Request ID generation and propagation
   - Security headers (HSTS, CSP, X-Frame-Options, etc.)
   - CORS handling
   - Recovery middleware for panic handling

4. **Handler Patterns:**
   - Handler factory functions returning `http.Handler`
   - Explicit dependency injection
   - Proper error handling and JSON responses
   - Input validation

5. **Health Check:**
   - `/healthz` endpoint with JSON response
   - Configurable health checks (database, external services)
   - Graceful degradation during shutdown

6. **Graceful Shutdown:**
   - Signal handling for SIGTERM and SIGINT
   - Context-based shutdown with timeout
   - Proper cleanup of resources

7. **Development Setup:**
   - Docker configuration for local development
   - Environment variable configuration
   - Hot reload setup instructions

**Implementation Requirements:**

- Use ONLY Go standard library (no external frameworks)
- Follow the exact patterns from the Grafana article research
- Include comprehensive error handling
- Add detailed code comments explaining patterns
- Ensure all code is production-ready
- Include example API endpoints (GET /api/items, POST /api/items)
- Configure proper logging with structured output
- Include security best practices

**Environment Configuration:**

- Support for PORT environment variable (default: 8080)
- LOG_LEVEL configuration (debug, info, warn, error)
- SHUTDOWN_TIMEOUT configuration (default: 30s)
- Support for TLS certificate paths

**API Endpoints to Include:**

- `GET /healthz` - Health check
- `GET /metrics` - Basic metrics (request count, uptime)
- `GET /api/v1/items` - Example resource listing
- `POST /api/v1/items` - Example resource creation
- `GET /api/v1/items/{id}` - Example resource retrieval

After scaffolding the project, create comprehensive documentation at `/docs/best-practices.md` with the following complete content that codifies all the research findings and implementation patterns for future reference and maintenance:

---

## Best Practices Documentation Content for `/docs/best-practices.md`:

````markdown
# Go HTTP Server Best Practices

This document codifies production-ready patterns for building minimal, performant HTTP servers in Go using only the standard library. Based on comprehensive research from Grafana, Go core team recommendations, and industry best practices.

## Table of Contents

- [Core Architecture Patterns](#core-architecture-patterns)
- [Production Server Configuration](#production-server-configuration)
- [Middleware Design](#middleware-design)
- [Handler Patterns](#handler-patterns)
- [Security Hardening](#security-hardening)
- [Performance Optimization](#performance-optimization)
- [Testing Strategies](#testing-strategies)
- [Deployment Guidelines](#deployment-guidelines)

## Core Architecture Patterns

### 1. Server Constructor Pattern (Grafana Gold Standard)

**DO**: Use a constructor function that takes dependencies explicitly:

```go
func NewServer(logger *Logger, db *Database) http.Handler {
    mux := http.NewServeMux()
    addRoutes(mux, logger, db)
    return mux
}

func addRoutes(mux *http.ServeMux, logger *Logger, db *Database) {
    mux.Handle("/api/v1/items", handleItems(logger, db))
    mux.Handle("/healthz", handleHealth(logger))
}
```
````

**Benefits:**

- No global variables or hidden dependencies
- Easy to test with mock dependencies
- Clear dependency graph
- Composable with middleware

**DON'T**: Use global variables or package-level state:

```go
// AVOID THIS
var globalDB *Database
var globalLogger *Logger

func init() {
    globalDB = connectToDatabase()
    globalLogger = createLogger()
}
```

### 2. Handler Factory Pattern

**DO**: Create handler factories that return `http.Handler`:

```go
func handleItems(logger *Logger, db *Database) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Handler has access to dependencies through closure
        items, err := db.GetItems(r.Context())
        if err != nil {
            logger.Error("Failed to get items", "error", err)
            http.Error(w, "Internal server error", http.StatusInternalServerError)
            return
        }
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(items)
    })
}
```

### 3. Minimal Main Function

**DO**: Keep main function minimal with a run() function:

```go
func main() {
    ctx := context.Background()
    if err := run(ctx, os.Stdout, os.Args); err != nil {
        fmt.Fprintf(os.Stderr, "%s\n", err)
        os.Exit(1)
    }
}

func run(ctx context.Context, w io.Writer, args []string) error {
    // Parse configuration
    cfg := parseConfig(args)
    
    // Initialize dependencies
    logger := newLogger(cfg.LogLevel)
    db := connectDatabase(cfg.DatabaseURL)
    defer db.Close()
    
    // Create server
    handler := NewServer(logger, db)
    server := &http.Server{
        Addr:              ":" + cfg.Port,
        Handler:           handler,
        ReadTimeout:       cfg.ReadTimeout,
        ReadHeaderTimeout: cfg.ReadHeaderTimeout,
        WriteTimeout:      cfg.WriteTimeout,
        IdleTimeout:       cfg.IdleTimeout,
    }
    
    return runServerWithGracefulShutdown(ctx, server, logger)
}
```

## Production Server Configuration

### Critical Timeout Settings

**CRITICAL**: Go's default `net/http` has NO timeouts and will break production systems.

**Essential server configuration:**

```go
server := &http.Server{
    Addr:              ":8080",
    Handler:           handler,
    ReadTimeout:       10 * time.Second,  // Time to read request headers and body
    ReadHeaderTimeout: 5 * time.Second,   // Time to read request headers (prevents Slowloris)
    WriteTimeout:      30 * time.Second,  // Time to write response
    IdleTimeout:       120 * time.Second, // Keep-alive timeout
    MaxHeaderBytes:    1 << 20,           // 1 MB max header size
}
```

**For HTTP clients:**

```go
client := &http.Client{
    Timeout: 30 * time.Second,
    Transport: &http.Transport{
        DialContext: (&net.Dialer{
            Timeout:   10 * time.Second,
            KeepAlive: 30 * time.Second,
        }).DialContext,
        TLSHandshakeTimeout:   10 * time.Second,
        ResponseHeaderTimeout: 10 * time.Second,
        MaxIdleConns:          100,
        MaxIdleConnsPerHost:   10,
        IdleConnTimeout:       90 * time.Second,
    },
}
```

### Graceful Shutdown Implementation

```go
func runServerWithGracefulShutdown(ctx context.Context, srv *http.Server, logger *Logger) error {
    // Setup signal handling
    ctx, cancel := signal.NotifyContext(ctx, os.Interrupt, syscall.SIGTERM)
    defer cancel()

    // Start server in goroutine
    serverErr := make(chan error, 1)
    go func() {
        logger.Info("Starting server", "addr", srv.Addr)
        if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            serverErr <- err
        }
    }()

    // Wait for shutdown signal or server error
    select {
    case err := <-serverErr:
        return fmt.Errorf("server failed: %w", err)
    case <-ctx.Done():
        logger.Info("Shutdown signal received")
    }

    // Graceful shutdown with timeout
    shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer shutdownCancel()

    if err := srv.Shutdown(shutdownCtx); err != nil {
        return fmt.Errorf("server shutdown failed: %w", err)
    }

    logger.Info("Server stopped gracefully")
    return nil
}
```

## Middleware Design

### Composable Middleware Pattern

```go
func middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Pre-processing
        next.ServeHTTP(w, r)
        // Post-processing (optional)
    })
}

// Chain middleware
handler := corsMiddleware(
    loggingMiddleware(
        authMiddleware(
            apiHandler,
        ),
    ),
)
```

### Essential Production Middleware

**1. Request Logging:**

```go
func loggingMiddleware(logger *Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            start := time.Now()
            
            // Wrap response writer to capture status code
            wrapped := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}
            
            next.ServeHTTP(wrapped, r)
            
            logger.Info("Request completed",
                "method", r.Method,
                "path", r.URL.Path,
                "status", wrapped.statusCode,
                "duration", time.Since(start),
                "ip", r.RemoteAddr,
                "user_agent", r.UserAgent(),
            )
        })
    }
}

type responseWriter struct {
    http.ResponseWriter
    statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
    rw.statusCode = code
    rw.ResponseWriter.WriteHeader(code)
}
```

**2. Request ID Generation:**

```go
func requestIDMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        requestID := generateRequestID() // Use crypto/rand for production
        ctx := context.WithValue(r.Context(), "requestID", requestID)
        w.Header().Set("X-Request-ID", requestID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

**3. Security Headers:**

```go
func securityHeadersMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("X-Content-Type-Options", "nosniff")
        w.Header().Set("X-Frame-Options", "DENY")
        w.Header().Set("X-XSS-Protection", "1; mode=block")
        w.Header().Set("Referrer-Policy", "strict-origin-when-cross-origin")
        w.Header().Set("Content-Security-Policy", "default-src 'self'")
        
        // Only set HSTS for HTTPS
        if r.TLS != nil {
            w.Header().Set("Strict-Transport-Security", "max-age=63072000; includeSubDomains")
        }
        
        next.ServeHTTP(w, r)
    })
}
```

**4. Recovery Middleware:**

```go
func recoveryMiddleware(logger *Logger) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            defer func() {
                if err := recover(); err != nil {
                    logger.Error("Panic recovered",
                        "error", err,
                        "path", r.URL.Path,
                        "method", r.Method,
                        "stack", string(debug.Stack()),
                    )
                    http.Error(w, "Internal server error", http.StatusInternalServerError)
                }
            }()
            next.ServeHTTP(w, r)
        })
    }
}
```

## Handler Patterns

### JSON API Handlers

```go
func handleCreateItem(logger *Logger, db *Database) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Validate content type
        if r.Header.Get("Content-Type") != "application/json" {
            http.Error(w, "Content-Type must be application/json", http.StatusUnsupportedMediaType)
            return
        }
        
        // Limit request body size
        r.Body = http.MaxBytesReader(w, r.Body, 1048576) // 1MB limit
        
        // Parse JSON
        var item Item
        dec := json.NewDecoder(r.Body)
        dec.DisallowUnknownFields() // Strict parsing
        
        if err := dec.Decode(&item); err != nil {
            logger.Warn("Invalid JSON", "error", err)
            http.Error(w, "Invalid JSON", http.StatusBadRequest)
            return
        }
        
        // Validate input
        if err := item.Validate(); err != nil {
            logger.Warn("Validation failed", "error", err)
            http.Error(w, err.Error(), http.StatusBadRequest)
            return
        }
        
        // Business logic
        createdItem, err := db.CreateItem(r.Context(), item)
        if err != nil {
            logger.Error("Failed to create item", "error", err)
            http.Error(w, "Internal server error", http.StatusInternalServerError)
            return
        }
        
        // Return response
        w.Header().Set("Content-Type", "application/json")
        w.WriteHeader(http.StatusCreated)
        json.NewEncoder(w).Encode(createdItem)
    })
}
```

## Security Hardening

### Input Validation

```go
type CreateItemRequest struct {
    Name        string `json:"name"`
    Description string `json:"description"`
}

func (r CreateItemRequest) Validate() error {
    if strings.TrimSpace(r.Name) == "" {
        return errors.New("name is required")
    }
    
    if len(r.Name) > 100 {
        return errors.New("name too long")
    }
    
    if len(r.Description) > 1000 {
        return errors.New("description too long")
    }
    
    return nil
}
```

## Performance Optimization

### Connection Pooling

```go
// For database connections
func newDBPool(databaseURL string) *sql.DB {
    db, err := sql.Open("postgres", databaseURL)
    if err != nil {
        log.Fatal(err)
    }
    
    // Configure connection pool
    db.SetMaxOpenConns(25)                  // Maximum open connections
    db.SetMaxIdleConns(5)                   // Maximum idle connections
    db.SetConnMaxLifetime(5 * time.Minute)  // Connection lifetime
    db.SetConnMaxIdleTime(time.Minute)      // Idle connection timeout
    
    return db
}
```

### Memory Management with sync.Pool

```go
var bufferPool = sync.Pool{
    New: func() interface{} {
        return make([]byte, 0, 1024)
    },
}

func efficientHandler(w http.ResponseWriter, r *http.Request) {
    buf := bufferPool.Get().([]byte)
    defer bufferPool.Put(buf[:0]) // Reset length, keep capacity
    
    // Use buffer for processing
    buf = append(buf, "response data"...)
    w.Write(buf)
}
```

## Testing Strategies

### Handler Testing

```go
func TestCreateItemHandler(t *testing.T) {
    logger := newTestLogger()
    db := newTestDatabase()
    handler := handleCreateItem(logger, db)
    
    tests := []struct {
        name           string
        body           string
        contentType    string
        expectedStatus int
    }{
        {
            name:           "valid item",
            body:           `{"name":"test","description":"test item"}`,
            contentType:    "application/json",
            expectedStatus: http.StatusCreated,
        },
        {
            name:           "invalid json",
            body:           `{"name":}`,
            contentType:    "application/json",
            expectedStatus: http.StatusBadRequest,
        },
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest(http.MethodPost, "/api/v1/items", strings.NewReader(tt.body))
            req.Header.Set("Content-Type", tt.contentType)
            rec := httptest.NewRecorder()
            
            handler.ServeHTTP(rec, req)
            
            if rec.Code != tt.expectedStatus {
                t.Errorf("expected status %d, got %d", tt.expectedStatus, rec.Code)
            }
        })
    }
}
```

## Health Check Implementation

```go
type HealthChecker struct {
    db     *sql.DB
    logger *Logger
}

func (hc *HealthChecker) Check(ctx context.Context) error {
    // Check database connectivity
    if err := hc.db.PingContext(ctx); err != nil {
        return fmt.Errorf("database unhealthy: %w", err)
    }
    
    return nil
}

func handleHealth(checker *HealthChecker) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ctx, cancel := context.WithTimeout(r.Context(), 5*time.Second)
        defer cancel()
        
        if err := checker.Check(ctx); err != nil {
            w.Header().Set("Content-Type", "application/json")
            w.WriteHeader(http.StatusServiceUnavailable)
            json.NewEncoder(w).Encode(map[string]interface{}{
                "status": "unhealthy",
                "error":  err.Error(),
                "time":   time.Now().Format(time.RFC3339),
            })
            return
        }
        
        w.Header().Set("Content-Type", "application/json")
        json.NewEncoder(w).Encode(map[string]interface{}{
            "status": "healthy",
            "time":   time.Now().Format(time.RFC3339),
        })
    })
}
```

## Production Checklist

Before deploying to production, ensure:

- [ ] All server timeouts are configured
- [ ] Graceful shutdown is implemented
- [ ] Health checks are working
- [ ] Security headers are set
- [ ] Input validation is comprehensive
- [ ] Error handling doesn't leak sensitive information
- [ ] Logging is structured and includes request IDs
- [ ] Rate limiting is implemented
- [ ] TLS is properly configured
- [ ] Dependencies are up to date
- [ ] Tests cover critical paths
- [ ] Monitoring and alerting are set up

## Common Pitfalls to Avoid

1. **Using default HTTP client/server without timeouts** - Will break in production
2. **Global variables for dependencies** - Makes testing difficult
3. **Missing error handling** - Leads to poor user experience
4. **Inadequate input validation** - Security vulnerability
5. **No graceful shutdown** - Can cause data corruption
6. **Missing security headers** - Leaves application vulnerable
7. **Poor logging practices** - Makes debugging impossible
8. **No health checks** - Makes deployment unreliable

## References

- [How I write HTTP services in Go after 13 years - Grafana](https://grafana.com/blog/2024/02/09/how-i-write-http-services-in-go-after-13-years/)
- [Go Security Best Practices](https://go.dev/doc/security/best-practices)
- [Standard net/http Configuration Issues](https://simon-frey.com/blog/go-as-in-golang-standard-net-http-config-will-break-your-production/)
- [Making and Using HTTP Middleware - Alex Edwards](https://www.alexedwards.net/blog/making-and-using-middleware)

This document should be updated as new patterns emerge and the Go ecosystem evolves.

```
---

If no project name is provided via $ARGUMENTS, use the current directory name or prompt for a project name.

**Final Steps:**
1. Initialize the Go module
2. Run `go mod tidy`
3. Test the server starts successfully
4. Create the `/docs/best-practices.md` file with the above content
5. Provide quick start instructions

Focus on creating a production-ready foundation that developers can build upon while maintaining the principles of simplicity, explicit dependencies, and standard library usage.
```
