---
description: Generate Dockerfile for project
allowed-tools: Bash(fd:*), Read, Write
argument-hint: <project-path>
---

## Context
- Target: $ARGUMENTS
- Project files: !`fd -g "{package.json,Cargo.toml,go.mod,flake.nix,deno.json}" ${1:-.} -d 2`

## Task
Create Dockerfile with:
- Multi-stage build if applicable
- Non-root user for security
- Appropriate base image for detected language/framework
- .dockerignore file
