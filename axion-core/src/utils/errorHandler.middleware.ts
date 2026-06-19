/*
/*
artifact_anchor:
  id: CORE.ERRORHANDLER.MIDDLEWARE.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

import { captureException } from "@sentry/node";
import { PhoenixLogger } from "@system/logging";
import { LoomError } from "@utils/LoomError";
import type { NextFunction, Request, Response } from "express";

/**
 * Global Error Handler: Normalizes all errors into LoomErrors,
 * reports fatal anomalies to Sentry, and formats the client response.
 */
export const errorHandler = (
  err: unknown,
  req: Request,
  res: Response,
  // NextFunction must be included in the signature for Express to recognize this as an error handler
  next: NextFunction,
) => {
  // 1. Normalize every error using the LoomError factory
  const standardError = LoomError.from(err);

  // 2. Telemetry and Logging (The "Memory" Stream)
  if (!standardError.isOperational) {
    // Fatal Crash: Log locally and send to Sentry
    PhoenixLogger.error("[FATAL ERROR]", standardError.originalError || standardError);

    captureException(standardError.originalError || standardError, {
      extra: {
        loomCode: standardError.code,
        path: req.path,
        method: req.method,
      },
    });
  } else {
    // Expected Rejection (e.g., NIM Validation Failure): Just log a local warning
    PhoenixLogger.info(
      `[NIM Guard] Operational Rejection: ${standardError.code} - ${standardError.message}`,
    );
  }

  // 3. Clean Client Response (Never leak stack traces in production!)
  res.status(standardError.statusCode).json({
    success: false,
    code: standardError.code,
    message: standardError.message,
    ...(process.env.NODE_ENV === "development" && { details: standardError.originalError }),
  });
};
