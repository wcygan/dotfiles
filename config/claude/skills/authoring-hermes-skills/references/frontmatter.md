# Hermes SKILL.md Frontmatter Reference

Complete field list for Hermes Agent `SKILL.md` files. Only `name` and
`description` are required; everything else is optional and should be added
deliberately.

## Table of contents

- [Required fields](#required-fields)
- [Identity and versioning](#identity-and-versioning)
- [Platform restriction](#platform-restriction)
- [Metadata block](#metadata-block)
- [Required environment variables](#required-environment-variables)
- [Full example](#full-example)

## Required fields

```yaml
---
name: skill-identifier        # kebab-case, unique within its category
description: >                # one-sentence summary shown in skills_list
  What it does and when to use it.
---
```

Both must be present. Empty `description` breaks discovery — the agent selects
skills from `skills_list` summaries, so a vague description means your skill
never gets invoked.

## Identity and versioning

```yaml
version: 1.0.0                # semver, optional but recommended once stable
```

The hub uses `version` for update detection (`hermes skills check`, `hermes
skills update`). Bump it whenever you change SKILL.md body or any reference
file.

## Platform restriction

```yaml
platforms: [macos, linux]     # subset of: macos, linux, windows
```

Only include when the skill genuinely cannot run on the omitted platforms
(e.g., uses `osascript`, `pbcopy`, `apt`, platform-specific CLIs). Omit the
field entirely to make the skill universally available — do **not** write
`platforms: [macos, linux, windows]`.

## Metadata block

All Hermes-specific metadata lives under `metadata.hermes`:

```yaml
metadata:
  hermes:
    category: devops                      # filesystem category (matches dir)
    tags: [kubernetes, deployment]        # freeform, used for hub search
    fallback_for_toolsets: [kubernetes]   # show only when toolset absent
    requires_toolsets: [kubernetes]       # show only when toolset present
    fallback_for_tools: [kubectl]         # individual-tool equivalents
    requires_tools: [kubectl]
```

**Rules:**

- `category` should match the parent directory name on disk. Hermes does not
  magically derive it.
- `fallback_for_*` and `requires_*` are mutually exclusive for any given
  toolset/tool — don't list the same name in both.
- `tags` are free-form; pick ones a user would actually type into
  `hermes skills search`.

See [conditional-activation.md](conditional-activation.md) for the full
semantics of the `fallback_for_*` / `requires_*` fields.

## Required environment variables

```yaml
required_environment_variables:
  - name: OPENAI_API_KEY
    prompt: Enter your OpenAI API key
    help: https://platform.openai.com/api-keys
    required_for: GPT-based analysis in this skill
  - name: ANOTHER_VAR
    prompt: ...
    help: ...
    required_for: ...
```

On first use, Hermes prompts the user interactively for any variable listed
here that isn't already set. Prefer this over raising errors from procedure
steps — the UX is much better and the value gets persisted via the normal env
loading rules.

**Field meanings:**

- `name` — the env var name as the skill will read it.
- `prompt` — short user-facing label for the interactive prompt.
- `help` — URL or short string telling the user how to obtain the value.
- `required_for` — one-line context on what in the skill uses it.

## Full example

```yaml
---
name: k8s-debug-pod
description: >
  Debug a failing Kubernetes pod by collecting logs, events, and describe
  output across its owning ReplicaSet and Deployment. Use when a pod is
  CrashLoopBackOff, Pending, ImagePullBackOff, or failing readiness.
version: 1.2.0
platforms: [macos, linux]
metadata:
  hermes:
    category: devops
    tags: [kubernetes, k8s, debugging, kubectl]
    requires_toolsets: [kubernetes]
required_environment_variables:
  - name: KUBECONFIG
    prompt: Path to your kubeconfig file
    help: https://kubernetes.io/docs/concepts/configuration/organize-cluster-access-kubeconfig/
    required_for: Targeting the correct cluster
---
```
