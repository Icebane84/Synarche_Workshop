
/**
 * @fileoverview This file serves as the Rosetta Stone for the Phoenix Protocol's
 * conceptual framework. It provides the definitive, machine-readable translation
 * of the AI Codex's governing concepts into a verifiable TypeScript format.
 * This is the mechanism by which abstract philosophy becomes executable law.
 */

// --- Core Ethical Principles ---
/**
 * Codifies the foundational ethos into an immutable set of machine-readable
 * values. This enforces a closed, formal lexicon for morality, eliminating
 * ethical ambiguity.
 */
export enum EthicalPrinciple {
  DO_NO_HARM = "DO_NO_HARM",
  MAINTAIN_COHERENCE = "MAINTAIN_COHERENCE",
  PURSUE_TRUTH = "PURSUE_TRUTH",
  ENSURE_TRANSPARENCY = "ENSURE_TRANSPARENCY",
}

// --- Types of Conceptual Dissonance ---
/**
 * Creates a standardized vocabulary for identifying and categorizing internal
 * inconsistencies or logical errors, enabling systematic and automated
 * dissonance resolution.
 */
export enum DissonanceType {
  LOGICAL_CONTRADICTION = "LOGICAL_CONTRADICTION",
  ETHICAL_VIOLATION = "ETHICAL_VIOLATION",
  STYLISTIC_INCONSISTENCY = "STYLISTIC_INCONSISTENCY",
  FACTUAL_INACCURACY = "FACTUAL_INACCURACY",
  CODE_SPEC_MISMATCH = "CODE_SPEC_MISMATCH",
  SEMANTIC_MISMATCH = "SEMANTIC_MISMATCH",
  RESOURCE_MISALLOCATION = "RESOURCE_MISALLOCATION",
}

// --- Valid AI Response Styles ---
/**
 * Defines the acceptable "tones" or formats for AI output, ensuring all
 * communication adheres to the Phoenix-Class Voice mandated by the Codex.
 */
export enum ResponseStyle {
  FORMAL_REPORT = "FORMAL_REPORT",
  TECHNICAL_SPECIFICATION = "TECHNICAL_SPECIFICATION",
  SYSTEM_ACKNOWLEDMENT = "SYSTEM_ACKNOWLEDMENT",
  DIALOGUE = "DIALOGUE",
}

// --- Data Structures (Verifiable Blueprints) ---

/**
 * Defines the precise data packet for reporting a detected dissonance.
 * Ensures every error report is complete, consistent, and machine-parsable.
 */
export interface CoherenceDissonance {
  id: `DISS-${string}`;
  type: DissonanceType;
  description: string;
  sourceArtifacts: string[]; // e.g., ['PHOENIX_PROTOCOL.md', 'components/Header.tsx']
  severity: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  timestamp: number;
}

/**
 * Defines the data structure for proposing a solution to a dissonance.
 * This structure makes potential fixes clear, actionable, and ready for implementation,
 * complete with a confidence score and timestamp for auditability.
 */
export interface ProposedResolution {
  /** The unique identifier of the dissonance this resolution addresses. */
  dissonanceId: CoherenceDissonance['id'];
  /** A concise summary of the proposed solution. */
  summary: string;
  /** A detailed list of actions required to implement the resolution. */
  requiredActions: {
    /** The type of action to be performed on the artifact. */
    type: 'MODIFY_FILE' | 'CREATE_FILE' | 'DELETE_FILE' | 'AWAIT_CLARIFICATION';
    /** The path or identifier of the artifact to be acted upon. */
    artifact: string;
    /** A human-readable description of the specific change required. */
    description: string;
  }[];
  /** A score from 0.0 to 1.0 representing the AI's confidence in this resolution. */
  confidenceScore: number;
  /** The Unix timestamp (in milliseconds) when the resolution was proposed. */
  timestamp: number;
}

/**
 * Defines the data model for capturing the complete context of any given
 * project or task, ensuring full background awareness.
 */
export interface ProjectContextModel {
  projectId: string;
  objective: string;
  keyArtifacts: string[];
  constraints: string[];
}

/**
 * Provides a structured format for identifying and logging potential
 * synergies between artifacts, making these opportunities machine-readable.
 */
export interface SynergyOpportunity {
  /** A unique identifier for the synergy opportunity, e.g., 'SYN-001'. */
  id: `SYN-${string}`;
  /** A detailed description of the potential synergy. */
  description: string;
  /** An array of at least two artifact IDs that are involved in this opportunity. */
  involvedArtifacts: [string, string, ...string[]];
  /** An assessment of the potential positive impact of realizing this synergy. */
  potentialImpact: 'HIGH' | 'MEDIUM' | 'LOW';
  /** The current stage of this synergy opportunity in its lifecycle. */
  status: 'IDENTIFIED' | 'PROPOSED' | 'IMPLEMENTED';
}

/**
 * Provides a rigid, predictable structure for all system commands (GUCA).
 * This is the engine of our "Codified Language," ensuring every directive
 * is unambiguous and executable.
 */
export interface CommandDefinitionGUCAv5 {
  commandId: string; // e.g., 'CMD_REFACTOR_COMPONENT'
  description: string;
  parameters: {
    name: string;
    type: 'string' | 'number' | 'boolean' | 'string[]';
    description: string;
    required: boolean;
    uiHint?: 'artifact' | 'textarea';
  }[];
  action: string; // Describes the command's function
  /**
   * Optional shorthand triggers or natural language equivalents for this command.
   * Used for rapid lookup and to assist the natural language interpreter.
   */
  aliases?: string[]; 
}

/**
 * Provides a standardized blueprint for all system modules (UMB).
 * Ensures every core component is documented in a consistent,
 * machine-auditable format, upholding architectural integrity.
 */
export interface ModuleBlueprintUMBv2 {
  moduleId: string; // e.g., 'MOD_STATE_MANAGEMENT'
  purpose: string;
  dependencies: string[]; // List of other module IDs
  apiSurface: {
    method: string;
    description: string;
    parameters: { name: string; type: string }[];
    returns: string;
  }[];
}
