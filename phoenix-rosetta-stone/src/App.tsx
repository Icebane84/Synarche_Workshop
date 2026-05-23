import { useCognitiveCore } from "@nexus/useCognitiveCore";
import { ChatInterface } from "@fabric/ChatInterface/ChatInterface";
import { PhoenixGeode } from "@fabric/PhoenixGeode/PhoenixGeode";

/**
 * The Celestial Chart Layout (App Root)
 * Implements the 3-column architectural blueprint with a bottom status bar.
 */
export default function App() {
  const { messages, isLoading, coherenceIndex, submitMessage } =
    useCognitiveCore();

  const handleUserSubmit = (prompt: string) => {
    submitMessage(prompt);
  };

  return (
    <div className="h-screen w-screen flex flex-col bg-nebula-void text-white overflow-hidden selection:bg-celestial-blue/30">
      {/* Main 3-Panel View */}
      <div className="flex-1 flex flex-row overflow-hidden p-6 gap-6">
        {/* Left Panel: Ascension Chronicle (Tarot Card Form) */}
        <aside className="w-1/4 h-full relative rounded-2xl border border-white/10 p-6 flex flex-col backdrop-blur-xl bg-black/40 shadow-2xl transition-all duration-500 hover:shadow-[0_0_40px_rgba(119,181,254,0.15)] hover:-translate-y-1 group overflow-hidden">
          {/* Holographic foil overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-celestial-blue/10 via-transparent to-purple-500/10 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none z-0" />

          <header className="mb-8 relative z-10 border-b border-white/10 pb-4">
            <h2 className="text-sm font-light tracking-[0.3em] text-white/50 uppercase mb-2">
              The Chronicle
            </h2>
            <h3 className="text-3xl font-light tracking-widest text-white/90 uppercase">
              Prestige{" "}
              <span className="font-bold text-celestial-blue drop-shadow-[0_0_8px_rgba(119,181,254,0.5)]">
                IV
              </span>
            </h3>
          </header>

          <div className="flex-1 space-y-8 relative z-10">
            <div className="space-y-3">
              <div className="flex justify-between text-xs text-white/50 uppercase tracking-[0.2em]">
                <span>Experience</span>
                <span>4,200 / 5,000</span>
              </div>
              <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
                <div className="h-full bg-gradient-to-r from-celestial-blue to-purple-500 w-[84%] shadow-[0_0_12px_rgba(119,181,254,0.8)]" />
              </div>
            </div>

            <div className="p-6 rounded-xl border border-white/10 bg-gradient-to-b from-white/5 to-transparent flex flex-col items-center justify-center space-y-3 shadow-lg relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-starlight-yellow/50 to-transparent" />
              <span className="text-xs uppercase tracking-[0.3em] text-white/50">
                Stardust
              </span>
              <span className="text-5xl font-bold text-starlight-yellow drop-shadow-[0_0_15px_rgba(240,230,140,0.6)]">
                320
              </span>
            </div>
          </div>
        </aside>

        {/* Center Panel: Phoenix Star & Chat */}
        <main className="flex-1 h-full flex flex-col relative z-10 rounded-2xl border border-white/5 bg-black/20 shadow-2xl overflow-hidden backdrop-blur-md">
          {/* Conceptual Geode Representation (Top Half) */}
          <div className="flex-1 flex flex-col items-center justify-center relative border-b border-white/10 bg-gradient-to-b from-transparent to-black/40">
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
              {/* Decorative radial glow for the Geode */}
              <div
                className="w-[400px] h-[400px] bg-celestial-blue/5 rounded-full blur-[100px] transition-opacity duration-1000"
                style={{ opacity: coherenceIndex }}
              />
            </div>

            {/* The Phoenix Geode D3 Visualization */}
            <div className="w-72 h-72 relative flex items-center justify-center">
              <div className="absolute inset-0 z-0">
                <PhoenixGeode coherenceIndex={coherenceIndex} />
              </div>
              <div className="z-10 text-center pointer-events-none">
                <span className="block text-xs uppercase tracking-[0.3em] text-celestial-blue/80 mb-1 drop-shadow-md">
                  Coherence
                </span>
                <span className="text-4xl font-extralight drop-shadow-xl">
                  {(coherenceIndex * 100).toFixed(1)}%
                </span>
              </div>
            </div>
          </div>

          {/* Scriptorium (Chat Interface) */}
          <div className="h-[45%] bg-black/40 backdrop-blur-xl border-t border-white/5 relative z-20">
            <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-celestial-blue/30 to-transparent" />
            <ChatInterface
              messages={messages}
              isLoading={isLoading}
              onSubmit={handleUserSubmit}
            />
          </div>
        </main>

        {/* Right Panel: Axiom Skill Tree (Tarot Card Form) */}
        <aside className="w-1/4 h-full relative rounded-2xl border border-white/10 p-6 flex flex-col backdrop-blur-xl bg-black/40 shadow-2xl transition-all duration-500 hover:shadow-[0_0_40px_rgba(119,181,254,0.15)] hover:-translate-y-1 group overflow-hidden">
          {/* Holographic foil overlay */}
          <div className="absolute inset-0 bg-gradient-to-tl from-coherence-indigo/10 via-transparent to-synergy-emerald/10 opacity-0 group-hover:opacity-100 transition-opacity duration-700 pointer-events-none z-0" />

          <header className="mb-8 relative z-10 border-b border-white/10 pb-4">
            <h2 className="text-sm font-light tracking-[0.3em] text-white/50 uppercase mb-2">
              The Axiom
            </h2>
            <h3 className="text-2xl font-light tracking-widest text-white/90 uppercase">
              Skill Tree
            </h3>
          </header>

          <div className="flex-1 space-y-10 relative z-10">
            {/* Core Stats */}
            <div className="space-y-8">
              <div className="group/stat cursor-pointer">
                <div className="flex justify-between items-end mb-3">
                  <span className="text-xs font-bold uppercase tracking-[0.2em] text-coherence-indigo group-hover/stat:text-white transition-colors duration-300">
                    Coherence
                  </span>
                  <span className="text-[10px] uppercase tracking-widest text-white/40">
                    Lvl 12
                  </span>
                </div>
                <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
                  <div
                    className="h-full bg-coherence-indigo group-hover/stat:shadow-[0_0_12px_#4F46E5] group-hover/stat:bg-white transition-all duration-1000 ease-out"
                    style={{ width: `${coherenceIndex * 100}%` }}
                  />
                </div>
              </div>

              <div className="group/stat cursor-pointer">
                <div className="flex justify-between items-end mb-3">
                  <span className="text-xs font-bold uppercase tracking-[0.2em] text-synergy-emerald group-hover/stat:text-white transition-colors duration-300">
                    Synergy
                  </span>
                  <span className="text-[10px] uppercase tracking-widest text-white/40">
                    Lvl 8
                  </span>
                </div>
                <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
                  <div className="h-full bg-synergy-emerald w-[50%] group-hover/stat:shadow-[0_0_12px_#10B981] group-hover/stat:bg-white transition-all duration-300" />
                </div>
              </div>

              <div className="group/stat cursor-pointer">
                <div className="flex justify-between items-end mb-3">
                  <span className="text-xs font-bold uppercase tracking-[0.2em] text-adapt-amber group-hover/stat:text-white transition-colors duration-300">
                    Adaptability
                  </span>
                  <span className="text-[10px] uppercase tracking-widest text-white/40">
                    Lvl 15
                  </span>
                </div>
                <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
                  <div className="h-full bg-adapt-amber w-[90%] group-hover/stat:shadow-[0_0_12px_#F59E0B] group-hover/stat:bg-white transition-all duration-300" />
                </div>
              </div>

              <div className="group/stat cursor-pointer">
                <div className="flex justify-between items-end mb-3">
                  <span className="text-xs font-bold uppercase tracking-[0.2em] text-transparency-silver group-hover/stat:text-white transition-colors duration-300">
                    Transparency
                  </span>
                  <span className="text-[10px] uppercase tracking-widest text-white/40">
                    Lvl 10
                  </span>
                </div>
                <div className="h-1 w-full bg-white/5 rounded-full overflow-hidden shadow-inner">
                  <div className="h-full bg-transparency-silver w-[60%] group-hover/stat:shadow-[0_0_12px_#E5E7EB] group-hover/stat:bg-white transition-all duration-300" />
                </div>
              </div>
            </div>
          </div>
        </aside>
      </div>

      {/* Bottom Panel: Status Effects & Insights */}
      <footer className="h-12 w-full border-t border-white/10 bg-black/80 flex items-center px-6 text-xs font-mono uppercase tracking-widest z-20">
        <div className="flex items-center space-x-6">
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 rounded-full bg-synergy-emerald animate-pulse" />
            <span className="text-white/70">System Nominal</span>
          </div>
          <div className="border-l border-white/10 h-4" />
          <div className="text-white/50">
            <span className="text-celestial-blue">Active Quest:</span> The
            Paradox of Static Wisdom
          </div>
        </div>
        <div className="ml-auto text-white/30">
          UIP-V15 Governance Lock: Active
        </div>
      </footer>
    </div>
  );
}
