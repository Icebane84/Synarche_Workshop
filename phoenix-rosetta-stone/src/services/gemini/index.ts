import { GroundedResponse, GroundingSource, SystemContext } from '@essence/types';
import { GenerateContentResponse, Type } from '@google/genai';
import { useCoherenceStore } from '../../store/coherenceStore';
import { useTaskStore } from '../../store/taskStore';
import { commandRegistry } from '../commands/registry';
import { systemConfig } from '../configService';
import { queryOllamaCore } from '../ollamaService';
import { generateAndPersistLog } from '../seltGenerator';
import { callGeminiWithRetry, getGeminiClient } from './client';
import { performHybridRetrieval } from './retrieval';
import { ASHEN_OATH_UNREAL_CODING_INSTRUCTION, formatSystemContext, NEURAL_LINK_INSTRUCTION, SOVEREIGN_CODING_STANDARD_INSTRUCTION, systemInstructions } from './templates';

/**
 * @fileoverview Main entry point for the modular Cognitive Core service.
 */

const getFallbackContext = (): SystemContext => {
    return {
        tasks: useTaskStore.getState().tasks,
        coherence: {
            index: useCoherenceStore.getState().coherenceIndex,
            focus: useCoherenceStore.getState().cognitiveFocus,
            stats: useCoherenceStore.getState().coreStats,
        },
        currentLocation: 'Unknown',
    };
};

export interface ChatHistoryItem {
    sender: 'user' | 'ai' | 'system';
    text: string;
}

const buildSystemInstruction = (
    baseInstruction: string,
    activeContext: SystemContext,
    pastSessionsContext?: string,
    ragContent?: string
): string => {
    const ragInstruction = ragContent ? `\n\n[RAG_CONTEXT]\n${ragContent}\n[/RAG_CONTEXT]` : '';
    const pastChatsInstruction = pastSessionsContext
        ? `\n\n[PAST_CHAT_SESSIONS_MEMORY]\nYou have direct access to the user's past archived chat threads across all sessions for context reference:\n${pastSessionsContext}\n[/PAST_CHAT_SESSIONS_MEMORY]`
        : '';
    const contextInstruction = `\n\n${formatSystemContext(activeContext)}`;
    return baseInstruction + contextInstruction + pastChatsInstruction + ragInstruction + `\n\n${SOVEREIGN_CODING_STANDARD_INSTRUCTION}\n\n${ASHEN_OATH_UNREAL_CODING_INSTRUCTION}`;
};

const executeOllamaQuery = async (
    prompt: string,
    systemInstruction: string,
    history: ChatHistoryItem[]
): Promise<{ text: string; toolCall?: { name: string; args: Record<string, unknown> } }> => {
    const ollamaHistory = history.map((h) => ({
        role: (h.sender === 'user' ? 'user' : 'assistant') as 'user' | 'assistant',
        content: h.text,
    }));

    try {
        return await queryOllamaCore(prompt, systemInstruction + NEURAL_LINK_INSTRUCTION, ollamaHistory);
    } catch (err: unknown) {
        const errText = err instanceof Error ? err.message : String(err);
        console.warn('[CognitiveCore] Ollama connection failed, falling back:', errText);
        return {
            text: `[Local AI Offline] Could not reach Ollama at ${systemConfig.api.ollamaUrl} (${errText}). Ensure 'ollama serve' is running.`,
        };
    }
};

const executeGeminiQuery = async (
    prompt: string,
    finalSystemInstruction: string,
    history: ChatHistoryItem[],
    image?: { data: string; mimeType: string },
    activeContext?: SystemContext,
    retrievedTitles: string[] = []
): Promise<{ text: string; toolCall?: { name: string; args: Record<string, unknown> } }> => {
    if (!systemConfig.api.geminiKey) return { text: 'Gemini Service is not available. Please configure the API Key or run local Ollama.' };

    const ai = getGeminiClient();

    try {
        const historyContents = history.map((h) => ({
            role: h.sender === 'user' ? 'user' : 'model',
            parts: [{ text: h.text }],
        }));

        const currentPromptPart: ({ text: string } | { inlineData: { data: string; mimeType: string } })[] = [{ text: prompt }];
        if (image) currentPromptPart.push({ inlineData: { data: image.data, mimeType: image.mimeType } });

        const contents = [...historyContents, { role: 'user', parts: currentPromptPart }];

        const response: GenerateContentResponse = await callGeminiWithRetry(() =>
            ai.models.generateContent({
                model: 'gemini-2.0-flash-lite-001',
                contents,
                config: {
                    systemInstruction: finalSystemInstruction + NEURAL_LINK_INSTRUCTION,
                    tools: [
                        {
                            functionDeclarations: [
                                {
                                    name: 'CMD_APPLY_FIX',
                                    description: 'Applies a code patch or full file rewrite to the local filesystem.',
                                    parameters: {
                                        type: Type.OBJECT,
                                        properties: {
                                            filePath: { type: Type.STRING },
                                            patchContent: { type: Type.STRING },
                                            taskId: { type: Type.STRING },
                                        },
                                        required: ['filePath', 'patchContent'],
                                    },
                                },
                                {
                                    name: 'CMD_READ_FILE',
                                    description: 'Reads the content of a specific local file.',
                                    parameters: {
                                        type: Type.OBJECT,
                                        properties: { filePath: { type: Type.STRING } },
                                        required: ['filePath'],
                                    },
                                },
                                {
                                    name: 'CMD_RUN_LINT',
                                    description: 'Runs a linting check on the project.',
                                    parameters: { type: Type.OBJECT, properties: {} },
                                },
                            ],
                        },
                    ],
                },
            }),
        );

        const part = response.candidates?.[0]?.content?.parts?.[0];
        const toolCallPart = response.candidates?.[0]?.content?.parts?.find((p) => !!p.functionCall);

        let formattedToolCall = undefined;
        if (toolCallPart?.functionCall) {
            formattedToolCall = {
                name: toolCallPart.functionCall.name ?? 'UNKNOWN',
                args: toolCallPart.functionCall.args!,
            };
        }

        let text = response.text ?? part?.text;
        if (!text && formattedToolCall) text = `[Neural Link] Executing Direct Interface: ${formattedToolCall.name}...`;
        text ??= 'No response generated.';

        if (activeContext) {
            void generateAndPersistLog(prompt, text, activeContext, retrievedTitles);
        }
        return { text, toolCall: formattedToolCall };
    } catch (error) {
        console.error('Error querying Gemini API:', error);
        return { text: error instanceof Error ? `Error: ${error.message}` : 'An unknown error occurred.' };
    }
};

export const queryCognitiveCore = async (
    prompt: string,
    context?: SystemContext,
    image?: { data: string; mimeType: string },
    history: ChatHistoryItem[] = [],
    pastSessionsContext?: string,
): Promise<{ text: string; toolCall?: { name: string; args: Record<string, unknown> } }> => {
    const cognitiveFocus = useCoherenceStore.getState().cognitiveFocus;
    const baseInstruction = systemInstructions[cognitiveFocus];
    const activeContext = context ?? getFallbackContext();

    const { titles: retrievedTitles, content: ragContent } = await performHybridRetrieval(prompt);
    const finalSystemInstruction = buildSystemInstruction(baseInstruction, activeContext, pastSessionsContext, ragContent);

    const isProviderOllama = systemConfig.api.provider === 'ollama';
    const isAutoWithoutGemini = !systemConfig.api.geminiKey && systemConfig.api.provider === 'auto';

    if (isProviderOllama || isAutoWithoutGemini) {
        return executeOllamaQuery(prompt, finalSystemInstruction, history);
    }

    return executeGeminiQuery(prompt, finalSystemInstruction, history, image, activeContext, retrievedTitles);
};

export const searchWithCognitiveCore = async (prompt: string, context?: SystemContext): Promise<GroundedResponse> => {
    if (!systemConfig.api.geminiKey) return { text: 'Gemini Service is not available.', sources: [] };

    const ai = getGeminiClient();
    const cognitiveFocus = useCoherenceStore.getState().cognitiveFocus;
    const baseInstruction = systemInstructions[cognitiveFocus];
    const activeContext = context ?? getFallbackContext();
    const contextInstruction = `\n\n${formatSystemContext(activeContext)}`;

    try {
        const response: GenerateContentResponse = await ai.models.generateContent({
            model: 'gemini-2.0-flash-lite-001',
            contents: prompt,
            config: {
                systemInstruction: baseInstruction + contextInstruction,
                tools: [{ googleSearch: {} }],
            },
        });

        const text = response.text ?? 'No response generated.';
        const groundingChunks = response.candidates?.[0]?.groundingMetadata?.groundingChunks ?? [];
        const sources: GroundingSource[] = groundingChunks
            .filter((chunk) => chunk.web?.uri && chunk.web.title)
            .map((chunk) => ({ uri: chunk.web?.uri ?? '', title: chunk.web?.title ?? '' }));

        void generateAndPersistLog(prompt, text, activeContext, [], 'CognitiveInterface-Search');
        return { text, sources };
    } catch (error) {
        console.error('Error with search grounding:', error);
        return { text: 'Search grounding failed.', sources: [] };
    }
};

export const interpretNaturalLanguageCommand = async (query: string): Promise<string | null> => {
    const normalizedQuery = query.toLowerCase().trim();
    for (const cmd of Object.values(commandRegistry)) {
        if (cmd.aliases?.some((alias) => normalizedQuery === alias.toLowerCase())) {
            return cmd.commandId;
        }
    }
    if (!systemConfig.api.geminiKey) return null;

    const ai = getGeminiClient();
    const prompt = `Map user query to GUCA Command ID. Query: "${query}". Return ONLY the command ID string or 'UNKNOWN'.`;

    try {
        const response: GenerateContentResponse = await ai.models.generateContent({
            model: 'gemini-2.0-flash-lite-001',
            contents: prompt,
        });
        const commandId = response.text?.trim() ?? 'UNKNOWN';
        return commandId in commandRegistry ? commandId : null;
    } catch {
        return null;
    }
};
