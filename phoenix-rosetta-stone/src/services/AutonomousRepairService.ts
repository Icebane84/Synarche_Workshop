import { FileSystemDirectoryHandle, LocalFile, Task } from '@essence/types';
import { useCoherenceStore } from '../store/coherenceStore';
import { useFileSystemStore } from '../store/fileSystemStore';
import { useTaskStore } from '../store/taskStore';
import { astAnalyzer } from './ast/ASTAnalyzer';
import { ASTViolation } from './ast/types';
import { resolveDissonance } from './repairService';

/**
 * AutonomousRepairService [OMEGA v15.3]
 * @relations
 * REF: RecoveryService.ts
 * REF: repairService.ts
 * The "Self-Healing" heart of the Phoenix Protocol.
 * Periodically scans for dissonances and manages the repair lifecycle.
 */

class AutonomousRepairService {
    private pulseTimer: ReturnType<typeof setInterval> | null = null;
    private isScanning = false;

    /**
     * Activates the Autonomous Maintenance Pulse.
     */
    public start() {
        if (this.pulseTimer) return;

        this.pulseTimer = setInterval(() => {
            void this.pulse();
        }, 60000); // 60s pulses

        void this.pulse(); // Initial pulse
    }

    /**
     * Deactivates the pulse.
     */
    public stop() {
        if (this.pulseTimer) {
            clearInterval(this.pulseTimer);
            this.pulseTimer = null;
        }
    }

    private async ensureActiveFiles(
        activeFiles: LocalFile[],
        rootHandle: FileSystemDirectoryHandle | null,
        setScannedFiles: (files: LocalFile[]) => void
    ): Promise<LocalFile[]> {
        if (activeFiles.length > 0 || !rootHandle) return activeFiles;
        console.log('[AutonomousRepairService] Pulse Polarization: Buffer empty, triggering sync...');
        try {
            const { scanDirectoryRecursively } = await import('./fileSystemService');
            const files = await scanDirectoryRecursively(rootHandle);
            setScannedFiles(files);
            return files;
        } catch (e) {
            console.error('[AutonomousRepairService] Sync failed:', e);
            return [];
        }
    }

    private async processViolation(
        file: LocalFile,
        violation: ASTViolation,
        tasks: Task[],
        addTask: (taskData: Omit<Task, 'id' | 'status' | 'createdAt' | 'updatedAt'>) => Promise<Task | undefined>,
        isSovereign: boolean
    ): Promise<void> {
        const existingTask = tasks.some(
            (t) => t.notes?.includes(`File: ${file.path}`) && t.title.includes(violation.type) && t.status !== 'Completed'
        );
        if (existingTask) return;

        const title = `[MAINTENANCE] ${violation.type}: ${file.name}`;
        const queueTag = isSovereign ? '[AUTONOMOUS_QUEUE]' : '[PROPOSED]';
        const notes = `Dissonance Type: ${violation.type}\nFile: ${file.path}\nMessage: ${violation.message}\n\n${queueTag}`;
        const priority = violation.severity === 'high' ? 'High' : 'Medium';

        const task = await addTask({
			title,
			notes,
			source: 'Dissonance Scanner',
			priority,
			timestamp: 0
		});

        if (isSovereign && task) {
            await resolveDissonance(task.id);
        }
    }

    private async scanFileViolations(
        file: LocalFile,
        tasks: Task[],
        addTask: (taskData: Omit<Task, 'id' | 'status' | 'createdAt' | 'updatedAt'>) => Promise<Task | undefined>,
        isSovereign: boolean
    ): Promise<void> {
        const violations = await astAnalyzer.analyzeFile(file.path, file.content);
        for (const violation of violations) {
            await this.processViolation(file, violation, tasks, addTask, isSovereign);
        }
    }

    /**
     * The heart of the machine.
     * Scans all known files and synchronizes with The Loom.
     */
    private async pulse() {
        const { maintenanceMode } = useCoherenceStore.getState();
        const { scannedFiles, isConnected, rootHandle, setScannedFiles } = useFileSystemStore.getState();
        const { tasks, addTask } = useTaskStore.getState();

        if (maintenanceMode === 'Manual' || this.isScanning || !isConnected) return;

        this.isScanning = true;
        const isSovereign = maintenanceMode === 'Sovereign';

        try {
            const activeFiles = await this.ensureActiveFiles(scannedFiles, rootHandle, setScannedFiles);
            for (const file of activeFiles) {
                await this.scanFileViolations(file, tasks, addTask, isSovereign);
            }
        } catch (error) {
            console.error('[AutonomousRepairService] Pulse Fault:', error);
        } finally {
            this.isScanning = false;
        }
    }
}

export const autonomousRepairService = new AutonomousRepairService();
