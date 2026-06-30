import { CommandDefinitionGUCAv5 } from '@essence/codex';

/**
 * @fileoverview Commands for task management and Loom interactions.
 */

export const logTaskToLoomCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_LOG_TASK_TO_LOOM',
    description: 'Log a new task directly into The Loom.',
    parameters: [
        { name: 'title', type: 'string', description: 'Task title.', required: true },
        { name: 'notes', type: 'string', description: 'Task details.', required: false, uiHint: 'textarea' },
    ],
    action: 'Task weaving.',
    aliases: ['task', 'todo', 'log', 'add task'],
};

export const fetchTasksCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_FETCH_TASKS',
    description: 'Forces synchronization from The Loom.',
    parameters: [],
    action: 'Task fetch.',
    aliases: ['refresh tasks', 'sync tasks'],
};

export const viewTaskDetailsCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_VIEW_TASK_DETAILS',
    description: 'Displays full details of a specific task.',
    parameters: [{ name: 'taskId', type: 'string', description: 'Task ID', required: true }],
    action: 'Task inspection.',
    aliases: ['view task', 'task details'],
};

export const resolveDissonanceCommand: CommandDefinitionGUCAv5 = {
    commandId: 'CMD_RESOLVE_DISSONANCE',
    description: 'Attempts to auto-repair a specific dissonance task.',
    parameters: [{ name: 'taskId', type: 'string', description: 'The ID of the dissonance task.', required: true }],
    action: 'Code Smith Patching',
    aliases: ['fix task', 'repair dissonance', 'auto fix'],
};
