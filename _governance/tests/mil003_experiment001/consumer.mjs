/**
 * GVRN.TEST.MIL003.EXP001.CONSUMER
 * Version: v15.0 [OMEGA]
 * Domain: GVRN-TEST
 * 
 * TypeScript/Node Consumer for MIL-003 Experiment 001:
 * Tests semantic equivalence of Python CognitiveEvent deserialized into EventContract_v0_1.
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

  const producer = pkg.producer_ground_truth;
  const wire = pkg.wire_payload;

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
    "Contract Version Discriminant",
    wire.contract_version === "v0.1",
    { expected: "v0.1", actual: wire.contract_version }
  );

  // 2. Identity Preservation
  assert(
    "ID Preservation (event_id -> id)",
    wire.id === producer.event_id,
    { expected: producer.event_id, actual: wire.id }
  );

  // 3. Source Preservation
  assert(
    "Source System Preservation",
    wire.source === producer.source,
    { expected: producer.source, actual: wire.source }
  );

  // 4. Type Preservation (event_type -> type)
  assert(
    "Event Type Preservation",
    wire.type === producer.event_type,
    { expected: producer.event_type, actual: wire.type }
  );

  // 5. Payload / Content Preservation
  assert(
    "Payload Content Preservation (content -> payload)",
    wire.payload === producer.content,
    { expected: producer.content, actual: wire.payload }
  );

  // 6. Timestamp Serialization & Deserialization Analysis
  const parsedDate = new Date(wire.timestamp);
  const parsedEpochMs = parsedDate.getTime();
  const dateValid = !isNaN(parsedEpochMs);
  const epochDelta = Math.abs(parsedEpochMs - producer.timestamp_epoch_ms);

  // Python microsecond (123456) vs JS Date millisecond (123)
  const isLosslessToMillisecond = epochDelta === 0;
  const subMillisecondTruncation = producer.timestamp_microseconds % 1000 !== 0;

  assert(
    "Timestamp Parseability (ISO-8601 -> JS Date)",
    dateValid,
    { raw_iso: wire.timestamp, parsed_epoch_ms: parsedEpochMs }
  );

  assert(
    "Timestamp Epoch Millisecond Parity",
    isLosslessToMillisecond,
    {
      producer_epoch_ms: producer.timestamp_epoch_ms,
      consumer_epoch_ms: parsedEpochMs,
      delta_ms: epochDelta,
      sub_millisecond_loss: subMillisecondTruncation ? "Microseconds truncated to milliseconds in JS standard Date" : "None"
    }
  );

  // 7. Vector Preservation (Float64 array)
  let vectorMatches = false;
  if (Array.isArray(wire.extension?.data?.vector) && Array.isArray(producer.vector)) {
    if (wire.extension.data.vector.length === producer.vector.length) {
      vectorMatches = wire.extension.data.vector.every((val, i) => Math.abs(val - producer.vector[i]) < 1e-6);
    }
  }
  assert(
    "Vector Embedding Fidelity",
    vectorMatches,
    {
      expected_len: producer.vector?.length,
      actual_len: wire.extension?.data?.vector?.length,
      sample_producer: producer.vector?.slice(0, 3),
      sample_consumer: wire.extension?.data?.vector?.slice(0, 3)
    }
  );

  // 8. Importance Score Parity
  const importanceMatches = wire.extension?.data?.importance === producer.importance;
  assert(
    "Importance Score Parity",
    importanceMatches,
    { expected: producer.importance, actual: wire.extension?.data?.importance }
  );

  // 9. Nested Metadata Fidelity
  const metadataMatches = JSON.stringify(wire.extension?.data?.metadata) === JSON.stringify(producer.metadata);
  assert(
    "Nested Metadata Fidelity",
    metadataMatches,
    { expected: producer.metadata, actual: wire.extension?.data?.metadata }
  );

  // 10. Discriminated Extension Typing
  const isDiscriminated = wire.extension?.kind === "cognitive" && typeof wire.extension?.data === "object";
  assert(
    "Extension Discrimination (kind === 'cognitive')",
    isDiscriminated,
    { kind: wire.extension?.kind }
  );

  const allPassed = assertions.every(a => a.status === "PASSED");

  const result = {
    experiment: "MIL-003 / Experiment 001",
    boundary: "Python CognitiveEvent -> JSON -> TypeScript EventContract_v0_1",
    overall_status: allPassed ? "PROVEN" : "FAILED",
    timestamp_classification: subMillisecondTruncation ? "LOSSLESS_TO_MILLISECOND (SUB_MS_TRUNCATED)" : "STRICTLY_LOSSLESS",
    total_assertions: assertions.length,
    passed_count: assertions.filter(a => a.status === "PASSED").length,
    failed_count: assertions.filter(a => a.status === "FAILED").length,
    assertions
  };

  const outPath = path.join(__dirname, 'results.json');
  fs.writeFileSync(outPath, JSON.stringify(result, null, 2), 'utf-8');
  console.log(`CONSUMER_SUCCESS: Results written to ${outPath}`);
  console.log(`OVERALL_STATUS: ${result.overall_status}`);
}

runConsumerTest();
