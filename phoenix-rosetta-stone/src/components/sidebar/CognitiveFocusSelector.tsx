import React, { useState, useRef, useEffect } from 'react';
import { ChevronDown, Check } from 'lucide-react';
import { useCoherenceStore } from '../../store/coherenceStore';
import { useTheme } from '../../hooks/useTheme';
import { CognitiveFocus } from '@essence/types';

export const focusModes: { id: CognitiveFocus; name: string; description: string }[] = [
    { id: 'Standard', name: 'Standard', description: 'Balanced operational mode.' },
    { id: 'Creative Ideation', name: 'Creative Ideation', description: 'Prioritizes novel connections.' },
    { id: 'Security Audit', name: 'Security Audit', description: 'Prioritizes rigorous analysis.' },
    { id: 'Strategy', name: 'Strategy', description: 'Prioritizes resource optimization and planning.' },
];

const CognitiveFocusSelector: React.FC = () => {
    const [isOpen, setIsOpen] = useState(false);
    const cognitiveFocus = useCoherenceStore((state) => state.cognitiveFocus);
    const setCognitiveFocus = useCoherenceStore((state) => state.setCognitiveFocus);
    const wrapperRef = useRef<HTMLDivElement>(null);
    const theme = useTheme();

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener('mousedown', handleClickOutside);
        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [wrapperRef]);

    const selectedMode = focusModes.find((m) => m.id === cognitiveFocus);

    return (
        <div ref={wrapperRef} className="relative px-4">
            <h3 className={`text-xs font-semibold tracking-widest text-${theme.primary}-400/60 uppercase mb-2`}>
                Cognitive Focus
            </h3>
            <button
                onClick={() => {
                    setIsOpen(!isOpen);
                }}
                className={`w-full flex items-center justify-between px-3 py-2 bg-black/30 border border-${theme.primary}-500/20 rounded-md text-left transition-colors hover:bg-${theme.primary}-500/10`}
            >
                <div>
                    <p className={`text-sm text-${theme.primary}-200`}>{selectedMode?.name}</p>
                    <p className={`text-xs text-${theme.primary}-400/70 truncate`}>{selectedMode?.description}</p>
                </div>
                <ChevronDown
                    className={`w-4 h-4 text-${theme.primary}-300/70 transition-transform duration-200 ${
                        isOpen ? 'rotate-180' : ''
                    }`}
                />
            </button>
            {isOpen && (
                <div
                    className={`absolute bottom-full left-0 right-0 mb-2 w-full bg-gray-900 border border-${theme.primary}-500/30 rounded-md shadow-lg z-10 animate-fade-in-up-sm`}
                >
                    <ul>
                        {focusModes.map((mode) => (
                            <li key={mode.id}>
                                <button
                                    onClick={() => {
                                        setCognitiveFocus(mode.id);
                                        setIsOpen(false);
                                    }}
                                    className={`w-full text-left px-3 py-2 hover:bg-${theme.primary}-500/10 flex items-center justify-between gap-2`}
                                >
                                    <div className="flex-1">
                                        <p className={`text-sm text-${theme.primary}-200`}>{mode.name}</p>
                                    </div>
                                    {cognitiveFocus === mode.id && (
                                        <Check className={`w-4 h-4 text-${theme.primary}-300 shrink-0`} />
                                    )}
                                </button>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    );
};

export default CognitiveFocusSelector;

