// [OMEGA AST Cleaned]: Tokenized design standards applied.

import React, { useState } from 'react';
import { graphData } from '../../data/graphData';
import { dispatchCommand, simulateSynergyCommand } from '../../services';
import { FlaskConical, Loader, Zap, Sparkles, Box } from 'lucide-react';
import * as LucideIcons from 'lucide-react';
import { useCoherenceStore } from '../../store/coherenceStore';
import ArtifactSelector from '../common/ArtifactSelector';

interface DreamUi {
    title: string;
    icon: string;
    metrics: { label: string; value: number; color: string }[];
}

const GenerativeWidget: React.FC<{ data: DreamUi }> = ({ data }) => {
    const Icon = (LucideIcons as unknown as Record<string, React.ElementType>)[data.icon] ?? Box;
    
    return (
        <div className="p-6 bg-cyan-900/10 border border-cyan-400/30 rounded-xl shadow-2xl animate-fade-in-up">
            <div className="flex items-center gap-3 mb-6">
                <div className="p-3 bg-cyan-500/20 rounded-lg">
                    <Icon size={24} className="text-cyan-300 animate-pulse" />
                </div>
                <div>
                    <h4 className="text-lg font-light text-cyan-100 tracking-wide">{data.title}</h4>
                    <p className="text-[10px] text-cyan-500/60 uppercase tracking-widest font-mono">Generative UI Interface</p>
                </div>
            </div>

            <div className="space-y-4">
                {data.metrics.map((m, i) => (
                    <div key={i}>
                        <div className="flex justify-between text-xs mb-1 font-mono">
                            <span className="text-cyan-400/80">{m.label}</span>
                            <span className={`text-${m.color}-400`}>{m.value}%</span>
                        </div>
                        <div className="h-1.5 w-full bg-black/40 rounded-full overflow-hidden">
                            <div 
                                className={`h-full bg-${m.color}-500 transition-all duration-1000 ease-out shadow-[0_0_8px_currentColor]`}
                                style={{ width: `${m.value.toString()}%` }}
                            />
                        </div>
                    </div>
                ))}
            </div>
            
            <div className="mt-6 flex justify-center">
                 <div className="px-3 py-1 bg-white/5 rounded-full border border-white/10 text-[9px] text-cyan-500/40 uppercase tracking-tighter flex items-center gap-2">
                     <Sparkles size={10} /> Dream Weave Protocol Active
                 </div>
            </div>
        </div>
    );
};

const SynergySimulatorPage: React.FC = () => {
    const [artifactId1, setArtifactId1] = useState<string | null>(null);
    const [artifactId2, setArtifactId2] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [report, setReport] = useState<string | null>(null);
    const [dreamUi, setDreamUi] = useState<DreamUi | null>(null);
    const [error, setError] = useState<string | null>(null);

    const addNovaSpark = useCoherenceStore(state => state.addNovaSpark);

    const handleSimulate = async () => {
        if (!artifactId1 || !artifactId2 || isLoading) return;

        setIsLoading(true);
        setReport(null);
        setDreamUi(null);
        setError(null);
        addNovaSpark('Initializing Synergy Simulation Chamber...');
        
        const result = await dispatchCommand(simulateSynergyCommand, { artifactId1, artifactId2 });
        
        if (result.success && result.data) {
            // result.data contains report and dreamUi as returned by dispatcher's Gemini call
            setReport(result.data.report as string);
            setDreamUi(result.data.dreamUi as DreamUi);
            addNovaSpark(`Synergy simulation complete.`);
        } else {
            setError(result.message);
        }
        setIsLoading(false);
    };
    
    return (
        <div className="min-h-full w-full p-4 md:p-6 flex flex-col items-center">
            <div className="w-full max-w-4xl text-center mb-8">
                <h2 className="text-3xl font-thin tracking-widest text-cyan-300 drop-shadow-[0_0_8px_rgba(100,220,255,0.7)] mb-2 flex items-center justify-center gap-3">
                    <FlaskConical className="w-8 h-8"/> Synergy Simulation Chamber
                </h2>
                <p className="text-cyan-400/80 max-w-3xl mx-auto">
                    Select two distinct artifacts to simulate their potential fusion and generate a predictive "SynergyOpportunity" report.
                </p>
            </div>

            <div className="w-full max-w-4xl flex items-center gap-4 mb-6">
                <ArtifactSelector 
                    artifacts={graphData.nodes}
                    selectedId={artifactId1}
                    onSelect={setArtifactId1}
                    placeholder="Select Artifact 1"
                    disabledId={artifactId2}
                />
                <Zap className="w-8 h-8 text-cyan-400 shrink-0"/>
                 <ArtifactSelector 
                    artifacts={graphData.nodes}
                    selectedId={artifactId2}
                    onSelect={setArtifactId2}
                    placeholder="Select Artifact 2"
                    disabledId={artifactId1}
                />
            </div>

            <div className="inline-block mb-10">
                <button 
                    onClick={() => { void handleSimulate(); }}
                    disabled={!artifactId1 || !artifactId2 || isLoading || artifactId1 === artifactId2}
                    className="flex items-center justify-center gap-2 px-8 py-3 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-400/30 rounded-md text-cyan-200 disabled:opacity-30 transition-all duration-300 shadow-[0_0_20px_rgba(34,211,238,0.1)] hover:shadow-[0_0_30px_rgba(34,211,238,0.2)]"
                >
                    {isLoading ? <><Loader className="w-5 h-5 animate-spin"/> Simulating...</> : 'Initiate Fusion'}
                </button>
            </div>
            
            <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                <div className="flex-1 min-h-[300px]">
                    {isLoading && (
                        <div className="h-full flex flex-col items-center justify-center text-cyan-300/70 animate-fade-in">
                            <Loader className="w-12 h-12 animate-spin mb-4" />
                            <p className="font-light">Cognitive Core is analyzing synergy vectors...</p>
                        </div>
                    )}

                    {report && (
                        <div className="p-6 bg-black/30 border border-cyan-500/20 rounded-lg backdrop-blur-sm animate-fade-in-up overflow-y-auto max-h-[60vh] scrollbar-thin">
                             <h3 className="text-xl font-light tracking-wider text-cyan-200 mb-4 flex items-center gap-2">
                                 <Sparkles size={18} className="text-amber-400" /> Speculative Analysis
                             </h3>
                             <div className="text-cyan-100/90 text-sm prose-invert whitespace-pre-wrap leading-relaxed">
                                {report}
                             </div>
                        </div>
                    )}
                </div>

                <div className="w-full">
                    {dreamUi && <GenerativeWidget data={dreamUi} />}
                </div>
            </div>

            {error && (
                <div className="w-full max-w-4xl p-4 mt-6 bg-red-900/30 border border-red-500/30 rounded-md text-red-200 animate-fade-in">
                    {error}
                </div>
            )}

            <style>{`
                @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
                @keyframes fade-in-up { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
                .animate-fade-in { animation: fade-in 0.5s ease-out forwards; }
                .animate-fade-in-up { animation: fade-in-up 0.5s ease-out forwards; }
                .scrollbar-thin::-webkit-scrollbar { width: 4px; }
                .scrollbar-thin::-webkit-scrollbar-thumb { background-color: rgba(0, 255, 255, 0.2); border-radius: 20px; }
            `}</style>
        </div>
    );
};

export default SynergySimulatorPage;
