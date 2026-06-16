/*
artifact_anchor:
  id: CORE.VALIDATION.MIDDLEWARE.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

/**
 * artifact_anchor:
 * - id: UMB-QB-VAL-MW-001
 * - type: MIDDLEWARE
 */
import { LoomError } from "@utils/LoomError";
import { NextFunction, Request, Response } from "express";
import { ZodError, ZodObject } from "zod";

/**
 * The NIM Gatekeeper: Validates incoming payloads against a Zod schema.
 * Triggers a NIM_VALIDATION_FAILED LoomError on failure.
 */
export const validatePayload = (schema: ZodObject<any>) => {
    return async (req: Request, res: Response, next: NextFunction) => {
        try {
            // parseAsync strips unknown fields and validates the payload
            req.body = await schema.parseAsync(req.body);
            next(); // Payload is pristine, proceed to the controller
        } catch (error) {
            if (error instanceof ZodError) {
                next(
                    new LoomError(
                        "Invalid request payload detected by the Noetic Immune System.",
                        "NIM_VALIDATION_FAILED",
                        400, // Bad Request
                        true, // Operational error (expected)
                        error.format(), // Expose Zod's detailed field errors
                    ),
                );
            } else {
                next(error); // Pass completely unknown errors down the chain
            }
        }
    };
};
