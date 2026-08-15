import {
  Database,
  Globe,
  Sparkles,
  Trash2,
  RotateCcw,
  Send,
  User,
  Cpu,
  Terminal,
  Volume2,
  VolumeX,
  Mic,
  MicOff,
  FolderKanban,
  Plus,
  Download,
  Edit3,
  Check,
  X,
  MessageSquare,
  ShieldCheck,
} from 'lucide-react';
import React, { useState, useEffect, useRef } from 'react';
import { useTheme } from '../hooks/useTheme';
import { createRecognitionSession, stopAuralResponse, transmitAuralResponse } from '../services/audioService';
import { useCognitiveCore } from '../state/useCognitiveCore';
import Tooltip from './common/Tooltip';

const Spinner: React.FC<{ color?: string }> = ({ color = 'cyan' }) => (
  <svg
    className={`animate-spin h-5 w-5 text-${color}-400`}
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
  >
    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
    <path
      className="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    ></path>
  </svg>
);

const QUICK_PROMPTS = [
  '⚔️ Where Light Fades: Kaelen & Shadow Self Arc',
  '🛡️ Serafina: Consecrated Circle & White Flame',
  '📜 Phoenix Codex Law 01 (Struggle)',
  '🔮 Eldrin: Inner World Transmutation in Act 2',
  '🏰 Brother Malakor & Architecture of Flesh',
];

const CognitiveInterface: React.FC = () => {
  const [prompt, setPrompt] = useState<string>('');
  const [activeSpeakingId, setActiveSpeakingId] = useState<string | null>(null);
  const [isRecording, setIsRecording] = useState<boolean>(false);
  const [autoSpeak, setAutoSpeak] = useState<boolean>(false);
  const [showSessionsDrawer, setShowSessionsDrawer] = useState<boolean>(false);
  const [editingSessionId, setEditingSessionId] = useState<string | null>(null);
  const [editingTitle, setEditingTitle] = useState<string>('');

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<ReturnType<typeof createRecognitionSession> | null>(null);
  const theme = useTheme();

  const messages = useCognitiveCore((state) => state.messages);
  const sessions = useCognitiveCore((state) => state.sessions);
  const activeSessionId = useCognitiveCore((state) => state.activeSessionId);
  const isLoading = useCognitiveCore((state) => state.isLoading);
  const useSearch = useCognitiveCore((state) => state.useSearch);
  const setUseSearch = useCognitiveCore((state) => state.setUseSearch);
  const submitMessage = useCognitiveCore((state) => state.submitMessage);
  const resetConsciousness = useCognitiveCore((state) => state.resetConsciousness);
  const removeMessage = useCognitiveCore((state) => state.removeMessage);

  const createNewSession = useCognitiveCore((state) => state.createNewSession);
  const switchSession = useCognitiveCore((state) => state.switchSession);
  const renameSession = useCognitiveCore((state) => state.renameSession);
  const deleteSession = useCognitiveCore((state) => state.deleteSession);
  const exportSessionMarkdown = useCognitiveCore((state) => state.exportSessionMarkdown);

  const activeSession = sessions.find((s) => s.id === activeSessionId);

  // Auto-scroll to bottom of chat feed when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });

    // Auto-speak latest AI response if autoSpeak mode is enabled
    if (autoSpeak && messages.length > 0 && !isLoading) {
      const lastMsg = messages[messages.length - 1];
      if (lastMsg.sender === 'ai' && lastMsg.id !== activeSpeakingId) {
        handleListen(lastMsg.id, lastMsg.text);
      }
    }
  }, [messages, isLoading, autoSpeak]);

  const handleListen = async (id: string, text: string) => {
    if (activeSpeakingId === id) {
      stopAuralResponse();
      setActiveSpeakingId(null);
      return;
    }

    stopAuralResponse();
    setActiveSpeakingId(id);
    await transmitAuralResponse(text);
  };

  const toggleRecording = () => {
    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
      return;
    }

    const session = createRecognitionSession(
      (transcript) => {
        setPrompt((prev) => (prev ? `${prev} ${transcript}` : transcript));
      },
      () => {
        setIsRecording(false);
      },
      (err) => {
        console.warn('[Aural Dictation] Speech error:', err);
        setIsRecording(false);
      }
    );

    if (session) {
      recognitionRef.current = session;
      session.start();
      setIsRecording(true);
    } else {
      alert('Speech Recognition is not supported by your browser.');
    }
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || isLoading) return;

    if (isRecording) {
      recognitionRef.current?.stop();
      setIsRecording(false);
    }

    const query = prompt;
    setPrompt('');
    await submitMessage(query);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      void handleFormSubmit(e as any);
    }
  };

  const handleQuickPrompt = (quickText: string) => {
    setPrompt(quickText);
  };

  const handleStartRename = (sessionId: string, currentTitle: string) => {
    setEditingSessionId(sessionId);
    setEditingTitle(currentTitle);
  };

  const handleSaveRename = (sessionId: string) => {
    if (editingTitle.trim()) {
      renameSession(sessionId, editingTitle.trim());
    }
    setEditingSessionId(null);
  };

  return (
    <div
      className={`w-full max-w-4xl p-4 md:p-6 border border-${theme.primary}-500/20 bg-black/40 backdrop-blur-lg rounded-xl shadow-2xl shadow-${theme.primary}-500/5 transition-all duration-500 flex flex-col gap-4 relative`}
    >
      {/* Header Bar */}
      <div className="flex flex-wrap items-center justify-between gap-3 border-b border-white/10 pb-3">
        <div className="flex items-center gap-2">
          <Cpu className={`text-${theme.primary}-400 animate-pulse`} size={18} />
          <div>
            <h3 className={`text-sm font-semibold tracking-widest text-${theme.primary}-300 uppercase font-mono flex flex-wrap items-center gap-2`}>
              Cognitive Chat & Aural Module
              <span className="text-[10px] text-cyan-400 font-normal px-2 py-0.5 bg-cyan-500/10 border border-cyan-500/30 rounded">
                {activeSession?.title || 'Active Thread'}
              </span>
              <span className="text-[10px] text-amber-400 font-mono px-2 py-0.5 bg-amber-500/10 border border-amber-500/30 rounded flex items-center gap-1">
                <ShieldCheck size={11} className="text-amber-400" /> Standard v15.1
              </span>
            </h3>
            <span className="text-[10px] text-white/40 font-mono">
              Sovereign Memory: {messages.length} message{messages.length === 1 ? '' : 's'} in current session
            </span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          {/* Chat Sessions Manager Drawer Toggle */}
          <Tooltip label="Saved Chat Sessions & History">
            <button
              type="button"
              onClick={() => setShowSessionsDrawer(!showSessionsDrawer)}
              className={`flex items-center gap-1.5 px-2.5 py-1 rounded text-xs font-mono transition-all border ${
                showSessionsDrawer
                  ? `bg-${theme.primary}-500/20 text-${theme.primary}-300 border-${theme.primary}-500/50 shadow-[0_0_10px_rgba(6,182,212,0.3)]`
                  : 'bg-black/40 text-gray-300 border-white/10 hover:border-white/20 hover:text-white'
              }`}
            >
              <FolderKanban size={13} className={`text-${theme.primary}-400`} />
              <span>Saved Chats ({sessions.length})</span>
            </button>
          </Tooltip>

          {/* New Chat Button */}
          <Tooltip label="Start a fresh chat session">
            <button
              type="button"
              onClick={() => {
                stopAuralResponse();
                setActiveSpeakingId(null);
                createNewSession();
              }}
              className="flex items-center gap-1 px-2.5 py-1 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 rounded text-cyan-300 text-xs font-mono transition-all hover:shadow-[0_0_8px_rgba(6,182,212,0.3)]"
            >
              <Plus size={13} />
              <span>New Chat</span>
            </button>
          </Tooltip>

          <Tooltip label="Export active session transcript as Markdown">
            <button
              type="button"
              onClick={() => exportSessionMarkdown(activeSessionId)}
              className="flex items-center gap-1 px-2 py-1 bg-white/5 hover:bg-white/10 border border-white/10 rounded text-gray-300 hover:text-white text-xs font-mono transition-all"
            >
              <Download size={13} />
              <span>Export</span>
            </button>
          </Tooltip>

          <Tooltip label="Automatically read aloud AI responses using Neural Voice">
            <label className="flex items-center gap-1.5 cursor-pointer text-xs text-white/60 hover:text-white transition-colors ml-1">
              <input
                type="checkbox"
                checked={autoSpeak}
                onChange={(e) => setAutoSpeak(e.target.checked)}
                className={`w-3.5 h-3.5 bg-black/40 border-${theme.primary}-500/50 text-${theme.primary}-400 rounded focus:ring-0`}
              />
              <Volume2 size={13} className={autoSpeak ? `text-${theme.primary}-400` : 'text-white/40'} />
              <span className="font-mono text-[11px]">Auto-Speak</span>
            </label>
          </Tooltip>

          <Tooltip label="Ground response in real-time web data via Google Search">
            <label className="flex items-center gap-1.5 cursor-pointer text-xs text-white/60 hover:text-white transition-colors">
              <input
                type="checkbox"
                checked={useSearch}
                onChange={(e) => setUseSearch(e.target.checked)}
                className={`w-3.5 h-3.5 bg-black/40 border-${theme.primary}-500/50 text-${theme.primary}-400 rounded focus:ring-0`}
              />
              <Globe size={13} className={useSearch ? `text-${theme.primary}-400` : 'text-white/40'} />
              <span className="font-mono text-[11px]">Search</span>
            </label>
          </Tooltip>
        </div>
      </div>

      {/* Saved Sessions Drawer / Panel */}
      {showSessionsDrawer && (
        <div className="w-full bg-black/80 border border-cyan-500/30 rounded-lg p-3 flex flex-col gap-3 animate-fade-in-sm">
          <div className="flex justify-between items-center border-b border-white/10 pb-2">
            <span className="text-xs font-mono font-bold text-cyan-300 uppercase tracking-widest flex items-center gap-2">
              <FolderKanban size={14} /> Saved Cognitive Threads ({sessions.length})
            </span>
            <button
              onClick={() => setShowSessionsDrawer(false)}
              className="text-gray-400 hover:text-white text-xs font-mono flex items-center gap-1"
            >
              <X size={14} /> Close Drawer
            </button>
          </div>

          <div className="max-h-56 overflow-y-auto space-y-2 pr-1 scrollbar-thin">
            {sessions.map((sess) => {
              const isActive = sess.id === activeSessionId;
              const isEditing = editingSessionId === sess.id;
              const lastMsgSnippet = sess.messages.length > 0 ? sess.messages[sess.messages.length - 1].text.slice(0, 50) + '...' : 'Empty session';

              return (
                <div
                  key={sess.id}
                  className={`p-2.5 rounded-lg border font-mono transition-all flex items-center justify-between gap-3 ${
                    isActive
                      ? 'bg-cyan-500/15 border-cyan-500/50 text-white shadow-[0_0_12px_rgba(6,182,212,0.2)]'
                      : 'bg-white/5 border-white/10 hover:border-white/20 text-gray-300'
                  }`}
                >
                  <div className="flex items-center gap-2 flex-1 min-w-0">
                    <MessageSquare size={14} className={isActive ? 'text-cyan-400' : 'text-gray-500'} />
                    <div className="flex-1 min-w-0">
                      {isEditing ? (
                        <div className="flex items-center gap-1">
                          <input
                            type="text"
                            value={editingTitle}
                            onChange={(e) => setEditingTitle(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSaveRename(sess.id)}
                            className="bg-black/60 border border-cyan-500/50 text-xs text-white px-2 py-0.5 rounded focus:outline-none w-full font-mono"
                            autoFocus
                          />
                          <button onClick={() => handleSaveRename(sess.id)} className="text-cyan-400 hover:text-cyan-300">
                            <Check size={14} />
                          </button>
                        </div>
                      ) : (
                        <>
                          <div className="flex items-center gap-2">
                            <span className="text-xs font-bold truncate">{sess.title}</span>
                            {isActive && <span className="text-[9px] px-1.5 py-0.2 bg-cyan-500/30 text-cyan-200 rounded">ACTIVE</span>}
                          </div>
                          <p className="text-[10px] text-gray-400 truncate leading-tight mt-0.5">{lastMsgSnippet}</p>
                        </>
                      )}
                    </div>
                  </div>

                  <div className="flex items-center gap-1.5 shrink-0">
                    {!isActive && (
                      <button
                        onClick={() => {
                          switchSession(sess.id);
                          setShowSessionsDrawer(false);
                        }}
                        className="px-2 py-1 bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-300 rounded text-[10px] tracking-wide"
                      >
                        Resume
                      </button>
                    )}

                    <button
                      onClick={() => handleStartRename(sess.id, sess.title)}
                      className="p-1 text-gray-400 hover:text-white transition-colors"
                      title="Rename Thread"
                    >
                      <Edit3 size={13} />
                    </button>

                    <button
                      onClick={() => exportSessionMarkdown(sess.id)}
                      className="p-1 text-gray-400 hover:text-white transition-colors"
                      title="Export Markdown"
                    >
                      <Download size={13} />
                    </button>

                    {sessions.length > 1 && (
                      <button
                        onClick={() => deleteSession(sess.id)}
                        className="p-1 text-red-400 hover:text-red-300 transition-colors"
                        title="Delete Session"
                      >
                        <Trash2 size={13} />
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Conversation Thread Feed */}
      <div className="w-full max-h-[460px] min-h-[220px] overflow-y-auto pr-2 space-y-4 font-mono scrollbar-thin scrollbar-thumb-white/10 select-text">
        {messages.map((msg) => {
          const isUser = msg.sender === 'user';
          const isSpeakingThisMsg = activeSpeakingId === msg.id;

          return (
            <div
              key={msg.id}
              className={`group flex flex-col gap-1 w-full animate-fade-in-sm ${
                isUser ? 'items-end' : 'items-start'
              }`}
            >
              {/* Message Meta Info */}
              <div className="flex items-center gap-2 text-[10px] text-white/40 px-1">
                {isUser ? (
                  <>
                    <span>{msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString() : ''}</span>
                    <span className="font-bold text-amber-400 flex items-center gap-1">
                      <User size={10} /> ARCHITECT
                    </span>
                  </>
                ) : (
                  <>
                    <span className={`font-bold text-${theme.primary}-400 flex items-center gap-1`}>
                      <Terminal size={10} /> AXION CORE
                    </span>
                    <span>{msg.timestamp ? new Date(msg.timestamp).toLocaleTimeString() : ''}</span>

                    {/* Listen Audio Button */}
                    <button
                      type="button"
                      onClick={() => handleListen(msg.id, msg.text)}
                      className={`flex items-center gap-1 text-[10px] px-2 py-0.5 rounded border font-mono transition-all ${
                        isSpeakingThisMsg
                          ? 'bg-cyan-500/20 border-cyan-400 text-cyan-200 animate-pulse shadow-[0_0_8px_rgba(34,211,238,0.5)]'
                          : 'bg-white/5 border-white/10 text-white/60 hover:text-white hover:bg-white/10'
                      }`}
                    >
                      {isSpeakingThisMsg ? <VolumeX size={11} /> : <Volume2 size={11} />}
                      <span>{isSpeakingThisMsg ? 'Stop Speech' : 'Listen'}</span>
                    </button>
                  </>
                )}

                <button
                  onClick={() => removeMessage(msg.id)}
                  className="opacity-0 group-hover:opacity-100 hover:text-red-400 transition-opacity ml-1"
                  title="Delete message from memory"
                >
                  <Trash2 size={10} />
                </button>
              </div>

              {/* Message Bubble */}
              <div
                className={`max-w-[88%] rounded-xl p-4 text-xs leading-relaxed font-sans shadow-lg ${
                  isUser
                    ? 'bg-amber-500/10 border border-amber-500/30 text-amber-100 rounded-tr-none'
                    : msg.error
                    ? 'bg-red-900/30 border border-red-500/40 text-red-200 rounded-tl-none'
                    : `bg-${theme.primary}-900/20 border border-${theme.primary}-500/20 text-${theme.primary}-100 rounded-tl-none`
                }`}
              >
                <div className="whitespace-pre-wrap select-text">{msg.text}</div>

                {/* Tool Call Notification */}
                {msg.activeToolCall && (
                  <div className="mt-3 p-2.5 bg-indigo-950/60 border border-indigo-500/30 rounded-md flex items-center gap-2 text-[11px] font-mono text-indigo-300">
                    <Sparkles size={13} className="text-indigo-400 animate-spin" />
                    <span>{msg.activeToolCall}</span>
                  </div>
                )}

                {/* Grounded Sources */}
                {msg.sources && msg.sources.length > 0 && (
                  <div className={`mt-3 pt-2.5 border-t border-${theme.primary}-500/15`}>
                    <div className="text-[10px] font-mono text-white/50 flex items-center gap-1 mb-1.5">
                      <Globe size={12} /> Grounded Sources:
                    </div>
                    <ul className="space-y-1">
                      {msg.sources.map((src, idx) => (
                        <li key={idx}>
                          <a
                            href={src.uri}
                            target="_blank"
                            rel="noopener noreferrer"
                            className={`text-[11px] text-${theme.primary}-400 hover:underline block truncate`}
                          >
                            [{idx + 1}] {src.title || src.uri}
                          </a>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          );
        })}

        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-center gap-3 p-3 bg-white/5 border border-white/10 rounded-lg max-w-sm text-xs font-mono text-cyan-300 animate-pulse">
            <Database size={14} className="animate-spin text-cyan-400" />
            <span>Synthesizing neural context & memory...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Quick Prompt Chips */}
      <div className="flex flex-wrap gap-2 pt-2">
        {QUICK_PROMPTS.map((qp, idx) => (
          <button
            key={idx}
            type="button"
            onClick={() => handleQuickPrompt(qp)}
            className={`text-[11px] font-mono px-2.5 py-1 bg-white/5 hover:bg-${theme.primary}-500/20 border border-white/10 hover:border-${theme.primary}-500/40 rounded-full text-white/70 hover:text-${theme.primary}-200 transition-all`}
          >
            {qp}
          </button>
        ))}
      </div>

      {/* Input Area */}
      <form onSubmit={(e) => void handleSubmit(e)} className="w-full flex flex-col gap-2">
        {isRecording && (
          <div className="flex items-center gap-2 text-xs font-mono text-red-300 animate-pulse px-1">
            <Mic size={14} className="text-red-400 animate-bounce" />
            <span>Aural Dictation Active: Speak now to dictate prompt...</span>
          </div>
        )}

        <div className="flex items-end gap-2 relative">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Transmit thought to Cognitive Core (Enter to send, Shift+Enter for new line)..."
            rows={2}
            className={`flex-1 bg-black/40 border border-${theme.primary}-500/30 rounded-lg p-3 text-sm text-${theme.primary}-100 placeholder-${theme.primary}-400/40 focus:outline-none focus:ring-2 focus:ring-${theme.primary}-400/60 transition-all resize-none font-sans`}
            disabled={isLoading}
          />

          {/* Voice Dictation Button */}
          <Tooltip label={isRecording ? 'Stop Voice Dictation' : 'Start Voice Dictation (Mic)'}>
            <button
              type="button"
              onClick={toggleRecording}
              className={`p-3.5 border rounded-lg font-mono text-xs transition-all ${
                isRecording
                  ? 'bg-red-500/20 border-red-400 text-red-300 animate-pulse shadow-[0_0_12px_rgba(239,68,68,0.5)]'
                  : 'bg-white/5 border-white/20 text-white/70 hover:text-white hover:bg-white/10'
              }`}
            >
              {isRecording ? <MicOff size={16} /> : <Mic size={16} />}
            </button>
          </Tooltip>

          {/* Transmit Button */}
          <Tooltip label="Transmit message (Enter)">
            <button
              type="submit"
              disabled={isLoading || !prompt.trim()}
              className={`flex items-center justify-center gap-2 px-5 py-3.5 bg-${theme.primary}-500/20 hover:bg-${theme.primary}-500/40 border border-${theme.primary}-400/50 rounded-lg text-${theme.primary}-200 font-mono text-xs disabled:opacity-40 disabled:cursor-not-allowed transition-all hover:drop-shadow-[0_0_10px_rgba(100,220,255,0.6)]`}
            >
              {isLoading ? <Spinner color={theme.primary} /> : <Send size={15} />}
            </button>
          </Tooltip>
        </div>
      </form>

      <style>{`
        @keyframes fade-in-sm {
          from { opacity: 0; transform: translateY(4px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-sm { animation: fade-in-sm 0.3s ease-out forwards; }
      `}</style>
    </div>
  );
};

export default CognitiveInterface;
