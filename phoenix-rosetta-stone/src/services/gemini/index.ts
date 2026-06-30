import { GenerateContentResponse, Type } from '@google/genai';
import { useCoherenceStore } from '../../store/coherenceStore';
import { useTaskStore } from '../../store/taskStore';
import { GroundedResponse, GroundingSource, SystemContext } from '@essence/types';
import { commandRegistry } from '../commands/registry';
import { systemConfig } from '../configService';
import { generateAndPersistLog } from '../seltGenerator';
import { getGeminiClient, callGeminiWithRetry } from './client';
import { performHybridRetrieval } from './retrieval';
import { systemInstructions, formatSystemContext, NEURAL_LINK_INSTRUCTION } from './templates';

/**
 * @fileoverview Main entry point for the modular Gemini Service.
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

export const queryCognitiveCore = async (
    prompt: string,
    context?: SystemContext,
    image?: { data: string; mimeType: string },
): Promise<{ text: string; toolCall?: { name: string; args: Record<string, unknown> } }> => {
    if (!systemConfig.api.geminiKey) return { text: 'Gemini Service is not available. Please configure the API Key.' };

    const ai = getGeminiClient();
    const cognitiveFocus = useCoherenceStore.getState().cognitiveFocus;
    const baseInstruction = systemInstructions[cognitiveFocus];
    const activeContext = context ?? getFallbackContext();

    const { titles: retrievedTitles, content: ragContent } = await performHybridRetrieval(prompt);
    const ragInstruction = ragContent ? `\n\n[RAG_CONTEXT]\n${ragContent}\n[/RAG_CONTEXT]` : '';
    const contextInstruction = `\n\n${formatSystemContext(activeContext)}`;
    const finalSystemInstruction = baseInstruction + contextInstruction + ragInstruction;

    try {
        const contents: ({ text: string } | { inlineData: { data: string; mimeType: string } })[] = [{ text: prompt }];
        if (image) contents.push({ inlineData: { data: image.data, mimeType: image.mimeType } });

        const response: GenerateContentResponse = await callGeminiWithRetry(() =>
            ai.models.generateContent({
                model: 'gemini-2.0-flash-lite-001',
                contents: { parts: contents },
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

        void generateAndPersistLog(prompt, text, activeContext, retrievedTitles);
        return { text, toolCall: formattedToolCall };
    } catch (error) {
        console.error('Error querying Gemini API:', error);
        return { text: error instanceof Error ? `Error: ${error.message}` : 'An unknown error occurred.' };
    }
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

