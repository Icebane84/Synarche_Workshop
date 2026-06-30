import { useFileSystemStore } from '../store/fileSystemStore';
import { writeToLocalFile, readLocalFile } from './fileSystemService';

/**
 * RecoveryService [OMEGA v15.3]
 * @relations
 * REF: AutonomousRepairService.ts
 * REF: repairService.ts
 * The "Git-Lite" substrate for non-destructive architectural repair.
 * Manages snapshots and rollbacks in the /.phoenix/restoration directory.
 */

interface RestorationHistory {
    timestamp: number;
    version: string;
}

type RestorationIndex = Record<string, RestorationHistory[]>;

class RecoveryService {
    private readonly RESTORATION_BASE = '.phoenix/restoration';
    private readonly INDEX_PATH = '.phoenix/restoration/INDEX.json';

    /**
     * Creates a restoration point for a file before modification.
     */
    public async createRestorePoint(filePath: string, content: string): Promise<boolean> {
        const { rootHandle } = useFileSystemStore.getState();
        if (!rootHandle) return false;

        try {
            const timestamp = Date.now();
            const versionId = `v_${String(timestamp)}`;
            const backupPath = `${this.RESTORATION_BASE}/${filePath.replace(/\//g, '_')}_${versionId}.bak`;

            // 1. Save the actual content backup
            await writeToLocalFile(rootHandle, backupPath, content);

            // 2. Update the Index
            const indexContent = await readLocalFile(rootHandle, this.INDEX_PATH);
            let index: RestorationIndex = {};
            
            if (indexContent) {
                try {
                    const parsed = JSON.parse(indexContent) as unknown;
                    if (typeof parsed === 'object' && parsed !== null) {
                        index = parsed as RestorationIndex;
                    }
                } catch (err: unknown) {
                    console.error('[RecoveryService] Index Corrupted, resetting.', err);
                }
            }

            if (!index[filePath]) index[filePath] = [];
            index[filePath].unshift({ timestamp, version: backupPath });

            // Keep only last 5 versions
            if (index[filePath].length > 5) {
                index[filePath] = index[filePath].slice(0, 5);
            }

            await writeToLocalFile(rootHandle, this.INDEX_PATH, JSON.stringify(index, null, 2));
            return true;
        } catch (error) {
            console.error('[RecoveryService] Failed to create restore point:', error);
            return false;
        }
    }

    /**
     * Lists available restore points for a file.
     */
    public async getRestorePoints(filePath: string): Promise<RestorationHistory[]> {
        const { rootHandle } = useFileSystemStore.getState();
        if (!rootHandle) return [];

        const indexContent = await readLocalFile(rootHandle, this.INDEX_PATH);
        if (!indexContent) return [];

        try {
            const index = JSON.parse(indexContent) as RestorationIndex;
            return index[filePath] ?? [];
        } catch (e) {
            return [];
        }
    }

    /**
     * Reverts a file to a specific restoration point.
     */
    public async rollback(filePath: string, backupPath: string): Promise<boolean> {
        const { rootHandle } = useFileSystemStore.getState();
        if (!rootHandle) return false;

        try {
            const backupContent = await readLocalFile(rootHandle, backupPath);
            if (!backupContent) throw new Error('Backup content missing.');

            return await writeToLocalFile(rootHandle, filePath, backupContent);
        } catch (error) {
            console.error('[RecoveryService] Rollback failed:', error);
            return false;
        }
    }
}

export const recoveryService = new RecoveryService();
