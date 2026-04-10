---
title: Sessions
canonical_url: https://platform.claude.com/docs/en/agent-sdk/sessions
fetch_before_acting: true
---

# Work with Sessions

> Before implementing session management, WebFetch https://platform.claude.com/docs/en/agent-sdk/sessions for the latest.

## Summary

Sessions persist conversation history to disk. Return to a session to get full context from prior turns.

### Choosing an Approach

| Scenario | Approach |
|----------|----------|
| One-shot task | Just use `query()` |
| Multi-turn chat in one process | `ClaudeSDKClient` (auto-manages sessions) |
| Resume after process restart | `continue_conversation=True` |
| Resume specific past session | Capture session_id, pass to `resume` |
| Try alternative approach | Fork the session |

### ClaudeSDKClient (Auto Session Management)

```python
async with ClaudeSDKClient(options=options) as client:
    await client.query("Analyze the auth module")
    async for msg in client.receive_response():
        print_response(msg)
    # Second query — same session, context retained
    await client.query("Now refactor it to use JWT")
    async for msg in client.receive_response():
        print_response(msg)
```

### Capture Session ID

```python
async for message in query(prompt="Analyze auth module", options=options):
    if isinstance(message, ResultMessage):
        session_id = message.session_id
```

### Resume by ID

```python
async for message in query(
    prompt="Implement the refactoring you suggested",
    options=ClaudeAgentOptions(resume=session_id, allowed_tools=[...]),
):
    ...
```

### Fork a Session

Creates a new session with copied history. Original unchanged.

```python
async for message in query(
    prompt="Try OAuth2 instead",
    options=ClaudeAgentOptions(resume=session_id, fork_session=True),
):
    if isinstance(message, ResultMessage):
        forked_id = message.session_id  # New session ID
```

### Session Utility Functions

- `list_sessions(directory, limit)` → `list[SDKSessionInfo]`
- `get_session_messages(session_id, directory)` → `list[SessionMessage]`
- `get_session_info(session_id, directory)` → `SDKSessionInfo | None`
- `rename_session(session_id, title)` → `None`
- `tag_session(session_id, tag)` → `None`

### Cross-Host Resume

Sessions stored at `~/.claude/projects/<encoded-cwd>/<session-id>.jsonl`. To resume on another host, copy the file to the same path with matching `cwd`.
