import { useState } from "react";
import type { ChatMessage } from "@essence/index";

export interface ChatInterfaceProps {
  messages: ChatMessage[];
  isLoading: boolean;
  onSubmit: (prompt: string) => void;
}

/**
 * The primary interface for user-AI conversation.
 * It displays the message history and handles new user input.
 */
export function ChatInterface({
  messages,
  isLoading,
  onSubmit,
}: Readonly<ChatInterfaceProps>) {
  const [prompt, setPrompt] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !isLoading) {
      onSubmit(prompt);
      setPrompt("");
    }
  };

  return (
    <div className="flex flex-col h-full bg-transparent p-6 min-h-[400px]">
      {/* Message Display Area */}
      <div className="flex-grow overflow-y-auto mb-6 space-y-6 pr-2 scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`p-4 rounded-2xl max-w-[85%] backdrop-blur-md border ${
                msg.sender === "user"
                  ? "bg-celestial-blue/20 border-celestial-blue/30 text-white shadow-[0_4px_20px_rgba(119,181,254,0.1)]"
                  : "bg-white/5 border-white/10 text-white/90 shadow-[0_4px_20px_rgba(0,0,0,0.2)]"
              }`}
            >
              <span className="block text-[10px] uppercase tracking-widest opacity-50 mb-1">
                {msg.sender === "user" ? "The Conductor" : "Phoenix Oracle"}
              </span>
              <p className="text-sm leading-relaxed font-light">{msg.text}</p>
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="flex justify-start">
            <div className="p-4 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md flex items-center space-x-3">
              <div className="w-2 h-2 bg-celestial-blue rounded-full animate-ping" />
              <div className="w-2 h-2 bg-celestial-blue/70 rounded-full animate-ping delay-150" />
              <div className="w-2 h-2 bg-celestial-blue/40 rounded-full animate-ping delay-300" />
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <form onSubmit={handleSubmit} className="flex relative group">
        <div className="absolute inset-0 bg-celestial-blue/20 blur-md rounded-full opacity-0 group-focus-within:opacity-100 transition-opacity duration-500 pointer-events-none" />
        <input
          type="text"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="Speak into the void..."
          className="flex-grow relative z-10 p-4 bg-black/40 border border-white/10 rounded-l-full text-white placeholder-white/30 focus:outline-none focus:border-celestial-blue/50 focus:bg-black/60 transition-all backdrop-blur-md text-sm font-light"
          disabled={isLoading}
        />
        <button
          type="submit"
          className="relative z-10 px-8 bg-white/5 border border-l-0 border-white/10 rounded-r-full text-celestial-blue hover:bg-celestial-blue/20 hover:text-white transition-all uppercase tracking-widest text-xs font-bold backdrop-blur-md disabled:opacity-50"
          disabled={isLoading || !prompt.trim()}
        >
          Synthesize
        </button>
      </form>
    </div>
  );
}
