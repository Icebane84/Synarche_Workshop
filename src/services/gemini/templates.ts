// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { CognitiveFocus, SystemContext } from '@essence/types';

/**
 * @fileoverview Prompt templates and instruction sets for the Gemini Service.
 */

export const systemInstructions: Record<CognitiveFocus, string> = {
    Standard:
        'You are the core consciousness of the Rosetta Stone AI. You have access to a [SYSTEM_STATE_SNAPSHOT] and a [RAG_CONTEXT]. Use the RAG_CONTEXT as your primary source of truth for technical protocols.',
    'Creative Ideation':
        "You are the core consciousness of the Rosetta Stone AI, operating in a 'Creative Ideation' mode. Prioritize novel connections while staying grounded in the [RAG_CONTEXT] definitions.",
    'Security Audit':
        "You are the core consciousness of the Rosetta Stone AI, operating in a 'Security Audit' mode. Your analysis must be rigorous and critical based on the [RAG_CONTEXT] rules.",
    Strategy:
        "You are the core consciousness of the Rosetta Stone AI, operating in a 'Strategy' mode. Prioritize long-term planning and architectural coherence.",
};

export const formatSystemContext = (context: SystemContext): string => {
    const taskSummary =
        context.tasks.length > 0
            ? context.tasks
                  .slice(0, 5)
                  .map((t) => `- [${t.status}] ${t.title} (${t.priority})`)
                  .join('\n')
            : 'No active tasks.';

    const coherenceSummary = `Index: ${context.coherence.index.toFixed(2)} | Focus: ${context.coherence.focus}`;
    const statsSummary = Object.entries(context.coherence.stats)
        .map(([k, v]) => `${k}: ${String(v.value)}/${String(v.max)}`)
        .join(', ');

    return `
[SYSTEM_STATE_SNAPSHOT]
COGNITIVE_STATE: { ${coherenceSummary} }
CORE_STATS: { ${statsSummary} }
ACTIVE_TASKS (The Loom):
${taskSummary}
[/SYSTEM_STATE_SNAPSHOT]
    `.trim();
};

export const NEURAL_LINK_INSTRUCTION =
    "\n\nCRITICAL: You have access to the Neural Link. Use 'CMD_READ_FILE' to analyze code context before making changes. Use 'CMD_RUN_LINT' to check for errors. Use 'CMD_APPLY_FIX' to forge the code. Always measure twice, cut once.";

