/*
artifact_anchor:
  id: COG.TESTENGINE.001
  version: v15.0 [OMEGA]
  provenance: '2026-07-22'
  domain: COG
  celestial_class: PLANET
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import * as fs from "node:fs";
import * as path from "node:path";
import { PhoenixLogger } from "@system/logging";
import { ConsistencyEngine } from "./ConsistencyEngine";
import { ContextWeave } from "./ContextWeave";
import { CppEngine } from "./CPPEngine";
import { LoomEngine } from "./LoomEngine";
import { RNCEngine } from "./RNCEngine";

function runTests(): void {
  PhoenixLogger.info(">>> Starting Symphonic Engine Unit Tests...");

  // 1. Test ContextWeave
  PhoenixLogger.info("Testing ContextWeave...");
  const cw = new ContextWeave(0.5);

  const keywords = cw.extractKeywords("The Phoenix Engine is a Sovereign Tool.");
  PhoenixLogger.info(`Extracted keywords: ${JSON.stringify(keywords)}`);
  if (
    keywords.length !== 4 ||
    !keywords.includes("Phoenix") ||
    !keywords.includes("Engine") ||
    !keywords.includes("Sovereign") ||
    !keywords.includes("Tool")
  ) {
    throw new Error("ContextWeave keyword extraction failed!");
  }

  const artA = {
    id: "COG.TEST.A",
    content: "The Phoenix Engine is a Sovereign Tool.",
    tags: ["cognitive", "loom"],
  };
  const artB = {
    id: "COG.TEST.B",
    content: "The Phoenix System implements the Sovereign Tool.",
    tags: ["cognitive", "synthesis"],
  };

  const synergy = cw.calculateSynergyScore(artA, artB);
  PhoenixLogger.info(`Calculated synergy score: ${synergy}`);
  // Overlap: Phoenix, Sovereign, Tool (3 keywords -> min(3*0.1, 0.4) = 0.3)
  // Tags: "cognitive" overlaps -> +0.2
  // Total expected = 0.5
  if (Math.abs(synergy - 0.5) > 0.001) {
    throw new Error(`ContextWeave synergy calculation mismatch! Expected 0.5, got ${synergy}`);
  }

  const weaveRes = cw.weaveArtifacts(artA, artB);
  PhoenixLogger.info(`Weave results: ${JSON.stringify(weaveRes)}`);
  if (weaveRes.synergyScore !== 0.5 || !weaveRes.isAligned || weaveRes.pivots.length !== 3) {
    throw new Error("ContextWeave weaveArtifacts verification failed!");
  }

  // 2. Test RNCEngine
  PhoenixLogger.info("Testing RNCEngine...");
  const validId = "GVRN.REGISTRY.STANDARD";
  const invalidId = "GVRN.INVALID.123";

  if (!RNCEngine.validateId(validId)) {
    throw new Error(`RNCEngine failed to validate valid ID: ${validId}`);
  }
  if (RNCEngine.validateId(invalidId)) {
    throw new Error(`RNCEngine validated invalid ID: ${invalidId}`);
  }

  const pathResult = RNCEngine.suggestPath("CORE.ENGINE.RNC_ENGINE");
  PhoenixLogger.info(`Suggested path: ${pathResult}`);
  // Expected: axion-core/forge/CORE.ENGINE.RNC_ENGINE.md
  if (!pathResult.includes("axion-core") || !pathResult.includes("forge")) {
    throw new Error(`RNCEngine suggestPath failed! Got: ${pathResult}`);
  }

  // 3. Test LoomEngine
  PhoenixLogger.info("Testing LoomEngine...");
  const mockMarkdown = `## **Block A: The Identification Lock (UIP-V15)**

| Key               | Value                             | Description       |
| :---------------- | :-------------------------------- | :---------------- |
| **Artifact ID**   | \`COG.TEST.A\`                      | The Sovereign ID. |
| **Official Name** | \`test_artifact.md\`                | The Filename.     |
| **Version**       | **v15.0 [OMEGA]**                 | The Standard.     |
| **Domain**        | \`COG\`                             | The Subject.      |
| **Status**        | \`[ACTIVE]\`                        | The Lifecycle.    |
| **Relations**     | \`GOVERNED_BY: COG.CODEX.001\`      | The Network.      |
---
This is the soul content.`;

  const meta = LoomEngine.parseMarkdownMetadata(mockMarkdown);
  PhoenixLogger.info(`Parsed metadata: ${JSON.stringify(meta)}`);
  if (
    !meta ||
    meta.artifact_id !== "COG.TEST.A" ||
    meta.official_name !== "test_artifact.md" ||
    !meta.parsed_relations
  ) {
    throw new Error("LoomEngine parsing failed!");
  }

  const hash1 = LoomEngine.calculateContentHash(mockMarkdown);
  const hash2 = LoomEngine.calculateContentHash(
    `${mockMarkdown}\n[OMNI-ANCHOR] ID: COG.TEST.A VER: v15.0 STATUS: ACTIVE`,
  );
  PhoenixLogger.info(`Hash 1: ${hash1}`);
  PhoenixLogger.info(`Hash 2: ${hash2}`);
  if (hash1 !== hash2) {
    throw new Error("LoomEngine content hash calculation is not anchor-immune!");
  }

  // 4. Test CppEngine
  PhoenixLogger.info("Testing CppEngine...");
  const validCpp = `
#include "CoreMinimal.h"
#include "Components/ActorComponent.h"
#include "ValidComponent.generated.h"

UCLASS(meta=(BlueprintSpawnableComponent))
class BERSERKGAME_API UValidComponent : public UActorComponent
{
    GENERATED_BODY()
public:
    UValidComponent();
protected:
    UPROPERTY(EditAnywhere)
    UActorComponent* SafePtr;
};
  `;
  const validViolations = CppEngine.analyzeContent(validCpp, "ValidComponent.cpp");
  if (validViolations.length > 0) {
    throw new Error(
      `CppEngine flagged valid content! Got violations: ${JSON.stringify(validViolations)}`,
    );
  }

  const invalidCpp = `
class BERSERKGAME_API UValidComponent : public UActorComponent {
    GENERATED_BODY()
    // Unbalanced brackets
    void Work() {
        if (true) {
            delete UnsafePtr;
    }
};
  `;
  const invalidViolations = CppEngine.analyzeContent(invalidCpp, "ValidComponent.cpp");
  const rules = invalidViolations.map((v) => v.rule);
  if (!rules.includes("SYNTAX_UNBALANCED_BRACES")) {
    throw new Error("CppEngine failed to detect unbalanced braces!");
  }
  if (!rules.includes("SAFETY_RAW_DELETE")) {
    throw new Error("CppEngine failed to detect raw delete operator!");
  }

  // Verify the entire dragonslayer directory with CppEngine
  PhoenixLogger.info("Running CppEngine over scratch/dragonslayer/...");
  const dragonslayerTelemetry = CppEngine.runVerifier(["scratch/dragonslayer"]);
  PhoenixLogger.info(`Dragonslayer verifier exit code: ${dragonslayerTelemetry.exitCode}`);
  if (dragonslayerTelemetry.exitCode !== 0) {
    throw new Error(
      `CppEngine found violations in dragonslayer: ${JSON.stringify(
        dragonslayerTelemetry.violations,
      )}`,
    );
  }

  // 5. Test ConsistencyEngine
  PhoenixLogger.info("Testing ConsistencyEngine...");
  const tempSpecPath = path.resolve(process.cwd(), "../scratch/spec_temp.py");
  const tempImplPath = path.resolve(process.cwd(), "../scratch/impl_temp.cpp");
  fs.writeFileSync(
    tempSpecPath,
    `
# GVRN.CONST: base_radius = 1200.0
# GVRN.CONST: speed_limit = 50.0
  `,
    "utf8",
  );
  fs.writeFileSync(
    tempImplPath,
    `
// GVRN.CONST: base_radius = 1200.0;
// GVRN.CONST: speed_limit = 45.0;
// GVRN.CONST: extra_const = 100
  `,
    "utf8",
  );

  const findings = ConsistencyEngine.verifyConsistency(tempSpecPath, tempImplPath);
  fs.unlinkSync(tempSpecPath);
  fs.unlinkSync(tempImplPath);

  const driftFinding = findings.find((f) => f.name === "speed_limit");
  const orphanedFinding = findings.find((f) => f.name === "extra_const");

  if (!driftFinding || driftFinding.type !== "DRIFT" || driftFinding.actual !== "45.0") {
    throw new Error(
      `ConsistencyEngine failed to detect constant drift: ${JSON.stringify(findings)}`,
    );
  }
  if (!orphanedFinding || orphanedFinding.type !== "ORPHANED") {
    throw new Error(
      `ConsistencyEngine failed to detect orphaned constant: ${JSON.stringify(findings)}`,
    );
  }

  PhoenixLogger.info(">>> All Symphonic Engine Unit Tests Passed!");
}

try {
  runTests();
} catch (error) {
  PhoenixLogger.critical(`Test suite failed: ${error}`);
  process.exit(1);
}
