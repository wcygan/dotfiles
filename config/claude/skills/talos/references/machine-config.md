# Machine Config (v1.12)

Authoritative reference: `https://docs.siderolabs.com/talos/v1.12/reference/configuration/`. **Always WebFetch that page (or the specific sub-page) before asserting a field name.** The schema is large and version-sensitive — do not guess keys.

## Top-level structure

A Talos machine config is a multi-document YAML. The primary document has:

```yaml
version: v1alpha1        # schema version, not Talos version
debug: false
persist: true
machine:                 # node-level config (kernel, network, install, files, services)
  type: controlplane     # or "worker"
  token: <bootstrap-token>
  ca:
    crt: <base64>
    key: <base64>        # present on controlplane only
  certSANs: []
  kubelet: { ... }
  network: { ... }       # see references/networking.md
  install: { ... }
  files: []
  env: {}
  time: { ... }
  sysctls: {}
  registries: { ... }
  systemDiskEncryption: { ... }
cluster:                 # cluster-wide config (only meaningful on first apply)
  id: <id>
  secret: <base64>
  controlPlane:
    endpoint: https://<vip-or-lb>:6443
  clusterName: <name>
  network:
    dnsDomain: cluster.local
    podSubnets: [10.244.0.0/16]
    serviceSubnets: [10.96.0.0/12]
    cni: { name: flannel }   # or "none" for custom CNI, or "custom"
  token: <k8s-bootstrap-token>
  aescbcEncryptionSecret: <base64>   # deprecated in favor of secretboxEncryptionSecret
  ca: { crt, key }
  etcd: { ca: { crt, key } }
  apiServer: { ... }
  controllerManager: { ... }
  scheduler: { ... }
  discovery: { enabled: true, registries: { ... } }
  inlineManifests: []
  extraManifests: []
```

Patches are a second YAML document (or separate file) applied on top with strategic merge semantics — same shape, partial fields.

## Validation recipe

Always run before applying:

```bash
# Static validation — no cluster contact
talosctl validate --config controlplane.yaml --mode metal
talosctl validate --config worker.yaml --mode metal

# --mode values: metal | cloud | container (must match the install target)

# Dynamic diff against a live node (safe, no reboot):
talosctl -n <node> apply-config --file new.yaml --mode=no-reboot --dry-run
```

If `validate` passes but `apply-config --dry-run` shows unexpected changes, the file drifted from the live config — inspect with `talosctl -n <node> get machineconfig -o yaml`.

## Common pitfalls

- **`machine.install.disk` vs `machine.install.diskSelector`** — `disk` is a literal path like `/dev/sda` and is fragile across boots; prefer `diskSelector` with `size`, `model`, or `type: ssd` matchers.
- **`cluster.network.cni.name: none`** — if you set this, you must also ship a CNI via `cluster.inlineManifests` or a separate `kubectl apply`. Forgetting this leaves pods stuck in ContainerCreating.
- **`machine.certSANs`** — must include every hostname/IP clients use to reach the API. Missing SANs = TLS errors after reboot, requires reconfig.
- **`machine.kubelet.extraArgs` is deprecated** — use `extraConfig` with kubelet-config.k8s.io/v1beta1 fields instead on v1.6+.
- **Secrets in config** — `machine.ca.key`, `cluster.secret`, `cluster.aescbcEncryptionSecret` are sensitive. Never paste these into conversation. Users commonly store config encrypted via sops or git-crypt.
- **Patches overwrite arrays, not merge them** — list fields like `certSANs`, `extraManifests`, `machine.files` are replaced wholesale by a patch, not concatenated. Use strategic-merge patch syntax (`$patch: merge`) if unsure.

## Generating vs editing

First-time config creation uses `talosctl gen config <cluster-name> <endpoint>` — this is a **write** operation that creates `controlplane.yaml`, `worker.yaml`, `talosconfig`. **Out of scope for this skill.** If the user needs to generate new config, tell them the command and let them run it.

Editing existing config is almost always done via patches (talhelper, kustomize-style, or hand-written YAML fragments) rather than editing the full file — it keeps diffs small and makes GitOps cleaner.

## Extensions and system extensions

Extensions add kernel modules, firmware, or userspace tools to the immutable image. Referenced in `machine.install.extensions` (deprecated) or via a custom image built with the Image Factory (`https://factory.talos.dev`). If the user asks about extensions, WebFetch `https://docs.siderolabs.com/talos/v1.12/talos-guides/configuration/system-extensions` — the pattern changed recently and the live doc is the source of truth.
