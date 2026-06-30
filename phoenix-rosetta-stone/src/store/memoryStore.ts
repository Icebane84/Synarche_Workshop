import { create } from 'zustand';
import { supabase } from '../services/supabaseClient';
import { useCoherenceStore } from './coherenceStore';

export interface MemoryNode {
    id: string | number;
    content: string;
    domain: string;
    layer: number;
    tags: string[];
    activation: number;
    state: string;
    created_at: string;
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
    nodes: MemoryNode[];
    links: MemoryLink[];
    isLoading: boolean;
    error: string | null;

    fetchMemories: () => Promise<void>;
    addMemory: (memory: Partial<MemoryNode>) => Promise<void>;
}

export const useMemoryStore = create<MemoryState>((set) => ({
    nodes: [],
    links: [],
    isLoading: false,
    error: null,

    fetchMemories: async () => {
        set({ isLoading: true, error: null });
        try {
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
            }));

            // Generate synthetic links based on shared tags or domains for Phase 1
            const generatedLinks: MemoryLink[] = [];
            for (let i = 0; i < fetchedNodes.length; i++) {
                for (let j = i + 1; j < fetchedNodes.length; j++) {
                    const nodeA = fetchedNodes[i];
                    const nodeB = fetchedNodes[j];

                    // Link by Domain
                    if (nodeA.domain === nodeB.domain && nodeA.domain !== 'General') {
                        generatedLinks.push({
                            source: nodeA.id,
                            target: nodeB.id,
                            label: 'Shared Domain',
                            weight: 0.5,
                        });
                    }

                    // Link by Tags
                    const commonTags = nodeA.tags.filter((t) => nodeB.tags.includes(t));
                    if (commonTags.length > 0) {
                        generatedLinks.push({ source: nodeA.id, target: nodeB.id, label: commonTags[0], weight: 0.8 });
                    }
                }
            }

            set({ nodes: fetchedNodes, links: generatedLinks, isLoading: false });
            useCoherenceStore.getState().addNovaSpark(`Memory Palace: ${String(fetchedNodes.length.toString())} nodes synthesized.`);
        } catch (err: unknown) {
            const msg = err instanceof Error ? err.message : String(err);
            set({ error: msg, isLoading: false });
            console.error('[MemoryStore] Sync Error:', err);
        }
    },

    addMemory: async (memory: Partial<MemoryNode>) => {
        try {
            const newNode = {
                content: memory.content ?? 'System Cogitation',
                domain: memory.domain ?? 'General',
                memory_layer: memory.layer ?? 2,
                tags: memory.tags ?? [],
                activation_score: memory.activation ?? 0.8,
                state: memory.state ?? 'Active',
            };

            const { data, error } = await supabase.from('memory_entries').insert(newNode).select().single();

            if (error ?? !data) throw error ?? new Error('No data returned');

            const raw = data as unknown as RawMemoryEntry;
            const node: MemoryNode = {
                id: raw.id,
                content: raw.content,
                domain: raw.domain ?? 'General',
                layer: raw.memory_layer ?? 2,
                tags: raw.tags ?? [],
                activation: raw.activation_score ?? 0.8,
                state: raw.state ?? 'Active',
                created_at: raw.created_at,
            };

            set((state) => ({
                nodes: [node, ...state.nodes],
            }));

            useCoherenceStore.getState().addNovaSpark(`Memory Crystallized: ${String(node.domain)}`);
        } catch (err: unknown) {
            console.error('[MemoryStore] Failed to add memory:', err);
        }
    },
}));
