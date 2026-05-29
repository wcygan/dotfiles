# Pilot and refine

How to drive pi against the local model, read what happened, and tighten the skill — plus the optional Codex co-authoring step. For pi internals beyond what's here, see the `pi-coding-agent` skill.

Table of contents:
- [Preflight](#preflight)
- [Pilot commands](#pilot-commands)
- [Reading the transcript](#reading-the-transcript)
- [The refine loop](#the-refine-loop)
- [Codex co-authoring](#codex-co-authoring)

## Preflight

Confirm the local server is up (this machine: llama.cpp on `:8080`, pi default provider `llamacpp`):

```bash
curl -s --max-time 2 http://127.0.0.1:8080/v1/models | jq -r '.data[].id' || echo "start llama.cpp first"
```

Confirm pi can see the skill you placed:

```bash
pi --no-session -p "List your available skills" | grep -i <name> || echo "pi does not see <name> — check placement and the skills array in ~/.pi/agent/settings.json"
```

## Pilot commands

Always pin the skill with `/skill:<name>` and use `--no-session` while iterating, so each run is clean and you're testing the *content*, not whether the model discovered it.

```bash
# Simplest: run the skill once with the local default model
pi --no-session -p "/skill:<name>"

# Pass arguments (appended to the skill as a user turn)
pi --no-session -p "/skill:<name> some-argument"

# Read-only pilot — for skills that must not write (repo-recon, commit-draft)
pi --no-session --tools read,grep,find,ls -p "/skill:<name>"

# Pin a specific local model (compare a smaller executor against the default)
pi --no-session --provider llamacpp --model "unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL" -p "/skill:<name>"

# Capture the full event stream for inspection (one JSON object per line)
pi --no-session --mode json -p "/skill:<name>" > /tmp/<name>.jsonl
```

A skill that only *reads/transforms* (commit-draft, changelog, repo-recon) is safe to pilot anywhere. A skill that *edits* (fish-shortcut) — pilot it on a throwaway branch or a copy so a bad run is trivially reverted:

```bash
git switch -c pilot/<name> && pi --no-session -p "/skill:<name> …" ; git diff
```

## Reading the transcript

The point of piloting is to find **where the small model deviated from the procedure** — that deviation is your next edit. From the JSON stream:

```bash
# What tools did it call, in order? (deviations show up as wrong/missing/extra calls)
jq -r 'select(.type=="tool_call") | .name + " " + (.arguments|tostring)' /tmp/<name>.jsonl

# What did it finally output? (check against the skill's output contract)
jq -r 'select(.type=="assistant_message") | .content' /tmp/<name>.jsonl | tail -1
```

Map each failure to a fix:

| Symptom in transcript | Root cause | Fix in SKILL.md |
|-----------------------|------------|-----------------|
| Skipped a step | step was implicit / phrased as optional | make it an explicit numbered command with a condition |
| Invented a value/flag | open-ended choice | replace with a closed enumeration |
| Wrong output format | no contract | add an exact output template + "print only this" |
| Over-ran / kept going | no stop condition | add "if X, stop" and a self-check terminator |
| Edited unrelated lines | no scope fence | add "do not modify other lines" + a diff-stat self-check |
| Confident but wrong, no error | no validator | add a machine-checkable validator — or move the task to a frontier model |

## The refine loop

```
- [ ] Pilot with /skill:<name> --no-session, capture --mode json
- [ ] Find the first deviation in the tool-call/output stream
- [ ] Apply the single smallest SKILL.md edit that prevents it (see table)
- [ ] Re-pilot. Stop when N consecutive clean runs (3 is a good bar for a skill you'll trust)
```

Change **one thing per iteration** so you know which edit fixed (or broke) the run. "Converged" means repeated runs produce a passing self-check and a correctly-shaped output — not one lucky run.

## Codex co-authoring

A second model surfaces procedure gaps the original author is blind to. Use the **`consult-codex`** skill (read-only `codex exec --sandbox read-only` by default) at two points:

- **Before piloting — get an independent draft or critique.** Ask Codex to either draft the SKILL.md from the same spec, or critique your draft specifically for *small-model executability*. A useful prompt to hand `consult-codex`:

  > "Critique this SKILL.md for execution by a small local model (Qwen-27B via pi). Flag every step that relies on judgment, lacks an exact command, has no stop condition, or can't be machine-validated. Suggest the closed-list or validator replacement for each."

- **After a stubborn failure — get a second opinion on the deviation.** Paste the transcript excerpt and the current SKILL.md; ask Codex why the small model deviated and what single edit fixes it.

**Reconcile, don't concatenate.** Take Codex's flagged steps and validator suggestions, keep the version with the tightest closed lists and the strongest validator, and discard anything that adds freedom. Two authors converging on a *narrower* bridge is the goal; if a suggestion widens it, drop it.
