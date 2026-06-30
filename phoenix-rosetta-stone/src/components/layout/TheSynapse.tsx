import React, { useEffect, useRef, useState } from "react";
import { useSynapseLogic, CommandDefinition } from "@hooks/useSynapseLogic";

interface TheSynapseProps {
  isOpen: boolean;
  onClose: () => void;
}

export const TheSynapse: React.FC<TheSynapseProps> = ({ isOpen, onClose }) => {
  const inputRef = useRef<HTMLInputElement>(null);
  
  const {
    searchQuery,
    setSearchQuery,
    selectedIndex,
    setSelectedIndex,
    commandForParams,
    setCommandForParams,
    isFiring,
    commandResult,
    filteredCommands,
    executeCommand,
    handleSelectCommand,
    resetState,
  } = useSynapseLogic({
    onClose,
    onSuccess: (msg) => {
      // Allow user to view result, reset is handled by closing or clicking Done
    },
  });

  const handleClose = () => {
    resetState();
    onClose();
  };

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 100);
    }
  }, [isOpen]);

  // Handle hotkeys (ArrowUp, ArrowDown, Enter, Escape)
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") {
      e.preventDefault();
      setSelectedIndex((prev) => Math.min(prev + 1, filteredCommands.length - 1));
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setSelectedIndex((prev) => Math.max(prev - 1, 0));
    } else if (e.key === "Enter") {
      e.preventDefault();
      if (filteredCommands[selectedIndex]) {
        handleSelectCommand(filteredCommands[selectedIndex]);
      }
    } else if (e.key === "Escape") {
      handleClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh] px-4 animate-appear">
      {/* Dimmed backdrop */}
      <div className="fixed inset-0 bg-black/70 backdrop-blur-sm" onClick={handleClose} />

      {/* Main Panel */}
      <div className="relative w-full max-w-3xl bg-zinc-950/95 border border-white/10 rounded-xl shadow-2xl flex flex-col overflow-hidden h-[450px]">
        {commandResult ? (
          // Result screen
          <div className="flex-1 flex flex-col justify-center items-center p-8 text-center font-mono">
            <div className={`w-12 h-12 rounded-full flex items-center justify-center border-2 mb-4 ${commandResult.success ? "border-emerald-500 bg-emerald-500/10 text-emerald-400" : "border-rose-500 bg-rose-500/10 text-rose-400"}`}>
              {commandResult.success ? (
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <polyline points="20 6 9 17 4 12" />
                </svg>
              ) : (
                <svg className="w-6 h-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <line x1="18" y1="6" x2="6" y2="18" />
                  <line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              )}
            </div>
            <h3 className="text-sm font-bold tracking-widest text-white uppercase mb-2">
              {commandResult.success ? "DIRECTIVE MANIFESTED" : "SYNAPSE FAULT"}
            </h3>
            <p className="text-xs text-white/70 max-w-md leading-relaxed mb-6">
              {commandResult.message}
            </p>
            <button
              onClick={handleClose}
              className="px-6 py-2 bg-white/10 hover:bg-white/20 text-white rounded text-xs tracking-widest uppercase transition-colors cursor-pointer"
            >
              DONE
            </button>
          </div>
        ) : commandForParams ? (
          // Parameter Weaver Form
          <ParameterWeaverForm
            command={commandForParams}
            onSubmit={(p) => executeCommand(commandForParams, p)}
            onCancel={() => setCommandForParams(null)}
          />
        ) : (
          // Standard Search list
          <div className="flex-1 flex h-full">
            {/* Left list panel */}
            <div className="flex-1 flex flex-col border-r border-white/5">
              <div className="p-3 border-b border-white/5 flex items-center gap-2">
                {isFiring ? (
                  <div className="w-4 h-4 border-2 border-amber-500 border-t-transparent rounded-full animate-spin" />
                ) : (
                  <svg className="w-4 h-4 text-white/40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                    <circle cx="11" cy="11" r="8" />
                    <line x1="21" y1="21" x2="16.65" y2="16.65" />
                  </svg>
                )}
                <input
                  ref={inputRef}
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Transmit directive..."
                  className="flex-1 bg-transparent border-none outline-none text-xs text-white placeholder-white/20 font-mono"
                />
              </div>

              {/* Suggestions */}
              <div className="flex-1 overflow-y-auto p-2 space-y-1 scrollbar-thin">
                {filteredCommands.map((cmd, idx) => {
                  const isSelected = idx === selectedIndex;
                  return (
                    <button
                      key={cmd.commandId}
                      onClick={() => handleSelectCommand(cmd)}
                      className={`w-full text-left px-3 py-2.5 rounded-lg flex items-center justify-between group transition-all duration-150 cursor-pointer ${
                        isSelected ? "bg-white/10 text-white" : "text-white/50 hover:bg-white/5 hover:text-white"
                      }`}
                    >
                      <div className="flex flex-col gap-0.5">
                        <span className="font-mono text-xs font-bold">{cmd.commandId}</span>
                        <span className="text-[10px] opacity-65 group-hover:opacity-100 truncate max-w-[360px]">
                          {cmd.description}
                        </span>
                      </div>
                      <span className="text-[9px] font-mono opacity-40 group-hover:opacity-100 uppercase tracking-widest px-2 py-0.5 rounded bg-white/5 border border-white/5">
                        {cmd.category}
                      </span>
                    </button>
                  );
                })}
                {filteredCommands.length === 0 && (
                  <div className="p-8 text-center text-xs text-white/20 italic font-mono">
                    No directives found matching query.
                  </div>
                )}
              </div>
            </div>

            {/* Right preview panel */}
            <div className="w-[280px] bg-black/20 p-4 flex flex-col justify-between font-mono text-left">
              <div>
                <h4 className="text-[9px] font-bold text-white/30 uppercase tracking-widest mb-3">Directive Preview</h4>
                {filteredCommands[selectedIndex] ? (
                  <div className="space-y-4">
                    <div>
                      <span className="text-xs font-bold text-amber-400 block">{filteredCommands[selectedIndex].commandId}</span>
                      <span className="text-[8px] bg-white/5 px-1.5 py-0.5 rounded border border-white/5 text-white/50 uppercase mt-1 inline-block">
                        {filteredCommands[selectedIndex].category}
                      </span>
                    </div>
                    <div>
                      <span className="text-[9px] text-white/30 uppercase block mb-1">Synopsis</span>
                      <p className="text-[11px] text-white/70 leading-relaxed">
                        {filteredCommands[selectedIndex].description}
                      </p>
                    </div>
                    {filteredCommands[selectedIndex].parameters.length > 0 && (
                      <div>
                        <span className="text-[9px] text-white/30 uppercase block mb-1">Parameters</span>
                        <div className="space-y-1">
                          {filteredCommands[selectedIndex].parameters.map((p) => (
                            <div key={p.name} className="text-[10px] text-white/60">
                              <span className="text-amber-300 font-bold">{p.name}</span>: <span className="opacity-50">{p.type}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-xs text-white/20 italic">Select a directive from the stream.</p>
                )}
              </div>
              <div className="text-[8px] text-white/20 border-t border-white/5 pt-3">
                KEYBOARD: ARROWS (NAV) / ENTER (EXEC)
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

interface ParameterWeaverFormProps {
  command: CommandDefinition;
  onSubmit: (params: Record<string, any>) => void;
  onCancel: () => void;
}

const ParameterWeaverForm: React.FC<ParameterWeaverFormProps> = ({ command, onSubmit, onCancel }) => {
  const [values, setValues] = useState<Record<string, any>>(() => {
    const initial: Record<string, any> = {};
    command.parameters.forEach((p) => {
      initial[p.name] = p.defaultValue ?? "";
    });
    return initial;
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(values);
  };

  return (
    <form onSubmit={handleSubmit} className="flex-1 flex flex-col justify-between p-6 font-mono text-left">
      <div>
        <h3 className="text-xs font-bold text-amber-400 mb-1">{command.commandId}</h3>
        <p className="text-[10px] text-white/40 mb-4 uppercase tracking-widest">Weave execution parameters</p>

        <div className="space-y-4 max-w-md">
          {command.parameters.map((p) => (
            <div key={p.name} className="flex flex-col gap-1.5">
              <label className="text-[11px] font-bold text-white/70 flex justify-between">
                <span>{p.name}</span>
                <span className="opacity-40">{p.type}</span>
              </label>
              <input
                type={p.type === "number" ? "number" : "text"}
                step={p.type === "number" ? "0.01" : undefined}
                value={values[p.name]}
                onChange={(e) => {
                  const val = p.type === "number" ? parseFloat(e.target.value) : e.target.value;
                  setValues((prev) => ({ ...prev, [p.name]: val }));
                }}
                className="w-full bg-white/5 border border-white/10 rounded px-3 py-1.5 text-xs text-white outline-none focus:border-amber-500/50 transition-colors"
                placeholder={p.description}
                required
              />
              <span className="text-[9px] text-white/40">{p.description}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end gap-3 border-t border-white/5 pt-4 mt-6">
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 border border-white/10 text-white/60 hover:text-white rounded text-xs tracking-wider transition-colors cursor-pointer"
        >
          CANCEL
        </button>
        <button
          type="submit"
          className="px-4 py-2 bg-amber-500/20 border border-amber-500/40 text-amber-300 hover:bg-amber-500/30 rounded text-xs tracking-wider transition-colors cursor-pointer"
        >
          MANIFEST DIRECTIVE
        </button>
      </div>
    </form>
  );
};
