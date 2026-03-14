---
description: "Full network documentation pipeline: discover live topology and generate a draw.io diagram, then sync to NetBox."
---

## Pre-run cleanup

Before starting the pipeline, use the `cleanup` skill to prepare for a fresh discovery run:

```
skill("cleanup")
```

The cleanup skill will:
- Remove previous output files (topology.drawio, topology.md)
- Wipe all NetBox objects tagged with source=live-discovery

Run the cleanup script as documented in the skill.

If you see errors, they are non-fatal — continue with the pipeline regardless.

---

Run the network documentation pipeline for the containerlab lab at /home/kamal/srl-telemetry-lab.

## Phase 1 — Topology discovery

Launch **topology_agent** and wait for it to complete.

It will log into every node, collect live state and full config, and write:
- `output/topology.drawio` — draw.io XML diagram (importable into diagrams.net / draw.io desktop)
- `output/topology.md` — Markdown summary with link tables, IP tables, per-device facts, and evidence

Do NOT produce or reference Mermaid diagrams.

## Phase 2 — NetBox sync

Once topology_agent has finished, launch **netbox_agent** using the topology model returned from Phase 1.

Sync all discovered nodes, interfaces, IPs, and links to NetBox at http://localhost:8001 using netbox_sync.py.

## Summary

After both phases complete, summarise:
- Topology: nodes found, links confirmed, output/topology.drawio and output/topology.md written
- NetBox: objects created/updated/failed
