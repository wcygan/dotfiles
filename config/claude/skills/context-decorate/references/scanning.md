---
title: Scanning & Filtering
description: How to enumerate directories and decide which need a CLAUDE.md
tags: [scanning, filtering, discovery, glob]
---

# Scanning & Filtering

## Enumerate Candidate Directories

Use Bash to find subdirectories at depth 1 and 2:

```bash
# All subdirs up to depth 2 relative to target
find <target> -mindepth 1 -maxdepth 2 -type d
```

## Skip Rules

Exclude any directory whose **name** matches:

| Category           | Names to skip                                              |
|--------------------|------------------------------------------------------------|
| VCS / packages     | `.git`, `node_modules`, `vendor`, `bower_components`       |
| Hidden dirs        | anything starting with `.` (`.cache`, `.venv`, `.direnv`)  |
| Build output       | `dist`, `build`, `target`, `out`, `.next`, `.nuxt`, `__pycache__` |

## Filter Logic

For each candidate directory `d`:

1. Does `d/CLAUDE.md` already exist? → **skip** (already decorated)
2. Does `d`'s basename match any skip rule? → **skip**
3. Is `d` entirely empty (no files or subdirs)? → **skip**
4. Otherwise → **add to work list**

## Batching

Split the work list into batches of 2–4 directories per agent:

```
N dirs → spawn ceil(N / 3) agents
```

Example: 9 undecoreated dirs → 3 agents, each handling 3 dirs.

## Shell One-Liner (for orchestrator)

```bash
# Find dirs at depth 1-2, skip common noise, check for missing CLAUDE.md
find <target> -mindepth 1 -maxdepth 2 -type d \
  | grep -Ev '/(\.git|node_modules|vendor|\..*|dist|build|target|out|__pycache__)(/|$)' \
  | while read d; do [ ! -f "$d/CLAUDE.md" ] && echo "$d"; done
```
