// [OMEGA AST Cleaned]: Tokenized design standards applied.
/**
 * Core Logic: src/hooks/useSynapseLogic.ts
 * Visual Interface: src/components/TheSynapse.tsx (now exporting SynapseInterface)
 * Superposition Demo: src/components/pages/ArtifactCatalogPage.tsx (Neural Assistant)
 */
import { ArrowUpRight, Box, BrainCircuit, Info, LayoutGrid, List, Loader, Search, Tag, X } from 'lucide-react';
import { useTheme } from '@/hooks/useTheme';
import { fetchAllArtifactsCommand, fetchArtifactMetadataCommand, systemHelpCommand, dispatchCommand } from '@/services';
import { useCoherenceStore } from '@/store/coherenceStore';
import { useState, useEffect, useMemo } from 'react';
import Tooltip from '../common/Tooltip';
import { SynapseInterface } from '../TheSynapse';

interface Artifact {
    id: string;
    name: string;
    type: 'Document' | 'Concept' | 'Principle' | 'Aesthetic';
    description: string;
}

const typeColorMap: Record<Artifact['type'], string> = {
    Document: 'cyan',
    Concept: 'violet',
    Principle: 'amber',
    Aesthetic: 'pink',
};

// Localized Registry Subset for Artifact Operations
const artifactLocalRegistry = {
    CMD_FETCH_ALL_ARTIFACTS: fetchAllArtifactsCommand,
    CMD_FETCH_ARTIFACT_METADATA: fetchArtifactMetadataCommand,
    CMD_SYSTEM_HELP: systemHelpCommand,
};

const ArtifactCatalogPage: React.FC = () => {
    const [artifacts, setArtifacts] = useState<Artifact[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [viewMode, setViewMode] = useState<'grid' | 'list'>('grid');
    const [isAssistantOpen, setIsAssistantOpen] = useState(false);

    const theme = useTheme();
    const addNovaSpark = useCoherenceStore((state) => state.addNovaSpark);

    useEffect(() => {
        const fetch = async () => {
            const result = await dispatchCommand(fetchAllArtifactsCommand, {});
            if (result.success && result.data && Array.isArray(result.data.artifacts)) {
                setArtifacts(result.data.artifacts as Artifact[]);
            } else {
                setArtifacts([]);
            }
            setIsLoading(false);
        };
        void fetch();
    }, []);

    const filtered = useMemo(() => {
        const query = searchQuery.toLowerCase();
        return (artifacts || []).filter(
            (a) =>
                (a.name || '').toLowerCase().includes(query) ||
                (a.id || '').toLowerCase().includes(query) ||
                (a.type || '').toLowerCase().includes(query) ||
                (a.description || '').toLowerCase().includes(query),
        );
    }, [artifacts, searchQuery]);

    const statsByType = useMemo(() => {
        return (artifacts || []).reduce<Record<string, number>>((acc, a) => {
            if (a && a.type) {
                acc[a.type] = (acc[a.type] || 0) + 1;
            }
            return acc;
        }, {});
    }, [artifacts]);

    if (isLoading) {
        return (
            <div className="h-full w-full flex flex-col items-center justify-center text-cyan-300/70">
                <Loader className="w-12 h-12 animate-spin mb-4" />
                <h2 className="text-2xl font-thin tracking-widest uppercase">Initializing Catalog...</h2>
            </div>
        );
    }

    return (
        <div className="relative h-screen overflow-hidden flex bg-black/20">
            {/* Main Content Area */}
            <div
                className={`flex-1 overflow-y-auto scrollbar-thin p-4 md:p-8 transition-all duration-500 ${isAssistantOpen ? 'mr-[400px]' : ''}`}
            >
                <div className="max-w-7xl mx-auto animate-fade-in">
                    <header className="mb-8 flex flex-col md:flex-row md:items-end justify-between gap-6">
                        <div>
                            <h2 className="text-4xl font-thin tracking-widest text-white drop-shadow-[0_0_10px_rgba(34,211,238,0.3)]">
                                Protocol Artifact Registry
                            </h2>
                            <p
                                className={`text-sm text-${theme.primary}-400/60 mt-2 font-mono uppercase tracking-widest`}
                            >
                                // Cognitive Topography: {artifacts.length} Indexed Entities
                            </p>
                        </div>

                        <div className="flex items-center gap-4">
                            <div className="flex items-center gap-2 bg-black/40 border border-white/10 rounded-lg p-1">
                                <Tooltip label="Grid View">
                                    <button
                                        onClick={() => {
                                            setViewMode('grid');
                                        }}
                                        className={`p-2 rounded transition-all ${viewMode === 'grid' ? 'bg-white/10 text-white shadow-inner' : 'text-gray-500 hover:text-gray-300'}`}
                                    >
                                        <LayoutGrid size={18} />
                                    </button>
                                </Tooltip>
                                <Tooltip label="List View">
                                    <button
                                        onClick={() => {
                                            setViewMode('list');
                                        }}
                                        className={`p-2 rounded transition-all ${viewMode === 'list' ? 'bg-white/10 text-white shadow-inner' : 'text-gray-500 hover:text-gray-300'}`}
                                    >
                                        <List size={18} />
                                    </button>
                                </Tooltip>
                            </div>

                            <button
                                onClick={() => {
                                    setIsAssistantOpen(!isAssistantOpen);
                                    addNovaSpark(
                                        isAssistantOpen ? 'Neural Assistant Detached' : 'Neural Assistant Initialized',
                                    );
                                }}
                                className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-300 ${
                                    isAssistantOpen
                                        ? `bg-${theme.primary}-500/20 border-${theme.primary}-500/40 text-white`
                                        : `bg-black/40 border-white/10 text-${theme.primary}-400 hover:border-${theme.primary}-500/50`
                                }`}
                            >
                                <BrainCircuit size={18} className={isAssistantOpen ? 'animate-pulse' : ''} />
                                <span className="text-xs font-mono uppercase tracking-widest">Neural Assistant</span>
                            </button>
                        </div>
                    </header>

                    {/* Stats Bar */}
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
                        {Object.entries(typeColorMap).map(([type, color]) => (
                            <div
                                key={type}
                                className={`p-3 bg-black/20 border border-${color}-500/20 rounded-lg flex items-center justify-between`}
                            >
                                <div className="flex items-center gap-2">
                                    <div
                                        className={`w-2 h-2 rounded-full bg-${color}-400 shadow-[0_0_8px_currentColor]`}
                                    />
                                    <span className="text-xs uppercase tracking-widest text-gray-400">{type}s</span>
                                </div>
                                <span className="text-xl font-mono text-white">{statsByType[type] || 0}</span>
                            </div>
                        ))}
                    </div>

                    {/* Search Module */}
                    <div className="relative mb-10">
                        <Search
                            className={`absolute left-4 top-1/2 -translate-y-1/2 text-${theme.primary}-500/50`}
                            size={20}
                        />
                        <input
                            type="text"
                            value={searchQuery}
                            onChange={(e) => {
                                setSearchQuery(e.target.value);
                            }}
                            placeholder="Search neural archive by name, ID, type or description..."
                            className={`w-full bg-black/40 border border-${theme.primary}-500/20 rounded-xl py-4 pl-12 pr-4 text-cyan-100 placeholder-${theme.primary}-500/30 focus:outline-none focus:ring-2 focus:ring-${theme.primary}-500/30 transition-all duration-300 backdrop-blur-md`}
                        />
                        {searchQuery && (
                            <div className="absolute right-4 top-1/2 -translate-y-1/2 text-[10px] font-mono text-cyan-500/40 uppercase tracking-tighter">
                                Matches: {filtered.length}
                            </div>
                        )}
                    </div>

                    {/* Artifact Collection */}
                    {filtered.length > 0 ? (
                        viewMode === 'grid' ? (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                                {filtered.map((artifact) => (
                                    <div
                                        key={artifact.id}
                                        className="group relative p-6 bg-black/40 border border-white/5 rounded-xl hover:border-cyan-500/40 hover:bg-black/60 transition-all duration-300 animate-fade-in-up"
                                    >
                                        <div className="flex justify-between items-start mb-4">
                                            <div
                                                className={`p-2 rounded-lg bg-${typeColorMap[artifact.type]}-500/10 border border-${typeColorMap[artifact.type]}-500/20`}
                                            >
                                                <Box size={20} className={`text-${typeColorMap[artifact.type]}-400`} />
                                            </div>
                                            <span
                                                className={`text-[10px] font-mono font-bold px-2 py-1 rounded bg-black/40 border border-white/10 text-gray-500 group-hover:text-cyan-400 group-hover:border-cyan-500/30 transition-colors`}
                                            >
                                                {artifact.id}
                                            </span>
                                        </div>

                                        <h3 className="text-xl font-light text-cyan-100 mb-2 group-hover:text-white transition-colors">
                                            {artifact.name}
                                        </h3>

                                        <div className="flex items-center gap-2 mb-4">
                                            <Tag size={12} className={`text-${typeColorMap[artifact.type]}-500/50`} />
                                            <span
                                                className={`text-[10px] uppercase tracking-widest font-bold text-${typeColorMap[artifact.type]}-400/80`}
                                            >
                                                {artifact.type}
                                            </span>
                                        </div>

                                        <p className="text-xs text-cyan-400/60 leading-relaxed line-clamp-3">
                                            {artifact.description}
                                        </p>

                                        <div className="mt-6 pt-4 border-t border-white/5 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button className="text-[10px] uppercase tracking-widest font-bold text-cyan-400 flex items-center gap-2 hover:text-cyan-200">
                                                Open Definition <ArrowUpRight size={10} />
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        ) : (
                            <div className="space-y-3">
                                {filtered.map((artifact) => (
                                    <div
                                        key={artifact.id}
                                        className="flex items-center gap-4 p-4 bg-black/20 border border-white/5 rounded-lg hover:border-cyan-500/20 hover:bg-black/40 transition-all group animate-fade-in-up"
                                    >
                                        <div
                                            className={`w-2 h-10 rounded-full bg-${typeColorMap[artifact.type]}-500/30 group-hover:bg-${typeColorMap[artifact.type]}-500 transition-colors shadow-[0_0_10px_currentColor]`}
                                        />
                                        <div className="flex-1 min-w-0">
                                            <div className="flex items-center gap-3">
                                                <h3 className="text-sm font-semibold text-cyan-100">{artifact.name}</h3>
                                                <span className="text-[9px] font-mono text-gray-500 bg-black/40 px-1.5 py-0.5 rounded border border-white/5">
                                                    {artifact.id}
                                                </span>
                                            </div>
                                            <p className="text-[10px] text-cyan-400/40 truncate max-w-2xl">
                                                {artifact.description}
                                            </p>
                                        </div>
                                        <div className="flex items-center gap-6">
                                            <div className="flex items-center gap-2 w-24">
                                                <Tag
                                                    size={12}
                                                    className={`text-${typeColorMap[artifact.type]}-500/50`}
                                                />
                                                <span
                                                    className={`text-[9px] uppercase tracking-widest font-bold text-${typeColorMap[artifact.type]}-400/80`}
                                                >
                                                    {artifact.type}
                                                </span>
                                            </div>
                                            <button className="p-2 text-gray-500 hover:text-cyan-400 opacity-0 group-hover:opacity-100 transition-all">
                                                <ArrowUpRight size={16} />
                                            </button>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )
                    ) : (
                        <div className="p-20 text-center border border-dashed border-white/10 rounded-2xl">
                            <Info className="w-12 h-12 text-gray-700 mx-auto mb-4" />
                            <h3 className="text-xl font-light text-gray-500">
                                No matching artifacts identified in neural registry.
                            </h3>
                            <button
                                onClick={() => {
                                    setSearchQuery('');
                                }}
                                className={`mt-4 text-xs font-mono uppercase tracking-widest text-${theme.primary}-400 hover:text-${theme.primary}-200 transition-colors`}
                            >
                                Clear Search Parameters
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Localized Neural Assistant (Superposition Demonstration) */}
            <aside
                className={`fixed right-0 top-0 h-full w-[400px] bg-gray-900 border-l border-white/10 z-40 transition-transform duration-500 shadow-[-20px_0_50px_rgba(0,0,0,0.5)] ${
                    isAssistantOpen ? 'translate-x-0' : 'translate-x-full'
                }`}
            >
                <div className={`flex flex-col h-full bg-gradient-to-b from-${theme.primary}-500/5 to-transparent`}>
                    <div className="p-4 border-b border-white/10 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <BrainCircuit className={`text-${theme.primary}-400 animate-pulse`} size={16} />
                            <h3 className="text-xs font-mono uppercase tracking-[0.2em] text-white">
                                Neural Assistant v1.0
                            </h3>
                        </div>
                        <button
                            onClick={() => setIsAssistantOpen(false)}
                            className="text-white/40 hover:text-white transition-colors"
                        >
                            <X size={16} />
                        </button>
                    </div>

                    <div className="flex-1 flex flex-col overflow-hidden">
                        <div className="p-4 bg-black/20 text-[10px] text-gray-500 font-mono leading-relaxed">
                            <span className="text-cyan-500/60 font-bold">// CONTEXT_AWARE_OPERATIONS:</span> This
                            localized Synapse instance is dedicated to Artifact Registry management. It operates in
                            isolation from the global interface.
                        </div>

                        <div className="flex-1 overflow-hidden">
                            {/* Injected SynapseInterface with Local Registry */}
                            <SynapseInterface
                                registry={artifactLocalRegistry}
                                onClose={() => setIsAssistantOpen(false)}
                                isGlobal={false} // Local instances are invisible to global resonance
                            />
                        </div>
                    </div>

                    <div className="p-3 border-t border-white/5 text-[9px] font-mono text-center text-gray-600 uppercase tracking-tighter">
                        Synapse Shard: [ArtifactCatalogExplorer] // Status: Active
                    </div>
                </div>
            </aside>

            <style>{`
                @keyframes fade-in-up {
                    from { opacity: 0; transform: translateY(10px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in-up { animation: fade-in-up 0.5s ease-out forwards; }
                .animate-fade-in { animation: fade-in 0.8s ease-out forwards; }
                @keyframes fade-in { from { opacity: 0; } to { opacity: 1; } }
            `}</style>
        </div>
    );
};

export default ArtifactCatalogPage;
