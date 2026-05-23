/**
 * artifact_anchor:
 * - id: UMB-QB-WCS-001
 * - type: STRATEGY
 */
import { CASTS_Strategy } from "@nexus/PhoenixSuperpositionEngine";
import { z } from "zod";

// 1. The NIM Gate: Define the EXACT shape of the messy external JSON.
// We strip away everything we don't explicitly allow.
const WebClientSchema = z.object({
    uiElement: z.string().min(1, "UI Element identifier is required"),
    action: z.enum(["CLICK", "SUBMIT", "HOVER", "NAVIGATE"]),
    textData: z.string().optional(),
    clientTime: z.string().datetime().optional(), // Must be a valid ISO Date string if present
});

// 2. The Core Domain: Define the pristine internal shape the system expects.
export interface WebCommand {
    element: string;
    actionType: "CLICK" | "SUBMIT" | "HOVER" | "NAVIGATE";
    payload: string | null;
    timestamp: Date; // Note: We want a real JS Date object here, not a string!
}

// 3. CASTS Transmutation: The bridge between the Schema and the Domain.
export const WebClientStrategy: CASTS_Strategy<WebCommand> = {
    strategyName: "WebClientTransmutationStrategy",
    schema: WebClientSchema,
    transmute: (parsed) => ({
        element: parsed.uiElement,
        actionType: parsed.action,
        payload: parsed.textData || null, // Normalize undefined to null
        timestamp: parsed.clientTime ? new Date(parsed.clientTime) : new Date(), // Type transformation!
    }),
};
