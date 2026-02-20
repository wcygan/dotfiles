# Node Client Usage

## Unary RPC

```typescript
import { userClient } from './clients/user';

// Simple call
const response = await userClient.getUser({ id: 'u123' });
console.log(response.user?.name);

// With options
const response = await userClient.getUser(
  { id: 'u123' },
  {
    headers: { 'X-Request-ID': crypto.randomUUID() },
    timeoutMs: 5000,
    signal: abortController.signal,
  }
);
```

## Server Streaming

```typescript
// Returns AsyncIterable — use for...await...of
const stream = userClient.watchUser({ userId: 'u123' });

for await (const event of stream) {
  console.log('Event:', event.type, event.user?.name);
}

// With options
const stream = userClient.watchUser(
  { userId: 'u123' },
  { signal: controller.signal, timeoutMs: 60_000 }
);
```

## Setting Request Headers

```typescript
// Per-call headers
const response = await userClient.getUser(
  { id: 'u123' },
  {
    headers: {
      'Authorization': `Bearer ${token}`,
      'X-Request-ID': crypto.randomUUID(),
      'X-Trace-ID': traceID,
    },
  }
);
```

## Reading Response Headers and Trailers

```typescript
const response = await userClient.getUser(
  { id: 'u123' },
  {
    onHeader(headers) {
      // Called when response headers arrive (before body)
      const requestID = headers.get('X-Request-ID');
      const version = headers.get('X-Version');
      console.log('Server version:', version);
    },
    onTrailer(trailers) {
      // Called when trailers arrive (mainly useful for streaming)
      const count = trailers.get('X-Total-Count');
    },
  }
);
```

## Error Handling

```typescript
import { ConnectError, Code } from '@connectrpc/connect';

try {
  const response = await userClient.getUser({ id: 'u123' });
} catch (err) {
  if (err instanceof ConnectError) {
    switch (err.code) {
      case Code.NotFound:
        console.error('User not found');
        break;
      case Code.Unauthenticated:
        await refreshToken();
        break;
      case Code.Unavailable:
        await sleep(1000);
        // retry...
        break;
      default:
        console.error(`RPC error ${err.code}: ${err.message}`);
    }
  } else {
    throw err; // unexpected
  }
}
```

## Extracting Error Details

```typescript
import { ConnectError, Code } from '@connectrpc/connect';
import { BadRequest } from '@bufbuild/protobuf/wkt';  // or google/rpc

try {
  await userClient.createUser({ email: 'bad', name: '' });
} catch (err) {
  if (err instanceof ConnectError) {
    const badRequest = err.findDetails(BadRequest);
    if (badRequest.length > 0) {
      for (const violation of badRequest[0].fieldViolations) {
        console.error(`Field '${violation.field}': ${violation.description}`);
      }
    }
  }
}
```

## Timeouts and Cancellation

```typescript
// Timeout via timeoutMs
const response = await userClient.getUser(
  { id: 'u123' },
  { timeoutMs: 3000 }  // 3 second timeout
);

// Cancellation via AbortController
const controller = new AbortController();

// Cancel after 5 seconds
setTimeout(() => controller.abort(), 5000);

try {
  const response = await userClient.getUser(
    { id: 'u123' },
    { signal: controller.signal }
  );
} catch (err) {
  if (err instanceof ConnectError && err.code === Code.Canceled) {
    console.log('Request was canceled');
  }
}

// Cancellation during streaming
const controller = new AbortController();
const stream = userClient.watchUser({ userId: 'u123' }, { signal: controller.signal });

for await (const event of stream) {
  if (shouldStop(event)) {
    controller.abort();
    break;
  }
}
```

## Interceptors

**Ordering note:** Interceptors are applied in **reverse array order** — the last entry runs first (innermost). `interceptors: [A, B, C]` → C wraps the call, then B, then A outermost.

```typescript
import type { Interceptor } from '@connectrpc/connect';

// Logging interceptor
const loggingInterceptor: Interceptor = (next) => async (req) => {
  const start = Date.now();
  try {
    const response = await next(req);
    console.log(`${req.method.name} OK (${Date.now() - start}ms)`);
    return response;
  } catch (err) {
    console.error(`${req.method.name} failed (${Date.now() - start}ms):`, err);
    throw err;
  }
};

// Auth interceptor
const authInterceptor = (getToken: () => string): Interceptor =>
  (next) => async (req) => {
    req.header.set('Authorization', `Bearer ${getToken()}`);
    return next(req);
  };

// Apply to transport
const transport = createConnectTransport({
  baseUrl: 'http://localhost:8080',
  httpVersion: '2',
  interceptors: [loggingInterceptor, authInterceptor(getToken)],
});
```

## Streaming Interceptor

```typescript
import type { Interceptor, StreamResponse } from '@connectrpc/connect';

const streamLoggingInterceptor: Interceptor = (next) => async (req) => {
  const response = await next(req);

  // For streaming responses, wrap the async iterable
  if (response.stream) {
    return {
      ...response,
      async *[Symbol.asyncIterator]() {
        let count = 0;
        for await (const msg of response) {
          count++;
          yield msg;
        }
        console.log(`Stream ${req.method.name} received ${count} messages`);
      },
    };
  }
  return response;
};
```

## Context Values (Type-Safe Propagation)

```typescript
import { createContextKey, createContextValues } from '@connectrpc/connect';

// Define a typed key
const requestIDKey = createContextKey<string>('', {
  description: 'HTTP request ID',
});

// Set value
const contextValues = createContextValues().set(requestIDKey, crypto.randomUUID());

// Pass to call
const response = await userClient.getUser(
  { id: 'u123' },
  { contextValues }
);

// Read in interceptor
const interceptor: Interceptor = (next) => async (req) => {
  const requestID = req.contextValues.get(requestIDKey);
  req.header.set('X-Request-ID', requestID);
  return next(req);
};
```

## Full Express Route Example

```typescript
import express from 'express';
import { ConnectError, Code } from '@connectrpc/connect';
import { userClient } from '../clients/user';

const router = express.Router();

router.get('/users/:id', async (req, res) => {
  try {
    const response = await userClient.getUser(
      { id: req.params.id },
      {
        headers: {
          Authorization: req.headers.authorization ?? '',
          'X-Request-ID': crypto.randomUUID(),
        },
        timeoutMs: 5000,
      }
    );

    const user = response.user!;
    res.json({ id: user.id, name: user.name, email: user.email });
  } catch (err) {
    if (err instanceof ConnectError) {
      const httpStatus: Record<number, number> = {
        [Code.NotFound]: 404,
        [Code.InvalidArgument]: 400,
        [Code.Unauthenticated]: 401,
        [Code.PermissionDenied]: 403,
        [Code.ResourceExhausted]: 429,
      };
      res.status(httpStatus[err.code] ?? 500).json({ error: err.message });
    } else {
      res.status(500).json({ error: 'Internal server error' });
    }
  }
});
```

## Docs

- https://connectrpc.com/docs/node/using-clients/ — Calling RPCs, streaming, options
- https://connectrpc.com/docs/node/interceptors/ — Node interceptors and context values
- https://connectrpc.com/docs/web/headers-and-trailers/ — Headers, trailers, binary encoding
- https://connectrpc.com/docs/web/cancellation-and-timeouts/ — Cancellation and timeouts
- https://connectrpc.com/docs/web/errors/ — ConnectError, Code enum, findDetails
