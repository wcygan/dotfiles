# Driving pi programmatically

Three integration surfaces, smallest to largest: **json mode** (observe), **rpc mode** (control), **SDK** (embed). Docs: `packages/coding-agent/docs/json.md`, `rpc.md`, `sdk.md`.

## json mode — observe a one-shot run

`pi --mode json "<prompt>"` emits one JSON object per line on stdout. First line is a session header; the rest are `AgentSessionEvent`s.

```bash
pi --mode json --no-session "List files in src/" 2>/dev/null \
  | jq -c 'select(.type=="message_end")'
```

Event types (the union you'll match on):
- Lifecycle: `agent_start`, `agent_end` (`agent_end` carries final `messages`)
- Turns: `turn_start`, `turn_end` (`message`, `toolResults`)
- Streaming: `message_start`, `message_update` (carries `assistantMessageEvent` delta), `message_end`
- Tools: `tool_execution_start`, `tool_execution_update`, `tool_execution_end`
- Queues: `queue_update`; Compaction: `compaction_start/end` (`reason`: manual|threshold|overflow); Retry: `auto_retry_start/end`

Stream assistant text deltas:
```bash
pi --mode json --no-session "Explain this repo" 2>/dev/null | \
  jq -rj 'select(.type=="message_update") | .assistantMessageEvent | select(.type=="text_delta") | .delta'
```

## rpc mode — control a long-lived agent

`pi --mode rpc [--provider … --model … --no-session]`. Protocol over stdin/stdout, **strict JSONL** (`\n`-delimited; strip trailing `\r`, never emit Unicode line separators):

- You send **commands** (one JSON per line, optional `id` for correlation).
- pi replies with a **response**: `{"type":"response","command":"…","success":true,"id":"…","data":{…}}` (or `success:false,"error":"…"`).
- pi also streams the same **events** as json mode (no `id` field).

Key commands:
| Category | Commands |
|----------|----------|
| Prompt | `prompt` (opt `images`, `streamingBehavior:"steer"\|"followUp"`), `steer`, `follow_up`, `abort` |
| State | `get_state`, `get_messages`, `get_fork_messages`, `get_last_assistant_text`, `get_session_stats`, `get_commands` |
| Model | `set_model` (`provider`,`modelId`), `cycle_model`, `get_available_models`, `set_thinking_level`, `cycle_thinking_level` |
| Queue | `set_steering_mode`, `set_follow_up_mode` (`"all"`\|`"one-at-a-time"`) |
| Context | `compact` (opt `customInstructions`), `set_auto_compaction`, `set_auto_retry`, `abort_retry` |
| Bash | `bash` (→ `output`,`exitCode`,`cancelled`,`truncated`,`fullOutputPath?`), `abort_bash` |
| Session | `new_session`, `switch_session`, `fork` (`entryId`), `clone`, `export_html`, `set_session_name` |

Extensions can request UI over the same channel via `extension_ui_request` (dialogs `select`/`confirm`/`input`/`editor` expect an `extension_ui_response` with matching `id`; `notify`/`setStatus`/`setWidget`/`setTitle` are fire-and-forget).

Minimal Python client:
```python
import json, subprocess
proc = subprocess.Popen(
    ["pi", "--mode", "rpc", "--no-session",
     "--provider", "llamacpp", "--model", "unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL"],
    stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True)

def send(cmd): proc.stdin.write(json.dumps(cmd) + "\n"); proc.stdin.flush()

send({"type": "prompt", "message": "List the files in this directory"})
for line in proc.stdout:
    ev = json.loads(line)
    if ev.get("type") == "message_update":
        d = ev.get("assistantMessageEvent", {})
        if d.get("type") == "text_delta": print(d["delta"], end="", flush=True)
    if ev.get("type") == "agent_end": break
```

## SDK — embed in a Node app

`@earendil-works/pi-coding-agent` exposes the agent runtime for embedding (custom UIs, automation servers). Read `packages/coding-agent/docs/sdk.md` for the current API surface and `packages/agent/` for the runtime (`pi-agent-core`). Reach for the SDK when rpc mode's process boundary is too coarse; reach for rpc when you want process isolation and language independence.

## Choosing

- One-off, just need the answer/events → **json mode** (or plain `-p`).
- Interactive control loop, model switching, steering, from any language → **rpc mode**.
- Tight in-process integration in TypeScript/Node → **SDK**.
