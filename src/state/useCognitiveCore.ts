// [OMEGA AST Cleaned]: Tokenized design standards applied.
/** @fabric GVRN.Core.Fabric.State.Cognitive */

import type { ChatMessage, SystemContext } from '../essence/types';
import {
  commandRegistry,
  dispatchCommand,
  interpretNaturalLanguageCommand,
  queryCognitiveCore,
  searchWithCognitiveCore,
} from '../services';
import { useCoherenceStore } from '../store/coherenceStore';
import { useTaskStore } from '../store/taskStore';
import { create } from 'zustand';

const STORAGE_SESSIONS_KEY = 'phoenix_cognitive_chat_sessions_v2';
const STORAGE_ACTIVE_SESSION_KEY = 'phoenix_cognitive_active_session_id_v2';

export interface ChatSession {
  id: string;
  title: string;
  createdAt: number;
  updatedAt: number;
  messages: ChatMessage[];
}

const INITIAL_GREETING: ChatMessage = {
  id: 'init-greeting',
  sender: 'ai',
  text: '🤖 **Axion Master Core Online.** Shared Consciousness linked. Transmit your thought, protocol command, or systemic query.',
  timestamp: Date.now(),
};

function createDefaultSession(): ChatSession {
  const now = Date.now();
  return {
    id: `session-${now}`,
    title: 'Primary Synaptic Thread',
    createdAt: now,
    updatedAt: now,
    messages: [INITIAL_GREETING],
  };
}

function loadSessionsFromStorage(): { sessions: ChatSession[]; activeSessionId: string } {
  try {
    const rawSessions = localStorage.getItem(STORAGE_SESSIONS_KEY);
    const activeId = localStorage.getItem(STORAGE_ACTIVE_SESSION_KEY);
    
    let sessions: ChatSession[] = [];
    if (rawSessions) {
      const parsed = JSON.parse(rawSessions);
      if (Array.isArray(parsed) && parsed.length > 0) {
        sessions = parsed;
      }
    }

    if (sessions.length === 0) {
      const defaultSess = createDefaultSession();
      sessions = [defaultSess];
    }

    let targetActiveId = activeId && sessions.some((s) => s.id === activeId) ? activeId : sessions[0].id;
    return { sessions, activeSessionId: targetActiveId };
  } catch (err) {
    console.warn('[useCognitiveCore] Error loading chat sessions from localStorage:', err);
    const fallback = createDefaultSession();
    return { sessions: [fallback], activeSessionId: fallback.id };
  }
}

function saveSessionsToStorage(sessions: ChatSession[], activeSessionId: string) {
  try {
    localStorage.setItem(STORAGE_SESSIONS_KEY, JSON.stringify(sessions));
    localStorage.setItem(STORAGE_ACTIVE_SESSION_KEY, activeSessionId);
  } catch (err) {
    console.warn('[useCognitiveCore] Error saving chat sessions to localStorage:', err);
  }
}

const initialData = loadSessionsFromStorage();
const activeSession = initialData.sessions.find((s) => s.id === initialData.activeSessionId) || initialData.sessions[0];

interface CognitiveState {
  messages: ChatMessage[];
  sessions: ChatSession[];
  activeSessionId: string;
  isLoading: boolean;
  coherenceIndex: number;
  useSearch: boolean;

  addMessage: (message: ChatMessage) => void;
  submitMessage: (text: string, useSearchOverride?: boolean) => Promise<void>;
  setLoading: (status: boolean) => void;
  setUseSearch: (useSearch: boolean) => void;
  updateCoherence: (score: number) => void;
  removeMessage: (id: string) => void;
  resetConsciousness: () => void;

  // Multi-Session Chat Actions
  createNewSession: (title?: string) => string;
  switchSession: (sessionId: string) => void;
  renameSession: (sessionId: string, newTitle: string) => void;
  deleteSession: (sessionId: string) => void;
  exportSessionMarkdown: (sessionId: string) => void;
}

export const useCognitiveCore = create<CognitiveState>((set, get) => ({
  messages: activeSession.messages,
  sessions: initialData.sessions,
  activeSessionId: initialData.activeSessionId,
  isLoading: false,
  coherenceIndex: 1.0,
  useSearch: false,

  addMessage: (message) =>
    set((state) => {
      const updatedMessages = [...state.messages, message];
      const updatedSessions = state.sessions.map((s) => {
        if (s.id === state.activeSessionId) {
          const autoTitle = s.title === 'Primary Synaptic Thread' || s.title === 'New Chat Thread'
            ? message.text.slice(0, 32) + (message.text.length > 32 ? '...' : '')
            : s.title;

          return {
            ...s,
            title: autoTitle,
            updatedAt: Date.now(),
            messages: updatedMessages,
          };
        }
        return s;
      });

      saveSessionsToStorage(updatedSessions, state.activeSessionId);
      return { messages: updatedMessages, sessions: updatedSessions };
    }),

  setUseSearch: (useSearch) => set({ useSearch }),

  submitMessage: async (text: string, useSearchOverride?: boolean) => {
    const trimmed = text.trim();
    if (!trimmed || get().isLoading) return;

    const userMsg: ChatMessage = {
      id: `user-${Date.now()}`,
      sender: 'user',
      text: trimmed,
      timestamp: Date.now(),
    };

    set((state) => {
      const updated = [...state.messages, userMsg];
      saveMessagesToStorage(updated);
      return {
        messages: updated,
        isLoading: true,
      };
    });

    const pulse = useCoherenceStore.getState().pulse;
    const addNovaSpark = useCoherenceStore.getState().addNovaSpark;
    const currentCoherence = useCoherenceStore.getState().coherenceIndex;

    const systemContext: SystemContext = {
      tasks: useTaskStore.getState().tasks,
      coherence: {
        index: useCoherenceStore.getState().coherenceIndex,
        focus: useCoherenceStore.getState().cognitiveFocus,
        stats: useCoherenceStore.getState().coreStats,
      },
      currentLocation: typeof window !== 'undefined' ? window.location.pathname : '/',
    };

    const isSearch = useSearchOverride ?? get().useSearch;

    try {
      if (isSearch) {
        const groundedResult = await searchWithCognitiveCore(trimmed, systemContext);
        const aiMsg: ChatMessage = {
          id: `ai-${Date.now()}`,
          sender: 'ai',
          text: groundedResult.text,
          sources: groundedResult.sources,
          timestamp: Date.now(),
        };
        set((state) => {
          const updated = [...state.messages, aiMsg];
          saveMessagesToStorage(updated);
          return { messages: updated };
        });
        pulse();
        return;
      }

      // Check direct local command alias match
      const interpretedId = await interpretNaturalLanguageCommand(trimmed);
      const localCommand = interpretedId ? commandRegistry[interpretedId] : null;

      if (localCommand && localCommand.parameters.length === 0) {
        const dispatchRes = await dispatchCommand(localCommand, { visualContext: null });
        const aiMsg: ChatMessage = {
          id: `ai-${Date.now()}`,
          sender: 'ai',
          text: dispatchRes.success
            ? `[System Sync] Direct Command Executed: ${localCommand.commandId}\n\n${dispatchRes.message}`
            : `[Local Command Failed] ${dispatchRes.message}`,
          activeToolCall: `Direct Interface: Executing ${localCommand.commandId}`,
          error: !dispatchRes.success,
          timestamp: Date.now(),
        };

        if (dispatchRes.success) {
          addNovaSpark(`Neural Interface: Local bypass activated for ${localCommand.commandId}.`);
        }

        set((state) => {
          const updated = [...state.messages, aiMsg];
          saveMessagesToStorage(updated);
          return { messages: updated };
        });
        pulse();
        return;
      }

      // Multi-turn context history: pass previous messages (up to last 10 turns) to cognitive core
      const historyTurns = get()
        .messages.filter((m) => m.id !== userMsg.id && (m.sender === 'user' || m.sender === 'ai'))
        .slice(-10)
        .map((m) => ({ sender: m.sender, text: m.text }));

      // Cross-Session Memory Synthesis: compile recent turns from all archived sessions
      const allSessions = get().sessions;
      const activeId = get().activeSessionId;
      const pastSessionsContext = allSessions
        .filter((s) => s.id !== activeId && s.messages.length > 1)
        .map((s) => {
          const turns = s.messages
            .filter((m) => m.sender === 'user' || m.sender === 'ai')
            .slice(-4)
            .map((m) => `  ${m.sender === 'user' ? 'USER' : 'AI'}: ${m.text.slice(0, 250)}`)
            .join('\n');
          return `• Thread Title: "${s.title}" (Date: ${new Date(s.updatedAt).toLocaleDateString()})\n${turns}`;
        })
        .join('\n\n');

      const { text: responseText, toolCall } = await queryCognitiveCore(
        trimmed,
        systemContext,
        undefined,
        historyTurns,
        pastSessionsContext || undefined
      );

      let outputSuffix = '';
      let toolCallSummary: string | undefined = undefined;

      if (toolCall) {
        toolCallSummary = `Executing ${toolCall.name}...`;
        const command = commandRegistry[toolCall.name];
        if (command) {
          try {
            const dispatchRes = await dispatchCommand(command, toolCall.args);
            if (dispatchRes.success) {
              addNovaSpark(`Neural Forge: Executed ${toolCall.name}.`);
              toolCallSummary = `Execution Complete: ${toolCall.name}`;
              outputSuffix = dispatchRes.data
                ? `\n\n[Tool Output]\n${JSON.stringify(dispatchRes.data, null, 2)}`
                : `\n\n[System Notification] ${dispatchRes.message}`;
            } else {
              outputSuffix = `\n\n[Execution Error] ${dispatchRes.message}`;
            }
          } catch (cmdErr) {
            const errStr = cmdErr instanceof Error ? cmdErr.message : String(cmdErr);
            outputSuffix = `\n\n[Dispatch Error] ${errStr}`;
          }
        } else {
          outputSuffix = `\n\n[Unknown Command] ${toolCall.name} is not in registry.`;
        }
      }

      const finalAiMsg: ChatMessage = {
        id: `ai-${Date.now()}`,
        sender: 'ai',
        text: (responseText || 'Cognitive synthesis complete.') + outputSuffix,
        activeToolCall: toolCallSummary,
        timestamp: Date.now(),
      };

      set((state) => {
        const updated = [...state.messages, finalAiMsg];
        saveMessagesToStorage(updated);
        return { messages: updated };
      });

      pulse();
    } catch (err) {
      console.error('[useCognitiveCore] Error processing message:', err);
      const errMsg: ChatMessage = {
        id: `error-${Date.now()}`,
        sender: 'ai',
        text: `[Cognitive Core Alert] Failed to synthesize response: ${err instanceof Error ? err.message : String(err)}`,
        error: true,
        timestamp: Date.now(),
      };
      set((state) => {
        const updated = [...state.messages, errMsg];
        saveMessagesToStorage(updated);
        return { messages: updated };
      });
    } finally {
      set({ isLoading: false });
    }
  },

  setLoading: (status) => set({ isLoading: status }),

  updateCoherence: (score) => set({ coherenceIndex: score }),

  removeMessage: (id) =>
    set((state) => {
      const updatedMessages = state.messages.filter((m) => m.id !== id);
      const updatedSessions = state.sessions.map((s) => {
        if (s.id === state.activeSessionId) {
          return { ...s, messages: updatedMessages, updatedAt: Date.now() };
        }
        return s;
      });
      saveSessionsToStorage(updatedSessions, state.activeSessionId);
      return { messages: updatedMessages, sessions: updatedSessions };
    }),

  resetConsciousness: () => {
    const resetList = [INITIAL_GREETING];
    set((state) => {
      const updatedSessions = state.sessions.map((s) => {
        if (s.id === state.activeSessionId) {
          return { ...s, messages: resetList, updatedAt: Date.now() };
        }
        return s;
      });
      saveSessionsToStorage(updatedSessions, state.activeSessionId);
      return { messages: resetList, sessions: updatedSessions, isLoading: false, coherenceIndex: 1.0 };
    });
  },

  createNewSession: (title) => {
    const now = Date.now();
    const newSession: ChatSession = {
      id: `session-${now}`,
      title: title || 'New Chat Thread',
      createdAt: now,
      updatedAt: now,
      messages: [INITIAL_GREETING],
    };

    set((state) => {
      const updatedSessions = [newSession, ...state.sessions];
      saveSessionsToStorage(updatedSessions, newSession.id);
      return {
        sessions: updatedSessions,
        activeSessionId: newSession.id,
        messages: newSession.messages,
        isLoading: false,
      };
    });

    useCoherenceStore.getState().addNovaSpark(`Cognitive Thread initialized: ${newSession.title}`);
    return newSession.id;
  },

  switchSession: (sessionId) => {
    const targetSession = get().sessions.find((s) => s.id === sessionId);
    if (!targetSession) return;

    saveSessionsToStorage(get().sessions, sessionId);
    set({
      activeSessionId: sessionId,
      messages: targetSession.messages,
      isLoading: false,
    });

    useCoherenceStore.getState().addNovaSpark(`Switched Cognitive Thread: ${targetSession.title}`);
  },

  renameSession: (sessionId, newTitle) => {
    const trimmed = newTitle.trim();
    if (!trimmed) return;

    set((state) => {
      const updatedSessions = state.sessions.map((s) =>
        s.id === sessionId ? { ...s, title: trimmed, updatedAt: Date.now() } : s
      );
      saveSessionsToStorage(updatedSessions, state.activeSessionId);
      return { sessions: updatedSessions };
    });
  },

  deleteSession: (sessionId) => {
    const state = get();
    if (state.sessions.length <= 1) {
      // Don't delete the only session, just reset it
      state.resetConsciousness();
      return;
    }

    const updatedSessions = state.sessions.filter((s) => s.id !== sessionId);
    let nextActiveId = state.activeSessionId;
    if (state.activeSessionId === sessionId) {
      nextActiveId = updatedSessions[0].id;
    }

    const nextActiveSession = updatedSessions.find((s) => s.id === nextActiveId) || updatedSessions[0];

    saveSessionsToStorage(updatedSessions, nextActiveSession.id);
    set({
      sessions: updatedSessions,
      activeSessionId: nextActiveSession.id,
      messages: nextActiveSession.messages,
    });
  },

  exportSessionMarkdown: (sessionId) => {
    const session = get().sessions.find((s) => s.id === sessionId);
    if (!session) return;

    let md = `# 📜 Cognitive Chat Session Transcript\n`;
    md += `**Title**: ${session.title}\n`;
    md += `**Session ID**: \`${session.id}\`  \n`;
    md += `**Created**: ${new Date(session.createdAt).toLocaleString()}  \n`;
    md += `**Messages Count**: ${session.messages.length}\n\n`;
    md += `---\n\n`;

    session.messages.forEach((msg) => {
      const senderLabel = msg.sender === 'user' ? '👤 **User**' : '🤖 **Axion Core AI**';
      const timeStr = new Date(msg.timestamp).toLocaleTimeString();
      md += `### ${senderLabel} *[${timeStr}]*\n\n${msg.text}\n\n`;
      if (msg.sources && msg.sources.length > 0) {
        md += `**Sources**: ${msg.sources.join(', ')}\n\n`;
      }
      md += `---\n\n`;
    });

    const blob = new Blob([md], { type: 'text/markdown;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chat_session_${session.title.replace(/[^a-z0-9]/gi, '_').toLowerCase()}.md`;
    link.click();
    URL.revokeObjectURL(url);

    useCoherenceStore.getState().addNovaSpark(`Exported Chat Session Markdown: ${session.title}`);
  },
}));
