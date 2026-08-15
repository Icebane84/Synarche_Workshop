/*
artifact_anchor:
  id: COG.LOOMENGINE.001
  version: v15.0 [OMEGA]
  provenance: '2026-07-22'
  domain: COG
  celestial_class: PLANET
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import * as crypto from "crypto";
import { PhoenixLogger } from "@system/logging";
import { RNCEngine } from "./RNCEngine";

export class LoomEngine {
  private static BLOCK_A_HEADER_RE = /^#+ \*\*Block A:.*?\*\*/mi;
  private static TABLE_ROW_RE = /\| \s*\*\*([^*]+)\*\*\s* \| \s*`?([^`|]+)`?\s* \|/i;
  private static ANCHOR_RE = /\[(?:OMNI|GATE|RNC)-ANCHOR\] ID: ([\w.-]+) VER: ([\w. \[\]]+) STATUS: ([\w. \[\]]+)/gi;
  private static RELATION_RE = /(\w+):\s*([\w.-]+)/gi;

  /**
   * Calculates the hash of the "Soul" content of the file (excluding Block A and anchor tags).
   */
  public static calculateContentHash(content: string): string {
    let soulContent = content;

    // 1. Remove Block A header and its table to isolate the soul content
    const match = this.BLOCK_A_HEADER_RE.exec(content);
    if (match) {
      const startPos = match.index;
      const sepPos = content.indexOf("---", startPos);
      if (sepPos !== -1) {
        soulContent = content.substring(sepPos + 3).trim();
      } else {
        soulContent = content.replace(match[0], "").trim();
      }
    } else {
      soulContent = content.trim();
    }

    // 2. Remove Anchor markers
    soulContent = soulContent.replace(this.ANCHOR_RE, "").trim();

    // 3. Compute SHA-256 hash
    return crypto.createHash("sha256").update(soulContent, "utf8").digest("hex");
  }

  /**
   * Parses the Block A metadata from markdown content.
   */
  public static parseMarkdownMetadata(content: string): Record<string, string> | null {
    const meta: Record<string, any> = {};

    if (content.includes("Block A:")) {
      const lines = content.split("\n");
      let inBlock = false;
      for (const line of lines) {
        if (line.includes("Block A:")) {
          inBlock = true;
          continue;
        }
        if (inBlock && (line.trim() === "---" || (line.startsWith("##") && !line.includes("Block A:")))) {
          break;
        }
        if (inBlock) {
          const m = this.TABLE_ROW_RE.exec(line);
          if (m) {
            const rawKey = m[1].replace(/\*\*/g, "").replace(/:/g, "").trim();
            const key = rawKey.toLowerCase().replace(/ /g, "_");
            const value = m[2].replace(/\*\*/g, "").trim();
            meta[key] = value;
          }
        }
      }

      // Parse relations into structured list if present
      if (meta.relations) {
        const rels: string[] = [];
        let match;
        // Reset lastIndex for reuse
        this.RELATION_RE.lastIndex = 0;
        while ((match = this.RELATION_RE.exec(meta.relations)) !== null) {
          rels.push(`${match[1]}:${match[2]}`);
        }
        if (rels.length > 0) {
          meta.parsed_relations = rels;
        }
      }

      if (meta && meta.artifact_id) {
        return meta;
      }
    }

    // Attempt to search for anchor tag if Block A parsing didn't find artifact_id
    this.ANCHOR_RE.lastIndex = 0;
    const anchorMatch = this.ANCHOR_RE.exec(content);
    if (anchorMatch && !meta.artifact_id) {
      meta.artifact_id = anchorMatch[1];
      meta.version = anchorMatch[2];
      meta.status = anchorMatch[3];
      return meta;
    }

    return Object.keys(meta).length > 0 ? meta : null;
  }

  /**
   * Generates UIP-V15 compliant Block A markdown block.
   */
  public static generateBlockA(meta: Record<string, any>): string {
    const lines = [
      "## **Block A: The Identification Lock (UIP-V15)**",
      "",
      "| Key               | Value                             | Description       |",
      "| :---------------- | :-------------------------------- | :---------------- |",
      `| **Artifact ID**   | \`${meta.artifact_id || "REQD"}\` | The Sovereign ID. |`,
      `| **Official Name** | \`${meta.official_name || (meta.artifact_id ? meta.artifact_id + ".md" : "REQD")}\` | The Filename.     |`,
      `| **Version**       | **${meta.version || "v15.0 [OMEGA]"}** | The Standard.     |`,
      `| **Domain**        | \`${meta.domain || "GVRN"}\` | The Subject.      |`,
      `| **Status**        | \`${meta.status || "[ACTIVE]"}\` | The Lifecycle.    |`,
      `| **Relations**     | \`${meta.relations || "REF: GVRN.Master.Registry"}\` | The Network.      |`,
      "",
    ];
    return lines.join("\n");
  }

  /**
   * Performs a validation of the metadata fields to ensure OMEGA compliance.
   */
  public static validateMetadata(meta: Record<string, any>): string[] {
    const errors: string[] = [];

    if (!meta.artifact_id) {
      errors.push("Missing required metadata field: artifact_id");
    } else {
      if (!RNCEngine.validateId(meta.artifact_id)) {
        errors.push(`Artifact ID '${meta.artifact_id}' does not conform to OMEGA v15.0 RNC format.`);
      }
    }

    if (!meta.official_name) {
      errors.push("Missing required metadata field: official_name");
    }

    if (!meta.version) {
      errors.push("Missing required metadata field: version");
    }

    return errors;
  }
}
