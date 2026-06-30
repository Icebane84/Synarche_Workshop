import { CommandDefinitionGUCAv5 } from '@essence/codex';
import { registerCommandHandler } from '@system/commandDispatcher';
import * as protocol from './definitions/protocolCommands';
import * as artifacts from './definitions/artifactCommands';
import * as system from './definitions/systemCommands';
import * as tasks from './definitions/taskCommands';
import * as audit from './definitions/auditCommands';
import * as utility from './definitions/utilityCommands';
import * as axiom from './definitions/axiomCommands';

// Import Handlers
import { handleArtifactCommand } from './artifactCommands';
import { handleCloudCommand } from './cloudCommands';
import { handleFileSystemCommand } from './fileSystemCommands';
import { handleMemoryCommand } from './memoryCommands';
import { handleSystemCommand } from './systemCommands';
import { handleTaskCommand } from './taskCommands';
import { handleUtilityCommand } from './utilityCommands';
import { handleAuditCommand } from './auditCommands';

/**
 * @fileoverview Aggregator for all modular GUCA command definitions.
 * This file maintains the unified commandRegistry for the system
 * and handles dispatcher registration.
 */

// Register all handlers with the system dispatcher
registerCommandHandler(handleMemoryCommand);
registerCommandHandler(handleCloudCommand);
registerCommandHandler(handleFileSystemCommand);
registerCommandHandler(handleSystemCommand);
registerCommandHandler(handleArtifactCommand);
registerCommandHandler(handleTaskCommand);
registerCommandHandler(handleUtilityCommand);
registerCommandHandler(handleAuditCommand);

export { commandRegistry } from './registry';

// Export individual commands for direct access if needed
export * from './definitions/protocolCommands';
export * from './definitions/artifactCommands';
export * from './definitions/systemCommands';
export * from './definitions/taskCommands';
export * from './definitions/auditCommands';
export * from './definitions/utilityCommands';
export * from './definitions/axiomCommands';


