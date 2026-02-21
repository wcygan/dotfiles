# Investigation Summarizer

The Summarizer is not a separate agent — it's the synthesis step performed by the orchestrator after all agents return. This reference describes how to combine findings.

## Synthesis Process

### Step 1: Deduplicate

Agents will discover overlapping information. Remove duplicates, keeping the version with the most detail and the best file:line reference.

### Step 2: Cross-Reference

Look for connections between agent findings:
- Scout found a hot spot → does the Tracer's call chain pass through it?
- Tracer found an entry point → does the Archaeologist have history on it?
- Boundary Mapper found an integration → does the Tracer show how it's used?

Mark cross-references explicitly: "The Tracer's call chain confirms the Scout's hot spot at `processor.rs:30`."

### Step 3: Conflict Resolution

If agents disagree (rare but possible):
- **Structure vs. behavior**: Trust the Tracer for "how it works", the Scout for "where things are"
- **Current vs. historical**: Note both — "Currently X (per Tracer), historically was Y (per Archaeologist)"
- **Never silently discard a finding** — if an agent found something contradictory, surface it

### Step 4: Narrative Assembly

Weave the findings into a coherent story:

1. **Start with the Scout's map** — orient the reader in the codebase
2. **Zoom into the Tracer's path** — show how the specific thing works
3. **Add the Archaeologist's context** — explain why it's like this (if spawned)
4. **Show the Boundary Mapper's connections** — place it in the larger system (if spawned)

### Step 5: Gap Identification

After synthesis, note what remains unknown:
- Areas the agents didn't explore
- Questions that arose during investigation
- Deeper topics the user might want to follow up on

## Quality Checklist

- [ ] Every factual claim has a `file:line` reference
- [ ] The TL;DR can stand alone — a reader who stops there still gets value
- [ ] Code snippets are included for non-obvious logic
- [ ] The file map is complete for the explored area
- [ ] Cross-references between agent findings are explicit
- [ ] Gaps and follow-up questions are noted
