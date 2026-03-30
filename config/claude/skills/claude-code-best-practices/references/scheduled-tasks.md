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

### The Power Pattern: Skills + Loops

Turn workflows into skills, then run them on loops. This combines reusable automation with periodic execution:

```
# PR babysitter — auto-addresses review comments, rebases, shepherds to merge
/loop 5m /babysit

# Feedback harvester — monitors Slack and puts up PRs for feedback
/loop 30m /slack-feedback

# Post-merge sweeper — catches missed review comments after merge
/loop /post-merge-sweeper

# PR pruner — closes stale or unnecessary PRs
/loop 1h /pr-pruner
```

**How to build this pattern:**

1. Package your workflow as a skill (`SKILL.md` with clear instructions)
2. Test it manually: `/my-skill`
3. Put it on a loop: `/loop 5m /my-skill`
4. Iterate: refine the skill based on what the loop reveals

### Cloud and Desktop Scheduled Tasks

For durable scheduling that survives restarts:

- **Cloud** (`/schedule`): runs on Anthropic infrastructure, works even when machine is off, minimum 1-hour interval
- **Desktop**: runs on your machine via the Desktop app, 1-minute minimum interval, access to local files
- **GitHub Actions**: tied to repo events or cron schedules in CI

Configure cloud tasks with `/schedule` or at claude.ai/code. Desktop tasks are configured in the Desktop app's scheduled tasks UI.

### Underlying Tools

- `CronCreate` — schedule with 5-field cron expression
- `CronList` — list all scheduled tasks
- `CronDelete` — cancel by ID

### Limitations

- Session-scoped only for `/loop` (exit = gone)
- No catch-up for missed fires
- Max 50 tasks per session
- 3-day auto-expiry for recurring tasks
- Disable with `CLAUDE_CODE_DISABLE_CRON=1`
