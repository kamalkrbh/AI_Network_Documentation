# Network Topology Documentation

**Discovery Timestamp:** 2026-03-13
**Source of Truth:** Live device state (LLDP neighbors, interface configs, route tables)
**Topology File:** `output/topology.drawio` (importable into diagrams.net / draw.io)

---

## Topology Summary

This document describes a containerlab-based streaming telemetry lab with:
- **2 Spine routers** (Nokia SR Linux)
- **3 Leaf switches** (Nokia SR Linux)
- **3 Client servers** (Linux multitool)
- **5 Telemetry/Logging nodes** (gnmic, Prometheus, Grafana, Promtail, Loki)

---

## Nodes Discovered

| Name | Role | Platform | OS Version | Loopback IP | Management IP |
|------|------|----------|------------|-------------|---------------|
| spine1 | spine | Nokia 7220 IXR-D3L | SR Linux v24.10.1 | 10.0.2.1 | 172.80.80.21 |
| spine2 | spine | Nokia 7220 IXR-D3L | SR Linux v24.10.1 | 10.0.2.2 | 172.80.80.22 |
| leaf1 | leaf | Nokia 7220 IXR-D2L | SR Linux v24.10.1 | 10.0.1.1 | 172.80.80.11 |
| leaf2 | leaf | Nokia 7220 IXR-D2L | SR Linux v24.10.1 | 10.0.1.2 | 172.80.80.12 |
| leaf3 | leaf | Nokia 7220 IXR-D2L | SR Linux v24.10.1 | 10.0.1.3 | 172.80.80.13 |
| client1 | client | Linux (network-multitool) | - | - | 172.80.80.31 |
| client2 | client | Linux (network-multitool) | - | - | 172.80.80.32 |
| client3 | client | Linux (network-multitool) | - | - | 172.80.80.33 |
| gnmic | telemetry | Linux (gnmic) | - | - | 172.80.80.41 |
| prometheus | telemetry | Linux (Prometheus) | v2.54.1 | - | 172.80.80.42 |
| grafana | telemetry | Linux (Grafana) | 11.2.0 | - | 172.80.80.43 |
| promtail | logging | Linux (Promtail) | 3.2.0 | - | 172.80.80.45 |
| loki | logging | Linux (Loki) | 3.2.0 | - | 172.80.80.46 |

---

## Link Inventory

All links derived from live LLDP neighbor discovery and interface configurations.

| A-Node | A-Interface | B-Node | B-Interface | Subnet | Evidence |
|--------|-------------|--------|--------------|--------|----------|
| spine1 | ethernet-1/1 | leaf1 | ethernet-1/49 | 192.168.11.0/31 | LLDP neighbor (spine1 sees leaf1:e1-49, leaf1 sees spine1:e1-1) |
| spine1 | ethernet-1/2 | leaf2 | ethernet-1/49 | 192.168.21.0/31 | LLDP neighbor (spine1 sees leaf2:e1-49, leaf2 sees spine1:e1-2) |
| spine1 | ethernet-1/3 | leaf3 | ethernet-1/49 | 192.168.31.0/31 | LLDP neighbor (spine1 sees leaf3:e1-49, leaf3 sees spine1:e1-3) |
| spine2 | ethernet-1/1 | leaf1 | ethernet-1/50 | 192.168.12.0/31 | LLDP neighbor (spine2 sees leaf1:e1-50, leaf1 sees spine2:e1-1) |
| spine2 | ethernet-1/2 | leaf2 | ethernet-1/50 | 192.168.22.0/31 | LLDP neighbor (spine2 sees leaf2:e1-50, leaf2 sees spine2:e1-2) |
| spine2 | ethernet-1/3 | leaf3 | ethernet-1/50 | 192.168.32.0/31 | LLDP neighbor (spine2 sees leaf3:e1-50, leaf3 sees spine2:e1-3) |
| leaf1 | ethernet-1/1 | client1 | eth1 | 172.17.0.0/24 | Interface config (leaf1:e1-1 in vrf-1 mac-vrf), client1:eth1 UP |
| leaf2 | ethernet-1/1 | client2 | eth1 | 172.17.0.0/24 | Interface config (leaf2:e1-1 in vrf-1 mac-vrf), client2:eth1 UP |
| leaf3 | ethernet-1/1 | client3 | eth1 | 172.17.0.0/24 | Interface config (leaf3:e1-1 in vrf-1 mac-vrf), client3:eth1 UP |

---

## IP Address Summary

### Loopback Addresses (Router IDs)
| Node | Loopback IP |
|------|-------------|
| spine1 | 10.0.2.1/32 |
| spine2 | 10.0.2.2/32 |
| leaf1 | 10.0.1.1/32 |
| leaf2 | 10.0.1.2/32 |
| leaf3 | 10.0.1.3/32 |

### Fabric /31 Point-to-Point Links
| Node | Interface | IP Address |
|------|-----------|------------|
| spine1 | ethernet-1/1 | 192.168.11.1/31 |
| spine1 | ethernet-1/2 | 192.168.21.1/31 |
| spine1 | ethernet-1/3 | 192.168.31.1/31 |
| spine2 | ethernet-1/1 | 192.168.12.1/31 |
| spine2 | ethernet-1/2 | 192.168.22.1/31 |
| spine2 | ethernet-1/3 | 192.168.32.1/31 |
| leaf1 | ethernet-1/49 | 192.168.11.0/31 |
| leaf1 | ethernet-1/50 | 192.168.12.0/31 |
| leaf2 | ethernet-1/49 | 192.168.21.0/31 |
| leaf2 | ethernet-1/50 | 192.168.22.0/31 |
| leaf3 | ethernet-1/49 | 192.168.31.0/31 |
| leaf3 | ethernet-1/50 | 192.168.32.0/31 |

### Client Networks
| Node | Interface | IP Address |
|------|-----------|------------|
| client1 | eth1 | 172.17.0.1/24 |
| client2 | eth1 | 172.17.0.2/24 |
| client3 | eth1 | 172.17.0.3/24 |

### Management Network
| Subnet | Gateway |
|--------|---------|
| 172.80.80.0/24 | 172.80.80.1 |

---

## Per-Device Facts

### spine1
- **Hostname:** spine1
- **Chassis:** 7220 IXR-D3L
- **Serial:** Sim Serial No.
- **MAC:** 1A:CC:0B:FF:00:00
- **Software:** SR Linux v24.10.1 (build 492-gf8858c5836)
- **Uptime:** 2026-03-12T13:43:46.934Z
- **Active Interfaces:** ethernet-1/1, ethernet-1/2, ethernet-1/3 (all UP, 100G)
- **Routing:** BGP learned routes to loopbacks via fabric interfaces

### spine2
- **Hostname:** spine2
- **Chassis:** 7220 IXR-D3L
- **Serial:** Sim Serial No.
- **MAC:** 1A:9E:0C:FF:00:00
- **Software:** SR Linux v24.10.1 (build 492-gf8858c5836)
- **Uptime:** 2026-03-12T13:43:47.085Z
- **Active Interfaces:** ethernet-1/1, ethernet-1/2, ethernet-1/3 (all UP, 100G)
- **Routing:** BGP learned routes to loopbacks via fabric interfaces

### leaf1
- **Hostname:** leaf1
- **Chassis:** 7220 IXR-D2L
- **Serial:** Sim Serial No.
- **MAC:** 1A:01:05:FF:00:00
- **Software:** SR Linux v24.10.1 (build 492-gf8858c5836)
- **Uptime:** 2026-03-12T13:43:46.997Z
- **Active Interfaces:** 
  - ethernet-1/1 (UP, 25G, bridged to vrf-1)
  - ethernet-1/49 (UP, 100G, routed)
  - ethernet-1/50 (UP, 100G, routed)
- **Routing:** BGP ECMP to spines, local routes to fabric /31s

### leaf2
- **Hostname:** leaf2
- **Chassis:** 7220 IXR-D2L
- **Serial:** Sim Serial No.
- **MAC:** 1A:1F:06:FF:00:00
- **Software:** SR Linux v24.10.1 (build 492-gf8858c5836)
- **Uptime:** 2026-03-12T13:43:47.094Z
- **Active Interfaces:**
  - ethernet-1/1 (UP, 25G, bridged to vrf-1)
  - ethernet-1/49 (UP, 100G, routed)
  - ethernet-1/50 (UP, 100G, routed)

### leaf3
- **Hostname:** leaf3
- **Chassis:** 7220 IXR-D2L
- **Serial:** Sim Serial No.
- **MAC:** 1A:20:07:FF:00:00
- **Software:** SR Linux v24.10.1 (build 492-gf8858c5836)
- **Uptime:** 2026-03-12T13:43:46.984Z
- **Active Interfaces:**
  - ethernet-1/1 (UP, 25G, bridged to vrf-1)
  - ethernet-1/49 (UP, 100G, routed)
  - ethernet-1/50 (UP, 100G, routed)

### client1
- **Management:** 172.80.80.31/24 (eth0)
- **Data:** 172.17.0.1/24 (eth1)
- **IPv6:** 2002::172:17:0:1/96
- **Services:** iperf3 servers on ports 5201, 5202

### client2
- **Management:** 172.80.80.32/24 (eth0)
- **Data:** 172.17.0.2/24 (eth1)
- **IPv6:** 2002::172:17:0:2/96

### client3
- **Management:** 172.80.80.33/24 (eth0)
- **Data:** 172.17.0.3/24 (eth1)
- **IPv6:** 2002::172:17:0:3/96

---

## Discovery Evidence

| Node | Command | Key Facts Confirmed |
|------|---------|---------------------|
| spine1 | `show version` | Platform: 7220 IXR-D3L, Software: v24.10.1 |
| spine1 | `show interface brief` | Active: e1-1, e1-2, e1-3 (100G UP) |
| spine1 | `show system lldp neighbor` | LLDP to leaf1:e1-49, leaf2:e1-49, leaf3:e1-49 |
| spine1 | `show interface ethernet-1/X` | Fabric IPs: 192.168.11.1/31, 192.168.21.1/31, 192.168.31.1/31 |
| spine1 | `show network-instance default route-table` | BGP routes to loopbacks 10.0.1.x and 10.0.2.x |
| spine2 | `show version` | Platform: 7220 IXR-D3L, Software: v24.10.1 |
| spine2 | `show system lldp neighbor` | LLDP to leaf1:e1-50, leaf2:e1-50, leaf3:e1-50 |
| spine2 | `show interface ethernet-1/X` | Fabric IPs: 192.168.12.1/31, 192.168.22.1/31, 192.168.32.1/31 |
| leaf1 | `show version` | Platform: 7220 IXR-D2L, Software: v24.10.1 |
| leaf1 | `show system lldp neighbor` | LLDP to spine1:e1-1, spine2:e1-1 |
| leaf1 | `show interface ethernet-1/1` | Type: bridged, Network-instance: vrf-1 (mac-vrf) |
| leaf1 | `show interface ethernet-1/49` | Fabric IP: 192.168.11.0/31 |
| leaf1 | `show interface ethernet-1/50` | Fabric IP: 192.168.12.0/31 |
| leaf1 | `show network-instance default route-table` | BGP ECMP routes to spines |
| leaf1 | `show arpnd arp-entries` | MAC addresses for spines and telemetry nodes |
| leaf2 | `show system lldp neighbor` | LLDP to spine1:e1-2, spine2:e1-2 |
| leaf3 | `show system lldp neighbor` | LLDP to spine1:e1-3, spine2:e1-3 |
| client1 | `ip addr show` | eth0: 172.80.80.31, eth1: 172.17.0.1 |
| client2 | `ip addr show` | eth0: 172.80.80.32, eth1: 172.17.0.2 |
| client3 | `ip addr show` | eth0: 172.80.80.33, eth1: 172.17.0.3 |
| gnmic | `ip addr show` | eth0: 172.80.80.41 |
| prometheus | `ip addr show` | eth0: 172.80.80.42 |
| grafana | `ip addr show` | eth0: 172.80.80.43 |
| loki | `ip addr show` | eth0: 172.80.80.46 |

---

## Topology Diagram

The topology diagram is available in `output/topology.drawio`. Import this file into diagrams.net or draw.io desktop to view and edit.

### Layout
- **Spines:** Top row (y=80) - Nokia IXR-D3L routers
- **Leaves:** Middle row (y=280) - Nokia IXR-D2L switches
- **Clients:** Bottom row (y=480) - Linux servers
- **Telemetry/Logging:** Right side (x=600) - Monitoring stack

### Visual Legend
- **Blue:** Spine routers (rounded, fillColor=#dae8fc)
- **Green:** Leaf switches (rounded, fillColor=#d5e8d4)
- **Yellow:** Client servers (rounded, fillColor=#fff2cc)
- **Red:** Telemetry/Logging (rounded, fillColor=#f8cecc)

---

## Notes

1. **Fabric Design:** Two-tier CLOS topology with dual-connected leaves
2. **Routing:** BGP unnumbered (using /31 point-to-point links)
3. **Client Connectivity:** Layer 2 bridge (mac-vrf) per leaf
4. **Telemetry:** gnmic collects gNMI telemetry from all routers; Prometheus stores metrics; Grafana provides visualization
5. **Logging:** Promtail forwards logs to Loki
