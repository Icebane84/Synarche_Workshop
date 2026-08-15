/*
artifact_anchor:
  id: COG.CPPENGINE.001
  version: v15.0 [OMEGA]
  provenance: '2026-07-23'
  domain: COG
  celestial_class: PLANET
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import * as fs from "node:fs";
import * as path from "node:path";

export interface CppViolation {
  line: number;
  rule: string;
  message: string;
}

export interface ProvenanceValue<T> {
  value: T;
  provenance: "MEASURED" | "SELF_REPORTED";
}

export interface CppTelemetry {
  timestamp: string;
  verifiedFiles: string[];
  violations: Record<string, CppViolation[]>;
  exitCode: number;
  telemetryMetrics?: {
    filesScanned: ProvenanceValue<number>;
    violationCount: ProvenanceValue<number>;
    exitCode: ProvenanceValue<number>;
  };
}

// biome-ignore lint/complexity/noStaticOnlyClass: Matches system engine architectural design patterns
export class CppEngine {
  private static loadSymbolManifests(): Set<string> {
    const symbols = new Set<string>();
    const pathsToTry = [
      path.join(__dirname, "../../../axion-core/tools/known_api_symbols"),
      path.join(process.cwd(), "axion-core/tools/known_api_symbols"),
      path.join(process.cwd(), "../axion-core/tools/known_api_symbols"),
    ];
    let manifestDir = "";
    for (const p of pathsToTry) {
      if (fs.existsSync(p)) {
        manifestDir = p;
        break;
      }
    }
    if (manifestDir && fs.existsSync(manifestDir)) {
      const files = fs.readdirSync(manifestDir);
      for (const file of files) {
        if (file.endsWith(".json")) {
          try {
            const content = fs.readFileSync(path.join(manifestDir, file), "utf8");
            const data = JSON.parse(content);
            const allowed = data.allowed_symbols || [];
            for (const sym of allowed) {
              symbols.add(sym);
            }
          } catch (e) {
            console.error(`Warning: Failed to load manifest ${file}: ${e}`);
          }
        }
      }
    }
    return symbols;
  }

  private static ALLOWED_UE_SYMBOLS = CppEngine.loadSymbolManifests();

  /**
   * Statically checks a single C++ file's content for syntax, reflection, and safety rules.
   */
  // biome-ignore lint/complexity/noExcessiveCognitiveComplexity: Legacy python port structural complexity
  public static analyzeContent(content: string, filePath: string): CppViolation[] {
    const violations: CppViolation[] = [];
    const lines = content.split(/\r?\n/);

    // 1. Balanced Brackets Check
    const bracesStack: number[] = [];
    const parensStack: number[] = [];

    for (let i = 0; i < content.length; i++) {
      const char = content[i];
      if (char === "{") {
        bracesStack.push(i);
      } else if (char === "}") {
        if (bracesStack.length === 0) {
          violations.push({
            line: content.substring(0, i).split("\n").length,
            rule: "SYNTAX_UNBALANCED_BRACES",
            message: "Unbalanced closing brace '}' found without opening brace.",
          });
        } else {
          bracesStack.pop();
        }
      } else if (char === "(") {
        parensStack.push(i);
      } else if (char === ")") {
        if (parensStack.length === 0) {
          violations.push({
            line: content.substring(0, i).split("\n").length,
            rule: "SYNTAX_UNBALANCED_PARENS",
            message: "Unbalanced closing parenthesis ')' found without opening parenthesis.",
          });
        } else {
          parensStack.pop();
        }
      }
    }

    if (bracesStack.length > 0) {
      violations.push({
        line: content.substring(0, bracesStack[0]).split("\n").length,
        rule: "SYNTAX_UNBALANCED_BRACES",
        message: `Unbalanced opening braces: ${bracesStack.length} braces remain unclosed.`,
      });
    }

    if (parensStack.length > 0) {
      violations.push({
        line: content.substring(0, parensStack[0]).split("\n").length,
        rule: "SYNTAX_UNBALANCED_PARENS",
        message: `Unbalanced opening parentheses: ${parensStack.length} parentheses remain unclosed.`,
      });
    }

    // 2. Class Declaration Parsing (handle optional API macro)
    const classDeclMatch =
      /\bclass\s+(?:[A-Za-z0-9_]+_API\s+)?([A-Za-z0-9_]+)\s*:\s*public\s+([A-Za-z0-9_]+)/.exec(
        content,
      );
    const className = classDeclMatch ? classDeclMatch[1] : null;

    const fileAllowedSymbols = new Set(CppEngine.ALLOWED_UE_SYMBOLS);
    if (className) {
      fileAllowedSymbols.add(className);
      if (
        className.startsWith("U") ||
        className.startsWith("A") ||
        className.startsWith("F") ||
        className.startsWith("T")
      ) {
        fileAllowedSymbols.add(className.substring(1));
      }
    }

    // 3. Line-by-Line Checks
    for (let idx = 0; idx < lines.length; idx++) {
      const lineNum = idx + 1;
      const line = lines[idx];
      const stripped = line.trim();

      if (!stripped || stripped.startsWith("//") || stripped.startsWith("/*")) {
        continue;
      }

      // Pointer Safety: Raw new/delete checks
      if (/\bdelete\s+[a-zA-Z_]/.test(stripped)) {
        violations.push({
          line: lineNum,
          rule: "SAFETY_RAW_DELETE",
          message:
            "Raw 'delete' operator is forbidden. Use TSharedPtr / TUniquePtr or engine garbage collection.",
        });
      }
      if (/\bnew\s+[A-Za-z0-9_]/.test(stripped)) {
        violations.push({
          line: lineNum,
          rule: "SAFETY_RAW_NEW",
          message: "Raw 'new' allocation is forbidden. Use CreateDefaultSubobject or MakeShared.",
        });
      }

      // Class Reflection Checks
      if (stripped.startsWith("class ") && stripped.includes(":")) {
        const fileBasename = path.basename(filePath).replace(".cpp", "").replace(".h", "");
        const expectedGenInclude = `#include "${fileBasename}.generated.h"`;

        let classBasename = className;
        if (
          className &&
          (className.startsWith("U") ||
            className.startsWith("A") ||
            className.startsWith("F") ||
            className.startsWith("T"))
        ) {
          classBasename = className.substring(1);
        }
        const expectedClassInclude = classBasename
          ? `#include "${classBasename}.generated.h"`
          : null;

        const hasCorrectInclude =
          content.includes(expectedGenInclude) ||
          (expectedClassInclude && content.includes(expectedClassInclude));
        if (!hasCorrectInclude) {
          let expectedDesc = expectedGenInclude;
          if (expectedClassInclude) {
            expectedDesc += ` or ${expectedClassInclude}`;
          }
          violations.push({
            line: lineNum,
            rule: "REFLECTION_MISSING_GENERATED_INCLUDE",
            message: `Missing generated include directive: expected ${expectedDesc}`,
          });
        }

        const classStartIdx = content.indexOf(line);
        const classEndBlock = content.substring(classStartIdx);
        const classDeclBlock = classEndBlock.split("};")[0];
        if (!classDeclBlock.includes("GENERATED_BODY()")) {
          violations.push({
            line: lineNum,
            rule: "REFLECTION_MISSING_BODY_MACRO",
            message: "Class declaration is missing the GENERATED_BODY() macro.",
          });
        }
      }

      // Pointer Safety: Untracked pointer member check
      const pointerDeclMatch = /^([A-Za-z0-9_]+)\*\s+([A-Za-z0-9_]+)\s*;/.exec(stripped);
      if (pointerDeclMatch) {
        const ptrType = pointerDeclMatch[1];
        let hasUproperty = false;

        // Check preceding lines for UPROPERTY()
        let prevLineIdx = idx - 1;
        while (prevLineIdx >= 0) {
          const prevStripped = lines[prevLineIdx].trim();
          if (prevStripped.startsWith("UPROPERTY")) {
            hasUproperty = true;
            break;
          }
          if (prevStripped && !prevStripped.startsWith("//")) {
            break;
          }
          prevLineIdx--;
        }

        if (!hasUproperty && (ptrType.startsWith("U") || ptrType.startsWith("A"))) {
          violations.push({
            line: lineNum,
            rule: "SAFETY_UNTRACKED_POINTER",
            message: `Raw member pointer '${stripped}' of type '${ptrType}' must be tracked by a UPROPERTY() macro to prevent garbage collection.`,
          });
        }
      }

      // Symbol Verification
      const potentialSymbols = stripped.match(/\b([UATF][A-Z][a-zA-Z0-9_]+|[A-Z_]{4,})\b/g);
      if (potentialSymbols) {
        for (const symbol of potentialSymbols) {
          if (
            symbol === className ||
            symbol.endsWith("_API") ||
            symbol.startsWith("FID_") ||
            symbol.endsWith("_generated_h")
          ) {
            continue;
          }
          if (!fileAllowedSymbols.has(symbol)) {
            violations.push({
              line: lineNum,
              rule: "SYMBOL_UNRECOGNIZED",
              message: `Unrecognized engine or system symbol referenced: '${symbol}'`,
            });
          }
        }
      }
    }

    return violations;
  }

  /**
   * Runs the C++ verifier on target file/directory paths and writes the JSON telemetry log.
   */
  public static runVerifier(targets: string[]): CppTelemetry {
    const allViolations: Record<string, CppViolation[]> = {};
    const verifiedFiles: string[] = [];

    for (const target of targets) {
      const resolved = path.resolve(target);
      if (fs.existsSync(resolved)) {
        const stat = fs.statSync(resolved);
        if (stat.isDirectory()) {
          CppEngine.scanDir(resolved, verifiedFiles, allViolations);
        } else if (stat.isFile() && (resolved.endsWith(".cpp") || resolved.endsWith(".h"))) {
          verifiedFiles.push(resolved);
          const content = fs.readFileSync(resolved, "utf8");
          const violations = CppEngine.analyzeContent(content, resolved);
          if (violations.length > 0) {
            allViolations[resolved] = violations;
          }
        }
      }
    }

    const exitCode = Object.keys(allViolations).length > 0 ? 1 : 0;
    const violationCount = Object.values(allViolations).reduce((sum, list) => sum + list.length, 0);

    const telemetry: CppTelemetry = {
      timestamp: new Date().toISOString(),
      verifiedFiles,
      violations: allViolations,
      exitCode,
      telemetryMetrics: {
        filesScanned: {
          value: verifiedFiles.length,
          provenance: "MEASURED",
        },
        violationCount: {
          value: violationCount,
          provenance: "MEASURED",
        },
        exitCode: {
          value: exitCode,
          provenance: "MEASURED",
        },
      },
    };

    const logDir = "c:\\Users\\Chris\\Synarche_Workspace\\_governance\\50_Logs";
    if (!fs.existsSync(logDir)) {
      fs.mkdirSync(logDir, { recursive: true });
    }
    const logPath = path.join(logDir, "LOG.MECS.TELEMETRY_CPP.json");
    fs.writeFileSync(logPath, JSON.stringify(telemetry, null, 2), "utf8");

    return telemetry;
  }

  private static scanDir(
    dir: string,
    verifiedFiles: string[],
    allViolations: Record<string, CppViolation[]>,
  ): void {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        // Skip ignored build/meta dirs
        if (item === "node_modules" || item === ".git" || item === ".venv") {
          continue;
        }
        CppEngine.scanDir(fullPath, verifiedFiles, allViolations);
      } else if (stat.isFile() && (fullPath.endsWith(".cpp") || fullPath.endsWith(".h"))) {
        verifiedFiles.push(fullPath);
        const content = fs.readFileSync(fullPath, "utf8");
        const violations = CppEngine.analyzeContent(content, fullPath);
        if (violations.length > 0) {
          allViolations[fullPath] = violations;
        }
      }
    }
  }
}
