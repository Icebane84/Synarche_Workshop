// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React, { useMemo } from 'react';
import { useTheme } from '../../hooks/useTheme';
import { useCoherenceStore } from '../../store/coherenceStore';
import { NovaSpark } from '@essence/types';

interface NeuralStreamProps {
    novaSparks: NovaSpark[];
    theme: any;
}

const NeuralStreamBase: React.FC<NeuralStreamProps> = ({ novaSparks, theme }) => {
    // Memoize reversed sparks to avoid re-calculating on every render
    const reversedSparks = useMemo(() => [...novaSparks].reverse(), [novaSparks]);

    return (
        <div
            className={`flex-1 flex flex-col min-h-[150px] px-4 py-4 border-t border-${theme.primary}-500/10 mt-2 overflow-hidden`}
        >
            <h3
                className={`text-[10px] font-semibold tracking-widest text-${theme.primary}-400/50 uppercase mb-3 flex items-center gap-2`}
            >
                <div className={`w-1.5 h-1.5 rounded-full bg-${theme.primary}-400 animate-pulse`} />
                Neural Stream
            </h3>
            <div className="flex-1 overflow-y-auto scrollbar-none mask-fade-bottom">
                <div className="flex flex-col gap-3">
                    {reversedSparks.map((spark, index) => (
                        <div key={`${spark.id}-${index}`} className="flex flex-col gap-0.5 animate-fade-in-left group">
                            <span
                                className={`text-[9px] font-mono text-${theme.primary}-500/40 group-hover:text-${theme.primary}-400/60 transition-colors`}
                            >
                                {spark.timeString || '--:--:--'}
                            </span>
                            <span
                                className={`text-[10px] font-mono text-${theme.primary}-300/70 leading-tight group-hover:text-${theme.primary}-200 transition-colors`}
                            >
                                {spark.summary}
                            </span>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

// Convert to a Pure Component via React.memo
export const NeuralStream = React.memo(NeuralStreamBase);

// Container component to handle data subscription
const NeuralStreamContainer: React.FC = () => {
    const novaSparks = useCoherenceStore((state) => state.novaSparks);
    const theme = useTheme();

    return <NeuralStream novaSparks={novaSparks} theme={theme} />;
};

export default NeuralStreamContainer;

