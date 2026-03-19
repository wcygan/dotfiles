# Zed Agent Settings

All settings live under the `"agent"` key in `settings.json`.

## Default Model

```json
{
  "agent": {
    "default_model": {
      "provider": "openai",
      "model": "gpt-4o"
    }
  }
}
```

Zed's hosted service defaults: `claude-sonnet-4-5` (agent work), `gpt-5-nano` (fast operations).

## Feature-Specific Models

Override the default model for specific features:

```json
{
  "agent": {
    "inline_assistant_model": {
      "provider": "anthropic",
      "model": "claude-3-5-sonnet"
    },
    "commit_message_model": {
      "provider": "openai",
      "model": "gpt-4o-mini"
    },
    "thread_summary_model": {
      "provider": "google",
      "model": "gemini-2.0-flash"
    }
  }
}
```

Falls back to `default_model` if unspecified.

## Inline Assistant Alternatives

Send the same prompt to multiple models at once:

```json
{
  "agent": {
    "inline_alternatives": [
      { "provider": "zed.dev", "model": "gpt-5-mini" },
      { "provider": "zed.dev", "model": "gemini-3-flash" }
    ]
  }
}
```

## Model Temperature

Customize by provider, model, or globally (last match wins):

```json
{
  "agent": {
    "model_parameters": [
      { "provider": "openai", "temperature": 0.5 },
      { "temperature": 0 },
      { "provider": "zed.dev", "model": "claude-sonnet-4-5", "temperature": 1.0 }
    ]
  }
}
```

## Agent Panel Settings

| Setting | Type | Default | Purpose |
|---------|------|---------|---------|
| `default_view` | `"thread"` / `"text_thread"` | `"thread"` | Initial panel view mode |
| `agent_ui_font_size` | integer | — | Font size for agent responses |
| `agent_buffer_font_size` | integer | `buffer_font_size` | Monospace editor font size |
| `message_editor_min_lines` | integer | 4 | Minimum message textarea height |
| `expand_edit_card` | boolean | `true` | Show full diffs in cards |
| `expand_terminal_card` | boolean | `true` | Show terminal output while running |
| `single_file_review` | boolean | `false` | Display accept/reject actions |
| `play_sound_when_agent_done` | boolean | `false` | Notification sound on completion |
| `use_modifier_to_send` | boolean | `false` | Require Ctrl/Cmd to send messages |
| `enable_feedback` | boolean | `true` | Show thumbs up/down buttons |
| `notify_when_agent_waiting` | boolean | — | Visual notifications when backgrounded |

## Favorite Models

```json
{
  "agent": {
    "favorite_models": [
      { "provider": "anthropic", "model": "claude-sonnet-4-5" },
      { "provider": "openai", "model": "gpt-4o" }
    ]
  }
}
```

## Tool Permissions

### Global Default

```json
{
  "agent": {
    "tool_permissions": {
      "default": "confirm"
    }
  }
}
```

Options: `"confirm"` (prompts), `"allow"` (auto-approve), `"deny"` (blocks).

### Per-Tool Rules with Patterns

```json
{
  "agent": {
    "tool_permissions": {
      "default": "allow",
      "tools": {
        "terminal": {
          "default": "confirm",
          "always_allow": [
            { "pattern": "^cargo\\s+(build|test)" }
          ],
          "always_deny": [
            { "pattern": "rm\\s+-rf\\s+(/|~)" }
          ],
          "always_confirm": [
            { "pattern": "sudo\\s" }
          ]
        },
        "edit_file": {
          "always_deny": [
            { "pattern": "\\.env" },
            { "pattern": "\\.(pem|key)$" }
          ]
        }
      }
    }
  }
}
```

**Pattern precedence** (highest to lowest):
1. Built-in security rules
2. `always_deny`
3. `always_confirm`
4. `always_allow`
5. Tool-specific `default`
6. Global `default`

Case-insensitive by default; set `"case_sensitive": true` to enforce.

### MCP Tool Permissions

Format: `mcp:<server_name>:<tool_name>`

```json
{
  "agent": {
    "tool_permissions": {
      "tools": {
        "mcp:github:create_issue": { "default": "confirm" },
        "mcp:github:create_pull_request": { "default": "deny" }
      }
    }
  }
}
```

## Custom Profiles

```json
{
  "agent": {
    "profiles": {
      "my-profile": {
        "tools": {
          "read_file": true,
          "edit_file": true,
          "terminal": false
        }
      }
    }
  }
}
```
