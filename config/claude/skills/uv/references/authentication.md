# UV — Authentication

## `uv auth login`

```bash
uv auth login <service>           # Interactive prompt
uv auth login <service> --token <token>   # Token auth (sets username to __token__)
uv auth login <service> --username <user> --password <pass>
```

`<service>` is the domain or URL of the package index.

## Keyring Integration

```bash
uv auth login --keyring-provider native <service>
```

Uses the system keyring (macOS Keychain, Windows Credential Manager, etc.) to store credentials.

## Private Index Configuration

```toml
[[tool.uv.index]]
name = "private"
url = "https://private.example.com/simple"
```

After `uv auth login private.example.com`, UV uses stored credentials automatically.

## Options

| Flag | Purpose |
|------|---------|
| `--token` | Token-based auth (username = `__token__`) |
| `--username` | Username for basic auth |
| `--password` | Password (use `-` for stdin) |
| `--keyring-provider native` | Store in system keyring |
| `--allow-insecure-host` | Allow unverified TLS |
| `--native-tls` | Use platform TLS certificates |

---

Docs: https://docs.astral.sh/uv/reference/cli/#uv-auth-login
