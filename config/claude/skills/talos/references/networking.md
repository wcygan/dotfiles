# Talos Networking (v1.12)

Authoritative: `https://docs.siderolabs.com/talos/v1.12/talos-guides/network/` and `https://docs.siderolabs.com/talos/v1.12/reference/configuration/v1alpha1/config/#Config.machine.network`. WebFetch these for exact field names — the schema is deeply nested and has renamed fields across versions.

All networking lives under `machine.network` in the machine config.

## Minimum skeleton

```yaml
machine:
  network:
    hostname: cp-1
    nameservers:
      - 1.1.1.1
      - 9.9.9.9
    interfaces:
      - interface: eth0          # or "deviceSelector" (preferred on v1.5+)
        dhcp: true
```

## Common interface patterns

### Static IP on a selected device (preferred over hardcoded `eth0`)

```yaml
machine:
  network:
    interfaces:
      - deviceSelector:
          hardwareAddr: "00:15:5d:*"    # glob match on MAC
          # or: busPath, driver, pciID, physical: true
        addresses:
          - 10.0.0.11/24
        routes:
          - network: 0.0.0.0/0
            gateway: 10.0.0.1
        mtu: 1500
```

`deviceSelector` is robust across reboots; `interface: eth0` breaks if the kernel renames NICs.

### VLAN

```yaml
- interface: eth0
  dhcp: false
  vlans:
    - vlanId: 100
      addresses: ["10.100.0.11/24"]
      routes:
        - network: 0.0.0.0/0
          gateway: 10.100.0.1
```

### Bond (LACP)

```yaml
- interface: bond0
  bond:
    mode: 802.3ad
    xmitHashPolicy: layer3+4
    lacpRate: fast
    interfaces:
      - eth0
      - eth1
  addresses: ["10.0.0.11/24"]
  routes:
    - network: 0.0.0.0/0
      gateway: 10.0.0.1
```

### Bridge (rare on Talos, useful for virtualization hosts)

```yaml
- interface: br0
  bridge:
    stp:
      enabled: true
    interfaces:
      - eth0
  addresses: ["10.0.0.11/24"]
```

### Dummy interface (for VIPs / loopback-style addresses)

```yaml
- interface: dummy0
  dummy: true
  addresses: ["10.100.0.100/32"]
```

### Shared VIP (control-plane HA without external LB)

```yaml
- interface: eth0
  dhcp: true
  vip:
    ip: 10.0.0.100       # floats across control-plane nodes via etcd lease
```

Only works on control-plane nodes. Not a substitute for a real LB in production.

## KubeSpan (built-in WireGuard mesh)

```yaml
machine:
  network:
    kubespan:
      enabled: true
cluster:
  discovery:
    enabled: true
    registries:
      kubernetes: { disabled: false }
      service: { disabled: false }
```

KubeSpan needs cluster discovery enabled to find peers. Useful for nodes split across NAT/clouds. WebFetch `https://docs.siderolabs.com/talos/v1.12/talos-guides/network/kubespan` for current behavior — kubespan has changed multiple times.

## Common pitfalls

- **Mixing `dhcp: true` with `addresses`** — the static addresses are *added on top* of the DHCP lease, they don't replace it. If you want pure static, set `dhcp: false`.
- **`routes` is not inferred** — setting an address does not create a default route. Always include the gateway route when not using DHCP.
- **`hostname` mismatch with DNS** — Talos uses the configured `hostname` for its own identity and certs. If DNS resolves the node to a different name, k8s components may get SAN errors.
- **VIP on workers** — not supported. VIPs are control-plane-only.
- **Bond `miimon`** — must be set (e.g. `miimon: 100`) or link-state failover won't trigger. Default is 0 = disabled.
- **`nameservers` empty on kubespan clusters** — if kubespan changes outbound IPs, DNS can break; always set explicit nameservers.
- **Firewall / host network policy** — Talos v1.6+ has `machine.network.kubespan` and `machine.network.extraHostEntries`, plus a host-level nftables firewall via `NetworkRuleConfig` — check the live doc for the current field layout.

## Diagnosing from a live node (safe)

```bash
talosctl -n <node> get links                  # interface state
talosctl -n <node> get addresses              # configured IPs
talosctl -n <node> get routes
talosctl -n <node> get resolvers              # DNS config
talosctl -n <node> get nodeaddresses          # summary
talosctl -n <node> netstat                    # connection table
talosctl -n <node> read /etc/resolv.conf
```

If a network change didn't take effect after `apply-config`, compare `talosctl get machineconfig -o yaml` against the file on disk — patches sometimes silently no-op if the YAML path is wrong.
