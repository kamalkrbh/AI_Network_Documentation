---
name: netbox-sync-from-live
description: "Use when: populating or reconciling NetBox from live-discovered topology and per-device facts; avoid containerlab config folders as source of truth."
---

# Skill: NetBox Sync From Live

Goal:

Populate NetBox from live-discovered device/interface/link data.

Important:

This skill supports direct write to NetBox from live device facts.

Prerequisites:

- Topology model produced by live-topology-discovery.
- NetBox API endpoint and token.

Do not use as source of truth:

- /home/kamal/srl-telemetry-lab/configs/**
- /home/kamal/srl-telemetry-lab/clab-st/**

Procedure:

1. Ensure target site exists (for example: containerlab-labs).
2. Upsert devices by node name.
3. Upsert interfaces from live interface list.
4. Upsert cables from validated live links.
5. Upsert management IPs only if discovered from live node data.
6. Tag all imported objects with source=live-discovery.

Conflict handling:

- If NetBox differs from live state, prefer live state.
- Keep an audit record with old and new values.

Output:

- Sync summary with created, updated, skipped, failed counts.
- Reconciliation report for conflicts.
