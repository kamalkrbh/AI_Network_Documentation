---
name: netbox-sync-from-live
description: "Use when: populating or reconciling NetBox from live-discovered topology and per-device facts; avoid containerlab config folders as source of truth."
---

# Skill: NetBox Sync From Live

Goal:

Populate NetBox from live-discovered device/interface/link data.

Important:

This skill supports direct write to NetBox from live device facts.

NetBox instance: http://localhost:8001
Credentials: admin / admin

Authentication (NetBox 4.5.4 — session-based):

1. GET /login/ to obtain csrftoken cookie
2. POST /login/ with csrfmiddlewaretoken, username, password
3. Set X-CSRFToken header on all subsequent API requests

Prerequisites:

- Topology model produced by live-topology-discovery.
- NetBox API endpoint and credentials (above).

Do not use as source of truth:

- /home/kamal/srl-telemetry-lab/configs/**
- /home/kamal/srl-telemetry-lab/clab-st/**

Sync order (respect foreign key dependencies):

1. Tag: source=live-discovery
2. Site: containerlab-labs
3. Manufacturers
4. Device Types
5. Device Roles (spine, leaf, server)
6. Devices
7. Interfaces
8. IP Addresses (assigned to interfaces)
9. Cables (only from live LLDP or veth peer evidence)

Procedure:

1. Ensure target site exists (for example: containerlab-labs).
2. Upsert devices by node name.
3. Upsert interfaces from live interface list.
4. Upsert cables from validated live links.
5. Upsert management IPs only if discovered from live node data.
6. Tag all imported objects with source=live-discovery.

Rules:

- Tag every created object with source=live-discovery
- If object exists, update it to match live state
- Never use /home/kamal/srl-telemetry-lab/configs/ or clab-st/ as source

Conflict handling:

- If NetBox differs from live state, prefer live state.
- Keep an audit record with old and new values.

Output:

- Sync summary with created, updated, skipped, failed counts.
- Reconciliation report for conflicts.
