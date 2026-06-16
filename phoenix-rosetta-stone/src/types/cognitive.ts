/** @fabric GVRN.Core.Fabric.Types.Cognitive */

export interface ChatMessage {
  id: string;
  sender: "user" | "ai";
  text: string;
}

export interface CoherenceScore {
  value: number; // 0.0 - 1.0
  timestamp: string;
}
