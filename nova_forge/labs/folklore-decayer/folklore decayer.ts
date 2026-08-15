import { Flow } from 'flow-sdk';
import { AnimatePresence, motion } from 'motion/react';
import type React from 'react';
import { useEffect, useState } from 'react';

// --- Constants ---
const DEFAULT_MODEL = '🍌 Nano Banana Pro';
const HIDDEN_STYLE = 'stark contrast, high shadow, cinematic lighting, and dark fantasy';

// --- Types ---
interface GeneratedImage {
  base64: string;
  mimeType: string;
  label: string;
}

// --- Components ---

const SectionLabel: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (<div className="flex items-center px-2 mb-2">
    <span className="text-[11px] font-medium text-[rgba(218,220,224,0.9)] tracking-[0.1px] uppercase">
      {children}
    </span>
  </div>);
};

const LoadingSkeleton = ({ label }: { label: string }) => {
  return (<div className="relative w-full aspect-square bg-[#1a1a1a] rounded-2xl border border-[#333] flex flex-col items-center justify-center overflow-hidden">
    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-full animate-[shimmer_2s_infinite]" />
    <span className="material-symbols-outlined text-[32px] text-white/20 mb-3 animate-pulse">auto_awesome</span>
    <span className="text-[11px] text-white/40 font-medium tracking-wider">{label.toUpperCase()}...</span>
  </div>);
};

const ResultPane = ({ image, label, phrase }: { image: GeneratedImage | null; label: string; phrase: string }) => {
  return (
    <div className="flex-1 min-w-[300px] flex flex-col gap-3">
      <div className="flex justify-between items-center px-1">
        <span className="text-[12px] font-bold text-white tracking-widest uppercase">{label}</span>
      </div>
      <div className="relative aspect-square w-full rounded-2xl border border-[#333] bg-[#111] overflow-hidden group">
        {image ? (
          <motion.img
            initial={{ opacity: 0, scale: 1.05 }}
            animate={{ opacity: 1, scale: 1 }}
            src={`data:${image.mimeType};base64,${image.base64}`}
            alt={label}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center border-2 border-dashed border-white/5">
            <span className="material-symbols-outlined text-[48px] text-white/5">image</span>
          </div>
        )}
        
        {image && (
          <div className="absolute inset-x-0 bottom-0 p-4 bg-gradient-to-t from-black/80 to-transparent opacity-0 group-hover:opacity-100 transition-opacity">
            <p className="text-[10px] text-white/60 italic leading-tight line-clamp-2">
              {phrase}
            </p>
          </div>
        )}
      </div>
    </div>
  );
};

export default function App() {
  const [phrase, setPhrase] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [literalResult, setLiteralResult] = useState<GeneratedImage | null>(null);
  const [decayedResult, setDecayedResult] = useState<GeneratedImage | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Inject custom shimmer animation
    const styleId = 'folklore-styles';
    if (!document.getElementById(styleId)) {
      const style = document.createElement('style');
      style.id = styleId;
      style.textContent = `
        @keyframes shimmer {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(100%); }
        }
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #333; border-radius: 10px; }
      `;
      document.head.appendChild(style);
    }
  }, []);

  const handleGenerate = async () => {
    if (!phrase.trim()) return;

    setIsGenerating(true);
    setError(null);
    setLiteralResult(null);
    setDecayedResult(null);

    try {
      // Prompt construction
      const literalPrompt = `${phrase}. A direct, literal folklore illustration. ${HIDDEN_STYLE}.`;
      const decayedPrompt = `${phrase}. Decayed, ominous, rotting, ancient eerie interpretation. ${HIDDEN_STYLE}.`;

      // Generate both images (using Nano Banana Pro for high quality dark fantasy)
      const [literal, decayed] = await Promise.all([
        Flow.generate.image({
          prompt: literalPrompt,
          modelDisplayName: DEFAULT_MODEL,
          aspectRatio: '1:1'
        }),
        Flow.generate.image({
          prompt: decayedPrompt,
          modelDisplayName: DEFAULT_MODEL,
          aspectRatio: '1:1'
        })
      ]);

      setLiteralResult({ base64: literal.base64, mimeType: literal.mimeType, label: 'Literal' });
      setDecayedResult({ base64: decayed.base64, mimeType: decayed.mimeType, label: 'Decayed' });
    } catch (err: any) {
      console.error(err);
      setError(err.message || 'Failed to summon interpretation.');
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0e0e0e] text-white flex flex-col items-center selection:bg-white/10 p-4 lg:p-8 custom-scrollbar">
      <div className="w-full max-w-5xl flex flex-col gap-8">
        
        {/* Header/Input Section */}
        <section className="flex flex-col items-center text-center gap-4">
          <div className="flex flex-col gap-2">
            <h1 className="text-3xl font-serif tracking-tight text-white/90">Folklore Decayer</h1>
            <p className="text-[12px] text-white/40 font-medium tracking-[2px] uppercase">Twin Paths of Myth</p>
          </div>
          
          <div className="w-full max-w-2xl mt-4 space-y-4">
            <div className="relative group">
              <textarea
                value={phrase}
                onChange={(e) => setPhrase(e.target.value)}
                placeholder="The king beneath the lake whispers to the reeds..."
                className="w-full bg-[#161616] border border-[#333] hover:border-[#555] focus:border-white/20 rounded-2xl px-6 py-5 text-lg font-serif italic text-white placeholder:text-white/20 outline-none transition-all resize-none h-[120px]"
                disabled={isGenerating}
              />
              <div className="absolute top-2 right-4 flex gap-1 opacity-20">
                <span className="material-symbols-outlined text-[16px]">ink_pen</span>
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={isGenerating || !phrase.trim()}
              className="group relative w-full h-[56px] rounded-xl overflow-hidden bg-white text-black font-bold tracking-[2px] uppercase transition-all disabled:opacity-50 disabled:grayscale hover:scale-[1.01] active:scale-[0.99] flex items-center justify-center gap-2 cursor-pointer"
            >
              {isGenerating ? (
                <>
                  <span className="material-symbols-outlined animate-spin text-[20px]">progress_activity</span>
                  <span>Summoning...</span>
                </>
              ) : (
                <>
                  <span className="material-symbols-outlined text-[20px] group-hover:rotate-12 transition-transform">bolt</span>
                  <span>Interpret Folklore</span>
                </>
              )}
            </button>
          </div>
        </section>

        {/* Results Section */}
        <section className="grid grid-cols-1 md:grid-cols-2 gap-6 lg:gap-12 pb-12">
          {isGenerating ? (
            <>
              <LoadingSkeleton label="Summoning Literal" />
              <LoadingSkeleton label="Invoking Decay" />
            </>
          ) : (
            <>
              <ResultPane 
                image={literalResult} 
                label="The Literal" 
                phrase={phrase} 
              />
              <ResultPane 
                image={decayedResult} 
                label="The Decayed" 
                phrase={phrase} 
              />
            </>
          )}
        </section>

        {/* Error State */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="fixed bottom-8 left-1/2 -translate-x-1/2 px-6 py-3 bg-red-900/20 border border-red-500/30 rounded-full backdrop-blur-xl flex items-center gap-3"
            >
              <span className="material-symbols-outlined text-red-400">error</span>
              <span className="text-[12px] text-red-200 font-medium">{error}</span>
              <button onClick={() => setError(null)} className="ml-2 opacity-50 hover:opacity-100">
                <span className="material-symbols-outlined text-[18px]">close</span>
              </button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}