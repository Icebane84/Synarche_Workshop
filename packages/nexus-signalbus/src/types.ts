export type NexusAppIdentifier = "neo-genesis" | "phoenix-rosetta-stone" | "tarot-forge" | "unknown";

export type NexusEventType =
  | "GAME_EVENT"
  | "ACHIEVEMENT_UNLOCKED"
  | "STATE_SYNC"
  | "HEARTBEAT";

export interface NexusSignalEnvelope<T = Record<string, any>> {
  id: string;
  sourceApp: NexusAppIdentifier;
  eventType: NexusEventType;
  action: string;
  payload: T;
  timestamp: number;
}

export type NexusSignalListener = (signal: NexusSignalEnvelope) => void;

export interface AscendEraPayload {
  nextStage: string;
}

export interface MissionCompletePayload {
  missionName: string;
  xpReward: number;
}

export interface ColonizePlanetPayload {
  planetName: string;
}

