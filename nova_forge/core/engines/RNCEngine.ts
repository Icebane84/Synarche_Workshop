/*
artifact_anchor:
  id: COG.RNCENGINE.001
  version: v15.0 [OMEGA]
  provenance: '2026-07-22'
  domain: COG
  celestial_class: PLANET
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import * as fs from "fs";
import * as path from "path";
import { PhoenixLogger } from "@system/logging";
import * as standards from "@domain/13_Standardization/GVRN.Standards.json";

export class RNCEngine {
  // [DOMAIN].[Subsystem].[Descriptor]
  private static RNC_PATTERN = /^([A-Z0-9]+)\.([A-Z0-9]+)\.([A-Za-z0-9_\-\.]+)$/;

  /**
   * Verifies if an ID aligns with OMEGA v15.0 RNC standards.
   */
  public static validateId(artifactId: string): boolean {
    const match = this.RNC_PATTERN.exec(artifactId);
    if (!match) {
      return false;
    }

    const domainStr = match[1];
    const subsystemStr = match[2];

    const validDomains = standards.enums.Domain;
    const validSubSystems = standards.enums.SubSystem;

    // Check if domain and subsystem exist in valid standards
    const hasDomain = Object.prototype.hasOwnProperty.call(validDomains, domainStr);
    const hasSubsystem = Object.prototype.hasOwnProperty.call(validSubSystems, subsystemStr);

    return hasDomain && hasSubsystem;
  }

  /**
   * Maps an RNC ID to its canonical filesystem location.
   */
  public static suggestPath(artifactId: string): string {
    const match = this.RNC_PATTERN.exec(artifactId);
    if (!match) {
      throw new Error(`Invalid RNC ID for path mapping: ${artifactId}`);
    }

    const domain = match[1];
    const subsystem = match[2];

    // Domain-to-Root Mapping
    const rootMap: Record<string, string> = {
      GVRN: "_governance",
      CORE: "axion-core",
      LAB: "nova_forge",
      SELT: "_governance/templates",
      COMM: "03_Avatar",
    };

    const root = rootMap[domain] || "unknown";

    // Subsystem-to-Folder Mapping
    const folderMap: Record<string, string> = {
      AVATAR: "03_Avatar",
      REGISTRY: "01_Registries",
      ENGINE: "forge",
      LEARNING: "06_Learning",
    };

    const folder = folderMap[subsystem] || subsystem.toLowerCase();

    return path.join(root, folder, `${artifactId}.md`);
  }

  /**
   * Applies a programmatic transformation with state-buffering to prevent truncation.
   */
  public static safeTransform(filePath: string, transformerFunc: (content: string) => string): void {
    if (!fs.existsSync(filePath)) {
      throw new Error(`Cannot transform non-existent file: ${filePath}`);
    }

    // 1. Read entire file into buffer (Kinetic -> Mind)
    const content = fs.readFileSync(filePath, "utf8");

    // 2. Apply transformation in-memory
    const transformedContent = transformerFunc(content);

    // 3. Validation: Ensure we haven't nuked the file (Zero Entropy protection)
    if (content.length > 0 && transformedContent.length === 0) {
      throw new Error(
        `Safety Trigger: Transformation returned 0 bytes for ${filePath}. Aborting write.`
      );
    }

    // 4. Atomic Write (Mind -> Substrate)
    fs.writeFileSync(filePath, transformedContent, "utf8");
    PhoenixLogger.info(`RNCEngine: Safely transformed ${filePath}`);
  }

  /**
   * Audits a directory for RNC compliance and returns a dissonance report.
   */
  public static syncFolder(folderPath: string): Array<{ file: string; issue: string; detectedId: string }> {
    const report: Array<{ file: string; issue: string; detectedId: string }> = [];

    const walk = (dir: string): void => {
      if (!fs.existsSync(dir)) {
        return;
      }
      const list = fs.readdirSync(dir);
      for (const file of list) {
        const fullPath = path.join(dir, file);
        const stat = fs.statSync(fullPath);
        if (stat.isDirectory()) {
          // Avoid scanning node_modules or system folders
          if (file !== "node_modules" && file !== ".git" && file !== "__pycache__") {
            walk(fullPath);
          }
        } else if (file.endsWith(".md")) {
          const artifactId = path.basename(file, ".md");
          if (!this.validateId(artifactId)) {
            report.push({
              file: fullPath,
              issue: "Non-compliant RNC ID",
              detectedId: artifactId,
            });
          }
        }
      }
    };

    walk(folderPath);
    return report;
  }
}
