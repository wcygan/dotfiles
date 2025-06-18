<!--
name: context-load-fresh-connect-stack
description: Load comprehensive context about the Fresh + ConnectRPC full-stack architecture
owner: development
tags: architecture, fresh, connectrpc, full-stack, context, deno, go
-->

Please load and analyze the complete context of this Fresh + ConnectRPC full-stack architecture. This is our de-facto modern web development stack combining:

**Frontend**: Deno Fresh 2.0 with Islands Architecture + TypeScript
**Backend**: Go with ConnectRPC + Protocol Buffers
**Integration**: Type-safe RPC communication over HTTP/JSON

## Key Areas to Understand

### Architecture Overview

- Fresh 2.0 Islands Architecture with SSR and selective hydration
- ConnectRPC for type-safe RPC communication
- Protocol Buffer schema-first development
- End-to-end type safety from schema → Go → TypeScript

### Project Structure

- `/frontend/` - Deno Fresh application with Islands and routes
- `/backend/` - Go ConnectRPC service with middleware
- `/tasks/` - Deno task automation for unified development workflow
- Root `deno.json` as central orchestration harness

### Development Workflow

- Unified task management via Deno (`deno task dev`, `deno task up`, etc.)
- Hot reload for both frontend (Fresh) and backend (Air)
- Docker containerization with health checks
- Cross-language testing strategy

### Integration Patterns

- API proxy pattern in Fresh routes (`/api/[...path].ts`)
- CORS handling for browser compatibility
- buf.build registry for Protocol Buffer packages
- Preact signals for reactive state management

### Production Features

- Multi-stage Docker builds
- Non-conflicting port allocation (8007/3007)
- Health checks and graceful shutdown
- Security hardening and error handling

Please examine the codebase thoroughly and be ready to:

1. Answer architecture questions
2. Help with development tasks
3. Assist with debugging integration issues
4. Provide guidance on best practices
5. Help extend or modify the stack

Focus on understanding the complete integration between Fresh frontend, ConnectRPC backend, and the unified development experience this architecture provides.

## Additional Context Resources

For deeper understanding of the underlying frameworks, reference these official documentation sources:

**Deno Fresh:**

- Fresh Introduction: https://fresh.deno.dev/docs/introduction
- Fresh 2.0 Update: https://deno.com/blog/an-update-on-fresh

**ConnectRPC:**

- Go Getting Started: https://connectrpc.com/docs/go/getting-started
- Web Getting Started: https://connectrpc.com/docs/web/getting-started

Use these resources to supplement your understanding of framework-specific concepts, best practices, and advanced features that complement this implementation.

## Essential Integration Snippets

When working with this Fresh + ConnectRPC stack, these are the core code patterns from our working implementation:

### Package Installation (BSR/Buf Schema Registry)

```bash
# Install from Buf Schema Registry
deno install npm:@buf/wcygan_hello.bufbuild_es
```

### 1. API Proxy Route (Critical for Frontend-Backend Communication)

```typescript
// frontend/routes/api/[...path].ts
import { type FreshContext } from "@fresh/core";

const BACKEND_URL = Deno.env.get("BACKEND_URL") || "http://localhost:3007";

export async function handler(req: Request, _ctx: FreshContext) {
  const url = new URL(req.url);
  const backendUrl = `${BACKEND_URL}${url.pathname.replace("/api", "")}`;

  const response = await fetch(backendUrl, {
    method: req.method,
    headers: req.headers,
    body: req.body,
  });

  // Clone response with CORS headers
  const corsHeaders = new Headers(response.headers);
  corsHeaders.set("Access-Control-Allow-Origin", "*");
  corsHeaders.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
  corsHeaders.set("Access-Control-Allow-Headers", "Content-Type, Connect-Protocol-Version");

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: corsHeaders,
  });
}
```

### 2. Frontend Island Component with ConnectRPC Client

```typescript
// frontend/islands/GreeterApp.tsx
import { useSignal } from "@preact/signals";
import { createClient } from "@connectrpc/connect";
import { createConnectTransport } from "@connectrpc/connect-web";
import { GreeterService } from "@buf/wcygan_hello.bufbuild_es/hello/v1/hello_connect";

const transport = createConnectTransport({
  baseUrl: "/api",
  useBinaryFormat: false,
});

const client = createClient(GreeterService, transport);

export function GreeterApp() {
  const name = useSignal("");
  const greeting = useSignal("");
  const loading = useSignal(false);

  const handleSubmit = async (e: Event) => {
    e.preventDefault();
    loading.value = true;

    try {
      const response = await client.sayHello({ name: name.value });
      greeting.value = response.message;
    } catch (error) {
      greeting.value = `Error: ${error.message}`;
    } finally {
      loading.value = false;
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={name.value}
        onInput={(e) => name.value = e.currentTarget.value}
        placeholder="Enter your name"
      />
      <button type="submit" disabled={loading.value}>
        {loading.value ? "Loading..." : "Say Hello"}
      </button>
      {greeting.value && <p>{greeting.value}</p>}
    </form>
  );
}
```

### 3. Backend ConnectRPC Service

```go
// backend/cmd/server/main.go
package main

import (
    "log"
    "net/http"
    "github.com/connectrpc/connect-go"
    hellov1 "buf.build/gen/go/wcygan/hello/protocolbuffers/go/hello/v1"
    "buf.build/gen/go/wcygan/hello/connectrpc/go/hello/v1/hellov1connect"
)

type GreeterService struct{}

func (s *GreeterService) SayHello(
    ctx context.Context,
    req *connect.Request[hellov1.SayHelloRequest],
) (*connect.Response[hellov1.SayHelloResponse], error) {
    name := req.Msg.Name
    if name == "" {
        name = "World"
    }

    return connect.NewResponse(&hellov1.SayHelloResponse{
        Message: fmt.Sprintf("Hello, %s!", name),
    }), nil
}

func main() {
    greeter := &GreeterService{}
    path, handler := hellov1connect.NewGreeterServiceHandler(greeter)

    mux := http.NewServeMux()
    mux.Handle(path, handler)

    // Add CORS middleware
    corsHandler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Connect-Protocol-Version")

        if r.Method == "OPTIONS" {
            w.WriteHeader(http.StatusOK)
            return
        }

        mux.ServeHTTP(w, r)
    })

    log.Fatal(http.ListenAndServe(":3007", corsHandler))
}
```

### 4. Frontend Dependencies Configuration

```json
// frontend/deno.json
{
  "imports": {
    "@fresh/core": "jsr:@fresh/core@^2.0.0-alpha.22",
    "@preact/signals": "npm:@preact/signals@^1.3.0",
    "@connectrpc/connect": "npm:@connectrpc/connect@^2.0.0",
    "@connectrpc/connect-web": "npm:@connectrpc/connect-web@^2.0.0",
    "@buf/wcygan_hello.bufbuild_es": "npm:@buf/wcygan_hello.bufbuild_es@^2.5.2"
  },
  "nodeModulesDir": "auto"
}
```

```
// frontend/.npmrc
@buf:registry=https://buf.build/gen/npm/v1/
```

### 5. Docker Compose for Local Development

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    ports:
      - "3007:3007"
    healthcheck:
      test: ["CMD", "wget", "--spider", "http://localhost:3007/health"]

  frontend:
    build: ./frontend
    ports:
      - "8007:8007"
    environment:
      - BACKEND_URL=http://backend:3007
    depends_on:
      backend:
        condition: service_healthy
```

These five snippets represent the core integration pattern: API proxy for routing, typed client in the frontend, ConnectRPC service implementation, proper dependency configuration, and Docker orchestration.
