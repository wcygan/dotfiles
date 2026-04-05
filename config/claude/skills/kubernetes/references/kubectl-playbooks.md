# kubectl Playbooks

Authoritative deep links (WebFetch for current details):

- <https://kubernetes.io/docs/reference/kubectl/>
- <https://kubernetes.io/docs/reference/kubectl/generated/kubectl_debug/>
- <https://kubernetes.io/docs/tasks/debug/debug-application/debug-running-pod/>
- <https://kubernetes.io/docs/tasks/debug/debug-cluster/>

## Context & Namespace Hygiene

```bash
kubectl config get-contexts
kubectl config current-context
kubectl config use-context <ctx>
kubectl config set-context --current --namespace=<ns>
```

Consider `kubectx`/`kubens` or `kubie` for multi-cluster daily driving, but every scripted action should pass `--context` and `--namespace` explicitly — never trust ambient state in automation.

## Debug a Failing Pod

```bash
# 1. Describe — look at Events at the bottom
kubectl describe pod <pod>

# 2. Logs from current and previous container
kubectl logs <pod> -c <container>
kubectl logs <pod> -c <container> --previous

# 3. Cluster events in time order
kubectl get events --sort-by=.lastTimestamp -n <ns>

# 4. Shell in (if container has a shell)
kubectl exec -it <pod> -c <container> -- sh

# 5. Ephemeral debug container (preferred for distroless)
kubectl debug -it <pod> --image=busybox:1.36 --target=<container>

# 6. Copy a troubled pod with a debuggable image
kubectl debug <pod> -it --image=ubuntu --share-processes --copy-to=<pod>-debug
```

## Logs — High Signal Flags

```bash
kubectl logs -f <pod>                    # follow
kubectl logs <pod> --tail=200            # last N
kubectl logs <pod> --since=15m           # time-bounded
kubectl logs -l app.kubernetes.io/name=app --all-containers --prefix
kubectl logs <pod> --previous            # prior crash
```

## Port-Forward & Exec

```bash
kubectl port-forward svc/<svc> 8080:80
kubectl port-forward pod/<pod> 5432
kubectl exec -it <pod> -- env
kubectl exec -it deploy/<name> -- sh     # pick any pod from a deployment
```

## Rollouts

```bash
kubectl rollout status deploy/<name> --timeout=2m
kubectl rollout history deploy/<name>
kubectl rollout history deploy/<name> --revision=3
kubectl rollout undo deploy/<name>
kubectl rollout undo deploy/<name> --to-revision=3
kubectl rollout restart deploy/<name>    # triggers new pods without image change
kubectl rollout pause deploy/<name>
kubectl rollout resume deploy/<name>
```

## Declarative Apply

```bash
# Always diff before apply in shared clusters
kubectl diff -f manifest.yaml
kubectl apply -f manifest.yaml --server-side
kubectl apply -k ./overlay/prod            # kustomize
```

Use `--server-side` to avoid the legacy last-applied-configuration annotation and get proper field management / conflict detection.

## Node Operations

```bash
kubectl get nodes -o wide
kubectl top nodes                          # requires metrics-server
kubectl cordon <node>                      # stop scheduling new pods
kubectl drain <node> --ignore-daemonsets --delete-emptydir-data
kubectl uncordon <node>
```

## Scaling & Resource Inspection

```bash
kubectl scale deploy/<name> --replicas=5
kubectl top pods -n <ns> --sort-by=memory
kubectl get hpa -n <ns>
kubectl describe hpa <name> -n <ns>
```

## Output Tricks

```bash
kubectl get pod <pod> -o jsonpath='{.status.phase}'
kubectl get pods -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\n"}{end}'
kubectl get pods -o custom-columns=NAME:.metadata.name,STATUS:.status.phase,NODE:.spec.nodeName
kubectl get deploy -o yaml | yq '.items[].spec.template.spec.containers[].image'
```

## Dry Run to Generate Starter YAML

```bash
kubectl create deployment app --image=nginx --dry-run=client -o yaml > deploy.yaml
kubectl create configmap cfg --from-literal=key=val --dry-run=client -o yaml
kubectl create secret generic s --from-literal=token=xxx --dry-run=client -o yaml
```

Use these as YAML scaffolds — never `kubectl create` imperatively in production.
