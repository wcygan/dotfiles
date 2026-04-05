# talosctl — Safe (Read-Only) Verbs

Complete reference at `https://docs.siderolabs.com/talos/v1.12/reference/cli/`. WebFetch that page to confirm flag signatures before using any command not listed here.

## Targeting flags (apply to every command)

- `-n, --nodes <ip>[,ip]` — which node(s) to run against. Comma-separated for fan-out.
- `-e, --endpoints <ip>[,ip]` — which control-plane endpoints to reach the API through.
- `--talosconfig <path>` — override the client config file (default: `~/.talos/config` or `$TALOSCONFIG`).
- `--context <name>` — switch between clusters defined in talosconfig.

**Rule of thumb:** `-e` is how you reach the cluster, `-n` is which node you're asking about. On a single-node quickstart, they're the same IP.

## Always-safe verbs

| Command | Purpose |
|---|---|
| `talosctl version` | Client + server versions. First thing to run. |
| `talosctl health` | Full cluster health (Talos + k8s). Add `--server=false` to skip k8s checks. |
| `talosctl get <resource>` | Query the Common Operating System Interface (COSI) resource graph. Safe, read-only. |
| `talosctl read <path>` | Read any file on the node filesystem (e.g. `/etc/kubernetes/kubelet.conf`). |
| `talosctl logs <service>` | Tail service logs. Use `-f` to follow, `--tail N` for last N lines. |
| `talosctl service` | List services and their states (no arg) or inspect one (`talosctl service etcd`). |
| `talosctl dashboard` | Interactive TUI — CPU, memory, network, logs. User must run it directly. |
| `talosctl containers` | Containerd containers; `--kubernetes` for k8s namespace. |
| `talosctl memory` / `cpu` / `disks` / `netstat` / `stats` | Per-node resource and network views. |
| `talosctl validate --config <file> --mode metal\|cloud\|container` | Static schema check on a config file. Never touches the cluster. |
| `talosctl apply-config --file <f> --mode=no-reboot --dry-run` | **Diff only** — shows what would change. The only `apply-config` form this skill runs. |

## Useful `talosctl get` resources

Full list: `talosctl get -h` and the resources doc `https://docs.siderolabs.com/talos/v1.12/learn-more/resources`.

- `members` — cluster discovery view (who's in the cluster)
- `nodeaddresses` — all addresses on the node
- `links` — network interfaces
- `addresses` — IPs per link
- `routes`
- `resolvers`, `timeservers`
- `machineconfig` — the currently-applied config (`-o yaml` for full dump)
- `machinestatus`
- `staticpods` — control-plane pod manifests
- `etcdmembers` — etcd cluster members (control plane only)
- `kubeletconfig`
- `serviceaccounts`

Output formats: `-o yaml`, `-o json`, `-o jsonpath='...'`, `-o table` (default).

## Patterns

**Tail kubelet logs on one node:**
```bash
talosctl -n 10.0.0.11 logs kubelet -f
```

**Check etcd health on all control-plane nodes:**
```bash
talosctl -n 10.0.0.11,10.0.0.12,10.0.0.13 service etcd
```

**Dump current machine config:**
```bash
talosctl -n 10.0.0.11 get machineconfig -o yaml > live.yaml
```

**See what a new config would change (safe):**
```bash
talosctl -n 10.0.0.11 apply-config --file new.yaml --mode=no-reboot --dry-run
```

## Hard stops — do not run from this skill

These verbs mutate the cluster and are out of scope:

- `apply-config` **without** `--dry-run`
- `upgrade`, `upgrade-k8s`
- `reset`
- `bootstrap`
- `etcd snapshot` (safe but destructive side-effects on disk; let the user run it)
- `etcd remove-member`, `etcd forfeit-leadership`
- `gen config`, `gen secrets` (creates/overwrites secrets on disk)
- `shutdown`, `reboot`
- `rollback`

When the user asks for one of these: show the command, link to the relevant doc page, explain the consequences, and ask them to run it.
