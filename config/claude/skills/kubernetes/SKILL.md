---
name: kubernetes
description: Kubernetes expert for cluster operations, manifests, kubectl debugging, RBAC, networking (Services/Ingress/Gateway API), workloads, storage, and troubleshooting. Auto-loads when the user mentions kubectl/kubernetes/k8s together with an action verb (apply, debug, troubleshoot, rollout, deploy, write manifest, fix pod, exec, logs). Do NOT trigger on incidental mentions of "service", "pod", or "cluster" outside a Kubernetes context, or for Terraform/Helm-only questions. Keywords: kubernetes, kubectl, k8s, deployment, pod, statefulset, daemonset, configmap, secret, ingress, gateway api, networkpolicy, rbac, serviceaccount, pvc, storageclass, crashloopbackoff, imagepullbackoff, manifest, rollout, kustomize
allowed-tools: Read, Grep, Glob, Bash(kubectl *), Bash(kustomize *), WebFetch
---

# Kubernetes

Kubernetes operational and authoring expertise: kubectl playbooks, manifest design, workload controllers, networking, storage, RBAC, and production troubleshooting.

## Authoritative Source

**Always prefer upstream docs over memory.** Root: <https://kubernetes.io/docs/home/>

For API schema, field semantics, deprecations, or "which version added X?" questions, **use WebFetch against versioned deep links** rather than answering from training data. Anchor citations to specific pages like:

- `https://kubernetes.io/docs/reference/kubectl/` — kubectl reference
- `https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.31/` — API reference (swap version as needed)
- `https://kubernetes.io/docs/concepts/workloads/` — workload controllers
- `https://kubernetes.io/docs/concepts/services-networking/` — Service, Ingress, Gateway API
- `https://kubernetes.io/docs/concepts/storage/` — PV/PVC/StorageClass
- `https://kubernetes.io/docs/concepts/security/` — RBAC, Pod Security Admission

Each `references/*.md` file opens with topic-scoped deep links.

## Version Posture

- Assume **Kubernetes ≥ v1.31** unless the user's manifests or `kubectl version` indicate otherwise. Verify with `kubectl version --short` before making version-sensitive claims.
- **PodSecurityPolicy is removed** (since v1.25). Use **Pod Security Admission** (`pod-security.kubernetes.io/*` namespace labels).
- Prefer **Gateway API** (`gateway.networking.k8s.io`) over legacy `Ingress` for new work where the cluster supports it; both remain valid.
- `autoscaling/v2` is the current HPA API. `autoscaling/v1` is legacy.
- Check CRD versions before recommending — operator-provided APIs (Istio, Argo, cert-manager, etc.) evolve independently.

## Scope Fence

**In scope**: core Kubernetes resources, kubectl, manifest authoring, RBAC, networking, storage, Pod Security Admission, troubleshooting, Kustomize basics.

**Out of scope** (do not sprawl into these): Helm chart authoring, Istio/Linkerd service meshes, specific operators (Argo, Flux, cert-manager) beyond referencing them, cloud-provider-specific IAM (EKS/GKE/AKS), container image building. Defer to project-local context for those.

## Quick kubectl Reflexes

```bash
# Context & namespace
kubectl config current-context
kubectl config use-context <ctx>
kubectl config set-context --current --namespace=<ns>

# Inspect
kubectl get pods -o wide
kubectl describe pod <pod>
kubectl logs <pod> -c <container> --previous --tail=200
kubectl get events --sort-by=.lastTimestamp

# Debug running workloads
kubectl exec -it <pod> -- sh
kubectl debug <pod> -it --image=busybox --target=<container>   # ephemeral container
kubectl port-forward svc/<svc> 8080:80

# Rollouts
kubectl rollout status deploy/<name>
kubectl rollout history deploy/<name>
kubectl rollout undo deploy/<name> [--to-revision=N]

# Apply / diff
kubectl diff -f manifest.yaml
kubectl apply -f manifest.yaml --server-side
```

Always prefer `kubectl apply --server-side` for declarative work to avoid last-applied-configuration drift.

## Minimal Workload Template

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels: { app.kubernetes.io/name: app }
spec:
  replicas: 2
  selector:
    matchLabels: { app.kubernetes.io/name: app }
  template:
    metadata:
      labels: { app.kubernetes.io/name: app }
    spec:
      containers:
        - name: app
          image: ghcr.io/org/app:v1.2.3  # pin, never :latest
          ports: [{ containerPort: 8080 }]
          resources:
            requests: { cpu: 100m, memory: 128Mi }
            limits:   { cpu: 500m, memory: 256Mi }
          readinessProbe:
            httpGet: { path: /healthz, port: 8080 }
            periodSeconds: 5
          livenessProbe:
            httpGet: { path: /livez, port: 8080 }
            periodSeconds: 10
          securityContext:
            runAsNonRoot: true
            readOnlyRootFilesystem: true
            allowPrivilegeEscalation: false
            capabilities: { drop: ["ALL"] }
```

## Operating Principles

1. **Declarative over imperative** — `kubectl apply` on checked-in YAML, not `kubectl create/edit` in production.
2. **Pin images** to immutable tags or digests; never `:latest`.
3. **Set resources** — requests for scheduling, limits for blast radius.
4. **Probes matter** — readiness gates traffic, liveness restarts, startup protects slow boots.
5. **Namespace isolation** — one logical app per namespace; use NetworkPolicy by default.
6. **Least privilege RBAC** — prefer Roles over ClusterRoles; never bind to `cluster-admin` outside break-glass.
7. **Read before write** — `kubectl diff` before `kubectl apply` in shared clusters.

## References

- [kubectl Playbooks](references/kubectl-playbooks.md) — debug pod, exec, logs, port-forward, rollout, drain
- [Workloads](references/workloads.md) — Deployment, StatefulSet, DaemonSet, Job, CronJob; probes, strategies
- [Manifests](references/manifests.md) — YAML structure, labels/selectors, recommended labels, Kustomize basics
- [Networking](references/networking.md) — Service types, Ingress, Gateway API, NetworkPolicy, DNS
- [Storage](references/storage.md) — PV/PVC, StorageClass, access modes, volume expansion, CSI
- [RBAC & Security](references/rbac-security.md) — Role/ClusterRole, ServiceAccount, Pod Security Admission, secrets
- [Troubleshooting](references/troubleshooting.md) — CrashLoopBackOff, ImagePullBackOff, Pending, OOMKilled, DNS

## Review

`Last reviewed: 2026-04-04. Re-audit by: 2026-10-04.` Delete or refactor if no demonstrable value over base-model Kubernetes knowledge by the re-audit date.
