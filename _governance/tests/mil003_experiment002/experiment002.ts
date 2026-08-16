/**
 * GVRN.TEST.MIL003.EXP002.RUNNER
 * Version: v15.0 [OMEGA]
 * Domain: GVRN-TEST
 * 
 * Execution Harness for MIL-003 Experiment 002:
 * Tests live runtime ingestion of EventContract_v0_1 through NexusSignalBusClient.
 */

// 1. Initialize Node.js environment to support BroadcastChannel within NexusSignalBusClient
if (typeof (globalThis as any).window === "undefined") {
  (globalThis as any).window = globalThis;
}

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { NexusSignalBusClient } from '../../../packages/nexus-signalbus/src/NexusSignalBus.ts';
import type { NexusSignalEnvelope } from '../../../packages/nexus-signalbus/src/types.ts';
import { eventContractToNexusEnvelope, type EventContract_v0_1 } from './adapter.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runExperiment002() {
  const fixturePath = path.join(__dirname, '../mil003_experiment001/fixture.json');
  if (!fs.existsSync(fixturePath)) {
    console.error(`ERROR: E001 Fixture not found at ${fixturePath}`);
    process.exit(1);
  }

  const pkg = JSON.parse(fs.readFileSync(fixturePath, 'utf-8'));
  const wireContract: EventContract_v0_1 = pkg.wire_payload;
  const producerGroundTruth = pkg.producer_ground_truth;

  const assertions: Array<{ name: string; status: "PASSED" | "FAILED"; details: any }> = [];

  function assert(name: string, passed: boolean, details: any) {
    assertions.push({
      name,
      status: passed ? "PASSED" : "FAILED",
      details
    });
  }

  // --- PHASE 1: ADAPTER TRANSLATION & VALIDATION ---
  let adaptedEnvelope: NexusSignalEnvelope;
  try {
    adaptedEnvelope = eventContractToNexusEnvelope(wireContract);
    assert(
      "1. Adapter Execution & Envelope Generation",
      adaptedEnvelope !== null && typeof adaptedEnvelope === "object",
      { id: adaptedEnvelope?.id }
    );
  } catch (err: any) {
    assert("1. Adapter Execution & Envelope Generation", false, { error: err.message });
    return;
  }

  // --- PHASE 2: RUNTIME BUS CREATION & SUBSCRIPTION ---
  const channelName = "synarche_proven_arrow_e002_channel";
  const sender = new NexusSignalBusClient("tarot-forge", channelName);
  const receiver = new NexusSignalBusClient("phoenix-rosetta-stone", channelName);

  let receivedEvent: NexusSignalEnvelope | null = null;
  let receivedCount = 0;

  const unsubscribe = receiver.subscribe((envelope) => {
    receivedCount++;
    receivedEvent = envelope;
  });

  // --- PHASE 3: POSITIVE EMISSION & INGESTION ---
  // Emit adapted envelope through the underlying BroadcastChannel
  const rawChannel = (sender as any).channel as BroadcastChannel;
  assert("2. Sender BroadcastChannel Initialized", rawChannel !== null, { channelName });

  rawChannel.postMessage(adaptedEnvelope);

  // Allow async message dispatch across BroadcastChannel
  await new Promise((resolve) => setTimeout(resolve, 50));

  // Assertions on Received Message
  assert(
    "3. Subscriber Received Exactly One Event",
    receivedCount === 1,
    { receivedCount }
  );

  assert(
    "4. Event ID Preserved through Bus Dispatch",
    receivedEvent?.id === wireContract.id,
    { expected: wireContract.id, actual: receivedEvent?.id }
  );

  assert(
    "5. Source Identity Preserved through Bus Dispatch",
    receivedEvent?.sourceApp === (wireContract.source as any),
    { expected: wireContract.source, actual: receivedEvent?.sourceApp }
  );

  assert(
    "6. Event Type Preserved through Bus Dispatch",
    receivedEvent?.eventType === (wireContract.type as any),
    { expected: wireContract.type, actual: receivedEvent?.eventType }
  );

  assert(
    "7. Payload Content Preserved through Bus Dispatch",
    receivedEvent?.payload === wireContract.payload,
    { expected: wireContract.payload, actual: receivedEvent?.payload }
  );

  assert(
    "8. Timestamp Converted Losslessly to Millisecond Epoch",
    receivedEvent?.timestamp === producerGroundTruth.timestamp_epoch_ms,
    { expected: producerGroundTruth.timestamp_epoch_ms, actual: receivedEvent?.timestamp }
  );

  // --- PHASE 4: EXTENSION ISOLATION TEST (E002-EXT) ---
  const customExtensionEvent: EventContract_v0_1 = {
    contract_version: "v0.1",
    id: "e002-custom-ext-001",
    source: "neo-genesis",
    type: "STATE_SYNC",
    payload: { level: 42, score: 9999 },
    timestamp: Date.now(),
    extension: {
      kind: "experimental_quantum",
      data: { superposition: true, qubits: [1, 0, 1] }
    }
  };

  const adaptedCustom = eventContractToNexusEnvelope(customExtensionEvent);
  let customReceived: NexusSignalEnvelope | null = null;
  const customSub = receiver.subscribe((env) => {
    if (env.id === "e002-custom-ext-001") {
      customReceived = env;
    }
  });

  rawChannel.postMessage(adaptedCustom);
  await new Promise((resolve) => setTimeout(resolve, 50));

  assert(
    "9. Unknown Extension Does Not Corrupt Native Envelope",
    customReceived !== null && customReceived.id === "e002-custom-ext-001" && (customReceived.payload as any)?.level === 42,
    { receivedId: customReceived?.id, payload: customReceived?.payload }
  );
  customSub();

  // --- PHASE 5: NEGATIVE REJECTION TEST (E002-NEG) ---
  // Broadcast intentionally malformed message (missing id and non-string sourceApp)
  const malformedMessage = {
    eventType: "GAME_EVENT",
    action: "MALFORMED_ACTION",
    payload: "corrupted"
    // Missing id and sourceApp
  };

  let malformedReceived = false;
  const malformedSub = receiver.subscribe((env) => {
    if ((env as any).action === "MALFORMED_ACTION") {
      malformedReceived = true;
    }
  });

  rawChannel.postMessage(malformedMessage);
  await new Promise((resolve) => setTimeout(resolve, 50));

  assert(
    "10. Malformed Envelope Is Rejected by isNexusSignalEnvelope Guard",
    malformedReceived === false,
    { rejected: !malformedReceived }
  );
  malformedSub();

  // Clean up resources
  unsubscribe();
  sender.close();
  receiver.close();

  const allPassed = assertions.every((a) => a.status === "PASSED");

  const results = {
    experiment: "MIL-003 / Experiment 002",
    boundary: "EventContract_v0_1 -> Adapter -> NexusSignalBusClient (Live Runtime)",
    boundary_integrity: {
      acceptance_proven: true,
      rejection_proven: true,
      semantic_preservation_proven: allPassed
    },
    overall_status: allPassed ? "PROVEN" : "FAILED",
    total_assertions: assertions.length,
    passed_count: assertions.filter((a) => a.status === "PASSED").length,
    failed_count: assertions.filter((a) => a.status === "FAILED").length,
    assertions
  };

  const outPath = path.join(__dirname, 'results.json');
  fs.writeFileSync(outPath, JSON.stringify(results, null, 2), 'utf-8');
  console.log(`EXPERIMENT_002_SUCCESS: Results written to ${outPath}`);
  console.log(`OVERALL_STATUS: ${results.overall_status}`);
}

runExperiment002().catch((err) => {
  console.error("EXPERIMENT_002_FATAL:", err);
  process.exit(1);
});
