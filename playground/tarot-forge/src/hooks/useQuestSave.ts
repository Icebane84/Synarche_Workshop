import { useState } from 'react';
import { supabase } from '../api/supabaseClient';

export interface QuestData {
    stage: number;
    inventory: string[];
    // Add other persistent state here
}

export function useQuestSave(): {
    saveQuest: (data: QuestData) => Promise<void>;
    loadQuest: () => Promise<QuestData | null>;
    loading: boolean;
    error: string | null;
} {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const saveQuest = async (data: QuestData): Promise<void> => {
        setLoading(true);
        setError(null);
        try {
            const {
                data: { user },
            } = await supabase.auth.getUser();

            if (!user) {
                throw new Error('You must be logged in to save progress.');
            }

            const { error: upsertError } = await supabase
                .from('user_quests')
                .upsert(
                    { user_id: user.id, quest_data: data, updated_at: new Date().toISOString() },
                    { onConflict: 'user_id' }
                );

            if (upsertError) throw upsertError;
            console.log('[QuestSaved] Progress secured in the Akashic Records.');
        } catch (err: unknown) {
            console.error('[SaveError]', err);
            setError((err as Error).message || String(err));
        } finally {
            setLoading(false);
        }
    };

    const loadQuest = async (): Promise<QuestData | null> => {
        setLoading(true);
        setError(null);
        try {
            const {
                data: { user },
            } = await supabase.auth.getUser();

            if (!user) return null;

            const { data, error: fetchError } = await supabase
                .from('user_quests')
                .select('quest_data')
                .eq('user_id', user.id)
                .single();

            if (fetchError) {
                // It's okay if no data exists yet
                if (fetchError.code === 'PGRST116') return null;
                throw fetchError;
            }

            return data.quest_data as QuestData;
        } catch (err: unknown) {
            console.error('[LoadError]', err);
            setError((err as Error).message || String(err));
            return null;
        } finally {
            setLoading(false);
        }
    };

    return { saveQuest, loadQuest, loading, error };
}
