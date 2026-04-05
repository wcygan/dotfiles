---
name: talos
description: Talos Linux expert for cluster documentation lookup and read-only talosctl diagnostics. Auto-loads when the user explicitly mentions Talos, talosctl, or Sidero Labs — covers machine config schema, networking (bonds, VLANs, static IPs, kubespan), cluster health checks, node inspection, and upgrade planning. Read-only scope only — does NOT run destructive verbs (apply-config without dry-run, upgrade, reset, bootstrap). Keywords: talos, talosctl, siderolabs, machineconfig, controlplane.yaml, worker.yaml, talconfig, kubespan, machine config, talos networking, talos upgrade
allowed-tools: Read, Grep, Glob, WebFetch, Bash(talosctl version:*), Bash(talosctl health:*), Bash(talosctl get:*), Bash(talosctl read:*), Bash(talosctl logs:*), Bash(talosctl service:*), Bash(talosctl dashboard:*), Bash(talosctl validate:*), Bash(talosctl containers:*), Bash(talosctl memory:*), Bash(talosctl cpu:*), Bash(talosctl disks:*), Bash(talosctl netstat:*), Bash(talosctl stats:*)
---

# Talos Linux

Talos is an immutable, minimal, API-driven Linux OS for Kubernetes. There is no shell on nodes — everything happens through `talosctl` against the gRPC machine API. Configuration is a single YAML document (`machineconfig`) applied atomically.

**Pinned docs version:** `v1.12` — base URL `https://docs.siderolabs.com/talos/v1.12/`
**Last verified:** 2026-04-04. If the user is on a different minor version, say so and update this file before trusting its URLs.

## Scope (read carefully)

This skill is **read-only**. It covers:

- Looking up machine config schema, networking fields, and upgrade procedures from the official docs
- Explaining `talosctl` commands and their output
- Running **non-destructive** `talosctl` verbs for diagnostics (see allowed-tools)
- Validating config files with `talosctl validate` and dry-runs

It does **NOT** cover — refuse or defer to explicit user invocation:

- `talosctl apply-config` without `--dry-run` (use `--mode=no-reboot --dry-run` for diffs)
- `talosctl upgrade`, `upgrade-k8s`
- `talosctl reset`, `bootstrap`, `etcd remove-member`
- `talosctl gen secrets --force` or any secret-overwriting command
- Cluster creation / destruction flows

When the user asks for one of these, explain what it would do (cite docs), show the exact command, and ask the user to run it themselves. Do not execute it.

## How to use the docs

When a user question touches a topic you are not 100% sure about (machine config field names, CLI flag spellings, upgrade ordering, network interface schema), **WebFetch the canonical doc page before answering**. Never guess YAML keys.

### URL map (v1.12)

Base: `https://docs.siderolabs.com/talos/v1.12/`

| Topic | Path |
|---|---|
| Getting started | `introduction/getting-started` |
| System requirements | `introduction/system-requirements` |
| Quickstart (Docker) | `introduction/quickstart` |
| Install overview | `talos-guides/install/` |
| `talosctl` reference | `reference/cli/` |
| Machine config reference | `reference/configuration/` |
| Networking guide | `talos-guides/network/` |
| Upgrading Talos | `talos-guides/upgrading-talos` |
| Upgrading Kubernetes | `kubernetes-guides/upgrading-kubernetes` |
| Disaster recovery | `advanced/disaster-recovery` |
| Resources (`talosctl get`) | `learn-more/resources` |

If a path 404s, fetch the docs root (`https://docs.siderolabs.com/talos/v1.12/`) and read the sidebar. Do not invent paths.

### When to WebFetch vs read local references

- **WebFetch** — machine config field schema, CLI flag signatures, upgrade procedures, anything version-sensitive, anything unfamiliar.
- **Local references/** — high-frequency cheatsheets that rarely change:
  - [`references/talosctl-readonly.md`](references/talosctl-readonly.md) — safe verbs, output patterns, common flags
  - [`references/machine-config.md`](references/machine-config.md) — top-level structure, common fields, validation recipe
  - [`references/networking.md`](references/networking.md) — interface patterns (static, DHCP, VLAN, bond, bridge) and common pitfalls
  - [`references/upgrades-readonly.md`](references/upgrades-readonly.md) — pre-flight checklist and version-skew rules (planning only, not execution)

## Common workflows (read-only)

### "Is my cluster healthy?"

```bash
talosctl version
talosctl health --server=false   # skip k8s checks, Talos-only
talosctl health                  # full check
talosctl get members             # cluster discovery
```

Explain any failures by reading `talosctl logs` for the relevant service.

### "What is node X doing?"

```bash
talosctl -n <node> dashboard           # interactive; user must run
talosctl -n <node> service             # list services + states
talosctl -n <node> logs <service>      # service logs
talosctl -n <node> containers          # running containers
talosctl -n <node> get staticpods      # control-plane pods
```

### "What's in the current machine config?"

```bash
talosctl -n <node> get machineconfig -o yaml
talosctl -n <node> read /etc/kubernetes/kubelet.conf    # any node file
```

See `references/talosctl-readonly.md` for the full safe-verb list.

### "Validate this config file before I apply it"

```bash
talosctl validate --config controlplane.yaml --mode metal
talosctl validate --config worker.yaml --mode metal
# Diff against live node (safe — dry-run, no reboot):
talosctl -n <node> apply-config --file new.yaml --mode=no-reboot --dry-run
```

The `--dry-run` here is the only `apply-config` form this skill runs. Anything without `--dry-run` requires the user to invoke it directly.

### "Plan an upgrade"

Read `references/upgrades-readonly.md` for the pre-flight checklist, then WebFetch the live upgrade guide to confirm current version-skew rules. Present the plan; do **not** run `talosctl upgrade`.

## Interacting with related skills

- A `kubernetes` skill exists in this environment. When the user's question is about k8s workloads (Deployments, Services, RBAC) rather than the Talos OS layer, defer to it. This skill handles the node/OS layer: machine config, node networking, `talosctl`, Talos upgrades.
- If the user needs destructive operations, suggest they create a separate `talos-ops` user-invocable skill with `disable-model-invocation: true`. Do not do destructive work from this skill.

## Safety reminders

- Never paste secrets from `talosconfig`, `controlplane.yaml`, or `talsecret.sops.yaml` into the conversation.
- `talosctl` commands target nodes via `-n <ip>` and endpoints via `-e <ip>`. Be explicit in examples; wrong targeting is a common mistake.
- Config changes on control plane nodes can brick the cluster — always recommend `--mode=no-reboot --dry-run` first, then staged rollout.
