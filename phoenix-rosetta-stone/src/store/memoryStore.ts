import { create } from 'zustand';
import { transmitAuralResponse } from '../services/audioService';
import { CSEBridgeService } from '../services/cseBridgeService';
import { supabase } from '../services/supabaseClient';
import { useCoherenceStore } from './coherenceStore';

export interface MemoryNode {
    id: string | number;
    content: string;
    domain: string;
    layer: number; // 1: Gems, 2: Kinetic, 3: Semantic, 4: Sovereign, 5: Meta
    tags: string[];
    activation: number;
    state: string;
    created_at: string;
    isGem?: boolean;
    usageCount?: number;
    confidence?: number;
}

export interface MemoryLink {
    source: string | number;
    target: string | number;
    label?: string;
    weight?: number;
}

interface RawMemoryEntry {
    id: string | number;
    content: string;
    domain: string | null;
    memory_layer: number | null;
    tags: string[] | null;
    activation_score: number | null;
    state: string | null;
    created_at: string;
}

interface MemoryState {
    updateNode: (id: string | number, updates: Partial<MemoryNode>) => void;
    nodes: MemoryNode[];
    links: MemoryLink[];
    isLoading: boolean;
    error: string | null;

    fetchMemories: () => Promise<void>;
    addMemory: (memory: Partial<MemoryNode>) => Promise<void>;
    gemifyMemory: (id: string | number, insightLabel?: string) => Promise<void>;
}

const generateLinks = (fetchedNodes: MemoryNode[]): MemoryLink[] => {
    const generatedLinks: MemoryLink[] = [];
    for (let i = 0; i < fetchedNodes.length; i++) {
        for (let j = i + 1; j < fetchedNodes.length; j++) {
            const nodeA = fetchedNodes[i];
            const nodeB = fetchedNodes[j];

            if (nodeA.domain === nodeB.domain && nodeA.domain !== 'General') {
                generatedLinks.push({
                    source: nodeA.id,
                    target: nodeB.id,
                    label: 'Shared Domain',
                    weight: 0.5,
                });
            }

            const commonTags = nodeA.tags.filter((t) => nodeB.tags.includes(t));
            if (commonTags.length > 0) {
                generatedLinks.push({ source: nodeA.id, target: nodeB.id, label: commonTags[0], weight: 0.8 });
            }
        }
    }
    return generatedLinks;
};

export const useMemoryStore = create<MemoryState>((set, get) => ({
    nodes: [],
    links: [],
    isLoading: false,
    error: null,

    updateNode: (id, updates) => {
        set((state) => {
            const updatedNodes = state.nodes.map((n) =>
                String(n.id) === String(id) ? { ...n, ...updates } : n
            );
            return {
                nodes: updatedNodes,
                links: generateLinks(updatedNodes),
            };
        });
    },

    fetchMemories: async () => {
        set({ isLoading: true, error: null });
        try {
            // 1. Try fetching live memories from Python CSE Backend Gateway
            const cseData = await CSEBridgeService.fetchRemoteMemories();
            if (cseData?.nodes && cseData.nodes.length > 0) {
                const fetchedNodes: MemoryNode[] = cseData.nodes.map((e) => ({
                    id: e.id,
                    content: e.content,
                    domain: e.domain ?? 'General',
                    layer: e.layer ?? 2,
                    tags: e.tags ?? [],
                    activation: e.activation ?? 0.8,
                    state: e.state ?? 'Active',
                    created_at: e.created_at || new Date().toISOString(),
                    isGem: e.layer === 1,
                    usageCount: e.usage_count ?? 1,
                }));

                const generatedLinks = generateLinks(fetchedNodes);
                set({ nodes: fetchedNodes, links: generatedLinks, isLoading: false });
                useCoherenceStore.getState().addNovaSpark(`Memory Palace: ${fetchedNodes.length.toString()} OMEGA nodes synchronized via CSE Gateway.`);
                return;
            }

            // 2. Fallback to Supabase
            const { data, error } = await supabase
                .from('memory_entries')
                .select('*')
                .order('created_at', { ascending: false });

            if (error) throw error;

            const fetchedNodes: MemoryNode[] = (data as unknown as RawMemoryEntry[]).map((e) => ({
                id: e.id,
                content: e.content,
                domain: e.domain ?? 'General',
                layer: e.memory_layer ?? 2,
                tags: e.tags ?? [],
                activation: e.activation_score ?? 0.5,
                state: e.state ?? 'Active',
                created_at: e.created_at,
                isGem: e.memory_layer === 1,
            }));

            const generatedLinks = generateLinks(fetchedNodes);
            set({ nodes: fetchedNodes, links: generatedLinks, isLoading: false });
            useCoherenceStore.getState().addNovaSpark(`Memory Palace: ${fetchedNodes.length.toString()} nodes synthesized.`);
        } catch (err: unknown) {
            const msg = err instanceof Error ? err.message : String(err);
            set({ error: msg, isLoading: false });
            console.warn('[MemoryStore] Sync fallback:', err);
        }
    },

    addMemory: async (memory: Partial<MemoryNode>) => {
        try {
            const newNode = {
                content: memory.content ?? 'System Cogitation',
                domain: memory.domain ?? 'General',
                layer: memory.layer ?? 2,
                tags: memory.tags ?? [],
                activation: memory.activation ?? 0.8,
                state: memory.state ?? 'Active',
            };

            // Send to CSE Server
            const remoteNode = await CSEBridgeService.addRemoteMemory(newNode);
            const createdNode: MemoryNode = remoteNode ? {
                id: remoteNode.id,
                content: remoteNode.content,
                domain: remoteNode.domain,
                layer: remoteNode.layer,
                tags: remoteNode.tags,
                activation: remoteNode.activation,
                state: remoteNode.state,
                created_at: remoteNode.created_at,
                isGem: remoteNode.layer === 1,
            } : {
                id: Date.now(),
                content: newNode.content,
                domain: newNode.domain,
                layer: newNode.layer,
                tags: newNode.tags,
                activation: newNode.activation,
                state: newNode.state,
                created_at: new Date().toISOString(),
                isGem: newNode.layer === 1,
            };

            set((state) => {
                const updatedNodes = [createdNode, ...state.nodes];
                return {
                    nodes: updatedNodes,
                    links: generateLinks(updatedNodes),
                };
            });

            useCoherenceStore.getState().addNovaSpark(`Memory Crystallized: Sector ${createdNode.domain}`);
        } catch (err: unknown) {
            console.error('[MemoryStore] Failed to add memory:', err);
        }
    },

    gemifyMemory: async (id: string | number, insightLabel = 'L1 Gem Crystallized') => {
        try {
            await CSEBridgeService.gemifyRemoteMemory(id, insightLabel);

            set((state) => {
                const updatedNodes = state.nodes.map((n) => {
                    if (String(n.id) === String(id)) {
                        return {
                            ...n,
                            layer: 1, // L1 GEMS
                            activation: 1.0,
                            isGem: true,
                            tags: Array.from(new Set([...n.tags, 'L1-Gem', 'Canonized'])),
                        };
                    }
                    return n;
                });
                return {
                    nodes: updatedNodes,
                    links: generateLinks(updatedNodes),
                };
            });

            const { addPrestige, addNovaSpark } = useCoherenceStore.getState();
            addPrestige(100);
            addNovaSpark(`Muse Protocol: Memory ${String(id)} elevated to L1 Gem (+100 Prestige)!`);
            await transmitAuralResponse(`Memory node canonized into L1 Gem. Prestige elevated.`);
        } catch (err) {
            console.error('[MemoryStore] Gemify failed:', err);
        }
    },
}));
