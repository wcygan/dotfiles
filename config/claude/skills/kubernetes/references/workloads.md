# Workloads

Authoritative deep links:

- <https://kubernetes.io/docs/concepts/workloads/>
- <https://kubernetes.io/docs/concepts/workloads/controllers/deployment/>
- <https://kubernetes.io/docs/concepts/workloads/controllers/statefulset/>
- <https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/>
- <https://kubernetes.io/docs/concepts/workloads/controllers/job/>
- <https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#container-probes>

## Picking a Controller

| Workload kind | When to use |
|---|---|
| **Deployment** | Stateless services; rolling updates; arbitrary pod identity |
| **StatefulSet** | Stable network IDs, ordered startup/shutdown, per-replica PVCs (databases, brokers) |
| **DaemonSet** | One pod per node (log shippers, CNI, node-exporters) |
| **Job** | Run-to-completion batch task |
| **CronJob** | Scheduled Job on cron expression |
| **ReplicaSet** | Rarely authored directly; Deployment manages one |

## Deployment — Rolling Update Strategy

```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 25%   # or integer
      maxSurge: 25%
  minReadySeconds: 10       # pod must be Ready this long before counted available
  revisionHistoryLimit: 10
  progressDeadlineSeconds: 600
```

`Recreate` strategy is only appropriate when concurrent old+new pods cannot coexist (e.g., exclusive lock on a resource).

## StatefulSet Essentials

```yaml
spec:
  serviceName: app-headless   # must reference a headless Service (clusterIP: None)
  replicas: 3
  podManagementPolicy: OrderedReady   # or Parallel
  volumeClaimTemplates:
    - metadata: { name: data }
      spec:
        accessModes: [ReadWriteOnce]
        resources: { requests: { storage: 10Gi } }
        storageClassName: fast
```

- Pods are named `<name>-0`, `<name>-1`, ... with stable DNS `<pod>.<serviceName>.<ns>.svc.cluster.local`.
- Each replica gets its own PVC from `volumeClaimTemplates`. **PVCs are not deleted** when you delete the StatefulSet — clean up manually if desired.
- Scale-down happens in reverse order.

## Probes

Three distinct probes with different purposes:

| Probe | Failure consequence | Use for |
|---|---|---|
| **startupProbe** | Kill container; restart | Slow-booting apps — disables liveness/readiness until first success |
| **livenessProbe** | Kill container; restart | Deadlock detection |
| **readinessProbe** | Remove from Service endpoints | Traffic gating (warmup, dependency checks) |

```yaml
startupProbe:
  httpGet: { path: /healthz, port: 8080 }
  failureThreshold: 30
  periodSeconds: 10           # allows up to 5 minutes to start
livenessProbe:
  httpGet: { path: /livez, port: 8080 }
  periodSeconds: 10
  timeoutSeconds: 2
  failureThreshold: 3
readinessProbe:
  httpGet: { path: /ready, port: 8080 }
  periodSeconds: 5
  failureThreshold: 3
```

**Anti-patterns**: using the same endpoint for liveness and readiness; liveness probe that depends on downstream services (causes restart storms); no startup probe on slow-boot apps.

## Resources

```yaml
resources:
  requests: { cpu: 100m, memory: 128Mi }  # scheduling, QoS
  limits:   { cpu: 500m, memory: 256Mi }  # hard cap
```

- **Requests** determine scheduling and QoS class.
- **Memory limit exceeded → OOMKill**. CPU limit exceeded → throttle (not kill).
- **QoS classes**: Guaranteed (requests==limits for both), Burstable (requests set), BestEffort (neither set). Guaranteed pods are evicted last under node pressure.
- Consider omitting CPU limits on latency-sensitive services — throttling can be worse than the protection.

## Jobs and CronJobs

```yaml
apiVersion: batch/v1
kind: Job
spec:
  parallelism: 4
  completions: 10
  backoffLimit: 3
  activeDeadlineSeconds: 600
  ttlSecondsAfterFinished: 3600   # auto-cleanup
  template:
    spec:
      restartPolicy: OnFailure
      containers: [...]
```

```yaml
apiVersion: batch/v1
kind: CronJob
spec:
  schedule: "*/5 * * * *"
  concurrencyPolicy: Forbid      # Allow | Forbid | Replace
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
  startingDeadlineSeconds: 60
  jobTemplate:
    spec: { ... }
```

**CronJob footguns**: the controller uses cluster time (UTC by default, `spec.timeZone` since v1.27 stable); long-running jobs plus `concurrencyPolicy: Allow` can pile up; missed schedules past `startingDeadlineSeconds` are skipped.

## PodDisruptionBudget

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata: { name: app }
spec:
  minAvailable: 2         # or maxUnavailable
  selector:
    matchLabels: { app.kubernetes.io/name: app }
```

PDBs protect against **voluntary** disruptions (drains, upgrades). They do not help with node crashes.
