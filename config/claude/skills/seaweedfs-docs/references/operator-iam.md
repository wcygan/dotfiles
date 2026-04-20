---
title: Operator IAM (embedded S3 identities)
canonical-url: https://github.com/seaweedfs/seaweedfs-operator/blob/master/IAM_SUPPORT.md
fetch-when: Wiring S3 identities via the operator, configuring OIDC, or understanding the `configSecret` shape.
---

# Embedded IAM in the SeaweedFS operator

The S3 server includes an IAM API on the **same port as S3** (8333). No separate IAM pod.

## Default state

- `spec.s3.iam: true` is the default. IAM is enabled and enforcing.
- To disable (anonymous S3), set `spec.s3.iam: false` explicitly.

## `configSecret` — static identities

Point the Seaweed CR at a Secret whose key contains a JSON `identities` document:

```yaml
spec:
  s3:
    replicas: 2
    iam: false           # or true, depending on policy
    configSecret:
      name: seaweedfs-s3-config
      key: s3.json
```

Secret `s3.json`:
```json
{
  "identities": [
    {
      "name": "admin",
      "actions": ["Admin"],
      "credentials": [{"accessKey": "AKIAXX…", "secretKey": "xxx"}]
    },
    {
      "name": "reader",
      "actions": ["Read", "List"],
      "credentials": [{"accessKey": "AKIAYY…", "secretKey": "yyy"}]
    }
  ]
}
```

The operator mounts the Secret at `/etc/sw` and starts the S3 server with `-config=/etc/sw/<key>`.

## Actions vocabulary

SeaweedFS-specific:
- `Admin` — everything
- `Read`, `Write`, `List`, `Tagging`, `ReadAcp`, `WriteAcp`
- `Read:<bucket>`, `Write:<bucket>` — bucket-scoped variants

## OIDC federation

Configure via a ConfigMap / Secret with:

```json
{
  "sts": {
    "tokenDuration": "1h",
    "maxSessionLength": "12h",
    "issuer": "seaweedfs-sts",
    "signingKey": "<base64>"
  },
  "providers": [
    {
      "name": "keycloak",
      "type": "oidc",
      "enabled": true,
      "config": {
        "issuer": "https://keycloak.example.com/realms/seaweedfs",
        "clientId": "seaweedfs-s3",
        "clientSecret": "...",
        "jwksUri": "https://.../certs",
        "tlsCaCert": "/etc/seaweedfs/certs/ca.pem",
        "tlsInsecureSkipVerify": false,
        "roleMapping": {
          "rules": [
            {"claim": "groups", "value": "admins", "role": "arn:aws:iam::role/S3AdminRole"}
          ],
          "defaultRole": "arn:aws:iam::role/S3ReadOnlyRole"
        }
      }
    }
  ],
  "policies": [...],
  "roles": [...]
}
```

## Service discovery

- Internal DNS: `<seaweed-name>-s3.<namespace>.svc.cluster.local:8333`
- Same endpoint serves both S3 and IAM APIs.

## Anton note

anton uses `iam: false` + static admin keys for simplicity (ADR 0019). Credentials come from 1Password via ESO into a `seaweedfs-s3-config` Secret. If/when Harbor lives on a dedicated bucket with scoped creds, migrate to `iam: true` + a per-consumer identity.
