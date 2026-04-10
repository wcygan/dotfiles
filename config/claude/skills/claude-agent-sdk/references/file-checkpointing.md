---
title: File Checkpointing
canonical_url: https://platform.claude.com/docs/en/agent-sdk/file-checkpointing
fetch_before_acting: true
---

# Rewind File Changes with Checkpointing

> Before implementing checkpointing, WebFetch https://platform.claude.com/docs/en/agent-sdk/file-checkpointing for the latest.

## Summary

File checkpointing tracks modifications via Write, Edit, and NotebookEdit tools. Rewind files to any previous state.

### Enable Checkpointing

```python
options = ClaudeAgentOptions(
    enable_file_checkpointing=True,
    permission_mode="acceptEdits",
    extra_args={"replay-user-messages": None},  # Required for checkpoint UUIDs
)
```

### Capture Checkpoint

```python
checkpoint_id = None
session_id = None

async with ClaudeSDKClient(options) as client:
    await client.query("Refactor the auth module")
    async for message in client.receive_response():
        if isinstance(message, UserMessage) and message.uuid and not checkpoint_id:
            checkpoint_id = message.uuid
        if isinstance(message, ResultMessage):
            session_id = message.session_id
```

### Rewind Files

```python
# Resume session with empty prompt, then rewind
async with ClaudeSDKClient(
    ClaudeAgentOptions(enable_file_checkpointing=True, resume=session_id)
) as client:
    await client.query("")
    async for message in client.receive_response():
        await client.rewind_files(checkpoint_id)
        break
```

### Patterns

- **Latest checkpoint**: keep one `checkpoint_id`, update on each `UserMessage`
- **Multiple restore points**: store all UUIDs in a list with metadata
- **Mid-stream rewind**: call `rewind_files()` during message processing, then `break`

### Limitations

- Only tracks Write, Edit, NotebookEdit (not Bash commands like `echo > file`)
- Checkpoints tied to the session that created them
- Restores file content only (not directory creation/deletion)
- Local files only
- Rewinding restores files on disk but does NOT rewind the conversation
