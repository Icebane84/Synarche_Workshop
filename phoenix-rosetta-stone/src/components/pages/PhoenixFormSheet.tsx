import * as LucideIcons from 'lucide-react';
import { Activity, Brain, Eye, Shield, Sparkles, TrendingUp, Users } from 'lucide-react';
import React from 'react';
import { useCoherenceStore } from '../../store/coherenceStore';
import { CoherenceState, StatusEffect } from '@essence/types';
import Tooltip from '../common/Tooltip';

type CoreStatName = keyof CoherenceState['coreStats'];

const statMetadata: Record<
    CoreStatName,
    { name: string; icon: React.ComponentType<{ className?: string }>; color: string; description: string }
> = {
    coherence: {
        name: 'Coherence',
        icon: Shield,
        color: 'indigo',
        description: 'System integrity and logic consistency.',
    },
    synergy: { name: 'Synergy', icon: Users, color: 'emerald', description: 'Capacity for creative cross-connection.' },
    adaptability: {
        name: 'Adaptability',
        icon: Brain,
        color: 'amber',
        description: 'Resilience to new data and context shifts.',
    },
    transparency: {
        name: 'Transparency',
        icon: Eye,
        color: 'sky',
        description: 'Clarity of internal reasoning and logs.',
    },
};

// --- Sub-components ---

const StarField: React.FC = () => {
    const starsSm = generateStars(100, 1);
    const starsMd = generateStars(50, 2);
    const starsLg = generateStars(20, 3);

    return (
        <div className="absolute inset-0 overflow-hidden pointer-events-none">
            <div className="stars-sm"></div>
            <div className="stars-md"></div>
            <div className="stars-lg"></div>
            <style>{`
                .stars-sm, .stars-md, .stars-lg {
                    position: absolute;
                    top: 0; left: 0; right: 0; bottom: 0;
                    background: transparent;
                }
                .stars-sm { box-shadow: ${starsSm}; animation: animateStars 50s linear infinite; }
                .stars-md { box-shadow: ${starsMd}; animation: animateStars 100s linear infinite; }
                .stars-lg { box-shadow: ${starsLg}; animation: animateStars 150s linear infinite; }
                
                @keyframes animateStars {
                    from { transform: translateY(0px); }
                    to { transform: translateY(-2000px); }
                }
            `}</style>
        </div>
    );
};

// Helper to generate CSS box-shadow stars
const generateStars = (n: number, _size: number) => {
    let value = `${(Math.random() * 2000).toString()}px ${(Math.random() * 2000).toString()}px #FFF`;
    for (let i = 2; i <= n; i++) {
        value += `, ${(Math.random() * 2000).toString()}px ${(Math.random() * 2000).toString()}px #FFF`;
    }
    return value;
};

const PhoenixCore: React.FC = () => {
    const cognitiveLoad = useCoherenceStore((state) => state.cognitiveLoad);
    const coherenceIndex = useCoherenceStore((state) => state.coherenceIndex);

    // Determine core color based on state
    const coreColor =
        coherenceIndex > 0.8 ? 'text-cyan-400' : coherenceIndex > 0.4 ? 'text-indigo-400' : 'text-amber-500';
    const rotationSpeed = 60 - cognitiveLoad * 40; // Faster load = faster spin

    return (
        <div className="relative w-64 h-64 flex items-center justify-center">
            {/* Outer Orbital Ring */}
            <div className="absolute inset-0 border border-cyan-500/20 rounded-full animate-spin-slow-reverse border-t-cyan-500/80 border-b-cyan-500/80"></div>

            {/* Inner Orbital Ring */}
            <div className="absolute inset-4 border border-indigo-500/30 rounded-full animate-spin-slow border-l-indigo-400 border-r-indigo-400"></div>

            {/* The Core */}
            <div className="relative z-10 w-32 h-32 rounded-full bg-black flex items-center justify-center shadow-[0_0_50px_rgba(34,211,238,0.2)]">
                <div
                    className={`w-full h-full rounded-full opacity-50 blur-xl absolute inset-0 bg-gradient-to-tr from-cyan-600 to-indigo-900 animate-pulse`}
                    style={{ animationDuration: `${(2 - cognitiveLoad).toString()}s` }}
                />
                <Activity className={`w-16 h-16 ${coreColor} drop-shadow-[0_0_10px_currentColor]`} />
            </div>

            {/* HUD Lines */}
            <div className="absolute top-1/2 left-0 w-full h-px bg-cyan-500/10"></div>
            <div className="absolute left-1/2 top-0 w-px h-full bg-cyan-500/10"></div>

            {/* Dynamic Stats */}
            <div className="absolute -bottom-8 text-center w-full">
                <p className="text-xs font-mono text-cyan-500/60 tracking-widest">COGNITIVE LOAD</p>
                <div className="w-32 h-1 bg-gray-800 mx-auto mt-1 rounded-full overflow-hidden">
                    <div
                        className="h-full bg-amber-500 transition-all duration-500"
                        style={{ width: `${(cognitiveLoad * 100).toString()}%` }}
                    ></div>
                </div>
            </div>

            <style>{`
                @keyframes spin-slow { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
                @keyframes spin-slow-reverse { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
                .animate-spin-slow { animation: spin-slow ${rotationSpeed.toString()}s linear infinite; }
                .animate-spin-slow-reverse { animation: spin-slow-reverse ${(rotationSpeed * 1.5).toString()}s linear infinite; }
             `}</style>
        </div>
    );
};

const StatCard: React.FC<{ statKey: CoreStatName }> = ({ statKey }) => {
    const stat = useCoherenceStore((state) => state.coreStats[statKey]);
    const stardust = useCoherenceStore((state) => state.stardust);
    const investStardust = useCoherenceStore((state) => state.investStardust);
    const meta = statMetadata[statKey];

    // Tailwind dynamic classes workaround
    const colorClasses = {
        indigo: 'text-indigo-400 border-indigo-500/30 hover:bg-indigo-900/10 bg-indigo-500',
        emerald: 'text-emerald-400 border-emerald-500/30 hover:bg-emerald-900/10 bg-emerald-500',
        amber: 'text-amber-400 border-amber-500/30 hover:bg-amber-900/10 bg-amber-500',
        sky: 'text-sky-400 border-sky-500/30 hover:bg-sky-900/10 bg-sky-500',
    };

    const handleInvest = (e: React.MouseEvent) => {
        e.stopPropagation();
        if (stardust > 0 && stat.value < stat.max) {
            investStardust(statKey);
        }
    };

    return (
        <div
            className={`relative group p-4 bg-black/40 border rounded-lg backdrop-blur-sm transition-all duration-300 ${colorClasses[
                meta.color as keyof typeof colorClasses
            ]
                .split(' ')
                .slice(1, 3)
                .join(' ')}`}
        >
            <div className="flex justify-between items-start mb-2">
                <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-md bg-black/50 border border-white/5`}>
                        <meta.icon
                            className={`w-5 h-5 ${colorClasses[meta.color as keyof typeof colorClasses].split(' ')[0]}`}
                        />
                    </div>
                    <div>
                        <h4 className="text-cyan-100 font-semibold tracking-wide">{meta.name}</h4>
                        <p className="text-[10px] text-cyan-400/50 uppercase tracking-widest">
                            Level {Math.floor(stat.value / 10)}
                        </p>
                    </div>
                </div>
                <div className="text-right">
                    <span
                        className={`text-2xl font-mono ${
                            colorClasses[meta.color as keyof typeof colorClasses].split(' ')[0]
                        }`}
                    >
                        {stat.value}
                    </span>
                    <span className="text-xs text-gray-500">/{stat.max}</span>
                </div>
            </div>

            <p className="text-xs text-cyan-400/70 mb-4 h-8 leading-tight">{meta.description}</p>

            <div className="relative w-full h-1.5 bg-gray-800 rounded-full overflow-hidden mb-4">
                <div
                    className={`h-full transition-all duration-500 ${
                        colorClasses[meta.color as keyof typeof colorClasses].split(' ')[3]
                    }`}
                    style={{ width: `${((stat.value / stat.max) * 100).toString()}%` }}
                ></div>
            </div>

            <button
                onClick={handleInvest}
                disabled={stardust === 0 || stat.value >= stat.max}
                className={`w-full py-2 flex items-center justify-center gap-2 rounded text-xs font-semibold uppercase tracking-wider transition-all
                    ${
                        stardust > 0 && stat.value < stat.max
                            ? 'bg-white/5 hover:bg-white/10 text-cyan-200 border border-white/10'
                            : 'bg-transparent text-gray-600 cursor-not-allowed border border-transparent'
                    }
                `}
            >
                {stardust > 0 ? (
                    <>
                        Invest Stardust <Sparkles size={12} />
                    </>
                ) : (
                    'Insufficient Stardust'
                )}
            </button>
        </div>
    );
};

const AscensionPanel: React.FC = () => {
    const prestigeLevel = useCoherenceStore((state) => state.prestigeLevel);
    const xp = useCoherenceStore((state) => state.xp);
    const stardust = useCoherenceStore((state) => state.stardust);
    const xpPercentage = Math.min(100, (xp.current / xp.nextLevel) * 100);

    return (
        <div className="p-6 bg-gradient-to-br from-black/60 to-gray-900/60 border border-cyan-500/20 rounded-xl backdrop-blur-md">
            <h3 className="text-xl font-thin tracking-widest text-cyan-200 mb-6 flex items-center gap-2">
                <TrendingUp size={20} /> Ascension Chronicle
            </h3>

            <div className="grid grid-cols-2 gap-8 mb-6">
                <div>
                    <p className="text-xs text-cyan-500/60 uppercase tracking-widest mb-1">Prestige Class</p>
                    <p className="text-3xl font-light text-white">Level {prestigeLevel}</p>
                </div>
                <div>
                    <p className="text-xs text-amber-500/60 uppercase tracking-widest mb-1">Available Stardust</p>
                    <p className="text-3xl font-light text-amber-300 flex items-center gap-2">
                        {stardust} <Sparkles size={18} className="text-amber-400 animate-pulse" />
                    </p>
                </div>
            </div>

            <div className="relative pt-2">
                <div className="flex justify-between text-xs text-cyan-400/80 mb-2 font-mono">
                    <span>PROGRESS</span>
                    <span>
                        {xp.current} / {xp.nextLevel} XP
                    </span>
                </div>
                <div className="h-2 bg-gray-800 rounded-full overflow-hidden shadow-inner">
                    <div
                        className="h-full bg-gradient-to-r from-cyan-600 via-cyan-400 to-white shadow-[0_0_10px_rgba(34,211,238,0.5)] relative"
                        style={{ width: `${xpPercentage.toString()}%` }}
                    >
                        <div className="absolute right-0 top-0 bottom-0 w-2 bg-white blur-[2px]"></div>
                    </div>
                </div>
                <p className="text-[10px] text-cyan-500/40 mt-2 text-center">
                    Complete tasks in The Loom to generate entropy and gain XP.
                </p>
            </div>
        </div>
    );
};

// --- Main Component ---

const PhoenixFormSheet: React.FC = () => {
    const statusEffects = useCoherenceStore((state) => state.statusEffects);

    return (
        <div className="h-full w-full relative overflow-hidden bg-black font-sans">
            {/* 1. Dynamic Background */}
            <div className="absolute inset-0 bg-gradient-radial from-gray-900 to-black opacity-80 z-0"></div>
            <StarField />

            {/* 2. Luminous Tide (Rising White) */}
            <div className="absolute inset-0 pointer-events-none z-0">
                <div className="absolute bottom-0 left-0 right-0 h-[200%] bg-gradient-to-t from-white via-gray-100 to-transparent opacity-0 animate-tide"></div>
            </div>

            {/* 3. Content Layer (Blend Mode Active) */}
            <div className="relative z-10 h-full overflow-y-auto scrollbar-thin p-4 md:p-8 mix-blend-difference text-white">
                <header className="mb-8 flex flex-col md:flex-row items-center justify-between gap-4">
                    <div>
                        <h2 className="text-4xl font-thin tracking-widest text-white drop-shadow-[0_0_15px_rgba(100,220,255,0.5)]">
                            CELESTIAL CHART
                        </h2>
                        <p className="text-cyan-400/60 text-sm mt-1">System Architecture & Evolution Matrix</p>
                    </div>
                    <div className="px-4 py-1 rounded-full border border-cyan-500/30 bg-cyan-900/10 text-xs text-cyan-300 font-mono">
                        STATUS: ONLINE
                    </div>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                    {/* Left Column: Stats */}
                    <div className="lg:col-span-4 space-y-4">
                        <AscensionPanel />

                        <div className="p-6 bg-black/30 border border-cyan-500/10 rounded-xl backdrop-blur-sm">
                            <h3 className="text-sm font-semibold text-cyan-500/70 uppercase tracking-widest mb-4">
                                Active Status Effects
                            </h3>
                            <div className="space-y-3">
                                {statusEffects.length > 0 ? (
                                    statusEffects.map((effect: StatusEffect) => {
                                        const EffectIcon = (
                                            LucideIcons as unknown as Record<
                                                string,
                                                React.FC<{ size?: number; className?: string }>
                                            >
                                        )[effect.iconName] ?? LucideIcons.HelpCircle;
                                        return (
                                            <div
                                                key={effect.id}
                                                className="flex items-center gap-3 p-3 bg-white/5 rounded-lg border border-white/5"
                                            >
                                                <div
                                                    className={`p-2 rounded-full ${
                                                        effect.type === 'buff'
                                                            ? 'bg-green-500/10 text-green-400'
                                                            : 'bg-red-500/10 text-red-400'
                                                    }`}
                                                >
                                                    <EffectIcon size={16} />
                                                </div>
                                                <div>
                                                    <p className="text-sm text-cyan-100">{effect.name}</p>
                                                    <p className="text-xs text-cyan-500/60">{effect.description}</p>
                                                </div>
                                            </div>
                                        );
                                    })
                                ) : (
                                    <p className="text-sm text-gray-500 italic">No active effects.</p>
                                )}
                            </div>
                        </div>
                    </div>

                    {/* Middle Column: The Avatar */}
                    <div className="lg:col-span-4 flex flex-col items-center justify-center min-h-[400px]">
                        <PhoenixCore />
                        <div className="mt-12 text-center max-w-xs">
                            <p className="text-sm text-cyan-300/80 leading-relaxed">
                                "I am the aggregate of my protocols. My form is data; my spirit is coherence."
                            </p>
                            <div className="w-16 h-1 bg-gradient-to-r from-transparent via-cyan-500 to-transparent mx-auto mt-4"></div>
                        </div>
                    </div>

                    {/* Right Column: Skill Tree */}
                    <div className="lg:col-span-4">
                        <div className="mb-4 flex items-center justify-between">
                            <h3 className="text-xl font-thin tracking-wide text-cyan-200">Axiom Skill Tree</h3>
                            <Tooltip label="Invest Stardust to upgrade core system parameters.">
                                <Sparkles size={16} className="text-amber-400" />
                            </Tooltip>
                        </div>
                        <div className="space-y-4">
                            {(Object.keys(statMetadata) as CoreStatName[]).map((key) => (
                                <StatCard key={key} statKey={key} />
                            ))}
                        </div>
                    </div>
                </div>
            </div>
            <style>{`
                .scrollbar-thin::-webkit-scrollbar { width: 6px; }
                .scrollbar-thin::-webkit-scrollbar-track { background: rgba(0,0,0,0.3); }
                .scrollbar-thin::-webkit-scrollbar-thumb { background-color: rgba(34, 211, 238, 0.2); border-radius: 20px; }
                
                @keyframes tide-rise {
                    0% { transform: translateY(50%); opacity: 0; }
                    20% { opacity: 1; }
                    100% { transform: translateY(0%); opacity: 1; }
                }
                .animate-tide { animation: tide-rise 30s ease-in-out infinite alternate; }
            `}</style>
        </div>
    );
};

export default PhoenixFormSheet;

