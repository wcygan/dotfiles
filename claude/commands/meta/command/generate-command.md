**Goal**
Add a reusable project-level slash command so anyone who clones your repo can invoke it with `/project:<name>` inside the Claude Code CLI.

---

## 1 Decide what the command should do

- **Name** → becomes the slash-command (`<file>.md` → `/project:<file-name>`).
- **Prompt text** → the body of the `.md` file; that text is sent to Claude when the command runs.
- **Parameters** (optional) → use the special token `$ARGUMENTS` to splice user-supplied arguments into the prompt.
- **Scope** → anything in `./.claude/commands/**` is project-scoped; nested folders add extra path segments (`frontend/build.md` → `/project:frontend:build`). ([docs.anthropic.com][1])

> **Clarify**: What action do you want this command to automate? (e.g., “spin up a dev container”, “generate a PR template”, “audit code for security issues”).

---

## 2 Scaffold the directory (one-time)

```bash
mkdir -p .claude/commands
```

---

## 3 Create the command file

### Simple, no parameters

`./.claude/commands/audit-security.md`

```md
Audit this repository for security vulnerabilities:

1. Identify common CWE patterns in the code.
2. Flag third-party dependencies with known CVEs.
3. Output findings as a Markdown checklist.
```

Run it:

```bash
claude > /project:audit-security
```

### Parameterised

`./.claude/commands/fix-issue.md`

```md
Fix issue #$ARGUMENTS.\
Steps:

1. Read the ticket description.
2. Locate the relevant code.
3. Implement a minimal fix with tests.
4. Output a concise PR body with changelog notes.
```

Invoke with an argument:

```bash
claude > /project:fix-issue 417
```

`$ARGUMENTS` is replaced by `417` at runtime. ([docs.anthropic.com][1])

---

## 4 (Optionally) add lightweight metadata

Claude ignores Markdown comments, so you can embed front-matter for human readers or tooling:

```md
<!--
name: audit-security
owner: dev-infra
tags: security, ci
-->

...prompt text...
```

---

## 5 Version-control it

```bash
git add .claude/commands
git commit -m "feat: add /project:audit-security command"
```

Everyone who pulls the repo now has access.

---

### Alternative patterns & trade-offs

| Pattern                                                 | Pros                                     | Cons                                            |
| ------------------------------------------------------- | ---------------------------------------- | ----------------------------------------------- |
| **One-file-per-command (above)**                        | Simple, explicit, Git-friendly           | Many small files if you create lots of commands |
| **Directory sub-grouping**                              | Logical namespaces (`frontend/`, `ops/`) | Slightly longer slash-path                      |
| **Templated prompts with multiple `$ARGUMENTS` tokens** | Flexible (e.g., `$1`, `$2` style)        | Harder for newcomers to infer correct usage     |
| **Personal commands (`~/.claude/commands`)**            | Portable across projects                 | Not shared with the team                        |

---

## Next step

Let me know the **specific task** you’d like your new command to perform and the **params** (if any). I’ll draft the exact `.md` file contents for you.

[1]: https://docs.anthropic.com/en/docs/claude-code/tutorials "Tutorials - Anthropic"
