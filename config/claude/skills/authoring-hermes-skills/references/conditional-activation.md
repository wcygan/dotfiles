# Conditional Activation

Hermes can hide or show skills based on what toolsets/tools are loaded and
what platform the agent is running on. Used well, this keeps `skills_list`
short and relevant.

## Fields

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]        # show ONLY when `web` toolset absent
    requires_toolsets:     [kubernetes] # show ONLY when `kubernetes` present
    fallback_for_tools:    [curl]       # same, for individual tools
    requires_tools:        [kubectl]
platforms: [macos, linux]               # OS allowlist
```

All five fields are additive (AND semantics): the skill is visible only when
every condition matches the current environment.

## The three patterns

### 1. Fallback skill — "do X when the better tool isn't available"

```yaml
metadata:
  hermes:
    fallback_for_toolsets: [web]
```

Canonical example from the Hermes docs: a DuckDuckGo skill is a fallback for
the `web` toolset. When the web toolset is loaded, it's hidden; when it isn't,
the skill surfaces so the agent can still perform searches.

Use for: offline alternatives, degraded modes, API-free approaches.

### 2. Required dependency — "only makes sense with X available"

```yaml
metadata:
  hermes:
    requires_toolsets: [kubernetes]
```

The skill is hidden entirely unless the Kubernetes toolset is loaded. Prevents
the agent from trying to invoke a skill whose procedure assumes unavailable
tools.

Use for: skills that call specific CLIs, skills that depend on an MCP server,
provider-specific workflows.

### 3. Platform restriction

```yaml
platforms: [macos]
```

Only shown on the listed platforms. Values: `macos`, `linux`, `windows`.

Use sparingly. A skill that shells out to `jq` and `curl` doesn't need a
platform restriction. A skill that uses `osascript`, `pbcopy`, `launchctl`,
`apt`, `dnf`, or `powershell` does.

## Toolsets vs tools

- **Toolset** = a named bundle of tools Hermes loads as a unit (e.g., `web`,
  `kubernetes`, `filesystem`).
- **Tool** = an individual callable (e.g., `curl`, `kubectl`).

Prefer `*_toolsets` when you can — the fallback/dependency semantics track the
toolset as a whole, which is more robust to internal tool name changes.

## Combining fields

Combining is fine but be deliberate:

```yaml
metadata:
  hermes:
    requires_toolsets: [kubernetes]
    fallback_for_tools: [k9s]
platforms: [macos, linux]
```

Reads as: "Show this skill on macOS/Linux, only when the `kubernetes` toolset
is loaded, and only if `k9s` specifically is not available."

**Don't put the same name in both `fallback_for_*` and `requires_*`** — it's
contradictory and will either never match or be treated as an error
depending on Hermes version.

## Debugging visibility

```bash
# What does the agent see right now?
hermes skills list

# Force load and inspect parsing
hermes skills inspect my-skill
```

If `inspect` shows the skill but `list` doesn't, a conditional-activation
field is excluding it. Check the current toolset/tool set with
`hermes` interactive session → `/tools`.
