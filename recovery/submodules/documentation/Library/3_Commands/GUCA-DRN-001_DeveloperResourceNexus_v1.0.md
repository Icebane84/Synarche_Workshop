---
# Universal Identification & Provenance (UIP)
| Key | Value |
| :--- | :--- |
| **Module ID** | `GUCA-DRN-001_DEVELOPERRESOURCENEXUS_V1.0` |
| **Version** | `v11.0` |
| **Evolution** | **Cognitive Ascension** |
| **Status** | `ACTIVE` |
---

---

# GUCA-DRN-001_DeveloperResourceNexus_v1.0

# [STAR] (The Central Gravity)

| :------------------ | :--------------------------------------------- |
| **1. Artifact ID** | `GUCA-DRN-001` |
| **2. Official Name** | `GUCA-DRN-001_DeveloperResourceNexus_v1.0.md` |
| **3. Version** | **v1.0** |
| **4. Provenance** | **Genesis Stamp: 2025-11-24** |
| **5. Domain** | `FLICSS` (Synthesis System) |
| **6. Evolution** | **Documentation Hub Genesis** |
| **7. Celestial Class** | `[STAR]` (The Central Gravity) |
| **8. Tier** | **Universal Command Architecture** |
| **9. State** | `[ACTIVE]` |
| **10. Ethos** | **Single Source of Truth** |
| **11. Catalyst** | **Comprehensive Documentation Mandate** |
| **12. Relations** | `ORCHESTRATES: FLICSS-BLUEPRINTS; GOVERNS: DEV_STANDARDS` |

---

> [!IMPORTANT]
> **Developer Resource Nexus (DRN):**
> The central, single-source-of-truth documentation system for the Phoenix Form AI project. This hub integrates architectural blueprints (UMB), operational playbooks (AOP), and universal commands (GUCA) into a synergistic framework.

## **1. Architectural Foundation**

The system is governed by the **Cognitive Loom (Phoenix Geode)**. It is a unified organism where data flow is managed by the **Spine** (central message bus), connecting specialized cognitive organs.

### **1.1. Cognitive Organs**

| Organ           | Function                              | Governing Artifact       |
| :-------------- | :------------------------------------ | :----------------------- |
| **The Stomach** | Ingestion & Sanitization              | `AOP-FLICSS-STOMACH-001` |
| **The Heart**   | Context & Urgency Orchestration       | `UMB-FLICSS-HEART-001`   |
| **The Brain**   | Long-Term Memory (Knowledge Graph)    | `UMB-FLICSS-BRAIN-001`   |
| **The Hands**   | Output & Personalization              | `AOP-FLICSS-HANDS-001`   |
| **The Spine**   | Central Nervous System (Data Highway) | `UMB-FLICSS-SPINE-001`   |

---

## **2. Initial Setup Instructions**

The project uses a microservices architecture with a React/TypeScript frontend and Neo4j graph database.

| Step  | Action             | Detail/Command                                      |
| :---- | :----------------- | :-------------------------------------------------- |
| **1** | **Environment**    | Install Node.js (LTS), Docker, and Git.             |
| **2** | **Database**       | `docker-compose up neo4j -d`                        |
| **3** | **Spine/Backend**  | `cd services/spine && npm install && npm run start` |
| **4** | **Hands/Frontend** | `cd client/hands-ui && npm install && npm run dev`  |
| **5** | **Calibration**    | `CMD:ORG:HANDSHAKE -a all`                          |

---

## **3. Coding Conventions**

### **3.1. Naming & Style**

- **PascalCase:** Components and Interfaces (e.g., `NodeData`).
- **camelCase:** Variables and Functions (e.g., `handleForgeSynergy`).
- **Module Style:** Logic must be self-contained within the AOP/UMB definitions.

### **3.2. Versioning & Provenance**

All official reports (AOP, UMB, GUCA, SELT) must include:

- **Date:** `YYYY-MM-DD`
- **Time:** `[Time] EST`
- **Standard:** Phoenix Genesis Presentation Standard (PGPS).

---

## **4. Universal Commands**

- `CMD:INGEST:FORGE`: Initiates a cross-organ ingestion cycle.
- `CMD:ORG:FINGERPRINT`: Modifies organ optimization priorities.
- `CMD:QA:COHERENCE`: Locks provenance and verifies metadata.

---

## **Actionable Prompt Packet**

- `CMD:ORG:HANDSHAKE --audit`
- `CMD:DATA:SPINE --status`
