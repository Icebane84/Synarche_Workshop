/*
artifact_anchor:
  id: CORE.SCHEMAS.001
  version: v15.0 [OMEGA]
  provenance: '2026-05-27'
  domain: CORE
  celestial_class: STAR
  tier: LOGIC
  state: ACTIVE
  ethos: SOVEREIGN_LOGIC_COMPONENT
  relations: []
*/
/** biome-ignore-all lint/style/useNamingConvention:false */

import * as standards from "@governance/13_Standardization/GVRN.Standards.json";
import type { MetadataSchema } from "@utils/validation";

/**
 * Sovereign ID Regex: Supports legacy IDs (PRS-001) and OMEGA v15.0 standards (DOMAIN.TYPE.CLASS.SUBSYSTEM.DESCRIPTOR)
 * Pulled from GVRN.Standards.json
 */
export const SOVEREIGN_ID_REGEX = new RegExp(standards.regex.SOVEREIGN_ID);

/**
 * PRS-001 Rosetta Stone Schema
 * Defines the structural requirements for the master knowledge graph.
 */
export const PRS_001_SCHEMA: MetadataSchema = {
  required: ["artifact_id", "official_name", "version", "cognitive_loom"],
  types: {
    artifact_id: "string",
    official_name: "string",
    version: "string",
    cognitive_loom: {
      nodes: "object", // The current validator treats arrays as objects
    },
  },
  formats: {
    // artifact_id format check (if using the global regex)
    artifact_id: SOVEREIGN_ID_REGEX,
  },
};
