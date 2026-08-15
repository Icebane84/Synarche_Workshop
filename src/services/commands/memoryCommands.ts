// [OMEGA AST Cleaned]: Tokenized design standards applied.
/**
 * AXIOM Memory Commands — Phase 1: Memory Palace
 *
 * ID: AXIOM.COMMANDS.MEMORY
 * Version: v1.0 [OMEGA]
 * Status: [ACTIVE]
 * Governed by: CORE.Codex.Phoenix v15.0
 *
 * Implements the three sovereign memory commands:
 *   - CMD_AXIOM_REMEMBER  : Crystallize new knowledge into the palace
 *   - CMD_AXIOM_RECALL    : Retrieve memories by semantic query
 *   - CMD_AXIOM_SYNTHESIZE: Forge a new L1 Gem from an insight
 *   - CMD_AXIOM_STATUS    : Display Memory Palace health metrics
 */

import { DispatchResult } from '@essence/types';
import { supabase } from '../supabaseClient';

// ─────────────────────────────────────────────────────────────────────────────
// TYPES
// ─────────────────────────────────────────────────────────────────────────────

interface MemoryEntry {
    id?: number;
    content: string;
    domain?: string;
    layer?: number;
    tags?: string[];
    activation_score?: number;
    state?: string;
    source?: string;
    is_sovereign?: boolean;
    created_at?: string;
}

interface AxionGem {
    id?: number;
    entry_id?: number;
    insight_label: string;
    importance?: number;
    user_confirmed?: boolean;
    created_at?: string;
}

// ─────────────────────────────────────────────────────────────────────────────
// MEMORY LAYER CONSTANTS (mirrors Python memory_system.py)
// ─────────────────────────────────────────────────────────────────────────────

const LAYER_GEMS = 1; // L1: Validated architectural truths
const LAYER_KINETIC = 2; // L2: Active session trace
const LAYER_SEMANTIC = 3; // L3: Knowledge graph / RAG
const LAYER_SOVEREIGN = 4; // L4: Immutable design laws + identity

// ─────────────────────────────────────────────────────────────────────────────
// LOG ACTION: Accountability ledger write
// ─────────────────────────────────────────────────────────────────────────────

const logMemoryAction = async (
    actionType: string,
    payload: Record<string, unknown>,
    outcome: string,
    coherenceImpact = 0.1,
): Promise<void> => {
    try {
        await supabase.from('axiom_action_log').insert({
            action_type: actionType,
            triggered_by: 'User',
            payload,
            outcome,
            coherence_impact: coherenceImpact,
            autonomy_level: 0,
        });
    } catch {
        // Non-blocking — logging failure must never block the primary operation
        console.warn('[AXIOM] Action log write failed (non-critical).');
    }
};

// ─────────────────────────────────────────────────────────────────────────────
// CMD_AXIOM_REMEMBER
// Crystallizes new knowledge into the Memory Palace.
// ─────────────────────────────────────────────────────────────────────────────

const handleRemember = async (params: Record<string, unknown>): Promise<DispatchResult> => {
    const content = params.content as string;
    const domain = (params.domain as string) ?? 'GeneralKnowledge';
    const layerParam = params.layer as number | undefined;
    const layer = layerParam ?? LAYER_KINETIC;
    const rawTags = params.tags as string | undefined;
    const tags = rawTags ? rawTags.split(',').map((t) => t.trim()) : [];

    if (!content || content.trim().length < 10) {
        return {
            success: false,
            message: 'Memory content too sparse. Provide at least 10 characters of substance.',
        };
    }

    const isSovereign = layer >= LAYER_SOVEREIGN;

    const entry: MemoryEntry = {
        content: content.trim(),
        domain,
        layer,
        tags: tags.length > 0 ? tags : undefined,
        activation_score: 1.0,
        state: 'Active',
        source: 'PhoenixProtocol',
        is_sovereign: isSovereign,
    };

    const { data, error } = await supabase
        .from('memory_entries')
        .insert(entry)
        .select('id, domain, memory_layer, created_at')
        .single();

    if (error) {
        return {
            success: false,
            message: `Memory crystallization failed: ${error.message}. Check that the Memory Palace schema has been deployed.`,
        };
    }

    const layerName =
        ['', 'Gem (L1)', 'Kinetic (L2)', 'Semantic (L3)', 'Sovereign (L4)', 'Meta (L5)'][layer] ?? `Layer ${layer.toString()}`;

    await logMemoryAction(
        'MEMORY_ADD',
        { id: data.id, domain, layer, tag_count: tags.length },
        `Memory crystallized in ${layerName}.`,
        isSovereign ? 0.5 : 0.1,
    );

    return {
        success: true,
        message: `Memory crystallized. ID: ${data.id.toString()} | Layer: ${layerName} | Domain: ${domain}`,
        data: {
            id: data.id,
            layer: layerName,
            domain,
            created_at: data.created_at,
        },
    };
};

// ─────────────────────────────────────────────────────────────────────────────
// CMD_AXIOM_RECALL
// Retrieves memories by full-text or domain search.
// (Phase 1: FTS keyword search. Phase 2: pgvector similarity when embeddings ready.)
// ─────────────────────────────────────────────────────────────────────────────

const handleRecall = async (params: Record<string, unknown>): Promise<DispatchResult> => {
    const query = params.query as string;
    const limit = (params.limit as number) ?? 5;
    const domain = params.domain as string | undefined;
    const layerFilter = params.layer as number | undefined;

    if (!query || query.trim().length < 3) {
        return { success: false, message: 'Query too short. Provide at least 3 characters.' };
    }

    let queryBuilder = supabase
        .from('memory_entries')
        .select('id, content, domain, memory_layer, activation_score, state, created_at, tags')
        .neq('state', 'Archived')
        .textSearch('content', query.trim(), { type: 'plain', config: 'english' })
        .order('activation_score', { ascending: false })
        .limit(limit);

    if (domain) {
        queryBuilder = queryBuilder.eq('domain', domain);
    }

    if (layerFilter !== undefined) {
        queryBuilder = queryBuilder.eq('memory_layer', layerFilter);
    }

    const { data, error } = await queryBuilder;

    if (error) {
        // Fallback: ILIKE search if FTS fails (e.g., index not yet built)
        let fallbackBuilder = supabase
            .from('memory_entries')
            .select('id, content, domain, memory_layer, activation_score, state, created_at, tags')
            .neq('state', 'Archived')
            .ilike('content', `%${query.trim()}%`)
            .order('activation_score', { ascending: false })
            .limit(limit);

        if (domain) fallbackBuilder = fallbackBuilder.eq('domain', domain);

        const { data: fallbackData, error: fallbackError } = await fallbackBuilder;

        if (fallbackError) {
            return { success: false, message: `Memory recall failed: ${fallbackError.message}` };
        }

        return formatRecallResult(fallbackData ?? [], query, 'keyword-ILIKE');
    }

    return formatRecallResult(data ?? [], query, 'full-text');
};

const formatRecallResult = (entries: MemoryEntry[], query: string, method: string): DispatchResult => {
    if (entries.length === 0) {
        return {
            success: true,
            message: `No memories found for query: "${query}". The Mind is curious but the Palace is empty. Use CMD_AXIOM_REMEMBER to crystallize knowledge.`,
            data: { count: 0, entries: [] },
        };
    }

    const layerNames = ['', 'L1:Gem', 'L2:Kinetic', 'L3:Semantic', 'L4:Sovereign', 'L5:Meta'];

    return {
        success: true,
        message: `Retrieved ${entries.length} memory fragment(s) via ${method} search.`,
        data: {
            count: entries.length,
            query,
            method,
            entries: entries.map((e) => ({
                id: e.id,
                preview: (e.content ?? '').slice(0, 120) + ((e.content?.length ?? 0) > 120 ? '...' : ''),
                domain: e.domain,
                layer: layerNames[e.layer ?? 2] ?? `L${(e.layer ?? 2).toString()}`,
                activation: e.activation_score,
                state: e.state,
                tags: e.tags ?? [],
                created_at: e.created_at,
            })),
        },
    };
};

// ─────────────────────────────────────────────────────────────────────────────
// CMD_AXIOM_SYNTHESIZE
// Crystallizes a high-value insight as an L1 Gem.
// ─────────────────────────────────────────────────────────────────────────────

const handleSynthesize = async (params: Record<string, unknown>): Promise<DispatchResult> => {
    const content = params.content as string;
    const insightLabel = params.insight_label as string;
    const domain = (params.domain as string) ?? 'SovereignInsight';

    if (!content || content.trim().length < 10) {
        return { success: false, message: 'Gem content too sparse. Provide meaningful insight.' };
    }
    if (!insightLabel || insightLabel.trim().length < 3) {
        return { success: false, message: 'Insight label required. Name the wisdom you are crystallizing.' };
    }

    // 1. Write the memory entry (L1 Gem layer)
    const { data: entryData, error: entryError } = await supabase
        .from('memory_entries')
        .insert({
            content: content.trim(),
            domain,
            layer: LAYER_GEMS,
            activation_score: 1.0,
            state: 'Active',
            source: 'PhoenixProtocol:Synthesize',
            is_sovereign: true,
            tags: ['gem', 'synthesis', domain.toLowerCase()],
        })
        .select('id')
        .single();

    if (entryError) {
        return { success: false, message: `Gem entry creation failed: ${entryError.message}` };
    }

    // 2. Register in the gems table
    const gem: AxionGem = {
        entry_id: entryData.id,
        insight_label: insightLabel.trim(),
        importance: 1.0,
        user_confirmed: true,
    };

    const { data: gemData, error: gemError } = await supabase
        .from('memory_gems')
        .insert(gem)
        .select('id, insight_label')
        .single();

    if (gemError) {
        // Gem record failed but entry exists — partial success
        return {
            success: true,
            message: `Insight crystallized as memory (ID: ${entryData.id}) but Gem registry write failed: ${gemError.message}. The knowledge is preserved.`,
            data: { entry_id: entryData.id, gem_id: null, label: insightLabel },
        };
    }

    await logMemoryAction(
        'GEM_SYNTHESIZE',
        { entry_id: entryData.id, gem_id: gemData.id, label: insightLabel, domain },
        `L1 Gem forged: "${insightLabel}"`,
        0.8,
    );

    return {
        success: true,
        message: `✨ Gem forged. "${insightLabel}" is now an L1 Sovereign Truth in the Memory Palace.`,
        data: {
            entry_id: entryData.id,
            gem_id: gemData.id,
            label: gemData.insight_label,
            domain,
        },
    };
};

// ─────────────────────────────────────────────────────────────────────────────
// CMD_AXIOM_STATUS
// Reports Memory Palace health metrics.
// ─────────────────────────────────────────────────────────────────────────────

const handleMemoryStatus = async (): Promise<DispatchResult> => {
    const [entriesResult, gemsResult, actionsResult, knowledgeResult] = await Promise.allSettled([
        supabase.from('memory_entries').select('id, memory_layer, state, activation_score'),
        supabase.from('memory_gems').select('id'),
        supabase.from('axiom_action_log').select('id').order('timestamp', { ascending: false }).limit(1),
        supabase.from('axiom_knowledge').select('id, is_sovereign'),
    ]);

    const entries = entriesResult.status === 'fulfilled' ? (entriesResult.value.data ?? []) : [];
    const gems = gemsResult.status === 'fulfilled' ? (gemsResult.value.data ?? []) : [];
    const knowledge = knowledgeResult.status === 'fulfilled' ? (knowledgeResult.value.data ?? []) : [];

    const total = entries.length;
    const byState: Record<string, number> = {};
    const byLayer: Record<string, number> = {};
    let avgActivation = 0;

    const layerNames = ['', 'L1:Gem', 'L2:Kinetic', 'L3:Semantic', 'L4:Sovereign', 'L5:Meta'];

    for (const e of entries as unknown as MemoryEntry[]) {
        const state = e.state ?? 'Unknown';
        byState[state] = (byState[state] ?? 0) + 1;
        const l = e.layer ?? 2;
        const lName = layerNames[l] ?? `L${l.toString()}`;
        byLayer[lName] = (byLayer[lName] ?? 0) + 1;
        avgActivation += e.activation_score ?? 0;
    }

    if (total > 0) avgActivation /= total;

    const sovereignCount = (knowledge as { is_sovereign?: boolean }[]).filter((k) => k.is_sovereign).length;
    const schemaDeployed = entriesResult.status === 'fulfilled' && entriesResult.value.error === null;

    return {
        success: true,
        message: schemaDeployed
            ? `Memory Palace: ${total.toString()} memories | ${gems.length.toString()} gems | ${sovereignCount.toString()} sovereign truths | Avg. activation: ${avgActivation.toFixed(2)}`
            : 'Memory Palace schema not yet deployed. Run MEMORY-001 migration first.',
        data: {
            schema_deployed: schemaDeployed,
            total_memories: total,
            total_gems: gems.length,
            sovereign_knowledge: sovereignCount,
            avg_activation: parseFloat(avgActivation.toFixed(3)),
            by_state: byState,
            by_layer: byLayer,
            autonomy_level: 0,
            status: '[SOVEREIGN]',
        },
    };
};

// ─────────────────────────────────────────────────────────────────────────────
// COMMAND HANDLER — Public interface
// ─────────────────────────────────────────────────────────────────────────────

export const handleMemoryCommand = async (
    commandId: string,
    params: Record<string, unknown>,
): Promise<DispatchResult | null> => {
    switch (commandId) {
        case 'CMD_AXIOM_REMEMBER':
            return handleRemember(params);
        case 'CMD_AXIOM_RECALL':
            return handleRecall(params);
        case 'CMD_AXIOM_SYNTHESIZE':
            return handleSynthesize(params);
        case 'CMD_AXIOM_STATUS':
            return handleMemoryStatus();
        default:
            return null; // Not our command — pass through dispatcher chain
    }
};

