// [OMEGA AST Cleaned]: Tokenized design standards applied.
import React from "react";
import { dispatchCommand, connectLocalFsCommand } from "../services";
import { useCoherenceStore } from "../store/coherenceStore";
import { useTheme } from "../hooks/useTheme";
import {
    Cloud,
    Sun,
    Moon,
    CloudRain,
    CloudSnow,
    CloudLightning,
    Wind,
    MapPin,
    Loader,
    Wifi,
    WifiOff,
} from "lucide-react";
import Tooltip from "./common/Tooltip";

interface WeatherIconProps {
    code: number;
    isDay: boolean;
    className?: string;
}

const WeatherIcon: React.FC<WeatherIconProps> = ({ code, isDay, className }) => {
    // WMO Weather interpretation codes (WW)
    // 0: Clear sky
    if (code === 0) {
        return isDay ? <Sun className={className} /> : <Moon className={className} />;
    }
    // 1, 2, 3: Mainly clear, partly cloudy, and overcast
    if ([1, 2, 3].includes(code)) {
        return <Cloud className={className} />;
    }
    // 45, 48: Fog
    if ([45, 48].includes(code)) {
        return <Wind className={className} />;
    }
    // 51, 53, 55, 56, 57: Drizzle
    // 61, 63, 65: Rain
    // 80, 81, 82: Rain showers
    if ([51, 53, 55, 56, 57, 61, 63, 65, 80, 81, 82].includes(code)) {
        return <CloudRain className={className} />;
    }
    // 71, 73, 75: Snow fall
    // 77: Snow grains
    // 85, 86: Snow showers
    if ([71, 73, 75, 77, 85, 86].includes(code)) {
        return <CloudSnow className={className} />;
    }
    // 95, 96, 99: Thunderstorm
    if ([95, 96, 99].includes(code)) {
        return <CloudLightning className={className} />;
    }

    // Default
    return <Cloud className={className} />;
};

const SensoryModule: React.FC = () => {
    const data = useCoherenceStore((state) => state.sensoryData);
    const theme = useTheme();

    const handleConnect = async () => {
        if (data.status === "offline") {
            await dispatchCommand(connectLocalFsCommand, {});
        }
    };

    return (
        <div
            className={`relative p-4 rounded-lg bg-black/30 border border-${theme.primary}-500/20 backdrop-blur-sm animate-fade-in-sm min-w-[250px]`}
        >
            {/* Header / Status Line */}
            <div className="flex items-center justify-between mb-3 border-b border-${theme.primary}-500/10 pb-2">
                <h3 className={`text-xs font-semibold tracking-widest uppercase text-${theme.primary}-400/80`}>
                    Sensory Bridge
                </h3>
                <div
                    onClick={() => { void handleConnect(); }}
                    className={`flex items-center gap-2 ${
                        data.status === "offline" ? "cursor-pointer hover:opacity-80" : ""
                    }`}
                    title={data.status === "offline" ? "Click to Initialize Neural Link" : "Link Active"}
                >
                    {data.status === "calibrating" && (
                        <Loader size={12} className={`text-${theme.primary}-400 animate-spin`} />
                    )}
                    {data.status === "online" && <Wifi size={12} className="text-emerald-400" />}
                    {data.status === "offline" && <WifiOff size={12} className="text-red-400" />}
                    <span
                        className={`text-[10px] font-mono ${
                            data.status === "online" ? "text-emerald-400" : "text-gray-500"
                        }`}
                    >
                        {data.status.toUpperCase()}
                    </span>
                </div>
            </div>

            {/* Time Display */}
            <div className="text-center mb-4">
                <div
                    className={`text-4xl font-light text-${theme.primary}-100 font-mono tracking-wider drop-shadow-lg`}
                >
                    {data.timeString}
                </div>
                <div className={`text-[10px] text-${theme.primary}-400/50 uppercase tracking-widest mt-1`}>
                    Local Temporal Reference
                </div>
            </div>

            {/* Environmental Data */}
            <div className="grid grid-cols-2 gap-2">
                {/* Location */}
                <div
                    className={`p-2 bg-${theme.primary}-900/10 rounded border border-${theme.primary}-500/10 flex flex-col items-center justify-center text-center`}
                >
                    <MapPin size={16} className={`text-${theme.primary}-400 mb-1`} />
                    {data.location ? (
                        <>
                            <p className={`text-xs text-${theme.primary}-200 font-medium`}>Active Sector</p>
                            <p className={`text-[10px] text-${theme.primary}-400/60 truncate max-w-full px-1`}>
                                {data.location.lat.toFixed(2)}, {data.location.lng.toFixed(2)}
                            </p>
                        </>
                    ) : (
                        <p className={`text-[10px] text-${theme.primary}-400/40 italic`}>Locating...</p>
                    )}
                </div>

                {/* Weather */}
                <div
                    className={`p-2 bg-${theme.primary}-900/10 rounded border border-${theme.primary}-500/10 flex flex-col items-center justify-center text-center`}
                >
                    {data.weather ? (
                        <>
                            <div className="flex items-center gap-2 mb-1">
                                <WeatherIcon
                                    code={data.weather.conditionCode}
                                    isDay={data.weather.isDay}
                                    className={`w-4 h-4 text-${theme.primary}-300`}
                                />
                                <span className={`text-sm text-${theme.primary}-200 font-medium`}>
                                    {data.weather.temperature}°C
                                </span>
                            </div>
                            <Tooltip label={`Wind: ${data.weather.windSpeed.toString()} km/h`}>
                                <p className={`text-[10px] text-${theme.primary}-400/60 truncate max-w-full`}>
                                    {data.weather.conditionText}
                                </p>
                            </Tooltip>
                        </>
                    ) : (
                        <p className={`text-[10px] text-${theme.primary}-400/40 italic`}>Scanning...</p>
                    )}
                </div>
            </div>

            <style>{`
                @keyframes fade-in-sm {
                    from { opacity: 0; transform: translateY(-5px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                .animate-fade-in-sm { animation: fade-in-sm 0.5s ease-out forwards; }
            `}</style>
        </div>
    );
};

export default SensoryModule;
