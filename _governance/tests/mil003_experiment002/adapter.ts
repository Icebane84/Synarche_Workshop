/**
 * GVRN.TEST.MIL003.EXP002.ADAPTER
 * Version: v15.0 [OMEGA]
 * Domain: GVRN-TEST
 * 
 * Test-Side Translation Adapter:
 * Maps EventContract_v0_1 instances into native NexusSignalEnvelope instances.
 * NOTE: Resides strictly within test harness; zero production code modified.
 */

import type { NexusSignalEnvelope, NexusAppIdentifier, NexusEventType } from "../../../packages/nexus-signalbus/src/types.ts";

export interface EventContract_v0_1<TPayload = unknown> {
  readonly contract_version: "v0.1";
  id: string;
  source: string;
  type: string;
  payload: TPayload;
  timestamp: string | number;
  extension?: 
    | { kind: "cognitive"; data: Record<string, any> }
    | { kind: "signal"; data: { action: string; sourceApp?: string } }
    | { kind: string; data: any };
}

export function eventContractToNexusEnvelope<T = any>(
  event: EventContract_v0_1<T>
): NexusSignalEnvelope<T> {
  // 1. Explicit Timestamp Normalization (ISO String or numeric -> epoch ms)
  const timestampMs = typeof event.timestamp === 'number'
    ? event.timestamp
    : new Date(event.timestamp).getTime();

  // 2. Explicit Source Identity Mapping
  let sourceApp: NexusAppIdentifier = "unknown";
  if (event.extension?.kind === "signal" && event.extension.data?.sourceApp) {
    sourceApp = event.extension.data.sourceApp as NexusAppIdentifier;
  } else if (typeof event.source === "string" && event.source.length > 0) {
    sourceApp = event.source as NexusAppIdentifier;
  }

  // 3. Explicit Action Mapping
  let action = event.type;
  if (event.extension?.kind === "signal" && event.extension.data?.action) {
    action = event.extension.data.action;
  }

  // 4. Construct Native NexusSignalEnvelope
  return {
    id: event.id,
    sourceApp,
    eventType: event.type as NexusEventType,
    action,
    payload: event.payload as T,
    timestamp: timestampMs,
  };
}
