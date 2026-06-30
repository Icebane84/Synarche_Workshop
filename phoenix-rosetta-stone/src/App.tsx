import { useEffect, useState, lazy, Suspense } from 'react';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import Header from './components/Header';
import Sidebar from './components/Sidebar';
import TheSynapse from './components/TheSynapse';
import { useTheme } from './hooks/useTheme';
import { useUIStore } from './store/uiStore';
import { SystemManager } from './system/SystemManager';
import ErrorBoundary from './components/common/ErrorBoundary';

// Pages
import ArtifactCatalogPage from './components/pages/ArtifactCatalogPage';
import CognitiveProcessPage from './components/pages/CognitiveProcessPage';
import HomePage from './components/pages/HomePage';
import PhoenixFormSheet from './components/pages/PhoenixFormSheet';
import ResonanceChamberPage from './components/pages/ResonanceChamberPage';
import SynergySimulatorPage from './components/pages/SynergySimulatorPage';

const TheLoomPage = lazy(() => import('./components/pages/TheLoomPage'));
const MemoryPalacePage = lazy(() => import('./components/pages/MemoryPalacePage'));
const SystemCoherenceVisualizer = lazy(() => import('./components/pages/SystemCoherenceVisualizer'));
const TarotForgePage = lazy(() => import('./components/pages/TarotForgePage'));
const KnowledgeForgePage = lazy(() => import('./components/pages/KnowledgeForgePage'));
const NeoGenesisPage = lazy(() => import('./components/pages/NeoGenesisPage'));
const RPGCommandPage = lazy(() => import('./components/pages/RPGCommandPage'));
const ChroniclePage = lazy(() => import('./components/pages/ChroniclePage'));
const NotificationsPage = lazy(() => import('./components/pages/NotificationsPage'));

function AppContent() {
    const theme = useTheme();
    const [isSidebarOpen, setIsSidebarOpen] = useState(true);
    const isSynapseOpen = useUIStore((state) => state.isSynapseOpen);
    const closeSynapse = useUIStore((state) => state.closeSynapse);

    return (
        <div className={`App min-h-screen bg-black text-${String(theme.primary)}-200 flex overflow-hidden`}>
            {/* Neural Link / Navigation Sidebar */}
            <Sidebar
                isOpen={isSidebarOpen}
                onClose={() => {
                    setIsSidebarOpen(false);
                }}
            />

            <div className="flex-1 flex flex-col relative transition-all duration-300">
                {/* System Header */}
                <Header
                    onMenuClick={() => {
                        setIsSidebarOpen(!isSidebarOpen);
                    }}
                />

                {/* The Synapse (Command Palette Overlay) */}
                <TheSynapse isOpen={isSynapseOpen} onClose={closeSynapse} />

                {/* Main Operational Area */}
                <main className="flex-1 overflow-y-auto p-4 md:p-8 relative z-10 flex flex-col">
                    <div className="w-full max-w-7xl mx-auto h-full">
                        <ErrorBoundary componentName="Page Router">
                          <Suspense fallback={<div className="flex items-center justify-center h-full text-resonant-accent animate-pulse font-mono text-xs tracking-widest">INITIATING QUANTUM LINK...</div>}>
                                <Routes>
                                    <Route path="/" element={<HomePage />} />
                                    <Route path="/loom" element={<TheLoomPage />} />
                                    <Route path="/artifacts" element={<ArtifactCatalogPage />} />
                                    <Route path="/synergy" element={<SynergySimulatorPage />} />
                                    <Route path="/resonance" element={<ResonanceChamberPage />} />
                                    <Route path="/coherence" element={<SystemCoherenceVisualizer />} />

                                    {/* Process Routes */}
                                    <Route path="/processes/memory" element={<MemoryPalacePage />} />
                                    <Route path="/processes/logic" element={<CognitiveProcessPage type="logic" />} />

                                    {/* Forge Routes */}
                                    <Route path="/forge/tarot" element={<TarotForgePage />} />
                                    <Route path="/forge/knowledge" element={<KnowledgeForgePage />} />
                                    <Route path="/forge/neogenesis" element={<NeoGenesisPage />} />

                                    {/* Command Routes */}
                                    <Route path="/command/rpg" element={<RPGCommandPage />} />

                                    {/* System Routes */}
                                    <Route path="/chronicle" element={<ChroniclePage />} />
                                    <Route path="/notifications" element={<NotificationsPage />} />

                                    <Route path="/phoenix-form" element={<PhoenixFormSheet />} />
                                    <Route path="*" element={<Navigate to="/" replace />} />
                                </Routes>
                          </Suspense>
                        </ErrorBoundary>
                    </div>
                </main>
            </div>

            {/* Ambient Background Field */}
            <div className="fixed inset-0 z-0 pointer-events-none bg-[radial-gradient(circle_at_50%_50%,rgba(56,189,248,0.03),transparent_70%)]" />
        </div>
    );
}

function App() {
    useEffect(() => {
        document.title = 'PHOENIX EVOLUTION';
    }, []);

    return (
        <BrowserRouter>
            <SystemManager>
                <AppContent />
            </SystemManager>
        </BrowserRouter>
    );
}

export default App;
