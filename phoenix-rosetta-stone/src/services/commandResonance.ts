import { CommandDefinitionGUCAv5 } from '@essence/codex';
import { CognitiveFocus, ScoredCommand, CommandUsage } from '@essence/types';
import { commandRegistry } from './commands';

const RESONANCE_STORAGE_KEY = 'phoenix_command_resonance';
// Decay factor means a command's recency score halves in about 3 days.
const RECENCY_DECAY_MS = 3 * 24 * 60 * 60 * 1000;

type ResonanceData = Record<string, CommandUsage | undefined>;

const getResonanceData = (): ResonanceData => {
  try {
    const data = localStorage.getItem(RESONANCE_STORAGE_KEY);
    return data ? (JSON.parse(data) as ResonanceData) : {};
  } catch (error) {
    console.error("Failed to parse resonance data from localStorage", error);
    return {};
  }
};

const saveResonanceData = (data: ResonanceData) => {
  try {
    localStorage.setItem(RESONANCE_STORAGE_KEY, JSON.stringify(data));
  } catch (error) {
    console.error("Failed to save resonance data to localStorage", error);
  }
};

export const trackCommandExecution = (commandId: string): void => {
  const data = getResonanceData();
  const existing = data[commandId] ?? { count: 0, lastUsed: 0 };
  data[commandId] = {
    count: existing.count + 1,
    lastUsed: Date.now(),
  };
  saveResonanceData(data);
};

const calculateScore = (usage: CommandUsage): number => {
  const timeSinceUsed = Date.now() - usage.lastUsed;
  // Recency score decays exponentially.
  const recencyScore = Math.exp(-timeSinceUsed / RECENCY_DECAY_MS);
  // Frequency score is logarithmic to prevent one command from dominating forever.
  const frequencyScore = Math.log10(usage.count + 1);
  // Combine scores, giving slightly more weight to what's been done recently.
  return (frequencyScore * 0.8) + (recencyScore * 1.2);
};

export const getResonantCommands = (
  allCommands: CommandDefinitionGUCAv5[],
  limit: number
): CommandDefinitionGUCAv5[] => {
  const data = getResonanceData();
  const scoredCommands = Object.keys(data)
    .map(commandId => {
      const usage = data[commandId];
      const command = allCommands.find(c => c.commandId === commandId);
      if (!command || !usage) return null;
      return {
        command,
        score: calculateScore(usage),
      };
    })
    .filter(Boolean) as { command: CommandDefinitionGUCAv5, score: number }[];

  scoredCommands.sort((a, b) => b.score - a.score);

  return scoredCommands.slice(0, limit).map(item => item.command);
};

export const getResonanceState = (): ScoredCommand[] => {
    const data: ResonanceData = getResonanceData();
    const allCommands = Object.values(commandRegistry);
    
    const scoredCommands = allCommands.map(command => {
        const usage = data[command.commandId] ?? null;
        const score = usage ? calculateScore(usage) : 0;
        return { command, score, usage };
    });

    return scoredCommands.sort((a, b) => b.score - a.score);
};

export const clearResonanceData = (): void => {
  try {
    localStorage.removeItem(RESONANCE_STORAGE_KEY);
  } catch (error) {
    console.error("Failed to clear resonance data from localStorage", error);
  }
};


// --- Cognitive Echo Logic ---

// Mapping of paths to relevant command IDs
export const pathCommandMap: Partial<Record<string, string[]>> = {
  '/': ['CMD_SCAN_FOR_DISSONANCE'],
  '/visualizer': ['CMD_ANALYZE_ARTIFACT_SYNERGY'],
  '/synergy-simulator': ['CMD_SIMULATE_SYNERGY'],
  '/loom': ['CMD_SCAN_FOR_DISSONANCE'],
};

// Mapping of cognitive focus to relevant command IDs
export const focusCommandMap: Partial<Record<CognitiveFocus, string[]>> = {
  'Security Audit': ['CMD_SCAN_FOR_DISSONANCE'],
  'Creative Ideation': ['CMD_SIMULATE_SYNERGY'],
};

/**
 * Determines contextually relevant "Cognitive Echo" commands based on the
 * user's current location and the AI's cognitive focus.
 *
 * @param pathname The current URL pathname from React Router.
 * @param focus The current CognitiveFocus from the coherence store.
 * @returns An array of command IDs that should be surfaced as suggestions.
 */
export const getEchoCommands = (pathname: string, focus: CognitiveFocus): string[] => {
  const echoIds = new Set<string>();

  // Add commands based on the current path
  if (pathCommandMap[pathname]) {
    pathCommandMap[pathname].forEach(id => echoIds.add(id));
  }

  // Add commands based on the cognitive focus
  if (focusCommandMap[focus]) {
    focusCommandMap[focus].forEach(id => echoIds.add(id));
  }

  return Array.from(echoIds);
};


