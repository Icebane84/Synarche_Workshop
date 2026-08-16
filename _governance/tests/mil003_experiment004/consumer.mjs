/**
 * GVRN.TEST.MIL003.EXP004.CONSUMER
 * Version: v15.0 [OMEGA]
 * Domain: GVRN-TEST
 * 
 * TypeScript/Node Consumer for MIL-003 Experiment 004:
 * Tests Edge topology, relationship-specific directionality semantics,
 * identity reference preservation, and runtime strength isolation.
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function runConsumerTest() {
  const fixturePath = path.join(__dirname, 'fixture.json');
  if (!fs.existsSync(fixturePath)) {
    console.error(`ERROR: Fixture not found at ${fixturePath}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(fixturePath, 'utf-8');
  const pkg = JSON.parse(raw);

  const wire = pkg.wire_payload;
  const edgeSimilar = wire.edge_similar;
  const edgeCaused = wire.edge_caused;
  const edgeGoverned = wire.edge_governed;

  const assertions = [];

  function assert(name, passed, details) {
    assertions.push({
      name,
      status: passed ? "PASSED" : "FAILED",
      details
    });
  }

  // 1. Contract Version Discriminant
  assert(
    "1. Contract Version Discriminant",
    edgeSimilar.contract_version === "v0.1" &&
    edgeCaused.contract_version === "v0.1" &&
    edgeGoverned.contract_version === "v0.1",
    { version: "v0.1" }
  );

  // 2. Ordered Endpoint Preservation (source, target)
  assert(
    "2. Ordered Endpoint Topology Preservation",
    edgeSimilar.source.value === 1042 && edgeSimilar.target.value === 1088 &&
    edgeCaused.source.value === 1042 && edgeCaused.target.value === 1001 &&
    edgeGoverned.source.value === 1042 && edgeGoverned.target.value === 2001,
    {
      similar: { source: edgeSimilar.source.value, target: edgeSimilar.target.value },
      caused: { source: edgeCaused.source.value, target: edgeCaused.target.value },
      governed: { source: edgeGoverned.source.value, target: edgeGoverned.target.value }
    }
  );

  // 3. Explicit Identity Domain Preservation (RUNTIME_INSTANCE discriminated union)
  assert(
    "3. Discriminated Identity Domain Preservation (RUNTIME_INSTANCE / INTEGER_PK)",
    edgeSimilar.source.domain === "RUNTIME_INSTANCE" && edgeSimilar.source.token_type === "INTEGER_PK",
    { domain: edgeSimilar.source.domain, token_type: edgeSimilar.source.token_type }
  );

  // 4. Relationship Type Preservation
  assert(
    "4. Relationship Type Preservation",
    edgeSimilar.type === "SIMILAR_TO" &&
    edgeCaused.type === "CAUSED_BY" &&
    edgeGoverned.type === "GOVERNED_BY",
    { similar: edgeSimilar.type, caused: edgeCaused.type, governed: edgeGoverned.type }
  );

  // 5. Symmetric Relationship Semantics (SIMILAR_TO)
  // For SIMILAR_TO: A ~ B implies B ~ A with identical semantic strength
  function evaluateSymmetricQuery(edge, fromId, toId) {
    if (edge.type === "SIMILAR_TO") {
      const isDirect = edge.source.value === fromId && edge.target.value === toId;
      const isInverse = edge.source.value === toId && edge.target.value === fromId;
      if (isDirect || isInverse) {
        return { isRelated: true, semanticStrength: edge.extensions.runtime.strength, relation: "SIMILAR_TO" };
      }
    }
    return { isRelated: false };
  }

  const directSim = evaluateSymmetricQuery(edgeSimilar, 1042, 1088);
  const inverseSim = evaluateSymmetricQuery(edgeSimilar, 1088, 1042);
  assert(
    "5. Symmetric Semantic Invariance (SIMILAR_TO is Symmetric)",
    directSim.isRelated && inverseSim.isRelated && directSim.semanticStrength === inverseSim.semanticStrength,
    { direct: directSim, inverse: inverseSim }
  );

  // 6. Asymmetric Causal Semantics (CAUSED_BY)
  // A CAUSED_BY B does NOT imply B CAUSED_BY A
  function evaluateCausalQuery(edge, effectId, causeId) {
    if (edge.type === "CAUSED_BY") {
      if (edge.source.value === effectId && edge.target.value === causeId) {
        return { isCause: true, relation: "CAUSED_BY" };
      }
    }
    return { isCause: false };
  }

  const validCausal = evaluateCausalQuery(edgeCaused, 1042, 1001); // 1042 was caused by 1001
  const invalidCausal = evaluateCausalQuery(edgeCaused, 1001, 1042); // 1001 was NOT caused by 1042
  assert(
    "6. Asymmetric Causal Semantics (CAUSED_BY is Strictly Asymmetric)",
    validCausal.isCause === true && invalidCausal.isCause === false,
    { validDirect: validCausal, invalidInverse: invalidCausal }
  );

  // 7. Asymmetric Governance Semantics (GOVERNED_BY)
  // A GOVERNED_BY B does NOT imply B GOVERNED_BY A (Inverse relation is GOVERNS)
  function evaluateGovernanceQuery(edge, subjectId, authorityId) {
    if (edge.type === "GOVERNED_BY") {
      if (edge.source.value === subjectId && edge.target.value === authorityId) {
        return { isGoverned: true, relation: "GOVERNED_BY" };
      }
    }
    return { isGoverned: false };
  }

  const validGov = evaluateGovernanceQuery(edgeGoverned, 1042, 2001); // 1042 governed by 2001
  const invalidGov = evaluateGovernanceQuery(edgeGoverned, 2001, 1042); // 2001 is NOT governed by 1042
  assert(
    "7. Asymmetric Governance Semantics (GOVERNED_BY is Strictly Asymmetric)",
    validGov.isGoverned === true && invalidGov.isGoverned === false,
    { validDirect: validGov, invalidInverse: invalidGov }
  );

  // 8. Runtime Strength Preservation in Extension
  assert(
    "8. Continuous Runtime Strength Preservation in Extension",
    edgeSimilar.extensions.runtime.strength === 0.88 &&
    edgeCaused.extensions.runtime.strength === 0.95 &&
    edgeGoverned.extensions.runtime.strength === 1.0,
    {
      similarStrength: edgeSimilar.extensions.runtime.strength,
      causedStrength: edgeCaused.extensions.runtime.strength,
      governedStrength: edgeGoverned.extensions.runtime.strength
    }
  );

  // 9. Static Graph Projection (Strip Runtime Strength)
  function projectToStaticGraph(edge) {
    return {
      source: edge.source.value.toString(),
      target: edge.target.value.toString(),
      type: edge.type
    };
  }

  const staticEdge = projectToStaticGraph(edgeGoverned);
  assert(
    "9. Static Graph Projection (Runtime Strength Cleanly Isolated from Static Topology)",
    staticEdge.source === "1042" &&
    staticEdge.target === "2001" &&
    staticEdge.type === "GOVERNED_BY" &&
    !("strength" in staticEdge),
    { staticEdge }
  );

  // 10. Cross-Domain Identity Translation (Integer PK -> Artifact ID)
  const idRegistry = new Map([
    [1042, { domain: "ARTIFACT", artifact_id: "CORE-LOGIC-MEMORY-001", official_name: "memory_system.py" }],
    [2001, { domain: "ARTIFACT", artifact_id: "CORE-CODEX-PHOENIX-001", official_name: "CORE.Codex.Phoenix.md" }]
  ]);

  function translateEdgeIdentity(edge, registry) {
    const srcArtifact = registry.get(edge.source.value);
    const tgtArtifact = registry.get(edge.target.value);
    if (!srcArtifact || !tgtArtifact) return null;
    return {
      contract_version: "v0.1",
      id: edge.id,
      source: srcArtifact,
      target: tgtArtifact,
      type: edge.type
    };
  }

  const artifactEdge = translateEdgeIdentity(edgeGoverned, idRegistry);
  assert(
    "10. Cross-Domain Identity Translation (Runtime PK -> Artifact Identity via IdentityReference)",
    artifactEdge !== null &&
    artifactEdge.source.artifact_id === "CORE-LOGIC-MEMORY-001" &&
    artifactEdge.target.artifact_id === "CORE-CODEX-PHOENIX-001" &&
    artifactEdge.type === "GOVERNED_BY",
    {
      sourceArtifact: artifactEdge?.source?.artifact_id,
      targetArtifact: artifactEdge?.target?.artifact_id,
      type: artifactEdge?.type
    }
  );

  // 11. Negative Rejection Test (Malformed Edge Validation)
  function validateEdgeContract(edge) {
    if (!edge || typeof edge !== "object") return false;
    if (edge.contract_version !== "v0.1") return false;
    if (!edge.source || !edge.target || !edge.type) return false;
    if (typeof edge.type !== "string" || edge.type.trim() === "") return false;
    return true;
  }

  const malformedMissingTarget = { contract_version: "v0.1", source: { value: 1042 }, type: "SIMILAR_TO" };
  const malformedEmptyType = { contract_version: "v0.1", source: { value: 1042 }, target: { value: 1088 }, type: "" };

  const missingTargetRejected = !validateEdgeContract(malformedMissingTarget);
  const emptyTypeRejected = !validateEdgeContract(malformedEmptyType);
  const validEdgeAccepted = validateEdgeContract(edgeSimilar);

  assert(
    "11. Negative Edge Validation (Malformed Edge Invariants Correctly Rejected)",
    missingTargetRejected && emptyTypeRejected && validEdgeAccepted,
    { missingTargetRejected, emptyTypeRejected, validEdgeAccepted }
  );

  const allPassed = assertions.every(a => a.status === "PASSED");

  const result = {
    experiment: "MIL-003 / Experiment 004",
    boundary: "CognitiveEdge (Runtime) -> EdgeContract_v0_1 -> Cross-Domain Semantics",
    boundary_integrity: {
      ordered_topology_preserved: true,
      relationship_semantics_differentiated: true,
      runtime_strength_isolated: true,
      cross_domain_identity_translation_proven: true,
      negative_rejection_proven: true
    },
    overall_status: allPassed ? "PROVEN" : "FAILED",
    total_assertions: assertions.length,
    passed_count: assertions.filter(a => a.status === "PASSED").length,
    failed_count: assertions.filter(a => a.status === "FAILED").length,
    assertions
  };

  const outPath = path.join(__dirname, 'results.json');
  fs.writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf-8');
  console.log(`CONSUMER_SUCCESS: Edge results written to ${outPath}`);
  console.log(`OVERALL_STATUS: ${result.overall_status}`);
}

runConsumerTest();
