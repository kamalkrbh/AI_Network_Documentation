---
name: cleanup
description: "Use when: preparing for a fresh network discovery run by cleaning output files and wiping NetBox tagged objects."
---

# Skill: Cleanup

Goal:

Prepare for a fresh network discovery run by cleaning previous outputs and NetBox data.

This skill provides a cleanup script that:

1. Removes generated output files (topology.drawio, topology.md)
2. Wipes all NetBox objects tagged with source=live-discovery

## Usage

Run the cleanup script before starting a new discovery:

```bash
python3 .opencode/skills/cleanup/cleanup.py
```

## What Gets Cleaned

### Output Files
- `/home/kamal/AI_Network_Documentation/output/topology.drawio`
- `/home/kamal/AI_Network_Documentation/output/topology.md`

### NetBox Objects
All objects tagged with `source=live-discovery`, deleted in reverse foreign-key order:
1. Cables
2. IP Addresses
3. Interfaces
4. Devices
5. Device Types
6. Device Roles
7. Manufacturers
8. Platforms
9. Sites
10. Tags

## Configuration

NetBox connection (configured in cleanup.py):
- Instance: http://localhost:8001
- Credentials: admin / admin

## When to Use

- Before running a fresh topology discovery
- When you need to reset NetBox to a clean state
- As part of the /document-network pipeline

## Notes

- If the tag 'live-discovery' doesn't exist in NetBox, the script will skip NetBox cleanup
- The script uses session-based authentication (NetBox 4.5.4)
- Deletion order respects foreign key constraints to avoid errors
