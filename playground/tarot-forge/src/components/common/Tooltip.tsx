import React, { useEffect, useRef, useState } from 'react';
import { createPortal } from 'react-dom';

interface TooltipProps {
    label: string;
    children: React.ReactNode;
    className?: string;
}

const Tooltip: React.FC<TooltipProps> = ({ label, children, className }) => {
    const [isVisible, setIsVisible] = useState(false);
    const [coords, setCoords] = useState({ top: 0, left: 0 });
    const triggerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        if (isVisible && triggerRef.current) {
            const rect = triggerRef.current.getBoundingClientRect();
            // Calculate position: Centered above the element
            const top = rect.top - 8; // 8px buffer
            const left = rect.left + rect.width / 2;
            setCoords({ top, left });
        }
    }, [isVisible]);

    return (
        <div
            ref={triggerRef}
            className={`relative ${className || ''}`}
            onMouseEnter={() => setIsVisible(true)}
            onMouseLeave={() => setIsVisible(false)}
        >
            {children}
            {isVisible &&
                createPortal(
                    <div
                        className="fixed z-[9999] px-3 py-1.5 bg-gray-900 text-cyan-200 text-xs border border-cyan-500/30 rounded-md shadow-lg shadow-cyan-500/10 pointer-events-none transform -translate-x-1/2 -translate-y-full whitespace-nowrap animate-fade-in-fast"
                        style={{ top: coords.top, left: coords.left }}
                    >
                        {label}
                    </div>,
                    document.body
                )}
            <style>{`
        @keyframes fade-in-fast {
            from { opacity: 0; transform: translate(-50%, -90%); }
            to { opacity: 1; transform: translate(-50%, -100%); }
        }
        .animate-fade-in-fast { animation: fade-in-fast 0.15s ease-out forwards; }
      `}</style>
        </div>
    );
};

export default Tooltip;
