# Troubleshooting

Authoritative deep links:

- <https://kubernetes.io/docs/tasks/debug/debug-application/>
- <https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/>
- <https://kubernetes.io/docs/tasks/debug/debug-cluster/>
- <https://kubernetes.io/docs/reference/kubectl/generated/kubectl_debug/>

## First Three Commands (always)

```bash
kubectl get pod <pod> -o wide
kubectl describe pod <pod>          # scroll to Events at the bottom
kubectl get events --sort-by=.lastTimestamp -n <ns> | tail -30
```

90% of cluster issues reveal themselves in Events and `describe`. Start there before diving into logs.

## Pod Status Cheat Sheet

| Status | Likely cause | First checks |
|---|---|---|
| **Pending** | Unschedulable | `describe` → Events. Insufficient CPU/memory? Taints without tolerations? No matching nodeSelector/affinity? Unbound PVC? |
| **ContainerCreating** (stuck) | Volume, image, or CNI | PVC bound? Image pullable? CNI healthy? |
| **ImagePullBackOff** / **ErrImagePull** | Image name/tag wrong, private registry | `describe` shows pull error. Check imagePullSecrets, registry auth, tag exists. |
| **CrashLoopBackOff** | Container exits repeatedly | `kubectl logs --previous`. Check command, config, dependencies, probes. |
| **Error** / **Completed** | Job-style pod, exit code | `kubectl logs`, inspect exit code in `describe`. |
| **OOMKilled** | Memory limit exceeded | Raise memory limit, investigate leak, check JVM heap sizing. `describe` → `Last State: Terminated, Reason: OOMKilled`. |
| **Evicted** | Node pressure (disk/memory) | `kubectl get events`, check node conditions, requests vs capacity. |
| **Terminating** (stuck) | Finalizer or graceful shutdown hang | `kubectl get pod <pod> -o yaml` → finalizers. `kubectl delete --grace-period=0 --force` as last resort. |

## CrashLoopBackOff Playbook

```bash
# 1. What did the previous container say?
kubectl logs <pod> -c <container> --previous --tail=200

# 2. Exit code and reason
kubectl get pod <pod> -o jsonpath='{.status.containerStatuses[*].lastState.terminated}' | jq

# 3. Is it the probes killing it?
kubectl get pod <pod> -o yaml | yq '.spec.containers[].livenessProbe, .spec.containers[].readinessProbe'

# 4. Exec into a working version (if any replica is up)
kubectl exec -it deploy/<name> -- sh

# 5. Ephemeral debug container for distroless images
kubectl debug -it <pod> --image=busybox:1.36 --target=<container>
```

Common root causes: missing env vars, unreachable dependency at boot, misconfigured command/args, probe failing before app is ready (needs `startupProbe`), permission denied on mounted volume, OOM on startup.

## ImagePullBackOff Playbook

```bash
kubectl describe pod <pod> | grep -A5 Events
```

Check in order:

1. **Typo in image name or tag** — most common.
2. **Tag does not exist** in the registry.
3. **Private registry auth** — is `imagePullSecrets` set on the Pod or its ServiceAccount?
   ```bash
   kubectl create secret docker-registry regcred \
     --docker-server=ghcr.io \
     --docker-username=<user> \
     --docker-password=<token>
   kubectl patch serviceaccount default \
     -p '{"imagePullSecrets":[{"name":"regcred"}]}'
   ```
4. **Architecture mismatch** — ARM image on amd64 node or vice versa.
5. **Rate limiting** — Docker Hub unauthenticated pull limits; mirror or authenticate.

## Pending Pod Playbook

```bash
kubectl describe pod <pod> | grep -A20 Events
kubectl get nodes
kubectl describe nodes | grep -A5 "Allocated resources"
```

Look for:

- `0/N nodes are available: insufficient cpu/memory` → scale the cluster, lower requests, or check for ghost reservations.
- `node(s) had untolerated taint` → add `tolerations` or remove the taint.
- `persistentvolumeclaim "X" not found` / `pod has unbound immediate PersistentVolumeClaims` → check PVC status and StorageClass.
- `node(s) didn't match Pod's node affinity/selector` → fix `nodeSelector`/`affinity` or relabel nodes.

## Service Has No Endpoints

```bash
kubectl get svc <svc> -o yaml | yq .spec.selector
kubectl get pods -l <selector-key>=<value>
kubectl get endpoints <svc>
kubectl get endpointslices -l kubernetes.io/service-name=<svc>
```

Usually one of: selector mismatch, pods not Ready (readiness probe failing), wrong `targetPort`, pods in a different namespace than the Service.

## DNS Not Resolving

```bash
kubectl run -it --rm dnsutils \
  --image=registry.k8s.io/e2e-test-images/jessie-dnsutils:1.3 -- sh

# Inside:
cat /etc/resolv.conf
nslookup kubernetes.default
nslookup <svc>.<ns>.svc.cluster.local
```

Check CoreDNS:

```bash
kubectl -n kube-system get pods -l k8s-app=kube-dns
kubectl -n kube-system logs -l k8s-app=kube-dns
kubectl -n kube-system get configmap coredns -o yaml
```

## Node Issues

```bash
kubectl get nodes
kubectl describe node <node>    # check Conditions, Capacity, Allocatable, Events
kubectl top nodes               # requires metrics-server

# Drain for maintenance
kubectl cordon <node>
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
# ... maintenance ...
kubectl uncordon <node>
```

Node Conditions to watch: `Ready=False`, `MemoryPressure`, `DiskPressure`, `PIDPressure`, `NetworkUnavailable`.

## When All Else Fails

1. **Bisect versions** — did it work yesterday? `kubectl rollout history` + `undo`.
2. **Minimal reproduction** — `kubectl run` a bare pod with the same image and config to isolate whether it's the workload or the controller.
3. **Compare a healthy pod** — `kubectl get pod <good> -o yaml` vs `kubectl get pod <bad> -o yaml` → `diff`.
4. **Cluster-level** — `kubectl get componentstatuses` (deprecated but sometimes informative), `kubectl -n kube-system get pods`, check control plane logs.
5. **API server reachability** — `kubectl get --raw=/healthz`, `kubectl get --raw=/livez?verbose`.
