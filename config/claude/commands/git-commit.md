---
description: Stage all changes and commit with semantic message based on changes
---

Analyze the current git changes, stage everything, and create a proper semantic commit message.

**Workflow:**
1. Run `git status` to see what's changed
2. Run `git diff` to analyze the actual changes
3. Determine the appropriate semantic commit type:
   - `feat:` - New feature or functionality
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code restructuring without behavior change
   - `test:` - Adding or updating tests
   - `chore:` - Tooling, dependencies, config changes
   - `perf:` - Performance improvements
   - `style:` - Formatting, whitespace, etc.
4. Craft a concise commit message (50 chars max for subject)
5. Stage all changes with `git add -A`
6. Commit with the generated message

**Message format:**
```
<type>: <subject>

<optional body with details>
```

**Rules:**
- Subject line: imperative mood, lowercase, no period
- Body: explain *what* and *why*, not *how*
- If multiple unrelated changes, suggest splitting into separate commits
- Show the proposed message and ask for confirmation before committing

**Safety:**
- Show full diff summary before committing
- Warn if committing to main/master branch
- Warn if there are unstaged files being added
- Allow user to edit message before final commit
