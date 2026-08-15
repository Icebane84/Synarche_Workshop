import { FileSystemDirectoryHandle, LocalFile } from '@essence/types';
import { create } from 'zustand';

interface FileSystemState {
  isConnected: boolean;
  projectName: string | null;
  rootHandle: FileSystemDirectoryHandle | null;
  scannedFiles: LocalFile[];

  connect: (handle: FileSystemDirectoryHandle) => Promise<void>;
  connectPolyglotBridge: (projectName?: string) => Promise<void>;
  disconnect: () => void;
  reconnect: () => Promise<boolean>;
  setScannedFiles: (files: LocalFile[]) => void;
}

export const useFileSystemStore = create<FileSystemState>((set, get) => ({
  isConnected: false,
  projectName: null,
  rootHandle: null,
  scannedFiles: [],

  connectPolyglotBridge: async (projectName = 'Synarche Workspace (CSE Bridge)') => {
    // If already connected via local handle, do not overwrite
    if (get().rootHandle) return;

    set({
      isConnected: true,
      projectName,
    });

    try {
      const { CSEBridgeService } = await import('../services/cseBridgeService');
      const res = await CSEBridgeService.fetchFileSystemScan();
      if (res?.files) {
        set({
          scannedFiles: res.files as LocalFile[],
          projectName: res.projectName ? `Sector ${res.projectName}` : projectName,
        });
      }
    } catch (e) {
      console.warn('[FileSystemStore] Polyglot bridge scan failed:', e);
    }
  },

  connect: async (handle: FileSystemDirectoryHandle) => {
    set({
      isConnected: true,
      rootHandle: handle,
      projectName: handle.name,
      scannedFiles: []
    });

    try {
      const { scanDirectoryRecursively } = await import('../services/fileSystemService');
      const files = await scanDirectoryRecursively(handle);
      set({ scannedFiles: files });
    } catch (e) {
      console.error('[FileSystemStore] Initial scan failed:', e);
    }
  },

  disconnect: () => { set({
    isConnected: false,
    projectName: null,
    rootHandle: null,
    scannedFiles: []
  }); },

  reconnect: async () => {
      // Lazy load to avoid circular dependencies if imports were top-level
      const { loadPersistedHandle, verifyPermission, scanDirectoryRecursively } = await import('../services/fileSystemService');

      const handle = await loadPersistedHandle();
      if (!handle) return false;

      // Check if we still have access
      const hasPermission = await verifyPermission(handle);

      if (hasPermission) {
          // If we have implicit permission (rare on reload, but possible in PWA contexts)
          set({ isConnected: true, rootHandle: handle, projectName: handle.name });
          const files = await scanDirectoryRecursively(handle);
          set({ scannedFiles: files });
          return true;
      } else {
          // We have the handle, but need a user gesture to re-verify.
          // We set it as "connected" but maybe in a "pending" state?
          // For now, let's set it as connected but with a special flag if we had one.
          // Or, better, we simply wait for the user to click "Reconnect" which might trigger this same logic.
          // Actually, 'verifyPermission' requests it if not granted.
          // Browser requires a user gesture for 'requestPermission'.
          // So 'reconnect' needs to be called FROM a user gesture if permission is missing.

          // Strategy: We return true that we FOUND a handle, but we can't fully connect until user interaction.
          // We can set a temporary "dormant" state if we wanted, but for now let's just return false
          // and let the UI show a "Resume Connection" button that calls this again.

          return false;
      }
  },

  setScannedFiles: (files: LocalFile[]) => { set({
    scannedFiles: files
  }); }
}));
