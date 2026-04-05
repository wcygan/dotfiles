# RBAC & Security

Authoritative deep links:

- <https://kubernetes.io/docs/reference/access-authn-authz/rbac/>
- <https://kubernetes.io/docs/concepts/security/pod-security-admission/>
- <https://kubernetes.io/docs/concepts/security/pod-security-standards/>
- <https://kubernetes.io/docs/concepts/configuration/secret/>
- <https://kubernetes.io/docs/tasks/configure-pod-container/security-context/>

## RBAC Primitives

| Kind | Scope | Grants |
|---|---|---|
| **Role** | Single namespace | Verbs on resources in that namespace |
| **ClusterRole** | Cluster-wide | Can grant cluster-scoped resources, all namespaces, or non-resource URLs |
| **RoleBinding** | Single namespace | Binds a subject to a Role **or** ClusterRole, scoped to one namespace |
| **ClusterRoleBinding** | Cluster-wide | Binds a subject to a ClusterRole across all namespaces |

**Subjects**: `User`, `Group`, `ServiceAccount`. Users and groups are authenticator-defined (x509 CN, OIDC claims); ServiceAccounts are Kubernetes objects.

## Least-Privilege Role

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: app-reader
  namespace: app
rules:
  - apiGroups: [""]
    resources: [pods, services, configmaps]
    verbs: [get, list, watch]
  - apiGroups: [apps]
    resources: [deployments]
    verbs: [get, list, watch]
---
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: app-reader
  namespace: app
subjects:
  - kind: ServiceAccount
    name: app
    namespace: app
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: app-reader
```

**Rules of thumb**:

- Start from `verbs: [get, list, watch]` and add write verbs only when required.
- Prefer `Role` + `RoleBinding` (namespace-scoped) over `ClusterRole` + `ClusterRoleBinding`.
- Never bind `cluster-admin` to workloads. Reserve for break-glass human accounts.
- Use `resourceNames` to scope to specific named objects when possible.

## Checking Permissions

```bash
# Can the current user do this?
kubectl auth can-i create deployments -n app
kubectl auth can-i '*' '*' -n app

# Can a ServiceAccount do this?
kubectl auth can-i get secrets \
  --as=system:serviceaccount:app:app -n app

# List all permissions for a SA
kubectl auth can-i --list \
  --as=system:serviceaccount:app:app -n app
```

## ServiceAccounts and Tokens

```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: app
  namespace: app
automountServiceAccountToken: false   # set true only if the pod calls the API
```

Since v1.24, Kubernetes no longer auto-creates long-lived token Secrets for ServiceAccounts. Use **projected service account tokens** with bounded audience and lifetime:

```yaml
volumes:
  - name: sa-token
    projected:
      sources:
        - serviceAccountToken:
            audience: my-api       # binds token to a specific audience
            expirationSeconds: 3600
            path: token
```

## Pod Security Admission (replaces PSP)

Enforce Pod Security Standards via **namespace labels** — no PSP objects, no OPA/Kyverno required for the baseline.

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: app
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/audit: restricted
    pod-security.kubernetes.io/warn: restricted
```

**Three levels**:

| Level | Intent |
|---|---|
| `privileged` | No restrictions (trust boundary) |
| `baseline` | Prevent known privilege escalations; permissive enough for common apps |
| `restricted` | Hardened; follows pod hardening best practices |

`restricted` requires: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem` strongly recommended, dropped capabilities, seccomp profile `RuntimeDefault`, no host namespaces/ports/paths.

## Hardened Pod SecurityContext

```yaml
spec:
  securityContext:                    # pod-level
    runAsNonRoot: true
    runAsUser: 10000
    runAsGroup: 10000
    fsGroup: 10000
    seccompProfile: { type: RuntimeDefault }
  containers:
    - name: app
      securityContext:                # container-level
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        privileged: false
        capabilities:
          drop: ["ALL"]
```

If the app needs write paths with `readOnlyRootFilesystem: true`, mount an `emptyDir` at those paths (`/tmp`, `/var/cache`, etc.).

## Secrets

```yaml
apiVersion: v1
kind: Secret
metadata: { name: db, namespace: app }
type: Opaque
stringData:                 # plain text — API server base64-encodes on write
  username: app
  password: s3cret
```

**Hard truths about Secrets**:

- By default, stored **base64-encoded, not encrypted at rest** in etcd. Enable [encryption at rest](https://kubernetes.io/docs/tasks/administer-cluster/encrypt-data/) via `EncryptionConfiguration`.
- Anyone with `get secrets` in a namespace can read them. Scope RBAC tightly.
- For strong secret management, integrate an external store (Vault, AWS Secrets Manager, GCP Secret Manager) via [Secrets Store CSI Driver](https://secrets-store-csi-driver.sigs.k8s.io/) or External Secrets Operator.

## Audit and Hardening Checklist

- [ ] Namespace has `pod-security.kubernetes.io/enforce` label
- [ ] ServiceAccount token not auto-mounted unless needed
- [ ] No `cluster-admin` bindings on workloads
- [ ] `readOnlyRootFilesystem: true` where possible
- [ ] Capabilities dropped to `ALL`, added back only as needed
- [ ] Images pinned to digest or immutable tag
- [ ] NetworkPolicy default-deny in place
- [ ] Secrets encrypted at rest in etcd
- [ ] Resource requests/limits set (prevents noisy-neighbor DoS)
