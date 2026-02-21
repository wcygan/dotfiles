---
title: Security & Permissions
description: Capabilities, permissions, scopes, CSP, trust boundaries, security lifecycle, vulnerability reporting
tags: [security, permissions, capabilities, scopes, csp, trust-boundaries, isolation]
---

# Security & Permissions

## Trust Boundaries

- **Rust/plugin code**: unrestricted system resource access
- **WebView code**: only resources explicitly exposed via IPC
- All backend command access controlled through capabilities configuration
- Individual command implementations enforce fine-grained access levels

## Access Control Framework (Layered)

```
Permissions (TOML) → Capabilities (JSON/TOML) → Runtime Authority
     define ops        bind to windows           enforce at runtime
```

1. **Permissions**: define what operations are available
2. **Scopes**: fine-grained access boundaries for permitted operations (allow/deny)
3. **Capabilities**: configure which commands specific windows/contexts can invoke
4. **Runtime Authority**: enforce access decisions at execution time

## Permissions

Permissions are "descriptions of explicit privileges of commands." Defined in TOML files.

### Core Structure

```toml
[[permission]]
identifier = "my-identifier"
description = "This describes the impact and more."
commands.allow = ["read_file"]

[[scope.allow]]
my-scope = "$HOME/*"

[[scope.deny]]
my-scope = "$HOME/secret"
```

### Naming Convention

- `<name>:default` — plugin/app default permission
- `<name>:<command-name>` — individual command permission
- Plugin prefix `tauri-plugin-` is auto-prepended at compile time
- ASCII lowercase `[a-z]` only, max 116 characters

### Directory Structure

**Application layout:**

```
src-tauri/
  permissions/
    <identifier>.toml           # TOML only for app permissions
  capabilities/
    <identifier>.json/.toml     # JSON or TOML for capabilities
```

**Plugin layout:**

```
tauri-plugin/
  permissions/
    <identifier>.json/toml
    default.json/toml
```

### Configuration Examples

**Scope definition:**

```toml
[[permission]]
identifier = "scope-home"
description = "Permits access to all files in $HOME."

[[scope.allow]]
path = "$HOME/*"
```

**Command permission:**

```toml
[[permission]]
identifier = "read-files"
description = "Enables all file read commands."
commands.allow = [
    "read_file",
    "read",
    "open",
    "read_text_file",
    "read_text_file_lines",
    "read_text_file_lines_next"
]
```

**Permission set (composing multiple):**

```toml
[[set]]
identifier = "allow-home-read-extended"
description = "Read access and dir creation in $HOME."
permissions = [
    "fs:read-files",
    "fs:scope-home",
    "fs:allow-mkdir"
]
```

### Capability File Example

```json
{
  "identifier": "main-capability",
  "description": "Capability for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "fs:allow-read-text-file",
    "fs:allow-resource-read-recursive"
  ]
}
```

## Content Security Policy (CSP)

Configured in `tauri.conf.json` to restrict what the WebView can load/execute. Reduces attack surface by limiting script sources, style sources, and network connections.

## Security Lifecycle

Threats exist at every stage: upstream, development, build, distribution, and runtime.

### Upstream

- Keep Tauri and all dependencies updated
- Audit with: `npm audit`, `cargo audit`, `cargo-vet`, `cargo crev`
- Consume critical dependencies from git using hash revisions

### Development

- Dev server lacks encryption/authentication — use trusted networks only
- Never use admin accounts for coding
- Prevent secrets on dev machines
- Use git pre-commit hooks to prevent secret leakage
- Require commit signing

### Build-Time

- Pin GitHub Action versions explicitly
- Sign binaries for target platforms
- Use hardware-backed signing keys

### Distribution

- Protect manifest server, build server, and binary hosting
- Consider CrabNebula for trusted distribution

### Runtime

- CSP restricts WebView communication types
- Capabilities prevent untrusted content from accessing system APIs
- The approach assumes "the webview is insecure"

## Vulnerability Reporting

- Report via GitHub Vulnerability Disclosure on affected repositories
- Alternative: `security@tauri.app`
- Do not publicly disclose before coordination

## Best Practices

1. Frontend is untrusted — never handle secrets there
2. Always sanitize user input
3. Defer business logic to the Core process
4. Use deny lists for exceptions within broader scopes
5. Use the isolation pattern for high-security apps
6. Keep attack surface minimal — only expose needed commands
7. Default permissions auto-add when using Tauri CLI for plugin installation

## Further Reading

- https://v2.tauri.app/security/
- https://v2.tauri.app/security/permissions/
- https://v2.tauri.app/security/lifecycle/
