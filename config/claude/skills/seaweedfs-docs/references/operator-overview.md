---
title: seaweedfs-operator overview
canonical-url: https://github.com/seaweedfs/seaweedfs-operator
fetch-when: Installing or upgrading the operator; working with the Seaweed CRD or operator Helm chart.
---

# seaweedfs-operator overview

A Kubernetes operator that manages the full SeaweedFS stack (master, volume, filer, S3, admin, worker) as a single `Seaweed` custom resource.

## Install paths

### Helm (recommended)
```sh
helm repo add seaweedfs-operator https://seaweedfs.github.io/seaweedfs-operator/
helm install seaweedfs-operator seaweedfs-operator/seaweedfs-operator -n <ns> --create-namespace
```

The chart installs: operator Deployment, Seaweed CRD, RBAC, webhook (validating + mutating), service.

### Flux (GitOps)
Standard `HelmRepository` + `HelmRelease`. Chart URL `https://seaweedfs.github.io/seaweedfs-operator/helm`. Note the operator README still shows the legacy `/helm` path; the canonical repo URL omits it now.

### Manual (kustomize)
`git clone` + `make deploy`. Requires cert-manager if webhooks are enabled. Needs `ENABLE_WEBHOOKS=true` in `config/manager/manager.yaml`.

## Webhook bootstrap dance

Default `values.yaml` sets `webhook.enabled: true`, but the validating webhook rejects CRs if the cert Secret isn't generated yet — a chicken/egg. The operator's own README admits:

> Due to an issue with the way the `seaweedfs-operator-webhook-server-cert` is created, `.Values.webhook.enabled` should be set to `false` initially, and then `true` later on.

Two-commit pattern:
1. Install with `webhook.enabled: false`. Let Seaweed CRD + operator come up, certgen Job runs.
2. Flip to `webhook.enabled: true`. Reconcile. Webhook now has a cert and starts enforcing.

## Seaweed CRD shape

```yaml
apiVersion: seaweed.seaweedfs.com/v1
kind: Seaweed
metadata:
  name: my-cluster
  namespace: storage
spec:
  image: chrislusf/seaweedfs:4.21
  master:
    replicas: 3
    defaultReplication: "000"
    volumeSizeLimitMB: 30000
  volume:
    replicas: 3
    requests:
      storage: 100Gi
    storageClassName: longhorn
  filer:
    replicas: 2
    # s3: {enabled: true}   # deprecated — prefer top-level spec.s3
  s3:
    replicas: 2
    iam: false
    configSecret:
      name: seaweedfs-s3-config
      key: s3.json
```

Detail → [operator-crd-schema](operator-crd-schema.md).

## Components the operator manages

- StatefulSet per role: `<name>-master`, `<name>-volume`, `<name>-filer`.
- Deployment for S3 (1.0.12+) when `spec.s3` is set.
- Services: `<name>-master`, `<name>-master-peer`, `<name>-filer`, `<name>-filer-peer`, `<name>-volume-<i>`, `<name>-volume-peer`, `<name>-s3`.
- Optional: Ingress per component, ServiceMonitor, Grafana dashboards.

## Not covered by operator

- Backups (use `weed filer.backup` outside the CRD).
- EC scheduling (run admin + worker, configure in admin UI).
- Cloud Drive / remote sync (post-install via `weed shell`).

## Related docs

- [operator-crd-schema](operator-crd-schema.md) — field reference
- [operator-iam](operator-iam.md) — embedded IAM, `configSecret` shape
- [operator-topology](operator-topology.md) — rack/DC for replication
- [operator-releases](operator-releases.md) — release cadence + breaking changes
