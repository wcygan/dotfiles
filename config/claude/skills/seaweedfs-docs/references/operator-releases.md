---
title: Operator release triage
canonical-url: https://github.com/seaweedfs/seaweedfs-operator/releases
fetch-when: Considering an upgrade, reading release notes for breaking changes, or diagnosing a regression.
---

# Operator release triage

The operator ships as two paired artifacts:
- **Operator image** — tag `1.0.Z` (controller + CRD logic)
- **Helm chart** — tag `seaweedfs-operator-0.1.W` (templates + default values)

These are released simultaneously. E.g. operator `1.0.12` pairs with chart `0.1.14`.

## How to read the release notes

Each release's body lists merged PRs. Triage priorities:

1. **RBAC additions** — the manager ClusterRole in `config/rbac/role.yaml` is regenerated from `// +kubebuilder:rbac:...` markers. When a release adds a resource (e.g. `apps/deployments` in 1.0.12 for standalone-S3), you need to ensure your deployed chart has it. **The chart templates in `deploy/helm/templates/rbac/` are hand-maintained and can drift.** See the anton Phase 1 story in plan 0005 for an example of this bite.
2. **CRD field additions/deprecations** — new subspecs (`admin`, `worker`, `volumeTopology`), field behavior changes, deprecation warnings. Check `api/v1/seaweed_types.go` diff.
3. **Webhook changes** — new validating rules may reject CRs that worked in the previous release.
4. **Image / chart default changes** — e.g. certgen image bumps can surface on air-gapped clusters.

## Recent releases (as of 2026-04-19)

| Operator | Chart | Notable |
|---|---|---|
| 1.0.12 | 0.1.14 | Standalone-S3 Deployment (PR #200); webhook mutual-exclusion between `spec.s3` and `filer.s3.enabled`; admin + worker CRDs (opt-in); configurable certgen image; ServiceMonitor RBAC; VolumeClaimTemplate auto-recreate. **Chart RBAC drift: `apps/deployments` missing in chart — file an issue or carry a supplement.** |
| 1.0.11 | 0.1.13 | 2026-02-03. Hardening + bugfixes. |
| 1.0.10 | 0.1.12 | 2026-01-19. |
| 1.0.9 | 0.1.11 | |

## Upgrade procedure (Helm)

1. Read the target release's notes end-to-end.
2. `helm repo update` → `helm search repo seaweedfs-operator/seaweedfs-operator --versions`.
3. If RBAC or CRD changed, plan for a brief reconcile pause. For major version jumps, read intermediate releases too.
4. `helm upgrade seaweedfs-operator seaweedfs-operator/seaweedfs-operator --version <X> --reuse-values`.
5. Watch operator logs for RBAC `Forbidden` errors — the most common upgrade fail mode when chart RBAC drifts from controller expectations.
6. Check any field-manager conflicts in helm's SSA output; add `--force-conflicts` only if you know what you're overriding.

## Anton pin

Currently pinned at operator `1.0.12` / chart `0.1.14` per ADR 0019. Renovate watches for bumps. Next upgrade should verify:
- Chart's `deploy/helm/templates/rbac/role.yaml` grants `apps/deployments` and `monitoring.coreos.com/servicemonitors` (so the local RBAC supplement can be dropped).
- No new validating-webhook rules collide with the current Seaweed CR.
- SeaweedFS image tag (`chrislusf/seaweedfs`) bump follows separately — the operator's release doesn't pin the server image.
