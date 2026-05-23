import { z } from "zod";

// ----------------------------------------------------------------------------
// 1. CONTEXT VECTOR DEFINITIONS (Environmental States)
// ----------------------------------------------------------------------------
const ContextEnvironmentSchema = z.enum(["ENV_PROD", "ENV_DEV", "ENV_TEST"]);
const ContextClientSchema = z.enum([
  "CLIENT_WEB",
  "CLIENT_ENGINE",
  "CLIENT_CLI",
]);
const ContextAuthSchema = z.enum([
  "AUTH_VERIFIED",
  "AUTH_GUEST",
  "AUTH_SYSTEM",
]);

const ContextVectorSchema = z
  .array(
    z.union([ContextEnvironmentSchema, ContextClientSchema, ContextAuthSchema]),
  )
  .min(1, { message: "ContextVector must contain at least one state flag." });

// ----------------------------------------------------------------------------
// 2. POLYGLOT PAYLOAD SCHEMAS (The Transformation Strategies)
// ----------------------------------------------------------------------------

// Strategy A: Web UI Interaction Payload
const WebPayloadSchema = z.object({
  type: z.literal("WEB_ACTION"),
  componentId: z.string(),
  action: z.string(),
  parameters: z.record(z.unknown()).optional(), // Flexible props for UI
});

// Strategy B: Godot 4.3 Engine Telemetry Payload
const EnginePayloadSchema = z.object({
  type: z.literal("ENGINE_TELEMETRY"),
  entityId: z.string(),
  velocity: z.tuple([z.number(), z.number(), z.number()]), // 3D Vector Logic
  activeState: z.string(),
});

// Strategy C: System CLI / Axiom Terminal Command
const AxiomCommandSchema = z.object({
  type: z.literal("AXIOM_COMMAND"),
  commandString: z.string(),
  overrideLevel: z.number().int().min(0).max(5),
});

// ----------------------------------------------------------------------------
// 3. THE QUANTUM BLOCK (Superposition Container)
// ----------------------------------------------------------------------------
export const QuantumBlockInputSchema = z.object({
  BlockID: z.string().uuid({ message: "BlockID must be a valid UUID v4." }),
  ContextVector: ContextVectorSchema,
  RawPayload: z.discriminatedUnion("type", [
    WebPayloadSchema,
    EnginePayloadSchema,
    AxiomCommandSchema,
  ]),
});

// ----------------------------------------------------------------------------
// 4. INSTANTIATION: COMPILE-TIME TYPE EXTRACTION
// ----------------------------------------------------------------------------
export type QuantumBlockInput = z.infer<typeof QuantumBlockInputSchema>;
export type ContextVector = z.infer<typeof ContextVectorSchema>;
export type WebPayload = z.infer<typeof WebPayloadSchema>;
export type EnginePayload = z.infer<typeof EnginePayloadSchema>;
export type AxiomCommand = z.infer<typeof AxiomCommandSchema>;
