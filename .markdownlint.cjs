/**
 * # GVRN-LINT-001: The Phoenix Linter (Markdownlint Config)
 *
 * ## Genesis Stamp: 2026-02-01 | Domain: GVRN | State: CANONIZED | Criticality: Critical
 *
 * ### I. Universal Identification & Provenance (The Vector Signature)
 *
 * #### The Chronos Lock & Axiomatic Metadata Layer
 *
 * | Field                  | Value                                                    |
 * | :--------------------- | :------------------------------------------------------- |
 * | **1. Artifact ID**     | `GVRN-LINT-001`                                          |
 * | **2. Official Name**   | `.markdownlint.cjs`                                      |
 * | **3. Version**         | **v13.0**                                                |
 * | **4. Provenance**      | **Reforged: 2026-02-01**                                 |
 * | **5. Domain**          | `GVRN`                                                   |
 * | **6. Evolution**       | **Cognitive Ascension**                                  |
 * | **7. Celestial Class** | `[MOON]`                                                 |
 * | **8. Tier**            | **Operational**                                          |
 * | **9. Status (State)**  | `[ACTIVE]`                                               |
 * | **10. Ethos**          | **Guardian of Coherence**                                |
 * | **11. Catalyst**       | **Protocol Standardization**                             |
 * | **12. Relations**      | `LINK: [./tools/rules/axion-rules.cjs], LINK: [./cspell.json]` |
 * | **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |
 *
 * ---
 *
 * ### I.B. Standardized Synergy Block (The Loom Signature)
 *
 * Synergistic Artifact ID | Relationship Type | Synergistic Impact
 * UMB-RULES-001          | INTEGRATES        | Imports custom logic to enforce the Phoenix Protocol.
 * GVRN-FMT-001          | ENFORCES          | The primary tool for enforcing the presentation standard.
 */

"use strict";

module.exports = {
    customRules: [require("./tools/rules/axion-rules.cjs")],
    config: {
        default: true,
        MD001: { level: 1 },
        MD003: { style: "atx" },
        MD004: { style: "dash" },
        MD005: true,
        MD007: { indent: 4 },
        MD009: { br_spaces: 0 },
        MD010: { code_blocks: false, tabs: false },
        MD013: { line_length: 120, code_blocks: false, tables: false },
        MD022: true,
        MD024: { allow_different_nesting: true },
        MD025: { level: 1, front_matter_title: "" },
        MD026: { punctuation: ".,;:!?" },
        MD029: { style: "ordered" },
        MD030: false,
        MD032: true,
        MD041: true,
        MD047: true,
        MD033: {
            allowed_elements: ["br", "details", "summary", "sub", "sup", "u", "integer"],
        },
        MD034: true,
        MD036: false,
        MD040: true,
        MD046: { style: "fenced" },
        MD048: { style: "backtick" },
        MD051: true,
        MD052: true,
        MD053: true,
        PF001: true,
        PF002: true,
        PF003: true,
        PF004: true,
        PF005: true,
        PF006: true,
        PF007: true,
        PF008: true,
        PF009: true,
        PF010: true,
        PF011: true,
        PF012: true,
        PF013: true,
        PF014: true,
        PF015: true,
        PF016: true,
        PF017: true,
        PF018: true,
        PF019: true,
        PF020: true,
        PF021: true,
        PF022: true,
        PF023: true,
    },
};
