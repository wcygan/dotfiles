# Local and custom models

Use `models.json` for providers that implement a supported API. Use an extension
only for non-standard streaming, dynamic discovery, or an OAuth flow.

## Location and inspection

The default file is:

```text
${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/models.json
```

Pi typically reloads custom models when the model picker is reopened. Verify
that behavior against the matching version's `docs/models.md`.

Before showing configuration, redact `apiKey`, authorization headers,
environment expansions, and command-backed secret expressions.

## Minimal OpenAI-compatible provider

```json
{
  "providers": {
    "local": {
      "baseUrl": "http://127.0.0.1:8080/v1",
      "api": "openai-completions",
      "apiKey": "local-placeholder",
      "models": [
        {
          "id": "served-model-id"
        }
      ]
    }
  }
}
```

Many local servers require a non-empty key in the client configuration even when
they do not authenticate it.

Common API adapters include `openai-completions`, `openai-responses`,
`anthropic-messages`, and `google-generative-ai`; confirm the current supported
set in `packages/coding-agent/docs/models.md`.

## Verification sequence

1. Confirm the server is listening.
2. Query its model endpoint.
3. Compare the returned ID with the redacted `models.json`.
4. Check `pi --list-models` if supported.
5. Run the smallest explicit smoke test.

```bash
curl --fail --silent --max-time 2 http://127.0.0.1:8080/v1/models |
  jq -r '.data[].id'

pi --provider local --model served-model-id --no-session -p "Reply with: ready"
```

Do not infer that a configured display name identifies the model actually loaded
by a single-model server. Some servers ignore the request's `model` field.

## Compatibility flags

Local servers may need compatibility settings for:

- developer-role support;
- reasoning-effort support;
- thinking format;
- streaming usage;
- maximum-token field names; or
- tool-result names.

Do not cargo-cult these settings. Read the matching `models.md`, then inspect the
provider transformation under `packages/ai/src/providers/` to understand the
wire-level effect.

## Credentials

Prefer environment-backed or Pi-managed credentials. When `models.json` supports
environment or command expansion, preserve the reference rather than resolving
and printing the secret. Never commit live credentials or machine-only endpoint
assumptions to a reusable skill.

## Diagnosing model-list failures

If `pi --list-models` crashes:

1. capture the installed version and exact error;
2. inspect custom and package-supplied model entries for missing metadata;
3. compare against the matching `list-models` source;
4. use the provider endpoint and redacted config as a fallback; and
5. avoid deleting or disabling a package without user authorization.
