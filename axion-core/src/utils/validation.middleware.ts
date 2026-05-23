/**
 * artifact_anchor:
 * - id: UMB-QB-VAL-MW-001
 * - type: MIDDLEWARE
 */
import { NextFunction, Request, Response } from "express";
import { ZodError, ZodObject } from "zod";
import { LoomError } from "../utils/LoomError";

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
