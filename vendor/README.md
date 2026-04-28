# 📦 DOMAIN: VENDOR
## OGLN Protocol: [EXTERNAL_CONTAINMENT]

> "Verify the Bridge, Secure the Shore."

---

### 📖 Intent
This directory contains all third-party dependencies and external integrations (e.g., Esperanto). These are treated as **Black Box** modules, isolated from the core Synarchy logic by mandatory **Nexus Beacons (index.ts)**.

### 📜 Sovereign Rules
1. **The Beacon Gate**: No core module may import from `vendor/` without passing through an `index.ts` gateway.
2. **Immutability**: Vendor code is never modified locally. All extensions must occur in the `@fabric` layer.
3. **Audit Trails**: All vendor updates must be preceded by a Systemic Synergy Audit.

### 🗺️ Signposts
- `esperanto/` — The primary LLM/STT/TTS abstraction bridge.
- `data/` — Static external reference datasets.

---
`[OMNI-ARTIFACT-ANCHOR] ID: VENDOR.DOMAIN.Gateway VER: v15.0 [OMEGA] STATUS: CANONIZED TS: 2026-04-28`
