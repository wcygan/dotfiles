# Body Structure Conventions

The Hermes docs recommend a consistent body structure for `SKILL.md`.
Following the convention helps the agent pick the right skill from
`skills_list` and locate information inside via `skill_view`.

## Canonical section order

```markdown
## When to Use
## Procedure
## Pitfalls
## Verification
```

Optional extras (add only when they carry weight):

- `## Inputs` — if the skill expects specific arguments or file context.
- `## Outputs` — if it produces artifacts the user should know where to find.
- `## Examples` — one or two concrete invocations.
- `## Related` — links to sibling skills.

## When to Use

One short paragraph (3-5 sentences max). State the trigger scenarios concretely.
Match phrasing users would actually say.

Good:

> Use when a Kubernetes pod is failing to start (CrashLoopBackOff, Pending,
> ImagePullBackOff) and you need to collect logs, events, and describe output
> in one pass before deciding whether it's an image, config, or scheduling
> issue.

Bad:

> This skill helps with Kubernetes.

## Procedure

Numbered steps. Link to `references/*.md` for anything over ~10 lines.

```markdown
## Procedure

1. Identify the pod and namespace. If the user hasn't specified, run
   `kubectl get pods -A` and ask.
2. Run the diagnostic bundle (see [references/kubectl-bundle.md](references/kubectl-bundle.md)):
   logs, describe, events, owning ReplicaSet.
3. Interpret the output using the decision tree in
   [references/decision-tree.md](references/decision-tree.md).
4. Propose a fix with a specific `kubectl edit` or manifest change.
```

**Steps should be imperative.** "Run X", "Check Y", "Propose Z" — not "You
might want to consider running X."

## Pitfalls

Bulleted list of known failure modes and how to avoid them. This is the
highest-ROI section because it's content the agent cannot derive elsewhere.

```markdown
## Pitfalls

- `kubectl logs` on a crash-looping pod returns nothing useful without
  `--previous` — always try both.
- `describe pod` truncates long events. Use `kubectl get events --sort-by
  .metadata.creationTimestamp -n <ns>` for the full history.
- Don't `kubectl delete` the pod before collecting diagnostics — you'll
  destroy the evidence.
```

## Verification

How the user (or the agent, reflexively) confirms the skill succeeded.

```markdown
## Verification

- `kubectl get pod <name>` shows `Running` and `1/1 Ready`.
- `kubectl logs <name>` shows application startup messages.
- The original failure mode (CrashLoopBackOff, etc.) is no longer present
  in `kubectl get events`.
```

Machine-verifiable signals beat "please double-check your work" by a wide
margin.

## Length budget

- SKILL.md body: **under 500 lines**. If you're over, move content into
  `references/`.
- Each `references/*.md`: **under 500 lines**. Over 100 lines, add a ToC.
- Never chain references (SKILL.md → a.md → b.md). Keep references one level
  deep; link from SKILL.md directly.

## Terminology discipline

Pick one name per concept and stick with it. Don't alternate "pod" / "workload"
/ "container" if you mean the same thing. Inconsistency forces the agent to
guess.
