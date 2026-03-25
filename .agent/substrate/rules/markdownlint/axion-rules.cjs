/**
 * # UMB-RULES-001: The Guardian's Logic (Axion Rules)
 *
 * ## Genesis Stamp: 2026-01-20 | Domain: GVRN | State: CANONIZED | Criticality: Critical
 *
 * ### I. Universal Identification & Provenance (The Vector Signature)
 *
 * #### The Chronos Lock & Axiomatic Metadata Layer
 *
 * | Field                  | Value                                                    |
 * | :--------------------- | :------------------------------------------------------- |
 * | **1. Artifact ID**     | `STA.Rules.Axion`                                        |
 * | **2. Official Name**   | `axion-rules.cjs`                                        |
 * | **3. Version**         | **v15.0 [OMEGA]**                                        |
 * | **4. Provenance**      | **Ascended: 2026-03-17**                                 |
 * | **5. Domain**          | `GVRN`                                                   |
 * | **6. Evolution**       | **Authentic Persona**                                    |
 * | **7. Celestial Class** | `[STAR]`                                                 |
 * | **8. Tier**            | **Foundational**                                         |
 * | **9. Status (State)**  | `[CANONIZED]`                                            |
 * | **10. Ethos**          | **Guardian of Semantic Coherence**                        |
 * | **11. Catalyst**       | **Phase 34: Rules Stabilization**                        |
 * | **12. Relations**      | `GOVERNED_BY: CORE-CODEX-001`, `VALIDATES: GVRN.Taxonomy.Relationships` |
 * | **13. Integrity Hash** | `[AUTO-GENERATED]`                                       |
 *
 * ---
 *
 * ### I.B. Standardized Synergy Block (The Loom Signature)
 *
 * Synergistic Artifact ID | Relationship Type | Synergistic Impact
 * AOP-MAP-001             | ENFORCES          | These rules enforce the Disciplined Execution Playbook.
 * markdownlint.json       | EXTENDS           | These rules extend the base markdownlint configuration.
 * GUCA-MAP-001            | USED_BY           | The Musashi Audit tool runs these rules.
 */

"use strict";

const fs = require("node:fs");
const path = require("node:path");

// --- Dynamic Loading of Acronyms from cspell.json ---
// Reads the cspell.json file to create a single source of truth for acronyms.
const cspellPath = path.resolve(__dirname, "../../../../cspell.json"); // Normalized path for Sovereign Substrate
const cspellContent = fs.readFileSync(cspellPath, "utf8");
// Strip comments (both // and /* */) before parsing, while preserving URLs in strings
const jsoncContent = cspellContent.replaceAll(
  /\\"|"(?:\\"|[^"])*"|(\/\/.*$|\/\*[\s\S]*?\*\/)/gm,
  (match, group1) => (group1 ? "" : match),
);
const cspellConfig = JSON.parse(jsoncContent);
// Filters for words that are all uppercase and may contain underscores.
const CANONICAL_ACRONYMS = cspellConfig.words.filter((word) =>
  /^[A-Z0-9_]+$/.test(word),
);
// Fallback/Common prefixes to ensure basic rules don't fail if cspell is missing them
[
  "GUCA",
  "TEST",
  "UMB",
  "AOP",
  "WLF",
  "DOC",
  "CODE",
  "CHAR",
  "CMD",
  "TOOL",
].forEach((p) => {
  if (!CANONICAL_ACRONYMS.includes(p)) CANONICAL_ACRONYMS.push(p);
});
// --- End of Dynamic Loading ---

// Security: Define Workspace Root to prevent Path Traversal
// We use cspellPath (resolved from __dirname) as the anchor for the workspace root.
const WORKSPACE_ROOT = path.dirname(cspellPath);

// Pre-compiled Regexes for Performance (Hoisted)
// Supports legacy (XXX-YYY-NNN) and new semantic (DOMAIN.Subsystem.Descriptor)
const DOCUMENT_ID_REGEX =
  /(?:\([A-Z0-9]{3,4}-[A-Z0-9]{3,4}-\d{3}\)|[A-Z0-9]{3,4}\.[A-Z0-9][a-zA-Z0-9]+\.[A-Z0-9][a-zA-Z0-9]+)/;
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
  "κ-nexus": [
    "crystallized_insight",
    "refutation",
    "disputed",
    "clarification",
  ],
  "κ-tempus": ["obsolete"],
};

// Controlled vocabulary for OSLM relationship types.
const VALID_RELATIONSHIP_TYPES = new Set([
  // Structural
  "CONTAINS",
  "IS_A_COMPONENT_OF",
  "UPGRADES",
  "EXTENDS",

  // Governance
  "GOVERNS",
  "IS_GOVERNED_BY",
  "MONITORS",
  "REMEDIATES",

  // Kinetic
  "TRIGGERS",
  "INVOKES",
  "ENABLES",
  "CONSUMES_DATA_FROM",
  "FEEDS_DATA_TO",
  "UTILIZES",

  // Synergy
  "SYNERGY",
  "ENHANCES",
  "RESOLVES_DISSONANCE_OF",
  "RESONATES_WITH",

  // Legacy (Allowed for migration period)
  "REFERENCES",
  "DEFINES",
  "ORCHESTRATES",
  "DEPENDS_ON",
]);

module.exports = [
  {
    names: ["PF001", "document-id-format"],
    description:
      "Validates that a Document ID (e.g., UMB-PRS-001 or GUCA-TOOL-001) is present in the H1 heading.",
    tags: ["phoenix-protocol", "document-id"],
    function: function PF001(params, onError) {
      let h1Token = null;
      for (const token of params.tokens) {
        if (token.type === "heading_open" && token.tag === "h1") {
          h1Token = params.tokens[params.tokens.indexOf(token) + 1];
          break;
        }
      }
      if (h1Token) {
        if (!DOCUMENT_ID_REGEX.test(h1Token.content)) {
          onError({
            lineNumber: h1Token.lineNumber,
            detail:
              "The H1 heading must contain a Document ID (e.g., UMB-PRS-001 or DOM.Sub.Desc).",
            context: h1Token.line,
          });
        }
      }
    },
  },
  {
    names: ["PF002", "episemantic-marker-valid"],
    description:
      "Validates that Episemantic Markers (e.g., [κ-nexus:value]) are valid.",
    tags: ["phoenix-protocol", "semantics"],
    function: function PF002(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "inline" && token.content) {
          let match;
          while (
            (match = POTENTIAL_MARKER_REGEX.exec(token.content)) !== null
          ) {
            const type = match[1];
            const value = match[2];
            if (type.startsWith("κ-")) {
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
    names: ["PF003", "table-requires-caption"],
    description:
      "Validates that every table is immediately followed by a caption line starting with 'Table: '.",
    tags: ["phoenix-protocol", "tables", "captions"],
    function: function PF003(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "table_open") {
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
              detail:
                "Table is missing a caption. Add a line after the table (optionally after a blank line) starting with 'Table: '.",
            });
          }
        }
      });
    },
  },
  {
    names: ["PF004", "heading-level-increment"],
    description: "Heading levels should only increment by one level at a time.",
    tags: ["phoenix-protocol", "headings", "structure"],
    function: function PF004(params, onError) {
      let lastLevel = 0;
      let firstHeadingFound = false;
      params.tokens.forEach((token) => {
        if (token.type === "heading_open") {
          const currentLevel = Number.parseInt(token.tag.slice(1), 10);
          if (!firstHeadingFound) {
            if (currentLevel !== 1) {
              onError({
                lineNumber: token.lineNumber,
                detail:
                  "The first heading in the file must be a level 1 (H1) heading.",
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
    names: ["PF005", "h2-h3-requires-horizontal-rule"],
    description:
      "Ensures every H2 and H3 heading is immediately followed by a horizontal rule (`---`).",
    tags: ["phoenix-protocol", "headings", "structure"],
    function: function PF005(params, onError) {
      params.tokens.forEach((token, index) => {
        const isTargetHeading =
          token.type === "heading_open" &&
          (token.tag === "h2" || token.tag === "h3");
        if (isTargetHeading) {
          // Find heading_close
          let closeIndex = index;
          for (let i = index + 1; i < params.tokens.length; i++) {
            if (
              params.tokens[i].type === "heading_close" &&
              params.tokens[i].tag === token.tag
            ) {
              closeIndex = i;
              break;
            }
          }
          const nextToken = params.tokens[closeIndex + 1];
          if (!nextToken || nextToken.type !== "hr") {
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
    names: ["PF006", "forbidden-words"],
    description: "Flags the use of specific forbidden words (e.g., 'legacy').",
    tags: ["phoenix-protocol", "terminology"],
    function: function PF006(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "inline" && token.content) {
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
    names: ["PF007", "no-emphasis-in-headings"],
    description:
      "Flags the use of bold (`**`) or italic (`*`) formatting inside headings.",
    tags: ["phoenix-protocol", "headings", "style"],
    function: function PF007(params, onError) {
      let inHeading = false;
      params.tokens.forEach((token) => {
        if (token.type === "heading_open") {
          inHeading = true;
        } else if (token.type === "heading_close") {
          inHeading = false;
        } else if (
          inHeading &&
          (token.type === "strong_open" || token.type === "em_open")
        ) {
          const formatType =
            token.type === "strong_open"
              ? "Bold text (`**`)"
              : "Italic text (`*`)";
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
    names: ["PF008", "link-requires-title"],
    description: "Requires all links to have a non-empty title attribute.",
    tags: ["phoenix-protocol", "links", "accessibility"],
    function: function PF008(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "link_open") {
          const hasTitle = token.attrs.some(
            (attr) => attr[0] === "title" && attr[1],
          );
          if (!hasTitle) {
            onError({
              lineNumber: token.lineNumber,
              detail:
                "Link is missing a title attribute. Add a title using the format `text`.",
              context: token.line,
            });
          }
        }
      });
    },
  },
  {
    names: ["PF009", "image-requires-alt-text"],
    description:
      "Requires all image links (`![]`) to have descriptive alt text.",
    tags: ["phoenix-protocol", "images", "accessibility"],
    function: function PF009(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "image") {
          if (!token.content.trim()) {
            onError({
              lineNumber: token.lineNumber,
              detail:
                "Image is missing alternative text (alt text). Add a description inside the square brackets.",
              context: token.line,
            });
          }
        }
      });
    },
  },
  {
    names: ["PF010", "canonical-acronyms"],
    description:
      "Ensures project-specific acronyms are in their canonical uppercase form.",
    tags: ["phoenix-protocol", "terminology", "acronyms"],
    function: function PF010(params, onError) {
      const canonicalAcronyms = CANONICAL_ACRONYMS;
      const acronymRegex = new RegExp(
        String.raw`\b(${canonicalAcronyms.join("|")})\b`,
        "gi",
      );
      params.tokens.forEach((token) => {
        if (token.type === "inline" && token.content) {
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
    names: ["PF011", "validate-doc-id-prefix"],
    description:
      "Validates that prefixes in a document ID (e.g., UMB-CSE-001) are known and valid.",
    tags: ["phoenix-protocol", "document-id"],
    function: function PF011(params, onError) {
      const validIdPrefixes = CANONICAL_ACRONYMS;
      // Matches legacy (XXX-YYY-NNN) and new semantic DOMAIN.Subsystem.Descriptor
      const documentIdRegex =
        /(?:\(?([A-Z0-9]{3,4})-([A-Z0-9]{3,4})-\d{3}\)?|^([A-Z0-9]{3,4})\.[A-Z0-9][a-zA-Z0-9]+\.[A-Z0-9][a-zA-Z0-9]+)/m;
      const linesToScan = params.lines.slice(0, 5);
      linesToScan.forEach((line, index) => {
        const match = documentIdRegex.exec(line);
        if (match) {
          // Extract prefixes based on which group matched
          const prefixes = match[3] ? [match[3]] : [match[1], match[2]];
          prefixes.forEach((prefix) => {
            if (prefix && !validIdPrefixes.includes(prefix)) {
              onError({
                lineNumber: index + 1,
                detail: `Invalid document ID prefix '${prefix}'. The prefix is not a recognized canonical acronym.`,
                context: line,
              });
            }
          });
        }
      });
    },
  },
  {
    names: ["PF012", "no-nested-blockquotes"],
    description: "Disallows nested blockquotes (e.g., '> > ...').",
    tags: ["phoenix-protocol", "blockquotes", "structure"],
    function: function PF012(params, onError) {
      let blockquoteDepth = 0;
      params.tokens.forEach((token) => {
        if (token.type === "blockquote_open") {
          blockquoteDepth++;
          if (blockquoteDepth > 1) {
            onError({
              lineNumber: token.lineNumber,
              detail:
                "Nested blockquotes are not allowed. Please flatten the structure.",
              context: token.line,
            });
          }
        } else if (token.type === "blockquote_close") {
          blockquoteDepth--;
        }
      });
    },
  },
  {
    names: ["PF013", "enforce-cite-format"],
    description: "Ensures that [cite: ...] markers use a numeric value.",
    tags: ["phoenix-protocol", "citations"],
    function: function PF013(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "inline" && token.content) {
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
    names: ["PF014", "require-disputed-justification"],
    description:
      "Requires that a `[κ-nexus:disputed]` marker is followed by a blockquote justification.",
    tags: ["phoenix-protocol", "semantics", "episemantic"],
    function: function PF014(params, onError) {
      const disputedMarker = "[κ-nexus:disputed]";
      params.lines.forEach((line, index) => {
        if (line.includes(disputedMarker)) {
          const nextLine = params.lines[index + 1];
          if (!nextLine?.trim()?.startsWith(">")) {
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
    names: ["PF015", "validate-internal-links"],
    description: "Validates that internal links point to existing files.",
    tags: ["phoenix-protocol", "links", "integrity"],
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
            const fileContent = fs.readFileSync(absolutePath, "utf8");
            const headingRegex = /^(#{1,6})\s+(.*)/gm;
            let match;
            while ((match = headingRegex.exec(fileContent)) !== null) {
              const headingText = match[2].trim();
              const slug = headingText
                .toLowerCase()
                .replaceAll(/<[^>]+>/g, "")
                .replaceAll(/[^\w\s-]/g, "")
                .replaceAll(/\s+/g, "-");
              slugs.push(slug);
            }
          } catch (error) {
            console.warn(
              `[PF015] Failed to read file for anchor validation: ${absolutePath}`,
              error,
            );
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
        if (token.type !== "link_open" && token.type !== "image") continue;

        const href = token.attrGet("href");
        if (
          !href ||
          href.startsWith("http") ||
          href.startsWith("mailto:") ||
          href.startsWith("#")
        ) {
          continue;
        }

        const [linkPath, anchor] = href.split("#");
        const absolutePath = path.resolve(docDir, linkPath);

        if (!validatePathSecurity(linkPath, absolutePath, token)) continue;
        if (!validateFileExistence(linkPath, absolutePath, token)) continue;

        validateAnchor(linkPath, absolutePath, anchor, token);
      }
    },
  },
  {
    names: ["PF016", "enforce-section-order"],
    description:
      "Enforces sequential order for H2 sections prefixed with Roman numerals (e.g., I., II., III.).",
    tags: ["phoenix-protocol", "structure", "headings"],
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
        if (token.type === "heading_open" && token.tag === "h2") {
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
    names: ["PF017", "no-etc"],
    description: "Flags the use of 'etc.' and suggests being more specific.",
    tags: ["phoenix-protocol", "terminology", "style"],
    function: function PF017(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "inline" && token.content) {
          if (ETC_REGEX.test(token.content)) {
            onError({
              lineNumber: token.lineNumber,
              detail:
                "The use of 'etc.' is discouraged. Be more specific or provide concrete examples.",
              context: token.line,
            });
          }
        }
      });
    },
  },
  {
    names: ["PF018", "enforce-table-column-alignment"],
    description: "Enforces consistent left-alignment for all table columns.",
    tags: ["phoenix-protocol", "tables", "style"],
    function: function PF018(params, onError) {
      const expectedAlignment = "left";
      params.tokens.forEach((token) => {
        if (token.type === "th_open") {
          const style = token.attrGet("style");
          const actualAlignment = style ? style.split(":")[1].trim() : "left";
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
    names: ["PF019", "no-multiple-blank-lines"],
    description: "Flags the use of more than one consecutive blank line.",
    tags: ["phoenix-protocol", "style", "whitespace"],
    function: function PF019(params, onError) {
      let lastLineWasBlank = false;
      params.lines.forEach((line, index) => {
        const currentLineIsBlank = line.trim() === "";
        if (currentLineIsBlank && lastLineWasBlank) {
          const lineBeforePrevious = params.lines[index - 2] || "not-blank";
          if (lineBeforePrevious.trim() !== "") {
            onError({
              lineNumber: index + 1,
              detail: "Multiple consecutive blank lines are not allowed.",
            });
          }
        }
        lastLineWasBlank = currentLineIsBlank;
      });
    },
  },
  {
    names: ["PF020", "no-trailing-whitespace"],
    description: "Flags lines that end with trailing whitespace.",
    tags: ["phoenix-protocol", "style", "whitespace"],
    function: function PF020(params, onError) {
      params.lines.forEach((line, index) => {
        if (TRAILING_WHITESPACE_REGEX.test(line)) {
          onError({
            lineNumber: index + 1,
            detail: "Line ends with trailing whitespace.",
            context: line,
          });
        }
      });
    },
  },
  {
    names: ["PF021", "actionable-prompt-packet-exists"],
    description:
      "Validates that artifacts contain the 'Actionable Prompt Packet' section (allows variable Roman Numerals).",
    tags: ["phoenix-protocol", "structure", "actionability"],
    function: function PF021(params, onError) {
      // Regex to match "X. Actionable Prompt Packet" where X is any Roman Numeral or number, and optional (APP) suffix
      const appHeadingRegex = /^[IVXLCDM\d]+\.\s+Actionable Prompt Packet/i;
      let packetFound = false;
      params.tokens.forEach((token) => {
        if (token.type === "heading_open" && token.tag === "h2") {
          const inlineToken = params.tokens[params.tokens.indexOf(token) + 1];
          if (inlineToken?.content && appHeadingRegex.test(inlineToken.content))
            packetFound = true;
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
    names: ["PF022", "validate-relationship-types"],
    description:
      "Validates that 'Relationship Type' in OSLM tables uses a controlled vocabulary.",
    tags: ["phoenix-protocol", "oslm", "synergy"],
    function: function PF022(params, onError) {
      let inOslmTable = false;
      let relationshipTypeColumn = -1;
      params.tokens.forEach((token, index) => {
        if (
          token.type === "heading_open" &&
          token.tag === "h2" &&
          params.tokens[index + 1]?.content.includes(
            "Synergistic Links Matrix Update",
          )
        ) {
          inOslmTable = true;
          relationshipTypeColumn = -1;
        }
        if (inOslmTable && token.type === "thead_open") {
          const headerRow = params.tokens.slice(index);
          const thTokens = headerRow.filter((t) => t.type === "th_open");
          thTokens.every((th, i) => {
            const thContent = headerRow.find(
              (t) => t.type === "inline" && t.map[0] === th.map[0],
            );
            if (thContent && thContent.content === "Relationship Type") {
              relationshipTypeColumn = i;
              return false;
            }
            return true;
          });
        }
        if (
          inOslmTable &&
          token.type === "td_open" &&
          token.map[1] === relationshipTypeColumn
        ) {
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
    names: ["PF023", "h2-requires-roman-numeral"],
    description:
      "Enforces that all H2 headings must be prefixed with a Roman numeral.",
    tags: ["phoenix-protocol", "structure", "headings"],
    function: function PF023(params, onError) {
      params.tokens.forEach((token, index) => {
        if (token.type === "heading_open" && token.tag === "h2") {
          const inlineToken = params.tokens[index + 1];
          if (inlineToken && !ROMAN_NUMERAL_REGEX.test(inlineToken.content)) {
            onError({
              lineNumber: token.lineNumber,
              detail:
                "H2 headings must be prefixed with a Roman numeral (e.g., 'I. ', 'II. ').",
            });
          }
        }
      });
    },
  },
  {
    names: ["PF024", "musashi-metadata-check"],
    description:
      "Validates that the metadata table contains the 'Evolutionary Alignment' or 'Evolution' row.",
    tags: ["phoenix-protocol", "metadata", "musashi"],
    function: function PF024(params, onError) {
      let firstTableFound = false;
      let hasAlignmentRow = false;
      for (const token of params.tokens) {
        if (token.type === "table_open") {
          firstTableFound = true;
          const tableStart = token.map[0];
          const tableEnd = token.map[1];
          const tableContent = params.lines
            .slice(tableStart, tableEnd)
            .join("\n");
          if (/(?:Evolutionary Alignment|Evolution)/i.test(tableContent))
            hasAlignmentRow = true;
          break;
        }
      }
      if (firstTableFound && !hasAlignmentRow) {
        onError({
          lineNumber: 1,
          detail:
            "Metadata block is missing the 'Evolutionary Alignment' or 'Evolution' row.",
        });
      }
    },
  },
  {
    names: ["PF025", "indent-four-spaces"],
    description: "Flags list items indented with non-4-space multiples.",
    tags: ["phoenix-protocol", "style", "indentation"],
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
    names: ["PF026", "enforce-hyphen-lists"],
    description: "Validates that unordered lists use the hyphen (-) marker.",
    tags: ["phoenix-protocol", "style", "lists"],
    function: function PF026(params, onError) {
      params.tokens.forEach((token) => {
        if (token.type === "bullet_list_open") {
          if (token.markup !== "-") {
            onError({
              lineNumber: token.lineNumber,
              detail: `Unordered lists must use hyphens (-) as markers. Found '${token.markup}'.`,
              context: token.line,
            });
          }
        }
      });
    },
  },
  {
    names: ["PF027", "integrity-gate-exists"],
    description:
      "Validates that artifacts contain the 'Integrity Gate' (Block F) section.",
    tags: ["phoenix-protocol", "structure", "validation"],
    function: function PF027(params, onError) {
      const integrityGateRegex =
        /^[IVXLCDM\d]+\.\s+The Integrity Gate \(CIV-GATE\)/i;
      let gateFound = false;
      params.tokens.forEach((token) => {
        if (
          token.type === "heading_open" &&
          (token.tag === "h2" || token.tag === "h3")
        ) {
          const inlineToken = params.tokens[params.tokens.indexOf(token) + 1];
          if (
            inlineToken?.content &&
            integrityGateRegex.test(inlineToken.content)
          )
            gateFound = true;
        }
      });
      if (!gateFound) {
        onError({
          lineNumber: 1,
          detail: `Document is missing the required 'The Integrity Gate (CIV-GATE)' section (Block F).`,
        });
      }
    },
  },
  {
    names: ["PF028", "strict-h-hierarchy"],
    description:
      "Enforces a strict heading hierarchy (e.g., H1 -> H2 -> H3). No jumping levels.",
    tags: ["phoenix-protocol", "structure", "accessibility"],
    function: function PF028(params, onError) {
      let lastLevel = 0;
      params.tokens.forEach((token) => {
        if (token.type === "heading_open") {
          const currentLevel = Number.parseInt(token.tag.slice(1), 10);
          if (currentLevel > lastLevel + 1) {
            onError({
              lineNumber: token.lineNumber,
              detail: `Heading level jump detected: H${lastLevel} -> H${currentLevel}. Law 7 requires strict H-Hierarchy.`,
              context: token.line,
            });
          }
          lastLevel = currentLevel;
        }
      });
    },
  },
  {
    names: ["PF029", "actionable-prompt-packet-at-end"],
    description:
      "Enforces that the Actionable Prompt Packet (APP) is the final major section.",
    tags: ["phoenix-protocol", "structure", "actionability"],
    function: function PF029(params, onError) {
      const appRegex = /Actionable Prompt Packet/i;
      const headings = params.tokens.filter((t) => t.type === "heading_open");
      if (headings.length > 0) {
        const lastHeadingToken = headings[headings.length - 1];
        const inlineToken =
          params.tokens[params.tokens.indexOf(lastHeadingToken) + 1];
        if (!inlineToken?.content || !appRegex.test(inlineToken.content)) {
          onError({
            lineNumber: lastHeadingToken.lineNumber,
            detail:
              "The document must conclude with an 'Actionable Prompt Packet' (APP) section.",
          });
        }
      }
    },
  },
  {
    names: ["PF030", "genesis-seed-exists-in-selt"],
    description:
      "Validates that SELT (Experience Log) artifacts contain a Genesis Seed marker.",
    tags: ["phoenix-protocol", "experience", "traceability"],
    function: function PF030(params, onError) {
      const fileName = path.basename(params.name || "");
      if (fileName.startsWith("SELT") || fileName.includes("ExperienceLog")) {
        const seedRegex = /Genesis Seed|Seed:\s+|\[seed:([^\]]+)\]/i;
        let seedFound = false;
        params.tokens.forEach((token) => {
          if (token.type === "inline" && seedRegex.test(token.content))
            seedFound = true;
        });
        if (!seedFound) {
          onError({
            lineNumber: 1,
            detail:
              "SELT artifacts must contain a 'Genesis Seed' marker for traceability.",
          });
        }
      }
    },
  },
  {
    names: ["PF031", "pre-preamble-blocks-valid"],
    description:
      "Ensures the artifact preamble contains mandatory Blocks A through F headers/tables.",
    tags: ["phoenix-protocol", "structure", "metadata"],
    function: function PF031(params, onError) {
      const blocks = [
        "Block A",
        "Block B",
        "Block C",
        "Block D",
        "Block E",
        "Block F",
      ];
      const missingBlocks = [];

      blocks.forEach((block) => {
        let found = false;
        params.tokens.forEach((token) => {
          if (token.type === "inline" && token.content.includes(block))
            found = true;
        });
        if (!found) missingBlocks.push(block);
      });

      if (missingBlocks.length > 0) {
        onError({
          lineNumber: 1,
          detail: `Document preamble is missing mandatory sections: ${missingBlocks.join(", ")}.`,
        });
      }
    },
  },
];
