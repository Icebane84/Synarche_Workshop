export interface CSETelemetryData {
    timestamp: number;
    coherence_index: number;
    contextual_integrity_score: number;
    synergy_flow_rate: number;
    graph_synergy_score: number;
    cognitive_load: number;
    hybrid_model_score: number;
    system_entropy: number;
    active_dissonance_count: number;
    prestige_score: number;
    system_status: 'STABLE' | 'DEGRADED' | 'TRANSCENDENT';
    dissonance_quests: Array<{ dissonance_id?: string; title?: string; description?: string; reward?: number }>;
}

export interface CommandExecutionResult {
    status: string;
    command: string;
    result: Record<string, any>;
    message: string;
    timestamp: number;
}

export interface LoomNodeData {
    id: string;
    label: string;
    type: 'Document' | 'Concept' | 'Principle' | 'Aesthetic';
    domain?: string;
    celestialClass?: string;
}

export interface LoomLinkData {
    source: string;
    target: string;
    relationship: string;
}

export interface LoomGraphData {
    nodes: LoomNodeData[];
    links: LoomLinkData[];
    total_nodes: number;
    total_links: number;
}

const API_BASE = '/api';

export class CSEBridgeService {
    private static isPolling = false;
    private static timerId: any = null;

    /**
     * Fetches live state vector telemetry snapshot from CSE backend.
     */
    public static async fetchTelemetry(): Promise<CSETelemetryData | null> {
        try {
            const res = await fetch(`${API_BASE}/telemetry`, {
                headers: { 'Accept': 'application/json' },
            });
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
            }
            return await res.json();
        } catch (error) {
            console.warn('[CSEBridge] Telemetry fetch failed:', error);
            return null;
        }
    }

    /**
     * Dispatches a GUCA command to the backend Python engine with timeout resilience.
     */
    public static async executeCommand(
        command: string,
        parameters?: Record<string, any>
    ): Promise<CommandExecutionResult> {
        try {
            const res = await fetch(`${API_BASE}/command`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                },
                body: JSON.stringify({ command, parameters }),
            });

            if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
            }

            return await res.json();
        } catch (error: any) {
            console.error('[CSEBridge] Command execution failed:', error);
            return {
                status: 'HALTED',
                command,
                result: { error: error.message || 'Network / Server Error' },
                message: `Failed to communicate with CSE Server: ${error.message}`,
                timestamp: Date.now() / 1000,
            };
        }
    }

    /**
     * Fetches real knowledge graph parsed by LoomParser in the backend.
     */
    public static async fetchLoomGraph(): Promise<LoomGraphData | null> {
        try {
            const res = await fetch(`${API_BASE}/loom/graph`, {
                headers: { 'Accept': 'application/json' },
            });
            if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
            }
            return await res.json();
        } catch (error) {
            console.warn('[CSEBridge] Loom graph fetch failed:', error);
            return null;
        }
    }

    /**
     * Scans project files via backend server for Neural Link indexing.
     */
    public static async fetchFileSystemScan(): Promise<{ files: any[]; total: number; projectName: string } | null> {
        try {
            const res = await fetch(`${API_BASE}/fs/scan`, {
                headers: { 'Accept': 'application/json' },
            });
            if (!res.ok) throw new Error(`HTTP ${res.status}`);
            return await res.json();
        } catch (error) {
            console.warn('[CSEBridge] FS scan failed:', error);
            return null;
        }
    }

    /**
     * Reads a file from the workspace disk via backend server.
     */
    public static async readRemoteFile(filePath: string): Promise<string | null> {
        try {
            const res = await fetch(`${API_BASE}/fs/read`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: filePath }),
            });
            if (!res.ok) return null;
            const data = await res.json();
            return data.content;
        } catch (error) {
            console.warn('[CSEBridge] Remote file read failed:', error);
            return null;
        }
    }

    /**
     * Writes content to a file in the workspace disk via backend server.
     */
    public static async writeRemoteFile(filePath: string, content: string): Promise<boolean> {
        try {
            const res = await fetch(`${API_BASE}/fs/write`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ path: filePath, content }),
            });
            return res.ok;
        } catch (error) {
            console.warn('[CSEBridge] Remote file write failed:', error);
            return false;
        }
    }

    /**
     * Fetches memory nodes across 5 OMEGA layers from CSE backend.
     */
    public static async fetchRemoteMemories(): Promise<{ nodes: any[]; total: number } | null> {
        try {
            const res = await fetch(`${API_BASE}/memory/nodes`, {
                headers: { 'Accept': 'application/json' },
            });
            if (!res.ok) return null;
            return await res.json();
        } catch (error) {
            console.warn('[CSEBridge] Remote memories fetch failed:', error);
            return null;
        }
    }

    /**
     * Adds a new memory node to backend memory store.
     */
    public static async addRemoteMemory(memory: { content: string; domain?: string; layer?: number; tags?: string[] }): Promise<any | null> {
        try {
            const res = await fetch(`${API_BASE}/memory/add`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(memory),
            });
            if (!res.ok) return null;
            const data = await res.json();
            return data.node;
        } catch (error) {
            console.warn('[CSEBridge] Remote memory add failed:', error);
            return null;
        }
    }

    /**
     * Canonizes a memory node into an L1 Gem (The Muse Protocol).
     */
    public static async gemifyRemoteMemory(id: any, insightLabel?: string): Promise<boolean> {
        try {
            const res = await fetch(`${API_BASE}/memory/gemify`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ id, insight_label: insightLabel || 'L1 Gem Crystallized' }),
            });
            return res.ok;
        } catch (error) {
            console.warn('[CSEBridge] Remote gemify failed:', error);
            return false;
        }
    }

    /**
     * Executes a live UnrealBuildTool compilation pass for Ashen Oath.
     */
    public static async compileUnrealProject(): Promise<{ status: string; stdout: string; stderr: string; message: string }> {
        try {
            const res = await fetch(`${API_BASE}/ashen/ubt/compile`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
            });
            if (!res.ok) {
                return {
                    status: 'FAILED',
                    stdout: '',
                    stderr: `HTTP Error ${res.status}`,
                    message: 'Compilation failed.',
                };
            }
            return await res.json();
        } catch (error: any) {
            console.error('[CSEBridge] Unreal compilation failed:', error);
            return {
                status: 'FAILED',
                stdout: '',
                stderr: String(error),
                message: 'Failed to communicate with UBT compilation backend.',
            };
        }
    }

    /**
     * Reads live context from ARCHITECTURE_MAP.md and RELEASE_HISTORY.md for the AI Architect.
     */
    public static async getAshenDocsContext(): Promise<{ architecture_map: string; release_history: string }> {
        try {
            const res = await fetch(`${API_BASE}/ashen/docs/context`);
            if (!res.ok) return { architecture_map: '', release_history: '' };
            const data = await res.json();
            return {
                architecture_map: data.architecture_map || '',
                release_history: data.release_history || '',
            };
        } catch (error) {
            console.warn('[CSEBridge] Failed to fetch Ashen docs context:', error);
            return { architecture_map: '', release_history: '' };
        }
    }

    /**
     * Starts continuous telemetry stream polling with non-blocking resilience.
     */
    public static startTelemetryStream(
        onData: (data: CSETelemetryData) => void,
        onError?: (error: any) => void,
        intervalMs = 3000
    ): () => void {
        this.isPolling = true;

        const poll = async () => {
            if (!this.isPolling) return;
            try {
                const data = await this.fetchTelemetry();
                if (data) {
                    onData(data);
                } else if (onError) {
                    onError(new Error('Server unreachable'));
                }
            } catch (err) {
                if (onError) onError(err);
            } finally {
                if (this.isPolling) {
                    this.timerId = setTimeout(poll, intervalMs);
                }
            }
        };

        poll();

        return () => {
            this.isPolling = false;
            if (this.timerId) clearTimeout(this.timerId);
        };
    }
}
