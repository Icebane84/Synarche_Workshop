// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { useKnowledgeStore } from '../../store/knowledgeStore';
import { useTaskStore } from '../../store/taskStore';
import { retrieveContext } from '../vectorStore';

/**
 * @fileoverview Hybrid RAG retrieval logic for the Cognitive Core.
 */

export const performHybridRetrieval = async (query: string) => {
    const { isSimulationMode } = useTaskStore.getState();

    if (isSimulationMode) {
        const localResults = await retrieveContext(query, 3);
        if (localResults.length > 0) {
            return {
                titles: localResults.map((r) => r.title),
                content: localResults.map((r) => `[Source: ${r.title}]\n${r.content}`).join('\n\n'),
            };
        }
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
        const localMatches = useKnowledgeStore.getState().searchDocuments(query).slice(0, 3);

        return {
            titles: localMatches.map((d) => d.title),
            content: localMatches.map((d) => `[Local Knowledge Base: ${d.title}]\n${d.content}`).join('\n\n'),
        };
    }
};
