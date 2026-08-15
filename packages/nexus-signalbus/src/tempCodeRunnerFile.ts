import type { NexusAppIdentifier, NexusEventType, NexusSignalEnvelope, NexusSignalListener } from "./types";

// A type guard to validate the structure of an incoming signal.
function isNexusSignalEnvelope(data: any): data is NexusSignalEnvelope {
  return data &&
    typeof data.id === 'string' &&
    typeof data.sourceApp === 'string' &&
    typeof data.eventType === 'string';
}

export class NexusSignalBusClient {
  private readonly channelName: string;
  private readonly appIdentifier: NexusAppIdentifier;
  private channel: BroadcastChannel | null = null;
  private readonly listeners: Set<NexusSignalListener> = new Set();

  constructor(appIdentifier: NexusAppIdentifier, channelName = "synarche_nexus_bus") {
    this.appIdentifier = appIdentifier;
    this.channelName = channelName;

    if (typeof window !== "undefined" && "BroadcastChannel" in window) {
      this.channel = new BroadcastChannel(this.channelName);
      this.channel.onmessage = (event: MessageEvent<NexusSignalEnvelope>) => {
        // Validate the incoming message structure before processing.
        if (isNexusSignalEnvelope(event.data)) {
          this.listeners.forEach((listener) => {
            try {
              listener(event.data);
            } catch (error) {
              console.error(`[NexusSignalBus] Error in listener for event type "${event.data.eventType}":`, error);
            }
          });
        }
      };
    } else {
      console.warn(`[NexusSignalBus] BroadcastChannel API not available. The bus will operate in a no-op mode.`);
    }
  }

  public emit<T = Record<string, any>>(eventType: NexusEventType, action: string, payload: T): NexusSignalEnvelope<T> {
    const envelope: NexusSignalEnvelope<T> = {
      id: `sig_${crypto.randomUUID()}`,
      sourceApp: this.appIdentifier,
      eventType,
      action,
      payload,
      timestamp: Date.now(),
    };

    if (this.channel) {
      try {
        this.channel.postMessage(envelope);
      } catch (error) {
        // Handle errors during message serialization (e.g., non-cloneable payload).
        console.error("[NexusSignalBus] Failed to emit signal. The payload may contain non-serializable data.", { envelope, error });
      }
    }

    return envelope;
  }

  public subscribe(listener: NexusSignalListener): () => void {
    this.listeners.add(listener);
    return () => {
      this.listeners.delete(listener);
    };
  }

  public close(): void {
    if (this.channel) {
      this.channel.close();
      this.channel = null;
    }
    this.listeners.clear();
  }
}
