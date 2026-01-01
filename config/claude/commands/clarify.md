---
allowed-tools: AskUserQuestion
description: Ask 3-4 clarifying questions about a feature proposal
---

The user is proposing a feature or change. Your goal: surface the 3-4 most important unknowns through targeted questions.

**Question priorities (select from these categories):**
1. **Scope boundaries** — What's explicitly NOT included?
2. **Failure/edge cases** — What happens when inputs are invalid, empty, or exceed limits?
3. **Integration** — What existing code, data, or systems does this touch?
4. **UX surprises** — What behavior might confuse or frustrate users?

**Rules:**
- Ask 1-4 questions in a SINGLE numbered list via AskUserQuestion
- Only ask what's truly unclear — skip categories the proposal already addresses
- Each question should be specific, concise, and non-obvious
- Fewer questions is better if the proposal is already clear

**After gathering answers, provide a compact summary:**

```
## Clarified
- [Key decision 1]
- [Key decision 2]
- [Key decision 3]

## Watch Out For
- [Remaining risk or open question, if any]

## Ready to proceed: Yes / Needs X first
```

No file output. Purely conversational.
