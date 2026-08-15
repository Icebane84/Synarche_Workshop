// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { del, get, set } from 'idb-keyval';
import { FileSystemDirectoryHandle, FileSystemFileHandle, LocalFile } from '@essence/types';

/**
 * @fileoverview The File System Service (Neural Link).
 * This sovereign module bridges the gap between the simulated "Mind" of the AI
 * and the physical reality of the user's local file system.
 */

const IGNORE_PATTERNS = ['node_modules', '.git', 'dist', 'build', '.DS_Store', 'coverage'];
const ALLOWED_EXTENSIONS = ['.ts', '.tsx', '.js', '.jsx', '.json', '.md', '.css', '.html'];
const DB_KEY = 'phoenix_neural_link_handle';

/**
 * Request the user to select a local directory with readwrite access.
 */
export const openDirectoryPicker = async (): Promise<FileSystemDirectoryHandle | null> => {
    try {
        if (!window.showDirectoryPicker) {
            throw new Error('File System Access API not supported in this environment.');
        }
        // Request readwrite access explicitly for Code Smith capabilities
        const dirHandle = await window.showDirectoryPicker({
            mode: 'readwrite',
        });

        // Persist the handle for future sessions
        await set(DB_KEY, dirHandle);

        return dirHandle;
    } catch (error) {
        console.warn('[FileSystem] Connection aborted:', error);
        return null;
    }
};

/**
 * Loads the persisted directory handle from IndexedDB.
 */
export const loadPersistedHandle = async (): Promise<FileSystemDirectoryHandle | null> => {
    try {
        const handle = await get<FileSystemDirectoryHandle>(DB_KEY);
        return handle || null;
    } catch (error) {
        console.error('[FileSystem] Failed to load persisted handle:', error);
        return null;
    }
};

/**
 * Verifies if the user has granted permission to the handle.
 * If not, requests it.
 */
export const verifyPermission = async (handle: FileSystemDirectoryHandle): Promise<boolean> => {
    // Check if permission was already granted
    if ((await handle.queryPermission({ mode: 'readwrite' })) === 'granted') {
        return true;
    }
    // Request permission
    if ((await handle.queryPermission({ mode: 'readwrite' })) === 'granted') {
        return true;
    }
    return false;
};

/**
 * Clears the persisted handle.
 */
export const clearPersistedHandle = async (): Promise<void> => {
    await del(DB_KEY);
};

/**
 * Recursively scans a directory handle.
 */
export const scanDirectoryRecursively = async (
    dirHandle: FileSystemDirectoryHandle,
    path = '',
): Promise<LocalFile[]> => {
    const files: LocalFile[] = [];

    for await (const entry of dirHandle.values()) {
        const fullPath = path ? `${path}/${entry.name}` : entry.name;

        if (entry.kind === 'file') {
            const fileHandle = entry as FileSystemFileHandle;
            const lastDotIndex = entry.name.lastIndexOf('.');
            const extension = lastDotIndex !== -1 ? entry.name.slice(lastDotIndex) : '';

            if (ALLOWED_EXTENSIONS.includes(extension)) {
                try {
                    const file = await fileHandle.getFile();
                    const content = await file.text();
                    files.push({
                        name: entry.name,
                        path: fullPath,
                        content: content,
                        handle: fileHandle,
                    });
                } catch (e) {
                    console.error(`[FileSystem] Failed to read ${fullPath}:`, e);
                }
            }
        } else if (entry.kind === 'directory') {
            if (!IGNORE_PATTERNS.includes(entry.name)) {
                try {
                    const subDirHandle = await dirHandle.getDirectoryHandle(entry.name);
                    const subFiles = await scanDirectoryRecursively(subDirHandle, fullPath);
                    files.push(...subFiles);
                } catch (e) {
                    console.error(`[FileSystem] Failed to access directory ${fullPath}:`, e);
                }
            }
        }
    }
    return files;
};

/**
 * Writes content to a specific file in the connected directory.
 * @param rootHandle The root directory handle.
 * @param filePath Path relative to root (e.g., 'src/App.tsx').
 * @param content New file content.
 */
export const writeToLocalFile = async (
    rootHandle: FileSystemDirectoryHandle,
    filePath: string,
    content: string,
): Promise<boolean> => {
    try {
        const parts = filePath.split('/');
        const fileName = parts.pop();
        if (!fileName) return false;

        let currentHandle = rootHandle;

        // Traverse to target directory
        for (const part of parts) {
            currentHandle = await currentHandle.getDirectoryHandle(part, { create: false });
        }

        const fileHandle = await currentHandle.getFileHandle(fileName, { create: false });

        // Protocol: Request permission if not already granted in the current session
        const permission = await fileHandle.requestPermission({ mode: 'readwrite' });
        if (permission !== 'granted') return false;

        const writable = await fileHandle.createWritable();
        await writable.write(content);
        await writable.close();
        return true;
    } catch (e) {
        console.error(`[Code Smith] Failed to repair ${filePath}:`, e);
        return false;
    }
};

/**
 * Reads the content of a specific local file.
 */
export const readLocalFile = async (
    rootHandle: FileSystemDirectoryHandle,
    filePath: string,
): Promise<string | null> => {
    try {
        const parts = filePath.split('/');
        const fileName = parts.pop();
        if (!fileName) return null;

        let currentHandle = rootHandle;

        for (const part of parts) {
            currentHandle = await currentHandle.getDirectoryHandle(part, { create: false });
        }

        const fileHandle = await currentHandle.getFileHandle(fileName, { create: false });
        const file = await fileHandle.getFile();
        return await file.text();
    } catch (e) {
        console.error(`[FileSystem] Failed to read ${filePath}:`, e);
        return null;
    }
};

