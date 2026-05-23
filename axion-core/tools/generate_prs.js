/**
 * # TOOL-STAR-002: PRS Generator (Coherence Filter)
 *
 * ## I. Universal Identification & Provenance (The Vector Signature)
 * | Field                  | Value                                                    |
 * | :--------------------- | :------------------------------------------------------- |
 * | **1. Artifact ID**     | `TOOL-STAR-002`                                          |
 * | **2. Official Name**   | `generate_prs.js`                                        |
 * | **3. Version**         | **v11.1**                                                |
 * | **4. Provenance**      | **Reforged: 2026-01-30**                                 |
 * | **5. Domain**          | `ARCH`                                                   |
 * | **6. Evolution**       | **Cognitive Ascension**                                  |
 * | **7. Celestial Class** | `[PLANET]`                                               |
 * | **8. Tier**            | **Operational**                                          |
 * | **9. Status (State)**  | `[ACTIVE]`                                               |
 * | **10. Ethos**          | **Knowledge Graphing**                                   |
 * | **11. Catalyst**       | **Rosetta Stone Generation**                             |
 * | **12. Relations**      | `LINK: [CHAR-AXION-001](../../../src/agents/axion/CHAR-AXION-001_AgentAxionPersona_v1.0.md)`, `LINK: [GVRN-SYNERGY-001](../../../docs/GVRN/GVRN-SYNERGY-001.md)` |
 * | **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |
 *
 * ---
 *
 * ### **I.B. Standardized Synergy Block (The Loom Signature)**
 *
 * > [!NOTE]
 * > The following block is parsed by `TOOL-MAP-001` for architectural visualization.
 *
 * Synergistic Artifact ID, Relationship Type, Synergistic Impact
 * CHAR-AXION-001, WIELDS, The Star persona uses this tool for master graphing.
 * GVRN-SYNERGY-001, GOVERNS, This tool is governed by the Workshop Synergy.
 *
 * ---
 *
 * # --- RPG FRAMEWORK INTEGRATION ---
 * # System Slot: Coherence Filter (The Star)
 * # Synergy Set: The Star's Radiance
 * # Primary Stat Buff: Perception (+10), Retention (+15)
 * # Passive Ability: The Guiding Light (Knowledge Mapping)
 * # Cognitive Load Cost: Medium
 * # XP Award Value: 100 XP
 *
 * ---
 *
 * ## IV. Actionable Prompt Packet (APP)
 * | Command ID | Action | Impact |
 * | :--- | :--- | :--- |
 * | `CMD: GENERATE_PRS` | Build Rosetta Stone JSON | Knowledge Graphing |
 * | `⚡ EXECUTE: RADIATE` | Global Metadata Scan | Universal Alignment |
 */

const fs = require("node:fs");
const path = require("node:path");

const log = console.log;

// --- CONFIGURATION ---
const CONFIG = {
    scanDirs: ["../../_governance", "../../.agent", "./"],
    outputFile: "./PRS-001.json",
    allowedExtensions: [".md", ".txt", ".py", ".js", ".cjs", ".ts"], // Added code extensions
    prsHeader: {
        artifact_id: "PRS-001",
        official_name: "The Phoenix Rosetta Stone (Axion Core)",
        version: "5.2 (Hephaestus Update)",
        last_updated: new Date().toISOString(),
        governing_ethos: "Guardian of Truth",
        description: "The Master Navigational Hub and Knowledge Graph for Axion Core.",
    },
};

/**
 * Generates an array of robust regex patterns for a specific metadata key.
 * @param {string} keyPattern - The key to match (e.g., "Artifact ID")
 * @returns {RegExp[]}
 */
const getPatterns = (keyPattern) => [
    // 1. Table Form: | **1. Artifact ID** | `UMB-PRS-001` |
    new RegExp(
        "\\|\\s*(?:\\*\\*[\\d.]+\\s*)?\\*\\*" + keyPattern + "\\*\\*\\s*\\|\\s*`?([^`|\\n]+)`?(?:\\s*\\|)?",
        "i",
    ),
    // 2. Bold/Colon Form: **Artifact ID:** `UMB-PRS-001` (Stops at next field or end of line)
    new RegExp("(?:\\*\\*)?" + keyPattern + "(?:\\*\\*)?\\s*[:|]\\s*`?(.*?)`?(?=\\s*(?:\\*\\*|\\||$))", "i"),
];

// --- REGEX PATTERNS (The Upgraded Eyes) ---
const PATTERNS = {
    id: [
        ...getPatterns("Artifact ID"),
        ...getPatterns("Module ID"),
        ...getPatterns("Blueprint ID"),
        ...getPatterns("Playbook ID"),
        ...getPatterns("Command ID"),
        ...getPatterns("Log ID"),
        ...getPatterns("Artifact-ID"),
        ...getPatterns("Metric ID"),
    ],
    name: [
        ...getPatterns("Official Name"),
        ...getPatterns("Module Name"),
        ...getPatterns("Blueprint Title"),
        ...getPatterns("Playbook Title"),
        ...getPatterns("Command Title"),
        ...getPatterns("Metric Title"),
        ...getPatterns("Log Title"),
    ],
    type: getPatterns("(?:Artifact Type|Type|Celestial Class)"),
    domain: getPatterns("(?:Primary Domain Alignment|Primary Domain|Domain)"),
    purpose: getPatterns("(?:Core Purpose|Purpose|Objective|Description)"),
    tags: getPatterns("(?:Semantic Tags|Tags)"),
    governance: getPatterns("(?:Governance|Authority)"),
    upstream: getPatterns("Upstream"),
    downstream: getPatterns("(?:Downstream|Subordinates)"),
    integrity: getPatterns("Integrity Hash"),
    dependencies: getPatterns("(?:Dependency-Hash|Dependencies|Upstream)"),
    references: /(?:UMB|AOP|GUCA|SELT|DOC|gw|PHL|ARCH|GVRN|CRTV|LOGS|CODE)-[A-Z0-9]{2,}-\d{3}|AISTF|OGLN|Synarche/g,
};

// --- HELPER FUNCTIONS ---

/**
 * Strips markdown syntax from text.
 * @param {string} text
 * @returns {string}
 */
function cleanText(text) {
    if (!text) return "";
    return text.replaceAll(/(?:^[\s*#_`]+)|(?:[\s*#_`]+$)/g, "").trim();
}

/**
 * Extracts specific metadata field using regex(es).
 * @param {string} content
 * @param {RegExp|RegExp[]} patterns
 * @returns {string|null}
 */
function extractField(content, patterns) {
    const patternList = Array.isArray(patterns) ? patterns : [patterns];
    for (const pattern of patternList) {
        const match = pattern.exec(content);
        if (match && match[1]) return cleanText(match[1]);
    }
    return null;
}

const TYPE_PREFIXES = {
    UMB: "Blueprint",
    AOP: "Protocol",
    GUCA: "Command",
    SELT: "Log",
    DOC: "Documentation",
};

/**
 * Infers artifact type from ID or explicit field.
 * @param {string} typeRaw
 * @param {string} id
 * @returns {string}
 */
function inferType(typeRaw, id) {
    if (typeRaw) return cleanText(typeRaw);
    const prefix = id.split("-")[0];
    return TYPE_PREFIXES[prefix] || "Artifact";
}

/**
 * Parses a string into an array of clean values (handles brackets, comma/pipe separation).
 * @param {string} raw
 * @returns {string[]}
 */
function parseList(raw) {
    if (!raw) return [];
    return raw
        .replace(/[\[\]]/g, "")
        .split(/[,|]/)
        .map((val) => cleanText(val))
        .filter(Boolean);
}

/**
 * Parses a single file for metadata.
 * @param {string} filePath
 * @returns {object|null} Node object or null if invalid
 */
function parseFile(filePath) {
    try {
        const content = fs.readFileSync(filePath, "utf8");
        const filename = path.basename(filePath);

        const id = extractField(content, PATTERNS.id) || `UNKNOWN-${filename}`;
        const label = extractField(content, PATTERNS.name) || filename;

        // Skip totally invalid files
        if (id.startsWith("UNKNOWN") && !filename.includes("PRS") && !filename.includes("test")) return null;

        const typeraw = extractField(content, PATTERNS.type);
        const type = inferType(typeraw, id);

        let definition = extractField(content, PATTERNS.purpose) || "No definition found.";
        definition = definition.replace(/^Summary:\s*/i, "");
        if (definition.length > 300) definition = definition.substring(0, 297) + "...";

        const domain = extractField(content, PATTERNS.domain);
        const tags = parseList(extractField(content, PATTERNS.tags));
        if (domain) tags.push(domain);

        // Dynamic Metadata Extraction
        const governance = parseList(extractField(content, PATTERNS.governance));
        const upstream = parseList(extractField(content, PATTERNS.upstream));
        const downstream = parseList(extractField(content, PATTERNS.downstream));
        const integrity_hash = extractField(content, PATTERNS.integrity);
        const dependencies = parseList(extractField(content, PATTERNS.dependencies));

        const refMatches = content.match(PATTERNS.references) || [];
        const referenced_ids = [...new Set(refMatches)].map(cleanText).filter((r) => r !== id);

        return {
            id,
            label,
            type,
            definition,
            tags: [...new Set(tags)],
            location: filePath.replaceAll("\\", "/"),
            governance,
            upstream,
            downstream,
            integrity_hash,
            dependencies,
            referenced_ids,
        };
    } catch (err) {
        console.warn(`[WARNING] Failed to read ${filePath}: ${err.message}`);
        return null;
    }
}

/**
 * Recursively scans directory for allowed files.
 * @param {string} dir
 * @returns {string[]}
 */
function scanFiles(dir) {
    let results = [];
    if (!fs.existsSync(dir)) return [];

    const list = fs.readdirSync(dir);
    for (const file of list) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);

        if (stat && stat.isDirectory()) {
            results = results.concat(scanFiles(fullPath));
        } else if (CONFIG.allowedExtensions.includes(path.extname(file))) {
            results.push(fullPath);
        }
    }
    return results;
}

// --- MAIN LOGIC ---

function buildRegistry(nodes) {
    const registry = { UMBs: [], AOPs: [], GUCAs: [], SELTs: [], Others: [] };

    nodes.forEach((node) => {
        const entry = { id: node.id, status: "Active", path: node.location };
        if (node.id.startsWith("UMB")) registry.UMBs.push(entry);
        else if (node.id.startsWith("AOP")) registry.AOPs.push(entry);
        else if (node.id.startsWith("GUCA")) registry.GUCAs.push(entry);
        else if (node.id.startsWith("SELT")) registry.SELTs.push(entry);
        else registry.Others.push(entry);
    });

    return registry;
}

function weaveLinks(nodes) {
    const links = [];
    const nodeMap = new Map(nodes.map((n) => [n.id, n]));

    nodes.forEach((source) => {
        if (!source.referenced_ids) return;
        source.referenced_ids.forEach((targetId) => {
            if (nodeMap.has(targetId)) {
                links.push({
                    source: source.id,
                    target: targetId,
                    relation: "REFERENCES",
                    weight: 0.5,
                    description: `Reference from ${source.label}`,
                });
            }
        });
    });

    return links;
}

function main() {
    log(`\n✨ RADIATING COHERENCE (THE STAR: GENESIS PROTOCOL)...`);

    const allFiles = CONFIG.scanDirs.flatMap((dir) => {
        console.log(`📂 Scanning: ${dir}`);
        return scanFiles(dir);
    });

    console.log(`📄 Found ${allFiles.length} candidates.`);

    // Ingest
    const nodes = allFiles.map(parseFile).filter((n) => n !== null);
    console.log(`✅ Ingested ${nodes.length} valid artifacts.`);

    // Link
    console.log(`🕸️  Weaving Connections...`);
    const links = weaveLinks(nodes);

    // Assemble
    const grimoire = {
        ...CONFIG.prsHeader,
        cognitive_loom: { nodes, links },
        registry: buildRegistry(nodes),
        omni_log_summary: {
            total_nodes: nodes.length,
            total_links: links.length,
            last_generated: new Date().toISOString(),
        },
    };

    // Save
    fs.writeFileSync(CONFIG.outputFile, JSON.stringify(grimoire, null, 2));
    console.log(`✨ SUCCESS: Grimoire updated at ${CONFIG.outputFile}`);
    console.log(`️  System Online. Zero Entropy Achieved.`);
}

// --- EXECUTE ---
main();
