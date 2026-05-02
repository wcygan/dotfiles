#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""SessionStart hook: inject the vendored superpowers-using-superpowers skill
content into the model's context.

This is a port of obra/superpowers' hooks/session-start (bash) script.
Rewritten in Python so the JSON escaping is handled by json.dumps and the
behavior is easy to audit.

Reads:  ~/.claude/skills/superpowers-using-superpowers/SKILL.md
Emits:  JSON with hookSpecificOutput.additionalContext (Claude Code format).

Fail-quiet: if the skill file is missing, exit 0 with empty output rather
than error out — a missing vendor file should never break session start.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

SKILL_PATH = Path.home() / ".claude/skills/superpowers-using-superpowers/SKILL.md"


def main() -> int:
    if not SKILL_PATH.is_file():
        return 0

    skill_content = SKILL_PATH.read_text()
    context = (
        "<EXTREMELY_IMPORTANT>\n"
        "You have superpowers.\n\n"
        "**Below is the full content of your 'superpowers-using-superpowers' "
        "skill - your introduction to using skills. For all other skills, "
        "use the 'Skill' tool:**\n\n"
        f"{skill_content}\n"
        "</EXTREMELY_IMPORTANT>"
    )

    payload = {
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context,
        }
    }
    json.dump(payload, sys.stdout)
    return 0


if __name__ == "__main__":
    sys.exit(main())
