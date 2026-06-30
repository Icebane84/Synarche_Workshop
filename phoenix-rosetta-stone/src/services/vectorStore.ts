// import { pipeline } from '@xenova/transformers'; // CRITICAL: Disabled due to Vite/React 19 crash
import { GoogleGenAI } from '@google/genai';
import { knowledgeBase } from '../data/knowledgeBase';
import { systemConfig } from './configService';
import { supabase } from './supabaseClient';

const ai = new GoogleGenAI({ apiKey: systemConfig.api.geminiKey as string });

/**
 * @fileoverview The Sovereign Vector Store [OMEGA v15.1].
 * Utilizing Google Gemini 'gemini-embedding-001' for high-precision semantic mapping.
 * This substrate powers the spatial reasoning of the Memory Palace.
 */

export interface RetrievalResult {
    title: string;
    content: string;
    contentSnippet?: string;
    score: number;
    docId: string;
    type: string;
}

export interface DocumentMatch {
    id: number;
    content: string;
    similarity: number;
    metadata: {
        docId?: string;
        title?: string;
        type?: string;
        chunkIndex?: number;
    } | null;
}

/**
 * GENERATES A VECTOR EMBEDDING via Gemini.
 * Maps high-dimensional semantic intent into a 3072-dimensional vector space.
 *
 * @param text The input text to vectorize.
 * @returns A 3072-dimensional vector.
 */
const generateEmbedding = async (text: string): Promise<number[]> => {
    try {
        // DEBUG: List models to verify availability
        try {
            await ai.models.list();
            // Models available
        } catch (e: unknown) {
            console.error('[VectorStore] Failed to list models:', e instanceof Error ? e.message : String(e));
        }

        const result = await ai.models.embedContent({
            model: 'gemini-embedding-001', // Verified available via check-models.js
            contents: [{ parts: [{ text }] }],
        });
        const embedding = result.embeddings?.[0]?.values;

        if (embedding?.length !== 3072) {
            // gemini-embedding-001 appears to be 3072 dimensions
            throw new Error(`Invalid embedding generated. Expected 3072, got ${String(embedding?.length)}`);
        }
        return embedding;
    } catch (error: unknown) {
        console.error(
            '[VectorStore] Embedding Generation Failed:',
            error instanceof Error ? error.message : String(error),
        );
        throw error;
    }
};

export const indexKnowledgeBase = async () => {
    for (const doc of knowledgeBase) {
        // Simple chunking
        const chunks = doc.content.split(/\n\s*\n/).filter((c) => c.length > 50);

        for (const [index, chunkContent] of chunks.entries()) {
            try {
                // 1. Generate Vector (Dummy)
                await new Promise((resolve) => setTimeout(resolve, 2000)); // Rate Limit: 2s delay
                const embedding = await generateEmbedding(chunkContent);

                // 2. Insert into Supabase
                const { error } = await supabase.from('documents').insert({
                    content: chunkContent,
                    embedding: embedding,
                    metadata: {
                        docId: doc.id,
                        title: doc.title,
                        type: doc.type,
                        chunkIndex: index,
                    },
                });

                if (error) {
                    console.error('[VectorStore] Insert Error:', error);
                }
            } catch (err: unknown) {
                console.error('[VectorStore] Processing Error:', err instanceof Error ? err.message : String(err));
            }
        }
    }
};

/**
 * Semantic Search / Retrieval Augmented Generation (RAG).
 * Queries the Supabase `match_documents` RPC function to find contextually relevant knowledge.
 *
 * @param query The user's question or input.
 * @param limit Max number of chunks to retrieve.
 */
export const retrieveContext = async (query: string, limit = 3): Promise<RetrievalResult[]> => {
    try {
        const queryVector = await generateEmbedding(query);

        const response = await supabase.rpc('match_documents', {
            query_embedding: queryVector,
            match_threshold: 0.001,
            match_count: limit,
        });
        const error = response.error;
        const data = response.data as DocumentMatch[] | null;

        if (error) {
            // Specific check for missing migration or function
            if (error.code === 'PGRST202' || error.message.includes('function match_documents')) {
                console.warn('[VectorStore] Search Function Missing. Please run: 001_vector_store_setup.sql');
                return [];
            }
            console.error('[VectorStore] Search Error:', error);
            throw error;
        }

        const matches = data ?? [];
        return matches.map((match) => ({
            title: match.metadata?.title ?? 'Untitled',
            content: match.content,
            score: match.similarity,
            docId: match.metadata?.docId ?? String(match.id),
            type: match.metadata?.type ?? 'unknown',
        }));
    } catch (err: unknown) {
        console.error('[VectorStore] Retrieval Failed:', err instanceof Error ? err.message : String(err));
        return [];
    }
};

export const getDocumentById = (id: string) => {
    // Basic lookup from static knowledge base as fallback
    const doc = knowledgeBase.find((d) => d.id === id);
    if (!doc) return null;
    return { ...doc, score: 1.0, docId: doc.id };
};

export const purgeVectorStore = async () => {
    const { error } = await supabase.from('documents').delete().neq('id', 0);
    if (error) console.error('Purge Failed', error);
};
