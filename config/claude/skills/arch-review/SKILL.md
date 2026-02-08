---
name: arch-review
description: RFC-style review of major technical decisions using a 5-agent debate team. Spawns tech-lead, security-auditor, performance-analyst, reliability-engineer, and devils-advocate for independent analysis followed by structured discussion. Produces decision document with pros/cons, dissenting opinions, and recommendation. Use for architecture decisions, technology selection, major refactors, design reviews. Keywords: architecture, RFC, design review, technical decision, architecture review, design decision, major change
disable-model-invocation: true
argument-hint: [proposal-description or path-to-RFC]
context: fork
---

# Architecture Review (RFC Pattern)

Orchestrate a 5-agent team for RFC-style technical decision reviews. Agents review independently, then debate trade-offs in structured discussion.

## Workflow

### 1. Parse Target

Extract the proposal from `$ARGUMENTS`. This could be:
- Path to an RFC document (e.g., `.claude/rfcs/001-new-api.md`)
- Path to a design document or ADR
- Inline description of the proposed change
- GitHub issue/PR number containing the proposal

If a path is provided, read the file. If it's a description, use it directly. If it's an issue/PR, fetch it with `gh`.

### 2. Spawn Review Team

Use the Teammate tool with operation `spawnTeam` to create the review team:

```fish
team_name: arch-review
description: RFC review for [proposal-name]
```

Then spawn 5 teammates using the Task tool, one for each agent type:

**Team composition:**
1. **tech-lead**: Overall architecture, team impact, maintainability
2. **security-auditor**: Security implications, threat model, attack surface
3. **performance-analyst**: Scalability, efficiency, resource usage
4. **reliability-engineer**: Failure modes, observability, operational complexity
5. **devils-advocate**: Necessity, simpler alternatives, hidden assumptions

### 3. Independent Review Phase

Create 5 tasks (one per agent) using TaskCreate. Each task should have:

**subject**: `Review [proposal] as [agent-role]`
**description**: Full proposal context + agent-specific review checklist (see REFERENCE.md)
**activeForm**: `Reviewing as [agent-role]`

Assign each task to the corresponding agent using TaskUpdate with `owner` field.

**CRITICAL**: Include the full proposal text in each task description. Agents don't share context, so each needs complete information.

### 4. Collect Independent Reviews

Wait for all 5 agents to complete their reviews. Each agent should produce:

```markdown
## [Agent Role] Review

### Assessment
[Overall judgment: Approve / Approve with conditions / Reject]

### Key Concerns
- [Prioritized list of concerns]

### Trade-offs Identified
- [Trade-offs specific to this lens]

### Questions for Team
- [Questions to raise in debate]

### Recommendation
[What this agent thinks should happen and why]
```

As agents complete, use TaskList to track progress and read their outputs.

### 5. Facilitate Structured Debate

Once all reviews are in, create a debate task. This can be a broadcast message or a new task assigned to tech-lead to facilitate.

**Debate structure:**

1. **Opening round**: Each agent states their key concern (1 min each)
2. **Trade-off discussion**: Focus on the top 3 conflicts identified across reviews
   - Example: security-auditor wants more encryption, performance-analyst warns of latency cost
3. **Alternative exploration**: devils-advocate presents simpler alternatives, team responds
4. **Consensus building**: What do we agree on? What remains contentious?
5. **Final positions**: Each agent gives final recommendation (Approve/Conditional/Reject)

Facilitate this by sending targeted messages:
- Ask agents to respond to each other's concerns
- Highlight conflicts that need resolution
- Push for concrete recommendations, not just analysis

### 6. Synthesize Decision Document

Consolidate findings into an RFC-style decision document:

```markdown
# Architecture Review: [Proposal Name]

**Date**: [current date]
**Reviewers**: tech-lead, security-auditor, performance-analyst, reliability-engineer, devils-advocate
**Proposal**: [one-line summary]

## Executive Summary

[2-3 sentences: What's being proposed, overall recommendation, biggest trade-off]

## Recommendation

**Decision**: [Approve / Approve with conditions / Reject / Need more information]

**Confidence**: [High / Medium / Low]

**Conditions** (if applicable):
1. [Must-have changes before approval]
2. [...]

## Review Summary

### Consensus Points
- [Things all agents agreed on]

### Key Trade-offs

#### [Trade-off 1: e.g., Security vs Performance]
- **security-auditor**: [position]
- **performance-analyst**: [position]
- **Resolution**: [recommended approach]

#### [Trade-off 2]
- **[agent]**: [position]
- **[agent]**: [position]
- **Resolution**: [recommended approach]

### Dissenting Opinions

**[Agent role]** disagrees because:
- [Key concern]
- [Recommended alternative]

### Questions Requiring Clarification
1. [Unresolved questions from the review]
2. [...]

## Detailed Findings

### Architecture (tech-lead)
[Summary of tech-lead's assessment]

### Security (security-auditor)
[Summary of security concerns and mitigations]

### Performance (performance-analyst)
[Summary of performance implications]

### Reliability (reliability-engineer)
[Summary of operational concerns]

### Simplicity (devils-advocate)
[Summary of complexity concerns and alternatives]

## Action Items

### Before Approval
1. [Must-do items]

### Post-Approval
1. [Follow-up work if approved]

### If Rejected
1. [What to do instead]

## Appendix: Individual Reviews

[Include full reviews from each agent for reference]
```

### 7. Cleanup

After synthesizing the decision document, gracefully shut down all teammates using SendMessage with `type: "shutdown_request"` for each agent.

Then use the Teammate tool with `operation: "cleanup"` to clean up team resources.

## Output Guidelines

- **Be decisive**: The team should converge on a clear recommendation, not "it depends"
- **Highlight conflicts**: Disagreements between agents are valuable signals
- **Preserve dissent**: If one agent strongly disagrees, document their reasoning
- **Actionable**: Conditions for approval should be concrete and testable
- **Time-boxed**: If debate stalls after 3 rounds, call for final votes

## Notes

- Agents may update their positions during debate — capture both initial and final stances
- The tech-lead doesn't override other agents; they're peers in the discussion
- If all 5 agents agree (rare), document why and check for groupthink
- Include the decision document in `.claude/decisions/` or `docs/adr/` if appropriate

## Related Files

- `REFERENCE.md`: Detailed review checklists for each agent role
