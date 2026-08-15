/*
artifact_anchor:
  id: COG.CONSISTENCYENGINE.001
  version: v15.1 [OMEGA]
  provenance: '2026-07-24'
  domain: COG
  celestial_class: PLANET
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import * as fs from "node:fs";

export interface ConsistencyFinding {
  type: "DRIFT" | "ORPHANED";
  name: string;
  expected?: string;
  actual?: string;
  message: string;
}

// biome-ignore lint/complexity/noStaticOnlyClass: Matches system engine architectural design patterns
export class ConsistencyEngine {
  /**
   * Static scan that extracts and diffs constants mapped in both specification and implementation files.
   */
  public static verifyConsistency(specPath: string, implPath: string): ConsistencyFinding[] {
    const findings: ConsistencyFinding[] = [];
    if (!fs.existsSync(specPath) || !fs.existsSync(implPath)) {
      return [
        {
          type: "ORPHANED",
          name: "FILE_MISSING",
          message: `One or both paths do not exist: ${specPath} or ${implPath}`,
        },
      ];
    }

    const specContent = fs.readFileSync(specPath, "utf8");
    const implContent = fs.readFileSync(implPath, "utf8");

    const specConstants = ConsistencyEngine.extractConstants(specContent);
    const implConstants = ConsistencyEngine.extractConstants(implContent);

    // 1. Check spec vs impl
    for (const [name, specVal] of Object.entries(specConstants)) {
      if (!(name in implConstants)) {
        findings.push({
          type: "ORPHANED",
          name,
          expected: specVal,
          message: `Constant '${name}' (value: ${specVal}) exists in specification but is missing from implementation.`,
        });
      } else {
        const implVal = implConstants[name];
        if (specVal !== implVal) {
          findings.push({
            type: "DRIFT",
            name,
            expected: specVal,
            actual: implVal,
            message: `Constant '${name}' drifted: spec expected '${specVal}' but implementation got '${implVal}'.`,
          });
        }
      }
    }

    // 2. Check impl vs spec
    for (const name of Object.keys(implConstants)) {
      if (!(name in specConstants)) {
        findings.push({
          type: "ORPHANED",
          name,
          actual: implConstants[name],
          message: `Constant '${name}' exists in implementation but is missing from specification.`,
        });
      }
    }

    return findings;
  }

  private static extractConstants(content: string): Record<string, string> {
    const constants: Record<string, string> = {};
    const regex = /(?:#|\/\/)\s*GVRN\.CONST:\s*([A-Za-z0-9_]+)\s*=\s*([^\r\n]+)/g;
    let match = regex.exec(content);
    while (match !== null) {
      const name = match[1].trim();
      const value = match[2].trim().replace(/;$/, "").trim(); // strip trailing semicolon
      constants[name] = value;
      match = regex.exec(content);
    }
    return constants;
  }
}
