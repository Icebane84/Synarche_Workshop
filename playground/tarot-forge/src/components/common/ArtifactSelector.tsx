import React, { useEffect, useMemo, useRef, useState } from 'react';
import { createPortal } from 'react-dom';
import type { GraphNode } from '../../data/graphData';

interface ArtifactSelectorProps {
    artifacts: GraphNode[];
    selectedId: string | null;
    onSelect: (id: string) => void;
    placeholder: string;
    disabledId?: string | null;
}

const ArtifactSelector: React.FC<ArtifactSelectorProps> = ({
    artifacts,
    selectedId,
    onSelect,
    placeholder,
    disabledId,
}) => {
    const [query, setQuery] = useState('');
    const [isOpen, setIsOpen] = useState(false);
    const [dropdownPosition, setDropdownPosition] = useState({ top: 0, left: 0, width: 0 });

    const buttonRef = useRef<HTMLButtonElement>(null);
    const inputRef = useRef<HTMLInputElement>(null);

    const selectedArtifact = artifacts.find((a) => a.id === selectedId);

    const filteredArtifacts = useMemo(() => {
        return artifacts.filter(
            (a) => a.name.toLowerCase().includes(query.toLowerCase()) && a.id !== disabledId
        );
    }, [query, artifacts, disabledId]);

    const toggleDropdown = () => {
        if (!isOpen && buttonRef.current) {
            const rect = buttonRef.current.getBoundingClientRect();
            setDropdownPosition({
                top: rect.bottom + 8,
                left: rect.left,
                width: rect.width,
            });
            setIsOpen(true);
            setTimeout(() => inputRef.current?.focus(), 50);
        } else {
            setIsOpen(false);
        }
    };

    useEffect(() => {
        if (!isOpen) return;
        const handleInteraction = (e: Event) => {
            if (e.type === 'scroll' || e.type === 'resize') setIsOpen(false);
        };

        window.addEventListener('scroll', handleInteraction, true);
        window.addEventListener('resize', handleInteraction);

        const handleClickOutside = (e: MouseEvent) => {
            if (buttonRef.current && !buttonRef.current.contains(e.target as Node)) {
                const target = e.target as HTMLElement;
                if (!target.closest('.fixed.z-\\[9999\\]')) {
                    setIsOpen(false);
                }
            }
        };

        document.addEventListener('mousedown', handleClickOutside);

        return () => {
            window.removeEventListener('scroll', handleInteraction, true);
            window.removeEventListener('resize', handleInteraction);
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [isOpen]);

    const handleWrapperBlur = (_e: React.FocusEvent<HTMLDivElement>) => {
        // Redundant with portal logic
    };

    return (
        <div className="relative w-full" onBlur={handleWrapperBlur}>
            <button
                ref={buttonRef}
                type="button"
                className="w-full p-3 bg-black/30 border border-cyan-500/20 rounded-lg flex items-center justify-between cursor-pointer text-left hover:border-cyan-500/40 transition-colors"
                onClick={toggleDropdown}
            >
                {selectedArtifact ? (
                    <span className="text-cyan-200">{selectedArtifact.name}</span>
                ) : (
                    <span className="text-cyan-400/60">{placeholder}</span>
                )}
            </button>
            {isOpen &&
                createPortal(
                    <div
                        className="fixed z-[9999] max-h-80 overflow-y-auto bg-gray-900/95 backdrop-blur-md border border-cyan-500/30 rounded-lg shadow-[0_0_30px_rgba(0,0,0,0.8)] p-2 scrollbar-thin animate-fade-in-sm"
                        style={{
                            top: dropdownPosition.top,
                            left: dropdownPosition.left,
                            width: dropdownPosition.width,
                            minWidth: '320px',
                        }}
                    >
                        <input
                            ref={inputRef}
                            type="text"
                            value={query}
                            onChange={(e) => setQuery(e.target.value)}
                            placeholder="Search artifacts..."
                            className="w-full bg-black/40 p-3 rounded-md text-cyan-200 mb-2 focus:outline-none focus:ring-1 focus:ring-cyan-400 border border-transparent focus:border-cyan-500/30 font-mono text-sm"
                        />
                        <ul className="space-y-1">
                            {filteredArtifacts.map((artifact) => (
                                <li
                                    key={artifact.id}
                                    className="p-3 rounded-md hover:bg-cyan-500/20 cursor-pointer text-cyan-100 flex flex-col gap-0.5 transition-colors border border-transparent hover:border-cyan-500/10"
                                    onMouseDown={(e) => {
                                        e.preventDefault(); // Prevent blur
                                        onSelect(artifact.id);
                                        setIsOpen(false);
                                        setQuery('');
                                    }}
                                >
                                    <span className="font-medium tracking-wide">
                                        {artifact.name}
                                    </span>
                                    <span className="text-[10px] uppercase tracking-widest text-cyan-400/50">
                                        {artifact.type}
                                    </span>
                                </li>
                            ))}
                            {filteredArtifacts.length === 0 && (
                                <li className="p-4 text-center text-cyan-500/40 italic text-sm">
                                    No artifacts found.
                                </li>
                            )}
                        </ul>
                    </div>,
                    document.body
                )}
        </div>
    );
};

export default ArtifactSelector;
