import { NexusAppIdentifier, NexusEventType, NexusSignalEnvelope, NexusSignalListener } from "./types";

export class NexusSignalBusClient {
  private channelName: string;
  private appIdentifier: NexusAppIdentifier;
  private channel: BroadcastChannel | null = null;
  private listeners: Set<NexusSignalListener> = new Set();

  constructor(appIdentifier: NexusAppIdentifier, channelName = "synarche_nexus_bus") {
    this.appIdentifier = appIdentifier;
    this.channelName = channelName;

    if (typeof window !== "undefined" && "BroadcastChannel" in window) {
      this.channel = new BroadcastChannel(this.channelName);
      this.channel.onmessage = (event: MessageEvent<NexusSignalEnvelope>) => {
        if (event.data && event.data.id) {
          this.listeners.forEach((listener) => listener(event.data));
        }
      };
    }
  }

  public emit<T = Record<string, any>>(eventType: NexusEventType, action: string, payload: T): NexusSignalEnvelope<T> {
    const envelope: NexusSignalEnvelope<T> = {
      id: `sig_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
      sourceApp: this.appIdentifier,
      eventType,
      action,
      payload,
      timestamp: Date.now(),
    };

    if (this.channel) {
      this.channel.postMessage(envelope);
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
