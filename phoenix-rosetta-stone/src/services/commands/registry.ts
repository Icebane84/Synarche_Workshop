import { CommandDefinitionGUCAv5 } from '@essence/codex';
import * as protocol from './definitions/protocolCommands';
import * as artifacts from './definitions/artifactCommands';
import * as system from './definitions/systemCommands';
import * as tasks from './definitions/taskCommands';
import * as audit from './definitions/auditCommands';
import * as utility from './definitions/utilityCommands';
import * as axiom from './definitions/axiomCommands';

/**
 * @fileoverview Canonical registry of all GUCA commands.
 * This file contains ONLY data and is safe for import by command handlers.
 */

export const commandRegistry: Record<string, CommandDefinitionGUCAv5> = {
    // Protocol Commands
    [protocol.syncProtocolLibraryCommand.commandId]: protocol.syncProtocolLibraryCommand,
    [protocol.invokeCloudFunctionCommand.commandId]: protocol.invokeCloudFunctionCommand,
    [protocol.indexKnowledgeCommand.commandId]: protocol.indexKnowledgeCommand,
    [protocol.migrateTasksCommand.commandId]: protocol.migrateTasksCommand,

    // Artifact Commands
    [artifacts.analyzeSynergyCommand.commandId]: artifacts.analyzeSynergyCommand,
    [artifacts.fetchArtifactMetadataCommand.commandId]: artifacts.fetchArtifactMetadataCommand,
    [artifacts.fetchAllArtifactsCommand.commandId]: artifacts.fetchAllArtifactsCommand,
    [artifacts.simulateSynergyCommand.commandId]: artifacts.simulateSynergyCommand,

    // System Commands
    [system.deepDiagnosticCommand.commandId]: system.deepDiagnosticCommand,
    [system.systemRecalibrationCommand.commandId]: system.systemRecalibrationCommand,
    [system.getSystemStateCommand.commandId]: system.getSystemStateCommand,
    [system.systemHelpCommand.commandId]: system.systemHelpCommand,
    [system.seedCodebaseGraphCommand.commandId]: system.seedCodebaseGraphCommand,

    // Task Commands
    [tasks.logTaskToLoomCommand.commandId]: tasks.logTaskToLoomCommand,
    [tasks.fetchTasksCommand.commandId]: tasks.fetchTasksCommand,
    [tasks.viewTaskDetailsCommand.commandId]: tasks.viewTaskDetailsCommand,
    [tasks.resolveDissonanceCommand.commandId]: tasks.resolveDissonanceCommand,

    // Audit Commands
    [audit.scanForDissonanceCommand.commandId]: audit.scanForDissonanceCommand,
    [audit.harmonyScanCommand.commandId]: audit.harmonyScanCommand,
    [audit.scanLocalProjectCommand.commandId]: audit.scanLocalProjectCommand,
    [audit.runLintCommand.commandId]: audit.runLintCommand,

    // Utility Commands
    [utility.beginClcCommand.commandId]: utility.beginClcCommand,
    [utility.executeDirectiveCommand.commandId]: utility.executeDirectiveCommand,
    [utility.initiateAutoRepairCommand.commandId]: utility.initiateAutoRepairCommand,
    [utility.applyFixCommand.commandId]: utility.applyFixCommand,
    [utility.readFileCommand.commandId]: utility.readFileCommand,
    [utility.syncSkillSeltCommand.commandId]: utility.syncSkillSeltCommand,
    [system.connectLocalFsCommand.commandId]: system.connectLocalFsCommand,

    // Axiom Commands
    [axiom.axiomRememberCommand.commandId]: axiom.axiomRememberCommand,
    [axiom.axiomRecallCommand.commandId]: axiom.axiomRecallCommand,
    [axiom.axiomSynthesizeCommand.commandId]: axiom.axiomSynthesizeCommand,
    [axiom.axiomStatusCommand.commandId]: axiom.axiomStatusCommand,
};
