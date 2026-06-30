/**
 * @relations
 * REF: systemCommands.ts
 */
import { useState, useMemo, useEffect } from "react";
import { useCognitiveCore } from "@state/useCognitiveCore";
import { NexusSignalBusClient } from "@synarche/nexus-signalbus";

export interface CommandParameter {
  name: string;
  type: "string" | "number" | "boolean";
  description: string;
  defaultValue?: any;
}

export interface CommandDefinition {
  commandId: string;
  description: string;
  parameters: CommandParameter[];
  category: "Core" | "Epistemic" | "Security";
}

export interface DispatchResult {
  success: boolean;
  message: string;
  data?: any;
}

export const COMMAND_REGISTRY: Record<string, CommandDefinition> = {
  CMD_COHERENCE_BOOST: {
    commandId: "CMD_COHERENCE_BOOST",
    description: "Inject kinetic energy to restore system coherence.",
    parameters: [
      { name: "amount", type: "number", description: "Boost intensity (0.01 - 0.50)", defaultValue: 0.1 }
    ],
    category: "Core",
  },
  CMD_COHERENCE_DRAIN: {
    commandId: "CMD_COHERENCE_DRAIN",
    description: "Simulate cognitive strain to drain system coherence.",
    parameters: [
      { name: "amount", type: "number", description: "Drain intensity (0.01 - 0.50)", defaultValue: 0.1 }
    ],
    category: "Core",
  },
  CMD_CLEAR_TRANSCRIPT: {
    commandId: "CMD_CLEAR_TRANSCRIPT",
    description: "Erase local dialogue logs and rebuild consciousness.",
    parameters: [],
    category: "Epistemic",
  },
  CMD_SYSTEM_AUDIT: {
    commandId: "CMD_SYSTEM_AUDIT",
    description: "Verify zero-entropy compliance and integrity of memory palace.",
    parameters: [],
    category: "Security",
  },
};

interface UseSynapseLogicOptions {
  onClose: () => void;
  onSuccess?: (msg: string) => void;
}

export const useSynapseLogic = ({ onClose, onSuccess }: UseSynapseLogicOptions) => {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [commandForParams, setCommandForParams] = useState<CommandDefinition | null>(null);
  const [isFiring, setIsFiring] = useState(false);
  const [commandResult, setCommandResult] = useState<DispatchResult | null>(null);

  const cognitiveCore = useCognitiveCore();

  // Instantiate Nexus Signal Bus client
  const bus = useMemo(() => new NexusSignalBusClient("phoenix-rosetta-stone"), []);

  useEffect(() => {
    return () => {
      bus.close();
    };
  }, [bus]);

  const commands = useMemo(() => Object.values(COMMAND_REGISTRY), []);

  const filteredCommands = useMemo(() => {
    if (!searchQuery) return commands;
    const q = searchQuery.toLowerCase();
    return commands.filter(
      (cmd) =>
        cmd.commandId.toLowerCase().includes(q) ||
        cmd.description.toLowerCase().includes(q)
    );
  }, [searchQuery, commands]);

  // Reset indices on search query change
  useEffect(() => {
    setSelectedIndex(0);
  }, [searchQuery]);

  const executeCommand = async (command: CommandDefinition, params: Record<string, any>) => {
    setIsFiring(true);
    
    // Artificial synthesis delay
    await new Promise((resolve) => setTimeout(resolve, 800));

    let result: DispatchResult = { success: true, message: "Directive manifested successfully." };

    try {
      switch (command.commandId) {
        case "CMD_COHERENCE_BOOST": {
          const val = Number(params.amount ?? 0.1);
          cognitiveCore.updateCoherence(Math.min(1.0, cognitiveCore.coherenceIndex + val));
          result.message = `Cognitive coherence boosted by ${(val * 100).toFixed(0)}%.`;
          break;
        }
        case "CMD_COHERENCE_DRAIN": {
          const val = Number(params.amount ?? 0.1);
          cognitiveCore.updateCoherence(Math.max(0.0, cognitiveCore.coherenceIndex - val));
          result.message = `Cognitive strain induced. Coherence drained by ${(val * 100).toFixed(0)}%.`;
          break;
        }
        case "CMD_CLEAR_TRANSCRIPT": {
          cognitiveCore.resetConsciousness();
          result.message = "Consciousness cleared. All dialogue buffers purged.";
          break;
        }
        case "CMD_SYSTEM_AUDIT": {
          const status = cognitiveCore.coherenceIndex > 0.7 ? "PASS" : "WARN";
          result.message = `System Audit Complete. Codebase nominal. Coherence verification: ${status} (${(cognitiveCore.coherenceIndex * 100).toFixed(0)}% resonance).`;
          break;
        }
        default:
          result = { success: false, message: "Directive unrecognized by Synapse." };
      }
    } catch (e: any) {
      result = { success: false, message: e.message || "Execution error." };
    }

    // Emit state sync to the shared Nexus Signal Bus
    if (result.success) {
      bus.emit("STATE_SYNC", command.commandId, {
        coherenceIndex: useCognitiveCore.getState().coherenceIndex,
        message: result.message,
      });
    }

    setIsFiring(false);
    setCommandResult(result);
    if (result.success && onSuccess) {
      onSuccess(result.message);
    }
  };

  const handleSelectCommand = (command: CommandDefinition) => {
    if (command.parameters.length > 0) {
      setCommandForParams(command);
    } else {
      void executeCommand(command, {});
    }
  };

  const resetState = () => {
    setSearchQuery("");
    setSelectedIndex(0);
    setCommandForParams(null);
    setCommandResult(null);
    setIsFiring(false);
  };

  return {
    searchQuery,
    setSearchQuery,
    selectedIndex,
    setSelectedIndex,
    commandForParams,
    setCommandForParams,
    isFiring,
    commandResult,
    filteredCommands,
    executeCommand,
    handleSelectCommand,
    resetState,
  };
};
