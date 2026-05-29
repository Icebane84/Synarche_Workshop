/*
artifact_anchor:
  id: CORE.COMMAND.ROUTES.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/

// src/routes/command.routes.ts
/**
 * artifact_anchor:
 * - id: UMB-QB-RT-001
 * - type: ROUTE
 */
import { NexusCoordinator } from "@nexus/NexusCoordinator";
import { Router } from "express";

const router = Router();

// Notice how clean the route is! No messy try/catch or if/else validation blocks here. All handled by the NexusCoordinator.
router.post("/execute", NexusCoordinator.handleClientCommand);

export default router;
/**
 * [OMNI-ARTIFACT-ANCHOR] ID: UMB-QB-RT-002 VER: v1.0.0 STATUS: ACTIVE
 * Objective: Health check and telemetry endpoint for the Nexus Coordinator.
 */
router.get("/status", (req, res) => {
    res.status(200).json({
        status: "ACTIVE",
        engine: "Phoenix Superposition Engine",
        timestamp: new Date().toISOString(),
        integrity: "COHERENT",
    });
});
