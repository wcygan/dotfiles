# Talos Upgrades — Planning Only (Read-Only)

**This file is for planning and pre-flight. It does NOT run upgrades.** `talosctl upgrade` and `talosctl upgrade-k8s` are out of scope for this skill. Show the plan, show the commands, let the user run them.

Authoritative docs — always WebFetch these before finalizing an upgrade plan, because version-skew rules change:
- Talos upgrade: `https://docs.siderolabs.com/talos/v1.12/talos-guides/upgrading-talos`
- Kubernetes upgrade: `https://docs.siderolabs.com/talos/v1.12/kubernetes-guides/upgrading-kubernetes`
- Release notes for the target version on GitHub: `https://github.com/siderolabs/talos/releases`

## Order of operations

Rough rule: **Talos first, Kubernetes second, one node at a time.** In detail:

1. Read the release notes for every version between current and target (not just the target). Breaking changes accumulate.
2. Verify current state: `talosctl version`, `talosctl health`, `talosctl get members`, `kubectl get nodes -o wide`.
3. Check etcd is healthy on every control-plane node: `talosctl -n <cp> service etcd`.
4. **Talos upgrade** — rolling, one node at a time, control-plane nodes last:
   - Workers first, one by one.
   - Control plane nodes one by one, waiting for `talosctl health` to go green and etcd to rejoin between each.
5. **Kubernetes upgrade** — after every node is on the new Talos — run `talosctl upgrade-k8s` from a single control-plane node. It handles kube-apiserver, controller-manager, scheduler, and kubelet across the cluster.
6. Post-check: `talosctl health`, `kubectl get nodes`, `kubectl get pods -A | grep -v Running`.

## Pre-flight checklist (always run these)

```bash
# Versions
talosctl version
kubectl version --short

# Cluster discovery and members
talosctl get members
kubectl get nodes -o wide

# etcd health on every control-plane node
talosctl -n <cp1>,<cp2>,<cp3> service etcd
talosctl -n <cp1> etcd status      # read-only view (NOT etcd snapshot)

# Service state
talosctl -n <all-nodes> service

# Recent errors
talosctl -n <all-nodes> logs machined --tail 100
talosctl -n <all-nodes> logs kubelet --tail 100

# k8s workloads
kubectl get pods -A --field-selector=status.phase!=Running
kubectl get pdb -A               # PodDisruptionBudgets that might block drains
```

If any of these show problems, **fix them before upgrading.** Upgrading an unhealthy cluster compounds the failure.

## Version-skew rules (verify against live docs)

- Kubernetes allows kubelet to be **up to 3 minor versions behind** kube-apiserver (as of k8s 1.28+). Do not rely on this — WebFetch current skew policy.
- Talos versions: **only skip one minor at a time.** Going from 1.8 → 1.12 requires stops at 1.9, 1.10, 1.11 (or at least the last patch of each). Siderolabs publishes a support matrix — check it.
- The Kubernetes version bundled in a given Talos release is documented in the release notes. Do not independently upgrade kubelet via `machine.kubelet.image` unless you know what you're doing.

## Rollback options (read-only description, user executes)

- `talosctl rollback` — reverts a single node to its previous boot partition. Works only if the previous version is still on disk (Talos keeps two partitions). **Destructive command — user invokes.**
- `talosctl edit machineconfig` — interactive edit with rollback-on-reboot semantics. Destructive.
- etcd recovery from snapshot — `talosctl etcd snapshot` must have been run **before** the upgrade. If you're reading this during a broken upgrade and there's no snapshot, your options are restore from backup or rebuild.

## Commands the user must run themselves

Present these explicitly; do not execute:

```bash
# Upgrade one node's Talos installation
talosctl -n <node> upgrade --image ghcr.io/siderolabs/installer:v1.12.X --preserve

# Upgrade Kubernetes across the cluster (run from one control-plane node)
talosctl -n <cp> upgrade-k8s --to 1.31.Y
```

Flags to know and explain when relevant:
- `--preserve` — preserve ephemeral data partition across upgrade (default true in recent versions; confirm from live docs).
- `--stage` — stage the upgrade to run on next reboot instead of immediately.
- `--debug` — verbose output; useful when an upgrade hangs.
- `--image` — pin an exact installer image; required for air-gapped clusters that mirror the image internally.

## After the upgrade

```bash
talosctl version                 # confirm new version on every node
talosctl health
kubectl get nodes
kubectl get pods -A | grep -v Running
```

If anything regressed, inspect `machined` logs on the affected node first (`talosctl logs machined`), then the specific service (`kubelet`, `etcd`, `apid`).
