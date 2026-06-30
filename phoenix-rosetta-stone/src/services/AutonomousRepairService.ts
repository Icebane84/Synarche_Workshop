import { useCoherenceStore } from '../store/coherenceStore';
import { useFileSystemStore } from '../store/fileSystemStore';
import { useTaskStore } from '../store/taskStore';
import { astAnalyzer } from './ast/ASTAnalyzer';
import { resolveDissonance } from './repairService';

/**
 * AutonomousRepairService [OMEGA v15.3]
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

        // Pulse Polarization: Wake up if buffer is empty
        let activeFiles = scannedFiles;
        if (activeFiles.length === 0 && rootHandle) {
            console.log('[AutonomousRepairService] Pulse Polarization: Buffer empty, triggering sync...');
            try {
                const { scanDirectoryRecursively } = await import('./fileSystemService');
                activeFiles = await scanDirectoryRecursively(rootHandle);
                setScannedFiles(activeFiles);
            } catch (e) {
                console.error('[AutonomousRepairService] Sync failed:', e);
                this.isScanning = false;
                return;
            }
        }


        try {
            for (const file of activeFiles) {
                const violations = await astAnalyzer.analyzeFile(file.path, file.content);

                for (const violation of violations) {
                    // Check if a task already exists for this violation
                    const existingTask = tasks.find(t => 
                        t.notes?.includes(`File: ${file.path}`) && 
                        t.title.includes(violation.type) &&
                        t.status !== 'Completed'
                    );

                    if (!existingTask) {
                        const isSovereign = maintenanceMode === 'Sovereign';
                        const title = `[MAINTENANCE] ${violation.type}: ${file.name}`;
                        const notes = `Dissonance Type: ${violation.type}\nFile: ${file.path}\nMessage: ${violation.message}\n\n${isSovereign ? '[AUTONOMOUS_QUEUE]' : '[PROPOSED]'}`;
                        
                        const task = await addTask({
                            title,
                            notes,
                            source: 'Dissonance Scanner',
                            priority: violation.severity === 'high' ? 'High' : 'Medium',
                        });

                        // If Sovereign, trigger immediate repair
                        if (isSovereign && task) {
                            await resolveDissonance(task.id);
                        }
                    }
                }
            }
        } catch (error) {
            console.error('[AutonomousRepairService] Pulse Fault:', error);
        } finally {
            this.isScanning = false;
        }
    }
}

export const autonomousRepairService = new AutonomousRepairService();
