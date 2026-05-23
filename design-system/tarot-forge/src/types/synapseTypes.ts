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
    type: "string" | "number" | "boolean" | "string[]";
    description: string;
    required: boolean;
    uiHint?: "artifact" | "textarea";
  }[];
  action: string; // Describes the command's function
  aliases?: string[];
}

export interface DispatchResult {
  success: boolean;
  message: string;
  data?: Record<string, unknown>;
}

export interface CoherenceDissonance {
  id: `DISS-${string}`;
  type: string;
  description: string;
  sourceArtifacts: string[];
  severity: "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";
  timestamp: number;
}

interface TarotCardMetadata {
  id: string;
  name: string;
  number: number;
  keywords: string[];
  archetype: string;
  suits: string[];
  astrology: string | null;
  mythology: string | null;
}

interface TarotCardBody {
  imagery: string;
  symbolism: string;
  storytelling: string;
  shadow_aspect: string;
  modern_application: string;
}

interface TarotCardEntry {
  metadata: TarotCardMetadata;
  body: TarotCardBody;
  [key: string]: any;
}

interface TarotForgeContext {
  deck: TarotCardEntry[];
  loadDeck: (path: string) => Promise<void>;
  saveCard: (card: TarotCardEntry) => Promise<void>;
  manifestCard: (
    name: string,
    number: number,
    concept: string,
  ) => Promise<TarotCardEntry>;
}
