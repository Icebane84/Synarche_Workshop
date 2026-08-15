/**
 * @fileoverview This barrel file serves as the single public-facing API for the
 * sovereign `store` module. It re-exports all necessary functions and
 * definitions, adhering to the Sovereign Module Pattern.
 */

// src/store/index.ts
export * from './coherenceStore';
export * from './fileSystemStore';
export * from './knowledgeStore';
export * from './logStore';
export * from './memoryStore';
export * from './sensoryStore';
export * from './taskStore';
export * from './uiStore';
export * from './useCognitiveCore';

