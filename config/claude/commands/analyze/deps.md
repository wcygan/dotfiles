---
description: Analyze project dependencies and versions
allowed-tools: Bash(fd:*), Read, WebFetch
argument-hint: <path>
---

## Context
- Target: ${1:-.}
- Manifests: !`fd -g "{package.json,Cargo.toml,go.mod,flake.nix,deno.json}" ${1:-.} -d 2`

## Task
Analyze dependencies:

1. Identify package manager and manifest files
2. List direct dependencies with versions
3. Check for outdated or vulnerable packages (use WebFetch if needed)
4. Note any dependency conflicts or issues
5. For Nix projects, show flake inputs

Focus on actionable insights.
