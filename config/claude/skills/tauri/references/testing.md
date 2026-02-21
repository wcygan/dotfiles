---
title: Testing
description: IPC mocking, event mocking, window mocking, WebDriver testing, tauri-driver, CI/CD
tags: [testing, mocking, mockipc, webdriver, tauri-driver, vitest, selenium, webdriverio]
---

# Testing

## Two Approaches

1. **Unit/Integration Testing**: mock runtime, test application logic in isolation — no native webview
2. **End-to-End Testing**: WebDriver protocol, desktop (Windows/Linux) + mobile

## IPC Request Mocking

```typescript
import { mockIPC } from "@tauri-apps/api/mocks";
import { invoke } from "@tauri-apps/api/core";

mockIPC((cmd, args) => {
    if (cmd === "add") {
        return (args.a as number) + (args.b as number);
    }
});
```

### Spy on IPC Calls

```typescript
import { vi } from "vitest";
import { mockIPC } from "@tauri-apps/api/mocks";

mockIPC((cmd, args) => {
    if (cmd === "add") {
        return (args.a as number) + (args.b as number);
    }
});

const spy = vi.spyOn(window.__TAURI_INTERNALS__, "invoke");
expect(invoke("add", { a: 12, b: 15 })).resolves.toBe(27);
expect(spy).toHaveBeenCalled();
```

## Sidecar / Shell Command Mocking

```typescript
mockIPC(async (cmd, args) => {
    if (args.message.cmd === 'execute') {
        const eventCallbackId = `_${args.message.onEventFn}`;
        const eventEmitter = window[eventCallbackId];

        eventEmitter({
            event: 'Stdout',
            payload: 'some data sent from the process',
        });

        eventEmitter({
            event: 'Terminated',
            payload: { code: 0, signal: 'kill' },
        });
    }
});
```

## Event System Mocking (v2.7.0+)

```typescript
import { mockIPC } from '@tauri-apps/api/mocks';
import { emit, listen } from '@tauri-apps/api/event';

mockIPC(() => {}, { shouldMockEvents: true });

const eventHandler = vi.fn();
listen('test-event', eventHandler);
emit('test-event', { foo: 'bar' });

expect(eventHandler).toHaveBeenCalledWith({
    event: 'test-event',
    payload: { foo: 'bar' },
});
```

**Limitation**: `emitTo` and `emit_filter` are not yet supported in mocking.

## Window Mocking

```typescript
import { mockWindows } from '@tauri-apps/api/mocks';

mockWindows('main', 'second', 'third');

const { getCurrent, getAll } = await import('@tauri-apps/api/webviewWindow');
expect(getCurrent()).toHaveProperty('label', 'main');
expect(getAll().map((w) => w.label)).toEqual(['main', 'second', 'third']);
```

Only simulates window existence, not properties. Use `mockIPC()` for property calls.

## WebCrypto Setup (jsdom)

Required when running tests in jsdom environment:

```typescript
import { randomFillSync } from 'crypto';

beforeAll(() => {
    Object.defineProperty(window, 'crypto', {
        value: {
            getRandomValues: (buffer) => randomFillSync(buffer),
        },
    });
});
```

## Critical: Always Clear Mocks

```typescript
import { clearMocks } from '@tauri-apps/api/mocks';

afterEach(() => {
    clearMocks();
});
```

## WebDriver Testing (E2E)

### tauri-driver

Cross-platform wrapper around native WebDriver servers:

```bash
cargo install tauri-driver --locked
```

### Platform Support

| Platform | Status | Driver |
|----------|--------|--------|
| Windows | Supported | Microsoft Edge Driver (must match Edge version) |
| Linux | Supported | WebKitWebDriver (`webkit2gtk-driver` package) |
| macOS | Not supported | WKWebView lacks WebDriver tooling |
| iOS/Android | Via Appium 2 | Mobile testing |

### Linux Prerequisites

```bash
which WebKitWebDriver
# Install: apt install webkit2gtk-driver (Debian/Ubuntu)
```

### Windows Prerequisites

Download [Edge Driver](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) matching your Edge version. Version mismatch causes connection timeouts.

Automated:

```bash
cargo install --git https://github.com/chippers/msedgedriver-tool
```

### Testing Frameworks

- **Selenium**: standard WebDriver implementation
- **WebdriverIO**: alternative WebDriver framework

### CI/CD

Use [tauri-action](https://github.com/tauri-apps/tauri-action) for GitHub Actions. Any CI runner works with platform-specific libraries installed.

### Reference

Example repository: [tauri-apps/webdriver-example](https://github.com/tauri-apps/webdriver-example)

## Further Reading

- https://v2.tauri.app/develop/tests/
- https://v2.tauri.app/develop/tests/mocking/
- https://v2.tauri.app/develop/tests/webdriver/
