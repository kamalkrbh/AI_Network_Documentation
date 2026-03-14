#!/usr/bin/env python3
"""
cleanup.py — Pre-run cleanup for the /document-network pipeline.

Deletes:
  1. output/topology.drawio and output/topology.md
  2. All NetBox objects tagged source=live-discovery (reverse FK order)

Run directly:  python3 .opencode/skills/cleanup/cleanup.py
"""

import os
import sys
import requests

# ── Config ────────────────────────────────────────────────────────────────────
SCRIPT_DIR  = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR)))
OUTPUT_DIR  = os.path.join(PROJECT_DIR, "output")

NETBOX = "http://localhost:8001"
USER   = "admin"
PASS   = "admin"

# ── 1. Remove output files ────────────────────────────────────────────────────
for fname in ("topology.drawio", "topology.md"):
    path = os.path.join(OUTPUT_DIR, fname)
    if os.path.exists(path):
        os.remove(path)
        print(f"[cleanup] Removed {fname}", flush=True)
    else:
        print(f"[cleanup] {fname}: not present", flush=True)

# ── 2. Wipe NetBox tagged objects ─────────────────────────────────────────────
s = requests.Session()

r = s.get(f"{NETBOX}/login/")
csrf = r.cookies.get("csrftoken")
if not csrf:
    print("[cleanup] ERROR: could not get csrftoken — skipping NetBox cleanup", flush=True)
    sys.exit(0)

resp = s.post(
    f"{NETBOX}/login/",
    data={"csrfmiddlewaretoken": csrf, "username": USER, "password": PASS, "next": "/"},
    headers={"Referer": f"{NETBOX}/login/"},
)
if not s.cookies.get("sessionid"):
    print(f"[cleanup] ERROR: NetBox login failed (HTTP {resp.status_code}) — skipping NetBox cleanup", flush=True)
    sys.exit(0)

csrf2 = s.cookies.get("csrftoken")
if csrf2:
    s.headers.update({"X-CSRFToken": csrf2, "Referer": NETBOX})
print("[cleanup] Authenticated to NetBox", flush=True)


def tag_exists(slug):
    """Return True only if the tag slug is known to NetBox."""
    r = s.get(f"{NETBOX}/api/extras/tags/?slug={slug}&limit=1")
    return r.ok and r.json().get("count", 0) > 0


def delete_tagged(resource_path, label, tag="live-discovery"):
    url = f"{NETBOX}/api{resource_path}?tag={tag}&limit=1000"
    r = s.get(url)
    if not r.ok:
        print(f"[cleanup] Could not list {label}: HTTP {r.status_code}", flush=True)
        return
    items = r.json().get("results", [])
    if not items:
        print(f"[cleanup] {label}: nothing to delete", flush=True)
        return
    for item in items:
        dr = s.delete(f"{NETBOX}/api{resource_path}{item['id']}/")
        name = item.get("name") or item.get("address") or item.get("display") or item["id"]
        if dr.status_code in (200, 204):
            print(f"[cleanup] Deleted {label} #{item['id']} ({name})", flush=True)
        else:
            print(f"[cleanup] Failed to delete {label} #{item['id']}: HTTP {dr.status_code}", flush=True)


# Check whether the tag exists at all — if not, there is nothing to clean up
if not tag_exists("live-discovery"):
    print("[cleanup] Tag 'live-discovery' not found in NetBox — nothing to wipe", flush=True)
else:
    # Delete in reverse FK order to avoid constraint errors
    delete_tagged("/dcim/cables/",        "Cable")
    delete_tagged("/ipam/ip-addresses/",  "IP Address")
    delete_tagged("/dcim/interfaces/",    "Interface")
    delete_tagged("/dcim/devices/",       "Device")
    delete_tagged("/dcim/device-types/",  "Device Type")
    delete_tagged("/dcim/device-roles/",  "Device Role")
    delete_tagged("/dcim/manufacturers/", "Manufacturer")
    delete_tagged("/dcim/platforms/",     "Platform")
    delete_tagged("/dcim/sites/",         "Site")
    delete_tagged("/extras/tags/",        "Tag")

print("[cleanup] NetBox wipe complete", flush=True)
print("[cleanup] Done — ready for fresh discovery run", flush=True)
