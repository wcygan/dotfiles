---
title: Error Recovery
description: How to handle search failures, source issues, and stuck states during the research loop
tags: [error, recovery, stuck, gaps]
---

# Error Recovery

## WebSearch returns no useful results

1. Rephrase the query using a different angle (see Search Strategy Progression in loop-protocol.md)
2. Try broader or narrower scope
3. If 2 rephrases fail, log as `gap` and move to next checklist item
4. Return to this item later with a completely different framing

## WebFetch fails (timeout, 403, paywall)

1. Try a different URL from the search results
2. If the source is paywalled, note it and look for summaries or discussions about it
3. If all fetches fail, rely on search snippets only (mark findings as lower confidence)

## Source contradicts prior validated finding

Do NOT discard the prior finding. Instead:
1. Re-read both sources carefully
2. Check dates, authority, and context
3. Update the knowledge artifact to reflect the contradiction
4. Mark the checklist item as `contested` instead of `validated`

## Stuck state: 3 consecutive gaps

1. **Pause and review**: Read the entire knowledge artifact and results log
2. **Diagnose**: Are the remaining items too niche? Too broad? Poorly framed?
3. **Reframe**: Rewrite the remaining checklist items with different wording or scope
4. **Try one more iteration** with the reframed items
5. If still stuck, mark remaining items as "insufficient sources available" and proceed to Phase 4

## Knowledge artifact becomes disorganized

If findings start sprawling:
1. Re-read the entire artifact
2. Consolidate redundant findings
3. Ensure each finding is under the correct checklist item
4. Remove any findings that lost their source citations

## Topic scope creep

If research is expanding beyond the original objective:
1. Re-read the original research objective
2. Note the tangent as a "Suggested Follow-Up" item
3. Return focus to uncovered checklist items
4. Do NOT add new checklist items mid-loop unless critical gaps were missed in framing
