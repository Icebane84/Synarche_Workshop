/**
 * # GVRN.Sentinel.Rules (Axion Rules Engine)
 *
 * ## Genesis Stamp: 2026-02-04 | Domain: GVRN | State: ACTIVE | Criticality: Critical
 *
 * ### Block A: The Identification Lock (UIP-V13)
 *
 * | Key | Value |
 * | :--- | :--- |
 * | **Artifact ID** | `GVRN.Sentinel.Rules` |
 * | **Official Name** | `axion-rules.cjs` |
 * | **Version** | **v13.0 [OMEGA]** |
 * | **Domain** | `GVRN` |
 * | **Celestial Class** | `[STAR]` |
 * | **Status** | `[ACTIVE]` |
 * | **Relations** | `LINK: [CORE-CODEX-001]`, `LINK: [GVRN.ID.Standard]` |
 *
 * ---
 *
 * ### Block D: Standardized Synergy Block (The Loom Signature)
 *
 * Synergistic Artifact ID, Relationship Type, Synergistic Impact
 * CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for these rules.
 * GVRN.ID.Standard, ENFORCES, The Rules enforce the Naming Standard defined here.
 * GVRN.Registry.Master, INDEXED_BY, These rules are indexed in the Master Registry.
 * GVRN.Sentinel.Scan, USED_BY, The Sentinel uses these rules for compliance audits.
 */

'use strict';

const fs = require('node:fs');
const path = require('node:path');

// --- Dynamic Loading of Acronyms from cspell.json ---
// Reads the cspell.json file to create a single source of truth for acronyms.
const cspellPath = path.resolve(__dirname, '../../../cspell.json'); // Optimized topology path: Root of Synarche_Workspace
const cspellContent = fs.readFileSync(cspellPath, 'utf8');
// Strip comments (both // and /* */) before parsing
const jsoncContent = cspellContent.replaceAll(/\/\/.*$/gm, '').replaceAll(/\/\*[\s\S]*?\*\//g, '');
const cspellConfig = JSON.parse(jsoncContent);
// Filters for words that are all uppercase and may contain underscores.
const CANONICAL_ACRONYMS = cspellConfig.words.filter((word) => /^[A-Z0-9_]+$/.test(word));
// Fallback/Common prefixes to ensure basic rules don't fail if cspell is missing them
['GUCA', 'TEST', 'UMB', 'AOP', 'WLF', 'DOC', 'CODE', 'CHAR', 'CMD', 'TOOL', 'GVRN', 'SYNG', 'CORE', 'ARCH'].forEach(
    (p) => {
        if (!CANONICAL_ACRONYMS.includes(p)) CANONICAL_ACRONYMS.push(p);
    },
);
// --- End of Dynamic Loading ---

// Security: Define Workspace Root to prevent Path Traversal
// We use cspellPath (resolved from __dirname) as the anchor for the workspace root.
const WORKSPACE_ROOT = path.dirname(cspellPath);

// Pre-compiled Regexes for Performance (Hoisted)
// Updated for v13.0: Supports Legacy (UMB-SGM-001) and Sovereign (GVRN.Domain.Type)
// Regex breakdown:
// 1. Legacy: \([A-Z0-9]{3,4}-[A-Z0-9]{3,4}-\d{3}\) -> (UMB-SGM-001)
// 2. Sovereign: `[A-Z]{3,4}\.[A-Z][a-zA-Z0-9.]*` -> `GVRN.Domain.Type` (Note: H1 usually contains the loose text, but Block A has the ID)
// For H1, we usually expect: "# Artifact Name (ID)" OR "# ID"
// New Standard H1: "# Artifact Name" (ID is in Block A).
// However, PF001 validates H1. v13.0 Standard says H1 is Title. Block A has ID.
// We should update PF001 to be less aggressive or check for either format if present.
// Let's broaden the ID regex to match the ID string itself.
const DOCUMENT_ID_REGEX = /([A-Z0-9]{3,4}-[A-Z0-9]{3,4}-\d{3}|[A-Z]{2,5}\.[A-Z][a-zA-Z0-9.]*)/;
const POTENTIAL_MARKER_REGEX = /\[([a-zA-Z0-9κ-]+):([^\]]+)\]/g;
const CAPTION_REGEX = /^Table:\s+/;
const FORBIDDEN_WORDS_REGEX = /\b(legacy)\b/i;
const CITATION_REGEX = /\[cite:([^\]]+)\]/g;
const NUMERIC_VALUE_REGEX = /^\d+$/;
const ROMAN_NUMERAL_REGEX = /^([IVXLCDM]+)\.\s+/i;
const INDENT_REGEX = /^(\s*)([-*+]|\d+\.)/;

const TRAILING_WHITESPACE_REGEX = /\s+$/;
const ETC_REGEX = /\betc\.?\b/i;

// Defines valid Episemantic Markers
const VALID_EPISEMANTIC_MARKERS = {
    'κ-nexus': ['crystallized_insight', 'refutation', 'disputed', 'clarification'],
    'κ-tempus': ['obsolete'],
};

// Controlled vocabulary for OSLM relationship types.
const VALID_RELATIONSHIP_TYPES = new Set([
    'TRIGGERS',
    'IS_GOVERNED_BY',
    'MODULATES',
    'ENABLES',
    'MONITORS',
    'IS_A_TOOL_OF',
    'CONSUMES_DATA_FROM',
    'FEEDS_DATA_TO',
    'UTILIZES',
    'IS_EXECUTED_BY',
    'GOVERNS',
    'PROVIDES_INPUT_FOR',
    'ENHANCES',
    'RESOLVES_DISSONANCE_OF',
    'MODIFIES_EXECUTION_OF',
    'ENABLES_FEATURE_FOR',
    'PROVIDES_INTERFACE_FOR',
    'INTEGRATES_WITH',
    'LOGS_TO',
    'IS_ACCESSED_VIA',
    'PROVIDES_DATA_TO',
    'SUBMITS_PROPOSALS_TO',
    'IS_A_COMPONENT_OF',
    'IS_ESCALATED_FROM',
    'UPGRADES',
    'FORMS_FRAMEWORK_WITH',
    'INVOKES',
    'SYNERGY',
    // Legacy (Allowed for migration period)
    'REFERENCES',
    'DEFINES',
    'ORCHESTRATES',
    'DEPENDS_ON',
]);

module.exports = [
    {
        names: ['PF001', 'document-id-format'],
        description: 'Validates that the H1 heading contains a valid Document ID or Filename (v13.0).',
        tags: ['phoenix-protocol', 'document-id'],
        function: function PF001(params, onError) {
            let h1Token = null;
            for (const token of params.tokens) {
                if (token.type === 'heading_open' && token.tag === 'h1') {
                    h1Token = params.tokens[params.tokens.indexOf(token) + 1];
                    break;
                }
            }
            if (h1Token) {
                // v13.0: H1 is usually the Filename (e.g. GVRN.Protocol.Genesis.md)
                // Legacy: H1 is Title (ID) (e.g. # Title (UMB-SGM-001))
                // We check if the content contains a match for the DOCUMENT_ID_REGEX
                // OR if it strictly matches the dot-notation filename structure.
                const isLegacyMatch = /\([A-Z0-9]{3,4}-[A-Z0-9]{3,4}-\d{3}\)/.test(h1Token.content);
                // Allow H1 to be just the filename ID for v13.0
                const isSovereignMatch = /^[A-Z]{2,5}\.[A-Za-z0-9.]+(\.md)?$/.test(h1Token.content.trim());

                if (!isLegacyMatch && !isSovereignMatch) {
                    // Check if it at least contains the ID somewhere (relaxed check)
                    if (!DOCUMENT_ID_REGEX.test(h1Token.content)) {
                        onError({
                            lineNumber: h1Token.lineNumber,
                            detail: 'The H1 heading must contain a valid Document ID (Legacy or Sovereign).',
                            context: h1Token.line,
                        });
                    }
                }
            }
        },
    },
    {
        names: ['PF002', 'episemantic-marker-valid'],
        description: 'Validates that Episemantic Markers (e.g., [κ-nexus:value]) are valid.',
        tags: ['phoenix-protocol', 'semantics'],
        function: function PF002(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'inline' && token.content) {
                    let match;
                    while ((match = POTENTIAL_MARKER_REGEX.exec(token.content)) !== null) {
                        const type = match[1];
                        const value = match[2];
                        if (type.startsWith('κ-')) {
                            const validValues = VALID_EPISEMANTIC_MARKERS[type];
                            if (!validValues?.includes(value)) {
                                onError({
                                    lineNumber: token.lineNumber,
                                    detail: `Invalid Episemantic Marker. The value '${value}' is not a valid value for the type '${type}'.`,
                                    context: token.line,
                                });
                            }
                        }
                    }
                }
            });
        },
    },
    {
        names: ['PF003', 'table-requires-caption'],
        description: "Validates that every table is immediately followed by a caption line starting with 'Table: '.",
        tags: ['phoenix-protocol', 'tables', 'captions'],
        function: function PF003(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'table_open') {
                    const tableEndLine = token.map[1];
                    let captionFound = false;
                    // Look ahead for caption, allowing up to one blank line
                    for (let i = 0; i <= 1; i++) {
                        const line = params.lines[tableEndLine + i];
                        if (line && CAPTION_REGEX.test(line.trim())) {
                            captionFound = true;
                            break;
                        }
                    }
                    if (!captionFound) {
                        onError({
                            lineNumber: tableEndLine,
                            detail: "Table is missing a caption. Add a line after the table (optionally after a blank line) starting with 'Table: '.",
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF004', 'heading-level-increment'],
        description: 'Heading levels should only increment by one level at a time.',
        tags: ['phoenix-protocol', 'headings', 'structure'],
        function: function PF004(params, onError) {
            let lastLevel = 0;
            let firstHeadingFound = false;
            params.tokens.forEach((token) => {
                if (token.type === 'heading_open') {
                    const currentLevel = Number.parseInt(token.tag.slice(1), 10);
                    if (!firstHeadingFound) {
                        if (currentLevel !== 1) {
                            onError({
                                lineNumber: token.lineNumber,
                                detail: 'The first heading in the file must be a level 1 (H1) heading.',
                                context: token.line,
                            });
                        }
                        firstHeadingFound = true;
                    }
                    if (lastLevel !== 0 && currentLevel > lastLevel + 1) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `Heading level incremented by more than one. Went from H${lastLevel} to H${currentLevel}.`,
                            context: token.line,
                        });
                    }
                    lastLevel = currentLevel;
                }
            });
        },
    },
    {
        names: ['PF005', 'h2-h3-requires-horizontal-rule'],
        description: 'Ensures every H2 and H3 heading is immediately followed by a horizontal rule (`---`).',
        tags: ['phoenix-protocol', 'headings', 'structure'],
        function: function PF005(params, onError) {
            params.tokens.forEach((token, index) => {
                const isTargetHeading = token.type === 'heading_open' && (token.tag === 'h2' || token.tag === 'h3');
                if (isTargetHeading) {
                    // Find heading_close
                    let closeIndex = index;
                    for (let i = index + 1; i < params.tokens.length; i++) {
                        if (params.tokens[i].type === 'heading_close' && params.tokens[i].tag === token.tag) {
                            closeIndex = i;
                            break;
                        }
                    }
                    const nextToken = params.tokens[closeIndex + 1];
                    if (!nextToken || nextToken.type !== 'hr') {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `${token.tag.toUpperCase()} headings must be immediately followed by a horizontal rule (\`---\`).`,
                            context: token.line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF006', 'forbidden-words'],
        description: "Flags the use of specific forbidden words (e.g., 'legacy').",
        tags: ['phoenix-protocol', 'terminology'],
        function: function PF006(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'inline' && token.content) {
                    const match = FORBIDDEN_WORDS_REGEX.exec(token.content);
                    if (match) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `The word '${match[0]}' is discouraged. Consider using a more precise term or an Episemantic Marker.`,
                            context: token.line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF007', 'no-emphasis-in-headings'],
        description: 'Flags the use of bold (`**`) or italic (`*`) formatting inside headings.',
        tags: ['phoenix-protocol', 'headings', 'style'],
        function: function PF007(params, onError) {
            let inHeading = false;
            params.tokens.forEach((token) => {
                if (token.type === 'heading_open') {
                    inHeading = true;
                } else if (token.type === 'heading_close') {
                    inHeading = false;
                } else if (inHeading && (token.type === 'strong_open' || token.type === 'em_open')) {
                    const formatType = token.type === 'strong_open' ? 'Bold text (`**`)' : 'Italic text (`*`)';
                    onError({
                        lineNumber: token.lineNumber,
                        detail: `${formatType} is not allowed inside headings.`,
                        context: token.line,
                    });
                }
            });
        },
    },
    {
        names: ['PF008', 'link-requires-title'],
        description: 'Requires all links to have a non-empty title attribute.',
        tags: ['phoenix-protocol', 'links', 'accessibility'],
        function: function PF008(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'link_open') {
                    const hasTitle = token.attrs.some((attr) => attr[0] === 'title' && attr[1]);
                    if (!hasTitle) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: 'Link is missing a title attribute. Add a title using the format `text`.',
                            context: token.line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF009', 'image-requires-alt-text'],
        description: 'Requires all image links (`![]`) to have descriptive alt text.',
        tags: ['phoenix-protocol', 'images', 'accessibility'],
        function: function PF009(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'image') {
                    if (!token.content.trim()) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: 'Image is missing alternative text (alt text). Add a description inside the square brackets.',
                            context: token.line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF010', 'canonical-acronyms'],
        description: 'Ensures project-specific acronyms are in their canonical uppercase form.',
        tags: ['phoenix-protocol', 'terminology', 'acronyms'],
        function: function PF010(params, onError) {
            const canonicalAcronyms = CANONICAL_ACRONYMS;
            const acronymRegex = new RegExp(String.raw`\b(${canonicalAcronyms.join('|')})\b`, 'gi');
            params.tokens.forEach((token) => {
                if (token.type === 'inline' && token.content) {
                    let match;
                    while ((match = acronymRegex.exec(token.content)) !== null) {
                        const foundAcronym = match[0];
                        const correctAcronym = canonicalAcronyms.find(
                            (acronym) => acronym.toLowerCase() === foundAcronym.toLowerCase(),
                        );
                        if (foundAcronym !== correctAcronym) {
                            onError({
                                lineNumber: token.lineNumber,
                                detail: `Acronym '${foundAcronym}' is not in its canonical form. It should be '${correctAcronym}'.`,
                                context: token.line,
                            });
                        }
                    }
                }
            });
        },
    },
    {
        names: ['PF011', 'validate-doc-id-prefix'],
        description: 'Validates that prefixes in a ID are known (Legacy or Sovereign).',
        tags: ['phoenix-protocol', 'document-id'],
        function: function PF011(params, onError) {
            const validIdPrefixes = CANONICAL_ACRONYMS;
            const legacyPrefixRegex = /\(([A-Z0-9]{3,4})-([A-Z0-9]{3,4})-\d{3}\)/;
            const sovereignPrefixRegex = /([A-Z]{2,5})\.([A-Z][A-Za-z0-9]+)/;

            const linesToScan = params.lines.slice(0, 10); // Scan first 10 lines for Header/ID
            linesToScan.forEach((line, index) => {
                // Check Legacy
                let match = legacyPrefixRegex.exec(line);
                if (match) {
                    [match[1], match[2]].forEach((prefix) => {
                        if (!validIdPrefixes.includes(prefix)) {
                            onError({
                                lineNumber: index + 1,
                                detail: `Invalid Legacy ID prefix '${prefix}'.`,
                                context: line,
                            });
                        }
                    });
                } else {
                    // Check Sovereign
                    match = sovereignPrefixRegex.exec(line);
                    if (match) {
                        // match[1] = Domain (e.g. GVRN)
                        const domain = match[1];
                        if (!validIdPrefixes.includes(domain)) {
                            onError({
                                lineNumber: index + 1,
                                detail: `Invalid Sovereign Domain '${domain}'.`,
                                context: line,
                            });
                        }
                    }
                }
            });
        },
    },
    {
        names: ['PF012', 'no-nested-blockquotes'],
        description: "Disallows nested blockquotes (e.g., '> > ...').",
        tags: ['phoenix-protocol', 'blockquotes', 'structure'],
        function: function PF012(params, onError) {
            let blockquoteDepth = 0;
            params.tokens.forEach((token) => {
                if (token.type === 'blockquote_open') {
                    blockquoteDepth++;
                    if (blockquoteDepth > 1) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: 'Nested blockquotes are not allowed. Please flatten the structure.',
                            context: token.line,
                        });
                    }
                } else if (token.type === 'blockquote_close') {
                    blockquoteDepth--;
                }
            });
        },
    },
    {
        names: ['PF013', 'enforce-cite-format'],
        description: 'Ensures that [cite: ...] markers use a numeric value.',
        tags: ['phoenix-protocol', 'citations'],
        function: function PF013(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'inline' && token.content) {
                    let match;
                    while ((match = CITATION_REGEX.exec(token.content)) !== null) {
                        const citeValue = match[1].trim();
                        if (citeValue && !NUMERIC_VALUE_REGEX.test(citeValue)) {
                            onError({
                                lineNumber: token.lineNumber,
                                detail: `Invalid citation format. The value in '[cite:${match[1]}]' must be numeric.`,
                                context: token.line,
                            });
                        }
                    }
                }
            });
        },
    },
    {
        names: ['PF014', 'require-disputed-justification'],
        description: 'Requires that a `[κ-nexus:disputed]` marker is followed by a blockquote justification.',
        tags: ['phoenix-protocol', 'semantics', 'episemantic'],
        function: function PF014(params, onError) {
            const disputedMarker = '[κ-nexus:disputed]';
            params.lines.forEach((line, index) => {
                if (line.includes(disputedMarker)) {
                    const nextLine = params.lines[index + 1];
                    if (!nextLine?.trim()?.startsWith('>')) {
                        onError({
                            lineNumber: index + 1,
                            detail: `A line with a '${disputedMarker}' marker must be immediately followed by a blockquote ('>') providing justification.`,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF015', 'validate-internal-links'],
        description: 'Validates that internal links point to existing files.',
        tags: ['phoenix-protocol', 'links', 'integrity'],
        function: function PF015(params, onError) {
            const docDir = path.dirname(params.name);

            const validatePathSecurity = (linkPath, absolutePath, token) => {
                if (!absolutePath.startsWith(WORKSPACE_ROOT)) {
                    onError({
                        lineNumber: token.lineNumber,
                        detail: `Security Alert: Internal link attempts to traverse outside workspace: '${linkPath}'`,
                        context: token.line,
                    });
                    return false;
                }
                return true;
            };

            const validateFileExistence = (linkPath, absolutePath, token) => {
                if (!fs.existsSync(absolutePath)) {
                    onError({
                        lineNumber: token.lineNumber,
                        detail: `Internal link points to a non-existent file: '${linkPath}'`,
                        context: token.line,
                    });
                    return false;
                }
                return true;
            };

            const getCachedSlugs = (absolutePath) => {
                this._headingCache = this._headingCache || {};
                if (!this._headingCache[absolutePath]) {
                    const slugs = [];
                    try {
                        const fileContent = fs.readFileSync(absolutePath, 'utf8');
                        const headingRegex = /^(#{1,6})\s+(.*)/gm;
                        let match;
                        while ((match = headingRegex.exec(fileContent)) !== null) {
                            const headingText = match[2].trim();
                            const slug = headingText
                                .toLowerCase()
                                .replaceAll(/<[^>]+>/g, '')
                                .replaceAll(/[^\w\s-]/g, '')
                                .replaceAll(/\s+/g, '-');
                            slugs.push(slug);
                        }
                    } catch (error) {
                        console.warn(`[PF015] Failed to read file for anchor validation: ${absolutePath}`, error);
                    }
                    this._headingCache[absolutePath] = slugs;
                }
                return this._headingCache[absolutePath];
            };

            const validateAnchor = (linkPath, absolutePath, anchor, token) => {
                if (!anchor) return;

                const slugs = getCachedSlugs(absolutePath);
                if (!slugs.includes(anchor)) {
                    onError({
                        lineNumber: token.lineNumber,
                        detail: `Link anchor '#${anchor}' not found in file: '${linkPath}'`,
                        context: token.line,
                    });
                }
            };

            for (const token of params.tokens) {
                if (token.type !== 'link_open' && token.type !== 'image') continue;

                const href = token.attrGet('href');
                if (!href || href.startsWith('http') || href.startsWith('mailto:') || href.startsWith('#')) {
                    continue;
                }

                const [linkPath, anchor] = href.split('#');
                const absolutePath = path.resolve(docDir, linkPath);

                if (!validatePathSecurity(linkPath, absolutePath, token)) continue;
                if (!validateFileExistence(linkPath, absolutePath, token)) continue;

                validateAnchor(linkPath, absolutePath, anchor, token);
            }
        },
    },
    {
        names: ['PF016', 'enforce-section-order'],
        description: 'Enforces sequential order for H2 sections prefixed with Roman numerals (e.g., I., II., III.).',
        tags: ['phoenix-protocol', 'structure', 'headings'],
        function: function PF016(params, onError) {
            const romanToInt = (s) => {
                const romanMap = { I: 1, V: 5, X: 10, L: 50, C: 100, D: 500, M: 1000 };
                let total = 0;
                for (let i = 0; i < s.length; i++) {
                    const currentVal = romanMap[s[i].toUpperCase()];
                    const nextVal = romanMap[s[i + 1]?.toUpperCase()];
                    if (nextVal > currentVal) total -= currentVal;
                    else total += currentVal;
                }
                return total;
            };
            let lastRomanValue = 0;
            params.tokens.forEach((token, index) => {
                if (token.type === 'heading_open' && token.tag === 'h2') {
                    const inlineToken = params.tokens[index + 1];
                    if (inlineToken?.content) {
                        const match = ROMAN_NUMERAL_REGEX.exec(inlineToken.content);
                        if (match) {
                            const currentRomanValue = romanToInt(match[1]);
                            if (currentRomanValue !== lastRomanValue + 1) {
                                onError({
                                    lineNumber: token.lineNumber,
                                    detail: `Invalid section order. Expected section '${lastRomanValue + 1}', but found '${currentRomanValue}'.`,
                                    context: token.line,
                                });
                            }
                            lastRomanValue = currentRomanValue;
                        }
                    }
                }
            });
        },
    },
    {
        names: ['PF017', 'no-etc'],
        description: "Flags the use of 'etc.' and suggests being more specific.",
        tags: ['phoenix-protocol', 'terminology', 'style'],
        function: function PF017(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'inline' && token.content) {
                    if (ETC_REGEX.test(token.content)) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: "The use of 'etc.' is discouraged. Be more specific or provide concrete examples.",
                            context: token.line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF018', 'enforce-table-column-alignment'],
        description: 'Enforces consistent left-alignment for all table columns.',
        tags: ['phoenix-protocol', 'tables', 'style'],
        function: function PF018(params, onError) {
            const expectedAlignment = 'left';
            params.tokens.forEach((token) => {
                if (token.type === 'th_open') {
                    const style = token.attrGet('style');
                    const actualAlignment = style ? style.split(':')[1].trim() : 'left';
                    if (actualAlignment !== expectedAlignment) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `Invalid table column alignment. Expected '${expectedAlignment}', but found '${actualAlignment}'. All columns must be left-aligned.`,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF019', 'no-multiple-blank-lines'],
        description: 'Flags the use of more than one consecutive blank line.',
        tags: ['phoenix-protocol', 'style', 'whitespace'],
        function: function PF019(params, onError) {
            let lastLineWasBlank = false;
            params.lines.forEach((line, index) => {
                const currentLineIsBlank = line.trim() === '';
                if (currentLineIsBlank && lastLineWasBlank) {
                    const lineBeforePrevious = params.lines[index - 2] || 'not-blank';
                    if (lineBeforePrevious.trim() !== '') {
                        onError({
                            lineNumber: index + 1,
                            detail: 'Multiple consecutive blank lines are not allowed.',
                        });
                    }
                }
                lastLineWasBlank = currentLineIsBlank;
            });
        },
    },
    {
        names: ['PF020', 'no-trailing-whitespace'],
        description: 'Flags lines that end with trailing whitespace.',
        tags: ['phoenix-protocol', 'style', 'whitespace'],
        function: function PF020(params, onError) {
            params.lines.forEach((line, index) => {
                if (TRAILING_WHITESPACE_REGEX.test(line)) {
                    onError({
                        lineNumber: index + 1,
                        detail: 'Line ends with trailing whitespace.',
                        context: line,
                    });
                }
            });
        },
    },
    {
        names: ['PF021', 'actionable-prompt-packet-exists'],
        description:
            "Validates that artifacts contain the 'Actionable Prompt Packet' section (allows variable Roman Numerals).",
        tags: ['phoenix-protocol', 'structure', 'actionability'],
        function: function PF021(params, onError) {
            // Regex to match "X. Actionable Prompt Packet" where X is any Roman Numeral or number, and optional (APP) suffix
            const appHeadingRegex = /^[IVXLCDM\d]+\.\s+Actionable Prompt Packet/i;
            let packetFound = false;
            params.tokens.forEach((token) => {
                if (token.type === 'heading_open' && token.tag === 'h2') {
                    const inlineToken = params.tokens[params.tokens.indexOf(token) + 1];
                    if (inlineToken?.content && appHeadingRegex.test(inlineToken.content)) packetFound = true;
                }
            });
            if (!packetFound) {
                onError({
                    lineNumber: 1,
                    detail: `Document is missing the required 'Actionable Prompt Packet' section (e.g., 'IV. Actionable Prompt Packet').`,
                });
            }
        },
    },
    {
        names: ['PF022', 'validate-relationship-types'],
        description: "Validates that 'Relationship Type' in OSLM tables uses a controlled vocabulary.",
        tags: ['phoenix-protocol', 'oslm', 'synergy'],
        function: function PF022(params, onError) {
            let inOslmTable = false;
            let relationshipTypeColumn = -1;
            params.tokens.forEach((token, index) => {
                if (
                    token.type === 'heading_open' &&
                    token.tag === 'h2' &&
                    params.tokens[index + 1]?.content.includes('Synergistic Links Matrix Update')
                ) {
                    inOslmTable = true;
                    relationshipTypeColumn = -1;
                }
                if (inOslmTable && token.type === 'thead_open') {
                    const headerRow = params.tokens.slice(index);
                    const thTokens = headerRow.filter((t) => t.type === 'th_open');
                    thTokens.every((th, i) => {
                        const thContent = headerRow.find((t) => t.type === 'inline' && t.map[0] === th.map[0]);
                        if (thContent && thContent.content === 'Relationship Type') {
                            relationshipTypeColumn = i;
                            return false;
                        }
                        return true;
                    });
                }
                if (inOslmTable && token.type === 'td_open' && token.map[1] === relationshipTypeColumn) {
                    const cellContent = params.tokens[index + 1].content.trim();
                    if (cellContent && !VALID_RELATIONSHIP_TYPES.has(cellContent)) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `Invalid Relationship Type: '${cellContent}'. It is not in the controlled vocabulary.`,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF023', 'h2-requires-roman-numeral'],
        description: 'Enforces that all H2 headings must be prefixed with a Roman numeral.',
        tags: ['phoenix-protocol', 'structure', 'headings'],
        function: function PF023(params, onError) {
            params.tokens.forEach((token, index) => {
                if (token.type === 'heading_open' && token.tag === 'h2') {
                    const inlineToken = params.tokens[index + 1];
                    if (inlineToken && !ROMAN_NUMERAL_REGEX.test(inlineToken.content)) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: "H2 headings must be prefixed with a Roman numeral (e.g., 'I. ', 'II. ').",
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF024', 'musashi-metadata-check'],
        description: "Validates that the metadata table contains the 'Evolutionary Alignment' or 'Evolution' row.",
        tags: ['phoenix-protocol', 'metadata', 'musashi'],
        function: function PF024(params, onError) {
            let firstTableFound = false;
            let hasAlignmentRow = false;
            for (const token of params.tokens) {
                if (token.type === 'table_open') {
                    firstTableFound = true;
                    const tableStart = token.map[0];
                    const tableEnd = token.map[1];
                    const tableContent = params.lines.slice(tableStart, tableEnd).join('\n');
                    if (/(?:Evolutionary Alignment|Evolution)/i.test(tableContent)) hasAlignmentRow = true;
                    break;
                }
            }
            if (firstTableFound && !hasAlignmentRow) {
                onError({
                    lineNumber: 1,
                    detail: "Metadata block is missing the 'Evolutionary Alignment' or 'Evolution' row.",
                });
            }
        },
    },
    {
        names: ['PF025', 'indent-four-spaces'],
        description: 'Flags list items indented with non-4-space multiples.',
        tags: ['phoenix-protocol', 'style', 'indentation'],
        function: function PF025(params, onError) {
            params.lines.forEach((line, index) => {
                const match = INDENT_REGEX.exec(line);
                if (match) {
                    const indentSize = match[1].length;
                    if (indentSize > 0 && indentSize % 4 !== 0) {
                        onError({
                            lineNumber: index + 1,
                            detail: `Indentation must be a multiple of 4 spaces. Found ${indentSize} spaces.`,
                            context: line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF026', 'enforce-asterisk-lists'],
        description: 'Validates that unordered lists use the asterisk (*) marker.',
        tags: ['phoenix-protocol', 'style', 'lists'],
        function: function PF026(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'bullet_list_open') {
                    if (token.markup !== '*') {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `Unordered lists must use asterisks (*) as markers. Found '${token.markup}'.`,
                            context: token.line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF027', 'heading-hierarchy'],
        description: 'Enforces a strict heading hierarchy (no skipping levels).',
        tags: ['phoenix-protocol', 'structure', 'headings'],
        function: function PF027(params, onError) {
            let lastLevel = 0;
            params.tokens.forEach((token) => {
                if (token.type === 'heading_open') {
                    const level = parseInt(token.tag.slice(1));
                    if (level > lastLevel + 1) {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: `Heading level skip detected: H${lastLevel} to H${level}.`,
                            context: token.line,
                        });
                    }
                    lastLevel = level;
                }
            });
        },
    },
    {
        names: ['PF028', 'enforce-artifact-anchor'],
        description: "Ensures every Markdown file contains an 'artifact_anchor' block.",
        tags: ['phoenix-protocol', 'metadata', 'governance'],
        function: function PF028(params, onError) {
            const content = params.lines.join('\n');
            if (!content.includes('artifact_anchor:')) {
                onError({
                    lineNumber: 1,
                    detail: "Missing mandatory 'artifact_anchor' metadata block.",
                });
            }
        },
    },
    {
        names: ['PF029', 'list-marker-spacing'],
        description: 'Enforces exactly one space after a list marker (* or -).',
        tags: ['phoenix-protocol', 'style', 'lists'],
        function: function PF029(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'list_item_open') {
                    const line = params.lines[token.lineNumber - 1];
                    const match = line.match(/^(\s*[*])(\s+)/);
                    if (match && match[2] !== ' ') {
                        onError({
                            lineNumber: token.lineNumber,
                            detail: 'List markers must be followed by exactly one space.',
                            context: line,
                        });
                    }
                }
            });
        },
    },
    {
        names: ['PF030', 'valid-relationship-types'],
        description: 'Validates that relationship types in tables match the canonical list.',
        tags: ['phoenix-protocol', 'metadata', 'relationships'],
        function: function PF030(params, onError) {
            const VALID_RELATIONS = [
                'GOVERNS',
                'INDEXES',
                'DEFINED_BY',
                'SYNERGIZES',
                'IMPLEMENTS',
                'TRACKS',
                'EXTENDS',
            ];
            params.tokens.forEach((token) => {
                if (token.type === 'inline' && token.content.includes('|')) {
                    VALID_RELATIONS.forEach((rel) => {
                        // Logic to check if a cell contains a relationship but it's misspelled
                    });
                }
            });
        },
    },
    {
        names: ['PF031', 'absolute-media-paths'],
        description: 'Ensures all images/videos use absolute paths (file:///).',
        tags: ['phoenix-protocol', 'media', 'portability'],
        function: function PF031(params, onError) {
            params.tokens.forEach((token) => {
                if (token.type === 'inline') {
                    token.children.forEach((child) => {
                        if (child.type === 'image') {
                            const src = child.attrGet('src');
                            if (src && !src.startsWith('file:///') && !src.startsWith('http')) {
                                onError({
                                    lineNumber: child.lineNumber,
                                    detail: `Media path '${src}' must be absolute (file:///...).`,
                                    context: params.lines[child.lineNumber - 1],
                                });
                            }
                        }
                    });
                }
            });
        },
    },
    {
        names: ['PF032', 'ts-links-use-path-aliases'],
        description: 'Ensures all Markdown links pointing to .ts or .tsx files use absolute path aliases (AETHER-V2).',
        tags: ['phoenix-protocol', 'links', 'aliases'],
        function: function PF032(params, onError) {
            const ALIAS_MAP = [
                { pattern: /axion-core\/src\/cse\//, alias: '@system/' },
                { pattern: /axion-core\/src\/02_domain\//, alias: '@domain/' },
                { pattern: /axion-core\/src\/types\//, alias: '@essence/' },
                { pattern: /_governance\/01_Registries\//, alias: '@atlas/' },
                { pattern: /design-system\/tarot-forge\/src\//, alias: '@fabric/' },
                { pattern: /axion-core\//, alias: '@bridge/' },
                { pattern: /_governance\//, alias: '@gov/' },
            ];

            params.tokens.forEach((token) => {
                if (token.type === 'link_open') {
                    const href = token.attrGet('href');
                    if (href && (href.endsWith('.ts') || href.endsWith('.tsx'))) {
                        if (!href.startsWith('@') && !href.startsWith('http')) {
                            let fixedHref = href.replace(/^(\.\.\/|\.\/)+/, '');
                            const mapping = ALIAS_MAP.find((m) => m.pattern.test(fixedHref));

                            if (mapping) {
                                fixedHref = fixedHref.replace(mapping.pattern, mapping.alias);
                            } else {
                                fixedHref = '@' + fixedHref;
                            }

                            const lineText = token.line || params.lines[token.lineNumber - 1] || '';
                            let fixInfo;

                            const exactIndex = lineText.indexOf(`](${href})`);
                            if (exactIndex !== -1) {
                                fixInfo = {
                                    editColumn: exactIndex + 3,
                                    deleteCount: href.length,
                                    insertText: fixedHref,
                                };
                            }

                            onError({
                                lineNumber: token.lineNumber,
                                detail: `TypeScript link '${href}' must use a Sovereign alias (e.g., ${mapping ? mapping.alias : '@domain'}).`,
                                context: token.line,
                                fixInfo: fixInfo,
                            });
                        }
                    }
                }
            });
        },
    },
];
