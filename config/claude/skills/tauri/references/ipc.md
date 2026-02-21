---
title: Inter-Process Communication
description: Commands, events, channels, brownfield pattern, isolation pattern, IPC security
tags: [ipc, commands, events, channels, invoke, brownfield, isolation, message-passing]
---

# Inter-Process Communication

Tauri implements **asynchronous message passing** between frontend (WebView) and backend (Core Process). All messages are serialized, routed through Core, and can be rejected before execution.

## Two IPC Primitives

### Commands (`invoke`)

- Request-response pattern, like browser `fetch`
- Frontend calls Rust functions, passes arguments, receives data
- Uses JSON-RPC-like serialization — all args/returns must be JSON-serializable
- Despite using message passing internally, commands do not share FFI security vulnerabilities

### Events

- Fire-and-forget, one-way messages
- Both frontend and Rust can emit and listen
- Asynchronous, unidirectional
- Best for lifecycle events and state changes
- Not type-safe; payloads are always JSON strings

## IPC Patterns

### Brownfield Pattern (Default)

The default approach — minimal modifications to existing web applications.

```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "brownfield"
      }
    }
  }
}
```

No additional configuration needed. Works with standard browser APIs. Note: not everything that works in browsers works out-of-the-box in Tauri.

### Isolation Pattern (Security Hardened)

Intercepts and validates all IPC messages using a sandboxed iframe before they reach Core. Uses **AES-GCM encryption** with runtime-generated keys.

**Message flow:**

1. IPC handler receives message
2. Routes to isolation app (sandboxed iframe)
3. Isolation hook runs — can modify/reject the message
4. Message encrypted with AES-GCM (keys regenerated each app run)
5. Encrypted message returns to IPC handler
6. Handler passes to Core for decryption

**Configuration:**

```json
{
  "app": {
    "security": {
      "pattern": {
        "use": "isolation",
        "options": {
          "dir": "../dist-isolation"
        }
      }
    }
  }
}
```

**Isolation HTML** (`../dist-isolation/index.html`):

```html
<!doctype html>
<html lang="en">
  <head><meta charset="UTF-8" /><title>Isolation</title></head>
  <body><script src="index.js"></script></body>
</html>
```

**Isolation JavaScript** (`../dist-isolation/index.js`):

```javascript
window.__TAURI_ISOLATION_HOOK__ = (payload) => {
  // Validate, modify, or reject IPC payloads
  // Examples: verify file paths, validate HTTP origins, sanitize event data
  console.log('hook', payload);
  return payload;
};
```

**Best practices:**

- Tauri "highly recommends using the isolation pattern whenever it can be used"
- Keep the isolation app as simple as possible — minimal dependencies reduce supply chain risk
- The hook intercepts **all** frontend messages, including event APIs
- ES Modules don't load in Windows sandboxed iframes; the build process inlines scripts
- AES-GCM overhead is "relatively small" (same algorithm underlying TLS)

## When to Use What

| Pattern | Use Case |
|---------|----------|
| Brownfield | Standard apps, web-compatible, minimal config |
| Isolation | High-security apps, untrusted content, payload validation required |
| Commands | Request-response, typed data, return values needed |
| Events | Notifications, state broadcasts, fire-and-forget |
| Channels | High-throughput streaming, large payloads, ordered data |

## Further Reading

- https://v2.tauri.app/concept/inter-process-communication/
- https://v2.tauri.app/concept/inter-process-communication/brownfield/
- https://v2.tauri.app/concept/inter-process-communication/isolation/
