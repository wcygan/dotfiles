---
title: Team Workflow
description: How to create, coordinate, and shut down the decorator agent team
tags: [team, agents, workflow, coordination, TeamCreate, SendMessage]
---

# Team Workflow

## Step 1 — Create the Team

```
TeamCreate(
  team_name="ctx-decorate-<unix-timestamp>",
  description="Writing CLAUDE.md context files for undecorated directories"
)
```

Use a timestamp suffix to avoid name collisions across invocations.

## Step 2 — Create Tasks

Before spawning agents, register each batch as a task so progress is trackable:

```
TaskCreate(subject="Decorate batch 1: src/, lib/", description="...")
TaskCreate(subject="Decorate batch 2: config/, scripts/", description="...")
```

## Step 3 — Spawn Agents (in parallel)

Spawn all agents in a **single message** so they run concurrently:

```
Task(
  subagent_type="general-purpose",
  team_name="ctx-decorate-<timestamp>",
  name="decorator-1",
  prompt="""
You are a context decorator agent on the ctx-decorate team.

Write a CLAUDE.md file for each of these directories:
- /path/to/src
- /path/to/lib

For each directory:
1. Use Glob and Read to examine its contents (entry points, manifests, READMEs)
2. Write a CLAUDE.md (under 40 lines) with:
   - 1-2 sentence overview
   - ## Contents: bullet list of key files and subdirs
   - ## Usage: how it fits in the larger project
3. Do NOT create a CLAUDE.md if one already exists

After writing all files, send a message to your team lead summarizing:
- Which CLAUDE.md files you created
- Any directories you skipped and why

Content guidelines: [content-guidelines](content-guidelines.md)
  """
)
```

Repeat for each batch, incrementing the agent name (`decorator-2`, `decorator-3`, …).

## Step 4 — Wait for Reports

Agents send messages when done. Wait for all to report before summarizing results.
If an agent goes quiet, check if its task was completed via TaskList.

## Step 5 — Shutdown & Cleanup

Send shutdown requests to each agent:

```
SendMessage(type="shutdown_request", recipient="decorator-1", content="All done, shutting down")
SendMessage(type="shutdown_request", recipient="decorator-2", content="All done, shutting down")
```

After all agents acknowledge, call `TeamDelete` to remove team resources.

## Batch Size Reference

| Undecoreated dirs | Agents to spawn | Dirs per agent |
|-------------------|-----------------|----------------|
| 1–3               | 1               | 1–3            |
| 4–6               | 2               | 2–3            |
| 7–12              | 3               | 3–4            |
| 13+               | 4               | 3–4            |

Cap at 4 agents to stay within reasonable resource limits.
