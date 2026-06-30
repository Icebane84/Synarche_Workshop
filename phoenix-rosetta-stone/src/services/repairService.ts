import { astAnalyzer } from './ast/ASTAnalyzer';
import { astRepairer } from './ast/ASTRepairer';
import { readLocalFile, writeToLocalFile } from './fileSystemService';
import { recoveryService } from './RecoveryService';

/**
 * RepairService [OMEGA v15.2]
 * The "Code Smith" engine for automated dissonance resolution.
 */

/**
 * Attempts to repair a specific dissonance task.
 * Implements "Permissioned" logic: 
 * 1. Creates a restoration point before modification.
 * 2. Uses ASTRepairer for surgical patching.
 * 3. Records cognitive intent in the Memory Palace.
 */
export const resolveDissonance = async (taskId: string): Promise<{ success: boolean; message: string }> => {
    // Dynamic imports to break circularity
    const { useTaskStore } = await import('../store/taskStore');
    const { useFileSystemStore } = await import('../store/fileSystemStore');
    const { useCoherenceStore } = await import('../store/coherenceStore');
    const { useMemoryStore } = await import('../store/memoryStore');

    const { tasks, updateTask } = useTaskStore.getState();
    const { rootHandle, scannedFiles, setScannedFiles } = useFileSystemStore.getState();
    const { addNovaSpark } = useCoherenceStore.getState();

    // 1. Identify Task
    const task = tasks.find((t) => t.id === taskId);
    if (!task) return { success: false, message: `Task ${taskId} not found in The Loom.` };

    // 2. Extract Metadata (expects "File: path/to/file")
    const notes = task.notes ?? '';
    const fileRegex = /File:\s*([^\n\r]+)/;
    const fileMatch = fileRegex.exec(notes);

    if (!fileMatch) {
        return {
            success: false,
            message: 'Task metadata corrupted: No file path found in notes.',
        };
    }
    const filePath = fileMatch[1].trim();

    if (!rootHandle) {
        return {
            success: false,
            message: 'Neural Link Disconnected: Please connect to the local file system first.',
        };
    }

    try {
        // 3. Read Current Content
        const content = await readLocalFile(rootHandle, filePath);
        if (content === null) {
            return { success: false, message: `Could not read file: ${filePath}. Check permissions.` };
        }

        // 4. Analyze for Current Offsets
        const violations = await astAnalyzer.analyzeFile(filePath, content);

        // Find the violation that matches this task's type
        const targetType = task.title.split(': ')[1] || '';
        const violation = violations.find((v) => v.type === targetType || (notes && notes.includes(v.message)));

        if (!violation || violation.start === undefined || violation.end === undefined) {
            return {
                success: true,
                message: 'Dissonance already resolved or offsets unavailable. Marking task as completed.',
            };
        }

        // 5. Create Restoration Point (Safety Net / Git-Lite)
        await recoveryService.createRestorePoint(filePath, content);

        // 6. Apply Surgical Patch via Code Smith
        const newContent = astRepairer.applyFix(violation, content);

        if (newContent === content) {
            return { success: false, message: `Repair logic for ${violation.type} failed to produce new content.` };
        }

        // 7. Write Back to Substrate
        const writeSuccess = await writeToLocalFile(rootHandle, filePath, newContent);
        if (!writeSuccess) {
            return { success: false, message: 'File write rejected by browser. Ensure permissions are granted.' };
        }

        // 8. Synchronize Store
        const updatedFiles = scannedFiles.map((f) => (f.path === filePath ? { ...f, content: newContent } : f));
        setScannedFiles(updatedFiles);

        // 9. Update Task Status
        await updateTask(taskId, { 
            status: 'Completed', 
            notes: `${notes}\n\n[RESOLVED] via Code Smith Autonomy [Restoration Point Created].` 
        });

        // 10. Record Cognitive "Why" in Memory Palace
        await (await import('../store/memoryStore')).useMemoryStore.getState().addMemory({
            content: `Autonomous Resolution: Repaired ${violation.type} in ${filePath} to resolve architectural dissonance. Substrate integrity preserved via RecoveryService.`,
            domain: 'Code Integrity',
            layer: 4, // Sovereign Layer
            tags: ['repair', violation.type, 'autonomy', 'recovery'],
            activation: 1.0,
        });

        addNovaSpark(`Dissonance Resolved: ${filePath} [Crystallized in Memory]`);

        return {
            success: true,
            message: `✨ Repair Success: ${violation.type} resolved in ${filePath}.`,
        };
    } catch (error) {
        console.error('[RepairService] Critical Fault:', error);
        return {
            success: false,
            message: `Critical Fault: ${error instanceof Error ? error.message : String(error)}`,
        };
    }
};

/**
 * Maintenance Pulse logic to batch repair tasks.
 * In Sovereign mode, it repairs all pending dissonances automatically.
 */
export const autoRepairApprovedTasks = async (isSovereign: boolean = false): Promise<{ count: number }> => {
    const { useTaskStore } = await import('../store/taskStore');
    const { tasks } = useTaskStore.getState();
    
    // In Sovereign mode, we repair ANY dissonance that isn't explicitly blocked.
    // In other modes, we only repair those with [APPROVED_FOR_REPAIR].
    const pendingTasks = tasks.filter(t => {
        const isDissonance = t.source === 'Dissonance Scanner' && t.status === 'To Do';
        if (!isDissonance) return false;
        
        if (isSovereign) {
            return !t.notes?.includes('[BLOCK_REPAIR]');
        }
        return t.notes?.includes('[APPROVED_FOR_REPAIR]');
    });
    
    let repairCount = 0;
    for (const task of pendingTasks) {
        const result = await resolveDissonance(task.id);
        if (result.success) repairCount++;
        // Throttle to avoid burning the Neural Link
        await new Promise(r => setTimeout(r, 1000));
    }
    
    return { count: repairCount };
};
