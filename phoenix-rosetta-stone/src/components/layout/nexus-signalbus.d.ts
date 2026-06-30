/**
 * Type definitions for the @synarche/nexus-signalbus package.
 * This file provides TypeScript with the necessary type information for this
 * local JavaScript module, resolving TS2307 errors.
 */
declare module "@synarche/nexus-signalbus" {
  /**
   * The envelope for signals transmitted over the Nexus SignalBus.
   */
  export interface NexusSignalEnvelope<T = Record<string, any>> {
    sourceApp: string;
    action: string;
    payload: T;
  }

  export interface AscendEraPayload {
    nextStage: string;
  }

  export interface ColonizePlanetPayload {
    planetName: string;
  }

  export interface MissionCompletePayload {
    missionName: string;
    xpReward: number;
  }

  export class NexusSignalBusClient {
    constructor(appName: string);
    subscribe(callback: (signal: NexusSignalEnvelope) => void): () => void;
    close(): void;
  }
}
