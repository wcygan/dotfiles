---
name: new-global-command
description: "Route a reusable command or slash-command request to the authoritative agent-skills repository; retain dotfiles-only workflows under .agents/skills."
---

# New Global Command Compatibility Skill

Requests for a reusable global command are requests for a reusable skill.
Dotfiles is not the source, installer, or validator for global skills.

1. Gather the skill's name, purpose, triggers, inputs, and required resources.
2. If it is portable across repositories, create or update it in the dedicated
   `agent-skills` repository using that repository's current instructions.
3. If it only governs this checkout, create it under `.agents/skills/` here.
4. Do not create legacy command files, global skill directories, vendor
   metadata, or installer links in this repository.
5. Report the destination, an invocation example, and the validation performed.
