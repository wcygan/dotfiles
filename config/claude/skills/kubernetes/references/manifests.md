# Manifests & Kustomize

Authoritative deep links:

- <https://kubernetes.io/docs/concepts/overview/working-with-objects/>
- <https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/>
- <https://kubernetes.io/docs/reference/labels-annotations-taints/>
- <https://kubernetes.io/docs/tasks/manage-kubernetes-objects/kustomization/>

## Object Shape

Every Kubernetes object shares a common envelope:

```yaml
apiVersion: <group>/<version>    # e.g. apps/v1, networking.k8s.io/v1
kind: <Kind>                     # e.g. Deployment, Service
metadata:
  name: <dns-1123-name>          # lowercase, alphanumeric, -, ., max 253 chars
  namespace: <ns>                # omit only for cluster-scoped kinds
  labels: { ... }                # identifying metadata — selectable
  annotations: { ... }           # non-identifying metadata — not selectable
spec: { ... }                    # desired state
status: { ... }                  # observed state (do not author)
```

Never author `status`. Do not set `resourceVersion`, `uid`, `generation`, `creationTimestamp` in source YAML.

## Recommended Labels

From the [common labels guide](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/):

```yaml
metadata:
  labels:
    app.kubernetes.io/name: mysql
    app.kubernetes.io/instance: mysql-abcxzy
    app.kubernetes.io/version: "8.0.36"
    app.kubernetes.io/component: database
    app.kubernetes.io/part-of: wordpress
    app.kubernetes.io/managed-by: kustomize
```

These are conventions, not enforced. Adopting them gives tooling (Lens, k9s, dashboards) a consistent view.

## Selectors

```yaml
# Equality-based
selector:
  matchLabels:
    app.kubernetes.io/name: app

# Set-based
selector:
  matchExpressions:
    - { key: tier, operator: In, values: [frontend, backend] }
    - { key: environment, operator: NotIn, values: [dev] }
    - { key: track, operator: Exists }
```

**Critical rule**: a Deployment's `spec.selector` is **immutable after creation**. Picking wrong labels forces delete+recreate.

## Field Management (Server-Side Apply)

Use `kubectl apply --server-side` to get proper field ownership tracking:

```bash
kubectl apply --server-side -f manifest.yaml
kubectl apply --server-side --force-conflicts -f manifest.yaml   # take over ownership
```

Server-side apply replaces the legacy `kubectl.kubernetes.io/last-applied-configuration` annotation and gives the API server authoritative conflict detection.

## Multi-Document YAML

```yaml
apiVersion: v1
kind: Namespace
metadata: { name: app }
---
apiVersion: v1
kind: ConfigMap
metadata: { name: cfg, namespace: app }
data:
  LOG_LEVEL: info
```

Apply order matters for namespaces, CRDs, and RBAC. Split into separate files or use Kustomize to manage apply ordering implicitly.

## Kustomize Layout

```
deploy/
├── base/
│   ├── kustomization.yaml
│   ├── deployment.yaml
│   ├── service.yaml
│   └── configmap.yaml
└── overlays/
    ├── dev/
    │   ├── kustomization.yaml
    │   └── replica-patch.yaml
    └── prod/
        ├── kustomization.yaml
        └── resources-patch.yaml
```

`base/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
commonLabels:
  app.kubernetes.io/name: app
resources:
  - deployment.yaml
  - service.yaml
  - configmap.yaml
images:
  - name: ghcr.io/org/app
    newTag: v1.2.3
```

`overlays/prod/kustomization.yaml`:

```yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
namespace: prod
resources:
  - ../../base
patches:
  - path: replica-patch.yaml
    target: { kind: Deployment, name: app }
configMapGenerator:
  - name: env
    literals:
      - ENVIRONMENT=prod
      - LOG_LEVEL=warn
```

Apply with `kubectl apply -k ./overlays/prod` or render with `kustomize build ./overlays/prod`.

## Validation Before Apply

```bash
kubectl apply --dry-run=server -f manifest.yaml      # server-side validation
kubectl apply --dry-run=client -f manifest.yaml      # schema only
kubeconform -strict -summary manifest.yaml           # offline schema check
kube-linter lint deploy/                              # opinionated policy checks
```

## Common Footguns

- **Mutable selectors myth** — Deployment selectors are immutable. StatefulSet selectors too.
- **Namespace mismatch** — `metadata.namespace` must match where you apply; otherwise `kubectl apply` silently puts the object in the current context's default namespace.
- **Number vs string** — `"8080"` and `8080` are different in YAML; image tags like `"1.0"` must be strings.
- **Integer vs millicpu** — `cpu: 1` = one core, `cpu: 1000m` = same. Memory uses binary (`Mi`, `Gi`) or decimal (`M`, `G`) — pick one style.
- **Forgetting `---`** between documents silently drops later resources.
