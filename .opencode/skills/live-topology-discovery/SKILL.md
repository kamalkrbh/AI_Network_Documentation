---
name: live-topology-discovery
description: "Use when: discovering topology from a lab that should be treated as a real network; read only node names from st.clab.yml; log into nodes individually; derive links from live device state."
---

# Skill: Live Topology Discovery

Goal:

Build topology from live node state, not from static containerlab links or config files.

Inputs:

- Bootstrap node list from /home/kamal/srl-telemetry-lab/st.clab.yml

Allowed from bootstrap file:

- topology.nodes keys (node names only)

Forbidden from bootstrap file:

- links
- interface mappings
- kinds/images
- startup-config references
- management IPs

Forbidden project paths for topology inference:

- /home/kamal/srl-telemetry-lab/configs/**
- /home/kamal/srl-telemetry-lab/clab-st/**

Procedure:

1. Read node names from topology.nodes.
2. Resolve runtime container endpoints for each node via `docker inspect <node> --format '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}'`.
3. Log in to each node individually and collect:
   - SR Linux nodes: `show version`, `show interface brief`, `show system lldp neighbor`, `show interface ethernet-1/*`, `show arpnd arp-entries`, `show network-instance default route-table`
   - Linux clients: `ip addr show`, `ip link show`, `ip route show`
4. Collect live facts: hostname, interfaces, LLDP neighbors, running config metadata.
5. Build graph from validated adjacencies only (LLDP bidirectional, MAC table evidence, or veth peer ifindex).
6. Every link must have live neighbor evidence — no link may come from the bootstrap file.
7. Output normalized topology model and write diagram files.

Output schema:

- nodes: [{ name, role_hint, platform_hint, loopback_ip, mgmt_ip }]
- links: [{ a_node, a_if, b_node, b_if, subnet, source: "live" }]
- evidence: [{ node, command, timestamp }]

Diagram output format: **draw.io XML** (mxGraph format)

Write the diagram to: `/home/kamal/AI_Network_Documentation/output/topology.drawio`

Do NOT produce Mermaid diagrams. Do NOT embed Mermaid code blocks in any output file.

draw.io XML rules:

- Root structure: `<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>...cells...</root></mxGraphModel>`
- One `<mxCell>` per node (vertex="1") and one per link (edge="1").
- Assign sequential integer IDs starting from 2.
- Node style by role:
  - spine:    `rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=#6c8ebf;`
  - leaf:     `rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=#82b366;`
  - client:   `rounded=1;whiteSpace=wrap;html=1;fillColor=#fff2cc;strokeColor=#d6b656;`
  - telemetry:`rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;`
- Node label (HTML): `<b>name</b><br/>loopback_ip<br/>mgmt_ip`
- Edge cells: connect node cell IDs with `<mxCell edge="1" source="..." target="..." parent="1">`. Set `value` to the interface pair label (e.g. `e1-1 | e1-49`).
- Edge style: `edgeStyle=orthogonalEdgeStyle;`
- Layout: 
  - Spines in a horizontal row at the top (y=80)
  - Leaves in a horizontal row in the middle (y=280), space evenly
  - Clients in a horizontal row at the bottom (y=480)
  - Telemetry nodes at y=680 or to the right

Markdown summary output: `/home/kamal/AI_Network_Documentation/output/topology.md`

- Discovery timestamp and source-of-truth statement
- Must NOT contain Mermaid code blocks.
- Must state that the diagram is in `output/topology.drawio` (importable into draw.io / diagrams.net)
- Must include: 
  - Link inventory table (A-node, A-interface, B-node, B-interface, subnet, evidence)
  - IP address summary (loopbacks, fabric /31s, client networks, mgmt network)
  - Per-device fact tables (role, platform, OS version, loopback, mgmt IP, active interfaces)
  - Discovery evidence table (node, commands run, key facts confirmed)

Quality checks:

- Every link must have live neighbor evidence.
- No link may originate from st.clab.yml links section.
- All nodes in output must exist in topology.nodes.

Return format:

Also return the full topology model in your response:
- nodes: [{ name, role, platform, loopback_ip, mgmt_ip }]
- interfaces: { node: [{ name, ip, state }] }
- links: [{ a_node, a_if, b_node, b_if, subnet, source }]
- evidence: [{ node, command, timestamp }]
