---
name: new-global-command
description: "Route a reusable command or slash-command request to the authoritative agent-skills repository; retain dotfiles-only workflows under .agents/skills."
---

# New Global Command Compatibility Skill

Requests for a reusable global command are requests for a reusable skill.
Dotfiles is not the source or provider-side validator for global skills; it
consumes the authoritative catalog through `$agent-skills-integration`.

1. Gather the skill's name, purpose, triggers, inputs, and required resources.
2. If it is portable across repositories, create or update it in the dedicated
   `agent-skills` repository using that repository's current instructions.
3. If it only governs this checkout, create it under `.agents/skills/` here.
4. Use `$agent-skills-integration` to advance the pinned consumer and install or
   verify the user-scope catalog when that work is requested.
5. Do not create legacy command files, mirrored global skill directories,
   vendor metadata, or per-skill installer links in this repository.
6. Report the source destination, invocation example, consumer pin impact, and
   validation performed.
