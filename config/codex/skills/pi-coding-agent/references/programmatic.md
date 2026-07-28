# Driving Pi programmatically

Choose the smallest integration surface:

- `-p` for a final text result;
- JSON mode for a machine-readable event stream;
- RPC mode for a controlled long-lived subprocess; or
- the TypeScript SDK for in-process embedding.

Verify event and command schemas against the installed version's help and the
matching `json.md`, `rpc.md`, or `sdk.md`.

## JSON mode

JSON mode emits one object per line. Keep stderr separate from the protocol.

```bash
pi --mode json --no-session "Summarize this repository" 2>pi.stderr |
  jq -c 'select(.type == "message_end")'
```

Typical event families cover agent lifecycle, turns, message streaming, tool
execution, queues, compaction, and retries. Consumers must tolerate unknown
event types so newer Pi versions do not break the parser.

Example text-delta filter:

```bash
pi --mode json --no-session "Explain this repository" 2>pi.stderr |
  jq -rj '
    select(.type == "message_update") |
    .assistantMessageEvent |
    select(.type == "text_delta") |
    .delta
  '
```

## RPC mode

RPC mode uses newline-delimited JSON on stdin and stdout. Commands may include an
ID for response correlation; streamed agent events are independent messages.

Protocol clients should:

- write exactly one JSON object per line;
- keep stderr out of the JSON parser;
- correlate command responses by ID;
- continue handling asynchronous agent events;
- implement cancellation and subprocess shutdown; and
- treat extension UI requests explicitly rather than hanging indefinitely.

Minimal Python skeleton:

```python
import json
import subprocess

process = subprocess.Popen(
    ["pi", "--mode", "rpc", "--no-session"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,
)

assert process.stdin is not None
assert process.stdout is not None

process.stdin.write(
    json.dumps(
        {
            "type": "prompt",
            "message": "List the files in this directory",
            "id": "prompt-1",
        }
    )
    + "\n"
)
process.stdin.flush()

for line in process.stdout:
    event = json.loads(line)
    if event.get("type") == "message_update":
        delta = event.get("assistantMessageEvent", {})
        if delta.get("type") == "text_delta":
            print(delta.get("delta", ""), end="", flush=True)
    if event.get("type") == "agent_end":
        break
```

Read the version-matched RPC documentation for the current command catalog.
Common categories include prompts and steering, state inspection, model and
thinking selection, queue behavior, compaction/retry control, shell execution,
and session lifecycle.

## SDK

The coding-agent package exposes an SDK for TypeScript applications. Prefer RPC
when process isolation or language independence is valuable. Prefer the SDK when
the application needs direct in-process control and is willing to track Pi's
package API.

Package scopes have changed across distributions. Read the installed package's
`package.json` or the selected source checkout; do not assume an npm scope.
