
/**
 * @fileoverview This barrel file serves as the single public-facing API for the
 * sovereign `services` module. It re-exports all necessary functions and
 * definitions, adhering to the Sovereign Module Pattern.
 */

export { 
  analyzeSynergyCommand, 
  scanForDissonanceCommand, 
  simulateSynergyCommand, 
  beginClcCommand, 
  logTaskToLoomCommand, 
  executeDirectiveCommand,
  systemRecalibrationCommand,
  getSystemStateCommand,
  fetchTasksCommand,
  systemHelpCommand,
  initiateAutoRepairCommand,
  viewTaskDetailsCommand,
  connectLocalFsCommand,
  scanLocalProjectCommand,
  testBackendHandshakeCommand,
  fetchArtifactMetadataCommand,
  fetchAllArtifactsCommand
} from './commands';
export {
  commandRegistry
} from './commands';
export { dispatchCommand } from '../system/commandDispatcher';
export { queryCognitiveCore, interpretNaturalLanguageCommand, searchWithCognitiveCore } from './gemini';
export { 
  trackCommandExecution,
  getResonantCommands,
  getEchoCommands,
  getResonanceState,
  clearResonanceData,
  pathCommandMap,
  focusCommandMap
} from './commandResonance';
export { supabase } from './supabaseClient';
export { generateAndPersistLog } from './seltGenerator';
export { useLogStore } from '../store/logStore';
export { retrieveContext } from './vectorStore';
export { transmitAuralResponse } from './audioService';
export { executeRemCycle } from './dreamService';
export { fetchEnvironmentalData, getSystemTime } from './sensoryService';
export { 
  signalBus,
  SignalType
} from '../system/signalBus';
export type { SignalData } from '../system/signalBus';

export { openDirectoryPicker, scanDirectoryRecursively } from './fileSystemService';
export { useFileSystemStore } from '../store/fileSystemStore';
