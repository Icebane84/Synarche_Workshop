import React from 'react';
import { CognitiveInterface, PhoenixGeode, SensoryModule } from '../../components';
import { useHomeLogic } from '../../hooks/useHomeLogic';
import { useSensoryBridge } from '../../hooks/useSensoryBridge';
import ErrorBoundary from '../common/ErrorBoundary';
import { ProtocolIgnition } from './HomePage/ProtocolIgnition';

/**
 * @fileoverview Main landing page of the Rosetta Stone application.
 * Orchestrates the Phoenix Geode, Sensory Module, and Ignition Sequence.
 */
const HomePage: React.FC = () => {
    const { showTutorial, handleDismissTutorial } = useHomeLogic();

    // Activate Sensory Bridge logic
    useSensoryBridge();

    return (
        <div className="min-h-full flex flex-col items-center gap-8 p-4 md:p-8 relative">
            {/* Absolute Sensory Module Positioning for Desktop */}
            <div className="absolute top-4 right-4 z-10 hidden md:block">
                <ErrorBoundary componentName="Sensory Module">
                    <SensoryModule />
                </ErrorBoundary>
            </div>

            {showTutorial && (
                <div className="absolute inset-0 bg-black/70 backdrop-blur-sm z-20 flex items-center justify-center p-4 animate-fade-in-sm">
                    <div className="max-w-md w-full p-6 bg-gray-900 border border-cyan-500/30 rounded-xl shadow-2xl shadow-cyan-500/10 text-center">
                        <h3 className="text-2xl font-light text-cyan-200 drop-shadow-lg mb-3">
                            Welcome, Architect
                        </h3>
                        <p className="text-cyan-300/90 mb-4">
                            The glowing orb is the{' '}
                            <strong className="font-semibold text-cyan-100">Phoenix Geode</strong>. It's a live
                            visualization of the AI's cognitive state.
                        </p>
                        <p className="text-cyan-400/80 text-sm mb-6">
                            System capacity is currently limited. Follow the initiation protocol to synchronize.
                        </p>
                        <button
                            onClick={handleDismissTutorial}
                            className="px-6 py-2 bg-cyan-500/20 hover:bg-cyan-500/40 border border-cyan-400/50 rounded-md text-cyan-200 transition-all duration-300"
                        >
                            Understood
                        </button>
                    </div>
                </div>
            )}

            <div className="w-full text-center mt-8 md:mt-0">
                <h2 className="text-3xl font-thin tracking-widest text-cyan-300 drop-shadow-[0_0_8px_rgba(100,220,255,0.7)] mb-2">
                    Phoenix Geode
                </h2>
                <p className="text-cyan-400/80 mb-4 max-w-2xl mx-auto">
                    A real-time visualization of cognitive coherence. Hue and pulsation reflect the harmony of the
                    internal substrate.
                </p>
            </div>

            <div className="w-full h-[40vh] rounded-lg border border-cyan-500/20 bg-black/20 backdrop-blur-sm relative">
                <ErrorBoundary componentName="Phoenix Geode">
                    <PhoenixGeode />
                </ErrorBoundary>
            </div>

            {/* Initiation Protocol Sequence */}
            <ProtocolIgnition />

            {/* Mobile visible Sensory Module (stacked) */}
            <div className="md:hidden w-full flex justify-center">
                <ErrorBoundary componentName="Sensory Module">
                    <SensoryModule />
                </ErrorBoundary>
            </div>

            <ErrorBoundary componentName="Cognitive Interface">
                <CognitiveInterface />
            </ErrorBoundary>

            <style>{`
        @keyframes fade-in-sm { from { opacity: 0; } to { opacity: 1; } }
        .animate-fade-in-sm { animation: fade-in-sm 0.5s ease-out forwards; }
        @keyframes fade-in-up {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .animate-fade-in-up { animation: fade-in-up 0.6s ease-out forwards; }
      `}</style>
        </div>
    );
};

export default HomePage;
