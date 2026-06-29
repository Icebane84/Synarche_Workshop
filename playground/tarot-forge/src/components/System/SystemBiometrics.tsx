import { Activity, Gauge, Thermometer } from 'lucide-react';
import React from 'react';
import { useSystemMetrics } from '../../hooks/useSystemMetrics';
import { useTheme } from '../../hooks/useTheme';

const Sparkline: React.FC<{ data: number[]; color: string; min?: number; max?: number }> = ({
    data,
    color,
    min = 0,
    max = 100,
}) => {
    const width = 80;
    const height = 24;

    // Normalize data to fit SVG
    const points = data
        .map((val, i) => {
            const x = (i / (data.length - 1)) * width;
            // Clamp value
            const clampedVal = Math.max(min, Math.min(max, val));
            // Invert Y because SVG origin is top-left
            const normalizedY = (clampedVal - min) / (max - min);
            const y = height - normalizedY * height;
            return `${x},${y}`;
        })
        .join(' ');

    return (
        <svg width={width} height={height} className="overflow-visible">
            <polyline
                points={points}
                fill="none"
                stroke={color}
                strokeWidth="1.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                className="transition-all duration-300 ease-linear"
            />
        </svg>
    );
};

// Simplified Tooltip for now to avoid dependency on missing common component
const Tooltip: React.FC<{ label: string; children: React.ReactNode }> = ({ label, children }) => (
    <div className="group relative">
        {children}
        <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 px-2 py-1 bg-black/80 text-xs rounded text-white opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none whitespace-nowrap z-50">
            {label}
        </div>
    </div>
);

const SystemBiometrics: React.FC = () => {
    const metrics = useSystemMetrics();
    const theme = useTheme();

    const currentFps = metrics.pulse[metrics.pulse.length - 1];
    const currentLoad = (metrics.pressure[metrics.pressure.length - 1] * 100).toFixed(0);
    const currentTemp = (metrics.temp[metrics.temp.length - 1] * 100).toFixed(0);

    return (
        <div className={`p-4 bg-black/20 border-t border-${theme.primary}-500/20 backdrop-blur-sm`}>
            <h4
                className={`text-[10px] font-semibold tracking-widest text-${theme.primary}-400/50 uppercase mb-3`}
            >
                System Biometrics
            </h4>

            <div className="space-y-3">
                {/* Pulse (FPS) */}
                <div className="flex items-center justify-between">
                    <Tooltip label="System Pulse (Frame Rate)">
                        <div className="flex items-center gap-2 w-20">
                            <Activity size={14} className="text-emerald-400" />
                            <span className="text-xs font-mono text-emerald-200">
                                {currentFps} Hz
                            </span>
                        </div>
                    </Tooltip>
                    <Sparkline data={metrics.pulse} color="#34d399" min={0} max={60} />
                </div>

                {/* Pressure (Cognitive Load) */}
                <div className="flex items-center justify-between">
                    <Tooltip label="Cognitive Pressure (Processing Load)">
                        <div className="flex items-center gap-2 w-20">
                            <Gauge size={14} className="text-amber-400" />
                            <span className="text-xs font-mono text-amber-200">{currentLoad}%</span>
                        </div>
                    </Tooltip>
                    <Sparkline
                        data={metrics.pressure.map((v) => v * 100)}
                        color="#fbbf24"
                        min={0}
                        max={100}
                    />
                </div>

                {/* Temperature (Dissonance/Entropy) */}
                <div className="flex items-center justify-between">
                    <Tooltip label="Core Temperature (Entropy Level)">
                        <div className="flex items-center gap-2 w-20">
                            <Thermometer size={14} className="text-rose-400" />
                            <span className="text-xs font-mono text-rose-200">{currentTemp}°</span>
                        </div>
                    </Tooltip>
                    <Sparkline
                        data={metrics.temp.map((v) => v * 100)}
                        color="#fb7185"
                        min={0}
                        max={100}
                    />
                </div>
            </div>
        </div>
    );
};

export default SystemBiometrics;
