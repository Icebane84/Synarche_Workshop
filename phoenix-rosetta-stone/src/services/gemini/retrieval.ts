import { knowledgeBase } from '../../data/knowledgeBase';
import { useTaskStore } from '../../store/taskStore';
import { retrieveContext } from '../vectorStore';

/**
 * @fileoverview Hybrid RAG retrieval logic for the Gemini Service.
 */

export const performHybridRetrieval = async (query: string) => {
    const { isSimulationMode } = useTaskStore.getState();

    if (isSimulationMode) {
        const localResults = await retrieveContext(query, 3);
        return {
            titles: localResults.map((r) => r.title),
            content: localResults.map((r) => `[Source: ${r.title}]\n${r.content}`).join('\n\n'),
        };
    }

    try {
        const docResults = await retrieveContext(query, 3);
        if (docResults.length > 0) {
            return {
                titles: docResults.map((r) => r.title),
                content: docResults.map((r) => `[Vector Source: ${r.title}]\n${r.content}`).join('\n\n'),
            };
        }
        throw new Error('Vector Store Empty'); // Trigger fallback
    } catch {
        const lowerQuery = query.toLowerCase();
        const keywords = lowerQuery.split(/\s+/).filter((k) => k.length > 3);
        const localMatches = knowledgeBase
            .filter((doc) => {
                const lowerContent = doc.content.toLowerCase();
                const lowerTitle = doc.title.toLowerCase();
                return lowerTitle.includes(lowerQuery) || keywords.some((k) => lowerContent.includes(k));
            })
            .slice(0, 2);

        return {
            titles: localMatches.map((d) => d.title),
            content: localMatches.map((d) => `[Local Fallback: ${d.title}]\n${d.content}`).join('\n\n'),
        };
    }
};
