// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React, { useState, useEffect, useCallback } from 'react';
import { NavLink } from 'react-router-dom';
import {
    BrainCircuit,
    Home,
    Network,
    X,
    ListChecks,
    FlaskConical,
    Signal,
    Database,
    Library,
    Compass,
    Wand2,
    BookOpen,
    Dna,
    Swords,
    ScrollText,
    Bell,
} from 'lucide-react';
import { useUIStore } from '../store/uiStore';
import { useTheme } from '../hooks/useTheme';
import SystemBiometrics from './SystemBiometrics';
import CognitiveFocusSelector from './sidebar/CognitiveFocusSelector';
import ConnectivityStatus from './sidebar/ConnectivityStatus';
import NeuralStream from './sidebar/NeuralStream';

interface SidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

const navGroups = [
    {
        title: 'Nexus',
        items: [{ name: 'Dashboard', path: '/', icon: Home }],
    },
    {
        title: 'Cognition',
        items: [
            { name: 'Memory Core', path: '/processes/memory', icon: Database },
            { name: 'Logic Matrix', path: '/processes/logic', icon: BrainCircuit },
        ],
    },
    {
        title: 'Analysis',
        items: [
            { name: 'Artifact Catalog', path: '/artifacts', icon: Library },
            { name: 'Coherence Map', path: '/coherence', icon: Network },
            { name: 'Resonance Chamber', path: '/resonance', icon: Signal },
        ],
    },
    {
        title: 'Synthesis',
        items: [
            { name: 'Synergy Simulator', path: '/synergy', icon: FlaskConical },
            { name: 'The Loom', path: '/loom', icon: ListChecks },
            { name: 'Celestial Chart', path: '/phoenix-form', icon: Compass },
        ],
    },
    {
        title: 'Forge',
        items: [
            { name: 'Tarot Studio', path: '/forge/tarot', icon: Wand2 },
            { name: 'Knowledge Forge', path: '/forge/knowledge', icon: BookOpen },
            { name: 'Neo-Genesis', path: '/forge/neogenesis', icon: Dna },
        ],
    },
    {
        title: 'Command',
        items: [
            { name: 'RPG Interface', path: '/command/rpg', icon: Swords },
        ],
    },
    {
        title: 'System',
        items: [
            { name: 'Chronicle Log', path: '/chronicle', icon: ScrollText },
            { name: 'Notifications', path: '/notifications', icon: Bell },
        ],
    },
];

const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
    const theme = useTheme();
    const stylePatches = useUIStore((state) => state.stylePatches);
    const [sidebarWidth, setSidebarWidth] = useState(256);
    const [isResizing, setIsResizing] = useState(false);

    const startResizing = useCallback((e: React.MouseEvent) => {
        e.preventDefault();
        setIsResizing(true);
    }, []);

    const stopResizing = useCallback(() => {
        setIsResizing(false);
    }, []);
    const resize = useCallback(
        (mouseMoveEvent: MouseEvent) => {
            if (isResizing) {
                setSidebarWidth(Math.min(Math.max(mouseMoveEvent.clientX, 200), 600));
            }
        },
        [isResizing],
    );

    useEffect(() => {
        if (isResizing) {
            window.addEventListener('mousemove', resize);
            window.addEventListener('mouseup', stopResizing);
        }
        return () => {
            window.removeEventListener('mousemove', resize);
            window.removeEventListener('mouseup', stopResizing);
        };
    }, [isResizing, resize, stopResizing]);

    const borderOpacity = stylePatches.sidebarBorderOpacity || '30';
    const sidebarBorderClass = `border-${theme.primary}-500/${borderOpacity}`;

    const linkClass = `flex items-center gap-3 px-4 py-2 text-${theme.primary}-300/70 transition-colors duration-200 hover:bg-${theme.primary}-500/10 hover:text-${theme.primary}-200 text-sm`;
    const activeLinkClass = `bg-${theme.primary}-500/20 text-${theme.primary}-100 border-r-2 border-${theme.primary}-300`;

    return (
        <aside
            className={`fixed inset-y-0 left-0 z-30 max-w-[85vw] border-r ${sidebarBorderClass} bg-black/30 backdrop-blur-lg flex flex-col transition-transform duration-300 ease-in-out md:relative md:translate-x-0 contain-content ${
                isOpen ? 'translate-x-0' : '-translate-x-full'
            }`}
            style={{ width: `${sidebarWidth.toString()}px` }}
        >
            <div className={`flex-none flex items-center justify-between p-4 border-b border-${theme.primary}-500/20`}>
                <div>
                    <h2 className={`text-lg font-semibold tracking-wider text-${theme.primary}-200`}>Navigation</h2>
                </div>
                <button
                    onClick={onClose}
                    className={`md:hidden text-${theme.primary}-400/70 hover:text-${theme.primary}-200`}
                >
                    <X size={20} />
                </button>
            </div>

            <div className="flex-1 overflow-y-auto scrollbar-thin flex flex-col">
                <nav className="py-4" onClick={onClose}>
                    {navGroups.map((group) => (
                        <div key={group.title} className="mb-4">
                            <h3
                                className={`px-4 text-[10px] font-bold uppercase tracking-widest text-${theme.primary}-500/50 mb-2`}
                            >
                                {group.title}
                            </h3>
                            <ul>
                                {group.items.map((item) => (
                                    <li key={item.name}>
                                        <NavLink
                                            to={item.path}
                                            className={({ isActive }) =>
                                                `${linkClass} ${isActive ? activeLinkClass : ''}`
                                            }
                                            end={item.path === '/'}
                                        >
                                            <item.icon className="w-4 h-4" />
                                            <span>{item.name}</span>
                                        </NavLink>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    ))}
                </nav>
                <div className={`py-4 border-t border-${theme.primary}-500/20`}>
                    <CognitiveFocusSelector />
                </div>
                <NeuralStream />
                <ConnectivityStatus />
                <SystemBiometrics />
            </div>
            <div
                className={`absolute top-0 right-0 w-1.5 h-full cursor-col-resize hover:bg-${theme.primary}-500/50 z-50`}
                onMouseDown={startResizing}
            />
        </aside>
    );
};

export default Sidebar;
