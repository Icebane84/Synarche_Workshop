import { systemConfig } from './configService';

export interface ToolCall {
  name: string;
  args: Record<string, unknown>;
}

export interface OllamaChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface OllamaQueryResponse {
  text: string;
  toolCall?: ToolCall;
}

/**
 * Queries local Ollama instance (e.g. Llama 3.1 8B, Qwen2.5-Coder 7B).
 * Supports RAG context, system instructions, conversation history, and tool calling via JSON structure parsing.
 */
export async function queryOllamaCore(
  prompt: string,
  systemInstruction: string,
  history: OllamaChatMessage[] = [],
  modelName: string = systemConfig.api.ollamaModel || 'llama3.1:8b',
  baseUrl: string = systemConfig.api.ollamaUrl || 'http://localhost:11434',
): Promise<OllamaQueryResponse> {
  const toolInstruction = `
You are Axion, the Sovereign Master Artificer of the Synarche.
You have access to the following local commands if action is required:
1. CMD_APPLY_FIX: {"name": "CMD_APPLY_FIX", "args": {"filePath": "...", "patchContent": "...", "taskId": "..."}}
2. CMD_READ_FILE: {"name": "CMD_READ_FILE", "args": {"filePath": "..."}}
3. CMD_RUN_LINT: {"name": "CMD_RUN_LINT", "args": {}}

If you invoke a command, output a valid JSON object block on its own line:
TOOL_CALL: {"name": "...", "args": {...}}
`;

  const fullSystemMessage = systemInstruction + '\n\n' + toolInstruction;

  const messagesPayload: OllamaChatMessage[] = [
    { role: 'system', content: fullSystemMessage },
    ...history,
    { role: 'user', content: prompt },
  ];

  try {
    const response = await fetch(`${baseUrl}/api/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        model: modelName,
        messages: messagesPayload,
        stream: false,
        options: {
          temperature: 0.3,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Ollama HTTP Error ${response.status}: ${await response.text()}`);
    }

    const data = await response.json();
    const rawText: string = data.message?.content || '';

    // Check for TOOL_CALL pattern in model output
    let toolCall: ToolCall | undefined;
    const toolCallMatch = rawText.match(/TOOL_CALL:\s*(\{.*\})/);
    if (toolCallMatch) {
      try {
        toolCall = JSON.parse(toolCallMatch[1]);
      } catch {
        // Ignore parse errors if model emitted malformed tool call
      }
    }

    const cleanText = rawText.replace(/TOOL_CALL:\s*\{.*\}/g, '').trim();

    return {
      text: cleanText || rawText,
      toolCall,
    };
  } catch (err: unknown) {
    const errorMsg = err instanceof Error ? err.message : String(err);
    console.error('[Ollama Service] Error querying local LLM:', errorMsg);
    throw err;
  }
}
