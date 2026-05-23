# HTTPS

Source: https://portless.sh/https
Checked: 2026-05-23

Use this reference when configuring TLS, troubleshooting browser trust warnings, using custom certificates, or deciding whether to disable HTTPS.

## Default Behavior

Portless enables HTTP/2 over TLS by default. The goal is to avoid HTTP/1.1 per-host connection limits that can slow dev servers serving many unbundled files.

First run behavior:

- Generate a local CA.
- Generate server certificates.
- Add the CA to the system trust store.
- Bind the proxy to port 443 by default.

After trust is configured, browsers should not show certificate warnings for generated Portless certificates.

## Custom Certificates

Use certs from a tool such as mkcert:

```sh
portless proxy start --cert ./cert.pem --key ./key.pem
```

Use custom certs when a project already has a local certificate workflow or when the user does not want Portless to generate/trust its own CA.

## Trust Later

If the first-run trust prompt was skipped:

```sh
portless trust
```

This changes the OS trust store and can prompt for admin privileges. Ask before running it.

## Disable HTTPS

Use plain HTTP:

```sh
portless proxy start --no-tls
```

The proxy uses port 80 by default when TLS is disabled.

Disable TLS when a framework, proxy, or local environment is blocked by HTTPS, but prefer fixing trust or cert configuration first because stable HTTPS origins are closer to production behavior.

## Child Process Trust

The repository README notes that Portless sets `NODE_EXTRA_CA_CERTS` for child Node.js processes so they trust the Portless CA. If a separate Node.js process is not started by Portless, set:

```sh
NODE_EXTRA_CA_CERTS=~/.portless/ca.pem
```

This matters when one local app calls another Portless HTTPS URL.
