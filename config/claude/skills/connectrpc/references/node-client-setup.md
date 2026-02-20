# Node Client Setup

## npm Packages

```bash
# Core ConnectRPC packages
npm install @connectrpc/connect @connectrpc/connect-node

# For TypeScript generated code (protobuf-es)
npm install @bufbuild/protobuf

# For generating TypeScript code (dev dependency)
npm install --save-dev @bufbuild/buf
```

## Transport Options

### Connect Protocol (default — recommended for Node → Go)

```typescript
import { createConnectTransport } from '@connectrpc/connect-node';

const transport = createConnectTransport({
  baseUrl: 'http://localhost:8080',

  // HTTP version: '1.1' uses fetch-compatible; '2' requires http2 module
  httpVersion: '2',  // recommended for production (full streaming support)
});
```

### gRPC Protocol

```typescript
import { createGrpcTransport } from '@connectrpc/connect-node';

const transport = createGrpcTransport({
  baseUrl: 'http://localhost:8080',
  // gRPC is HTTP/2 only — no httpVersion option
});
```

### gRPC-Web Protocol

```typescript
import { createGrpcWebTransport } from '@connectrpc/connect-node';

const transport = createGrpcWebTransport({
  baseUrl: 'http://localhost:8080',
});
```

## Creating Clients

```typescript
import { createClient } from '@connectrpc/connect';
import { UserService } from '../gen/ts/api/v1/user_connect';
import { transport } from './transport';

// Type-safe client — methods match your proto service definition
const userClient = createClient(UserService, transport);

// client.getUser, client.listUsers, client.createUser, etc.
```

## Transport Configuration Options

```typescript
const transport = createConnectTransport({
  baseUrl: process.env.BACKEND_URL ?? 'http://localhost:8080',
  httpVersion: '2',

  // Custom fetch (optional — uses undici by default for Node)
  // fetch: customFetch,

  // Default headers for all requests (or use interceptors)
  // No built-in defaultHeaders — use interceptors instead

  // Interceptors applied to all requests from this transport
  interceptors: [authInterceptor, loggingInterceptor],

  // JSON codec options (for Connect protocol in JSON mode)
  // jsonOptions: { ignoreUnknownFields: true },

  // Signal to abort all in-flight requests
  // signal: globalAbortController.signal,
});
```

## Transport Reuse Pattern

Create one transport per service target; share it across clients:

```typescript
// src/clients/transport.ts
import { createConnectTransport } from '@connectrpc/connect-node';

export const backendTransport = createConnectTransport({
  baseUrl: process.env.BACKEND_URL!,
  httpVersion: '2',
  interceptors: [authInterceptor],
});

// src/clients/user.ts
import { createClient } from '@connectrpc/connect';
import { UserService } from '../../gen/ts/api/v1/user_connect';
import { backendTransport } from './transport';

export const userClient = createClient(UserService, backendTransport);

// src/clients/order.ts
import { OrderService } from '../../gen/ts/api/v1/order_connect';
import { backendTransport } from './transport';

export const orderClient = createClient(OrderService, backendTransport);
```

## TypeScript Configuration

```json
// tsconfig.json — required settings for protobuf-es
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "strict": true
  }
}
```

## Binary Header Utilities

```typescript
import { encodeBinaryHeader, decodeBinaryHeader } from '@connectrpc/connect';
import { MyMessageSchema } from './gen/api/v1/foo_pb';
import { create } from '@bufbuild/protobuf';

// Encode raw bytes
const data = new Uint8Array([0xde, 0xad, 0xbe, 0xef]);
headers.set('Data-Bin', encodeBinaryHeader(data));

// Encode a proto message
const msg = create(MyMessageSchema, { field: 'value' });
headers.set('My-Message-Bin', encodeBinaryHeader(msg, MyMessageSchema));

// Encode text (handles emoji/unicode safely)
headers.set('Greet-Emoji-Bin', encodeBinaryHeader('👋'));

// Decode
const value = responseHeaders.get('My-Message-Bin');
if (value != null) {
  const decoded = decodeBinaryHeader(value, MyMessageSchema);
}
```

## Verifying Setup

```typescript
import { userClient } from './clients/user';
import { ConnectError } from '@connectrpc/connect';

async function test() {
  try {
    const response = await userClient.getUser({ id: 'test-id' });
    console.log('Connected! User:', response.user?.name);
  } catch (err) {
    if (err instanceof ConnectError) {
      console.error('ConnectError:', err.code, err.message);
    } else {
      console.error('Unexpected error:', err);
    }
  }
}
```

## Docs

- https://connectrpc.com/docs/node/getting-started/ — Node.js getting started guide
- https://connectrpc.com/docs/node/using-clients/ — Using clients in Node.js
- https://www.npmjs.com/package/@connectrpc/connect-node — @connectrpc/connect-node on npm
- https://www.npmjs.com/package/@connectrpc/connect — @connectrpc/connect on npm
