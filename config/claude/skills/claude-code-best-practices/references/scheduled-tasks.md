---
title: Scheduled Tasks
canonical_url: https://code.claude.com/docs/en/scheduled-tasks
fetch_before_acting: true
---

# Scheduled Tasks

> Before setting up scheduled tasks, WebFetch https://code.claude.com/docs/en/scheduled-tasks for the latest.

## Summary

Run prompts on a schedule using `/loop`, cron tools, or natural language reminders. Session-scoped (gone when you exit).

### /loop

Quickest way to schedule recurring work:

```
/loop 5m check if the deployment finished
/loop 20m /review-pr 1234
```

Interval syntax: `30m`, `2h`, `1d`. Defaults to 10m if omitted.

### One-Time Reminders

```
remind me at 3pm to push the release branch
in 45 minutes, check whether tests passed
```

### Scheduling Options Comparison

| | Cloud | Desktop | /loop |
|---|---|---|---|
| Runs on | Anthropic cloud | Your machine | Your machine |
| Requires open session | No | No | Yes |
| Persistent across restarts | Yes | Yes | No |
| Minimum interval | 1 hour | 1 minute | 1 minute |

### Underlying Tools

- `CronCreate` — schedule with 5-field cron expression
- `CronList` — list all scheduled tasks
- `CronDelete` — cancel by ID

### Limitations

- Session-scoped only (exit = gone)
- No catch-up for missed fires
- Max 50 tasks per session
- 3-day auto-expiry for recurring tasks
- Disable with `CLAUDE_CODE_DISABLE_CRON=1`
