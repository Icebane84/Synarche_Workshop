import { SensoryData } from '@essence/types';
import { weatherCodeMap } from './sensory/weatherConstants';

/**
 * Sensory Bridge Service [OMEGA v15.0]
 * Handles environmental awareness (Time, Location, Weather) with caching.
 * Implements Sovereign Isolation to prevent UI-blocking sensor reads.
 */

interface WeatherApiResponse {
    current_weather: {
        temperature: number;
        weathercode: number;
        is_day: number;
        windspeed: number;
    };
}

interface CachedSensory {
    data: Partial<SensoryData>;
    timestamp: number;
}

// Internal State
let sensoryCache: CachedSensory | null = null;
const CACHE_TTL = 15 * 60 * 1000; // 15 Minutes (900,000ms)

/**
 * Gets the browser's current position using the Geolocation API.
 * Returns a Promise that resolves with a GeolocationPosition.
 */
const getPosition = (): Promise<GeolocationPosition> => {
    return new Promise((resolve, reject) => {
        // eslint-disable-next-line @typescript-eslint/no-unnecessary-condition
        if (!navigator.geolocation) {
            reject(new Error('GEOLOCATION_UNSUPPORTED: Browser lacks required sensors.'));
            return;
        }

        navigator.geolocation.getCurrentPosition(
            (pos) => {
                resolve(pos);
            },
            (err) => {
                reject(new Error(`GEOLOCATION_ERROR: ${String(err.message)}`));
            },
            { timeout: 10000, enableHighAccuracy: false },
        );
    });
};

/**
 * Fetches environmental data from Open-Meteo with 15-minute caching.
 * Orchestrates Geolocation and Weather Fetch into a single SensoryData object.
 */
export const fetchEnvironmentalData = async (): Promise<Partial<SensoryData>> => {
    const now = Date.now();

    // 1. Sovereign Cache Resolution
    if (sensoryCache && now - sensoryCache.timestamp < CACHE_TTL) {
        return sensoryCache.data;
    }

    try {
        // 2. Geolocation Acquisition
        const position = await getPosition();
        const { latitude, longitude } = position.coords;

        // 3. Weather Data Acquisition (Open-Meteo)
        // Note: No API key required for non-commercial use as per Open-Meteo terms.
        const weatherUrl = `https://api.open-meteo.com/v1/forecast?latitude=${latitude}&longitude=${longitude}&current_weather=true`;

        const weatherRes = await fetch(weatherUrl);
        if (!weatherRes.ok) {
            throw new Error(`WEATHER_API_FAILURE: HTTP ${weatherRes.status}`);
        }

        const weatherData = (await weatherRes.json()) as WeatherApiResponse;
        const current = weatherData.current_weather;

        const data: Partial<SensoryData> = {
            location: {
                lat: latitude,
                lng: longitude,
                description: `Sector [${latitude.toFixed(4).toString()}, ${longitude.toFixed(4).toString()}]`,
            },
            weather: {
                temperature: current.temperature,
                conditionCode: current.weathercode,
                conditionText: weatherCodeMap[current.weathercode] ?? 'Atmospheric Anomaly',
                isDay: current.is_day === 1,
                windSpeed: current.windspeed,
            },
            status: 'online',
        };

        // 4. Cache Update
        sensoryCache = { data, timestamp: now };
        return data;
    } catch (error) {
        // 5. Resilience Fallback (The "Digital Void" Protocol)
        // Ensures the system remains operational even in isolated or blocked environments.
        console.warn('[SensoryService] Environmental sense failure. Engaging Digital Void fallback.', error);

        return {
            location: {
                lat: 0,
                lng: 0,
                description: 'Digital Void (Sovereign Bypass)',
            },
            weather: {
                temperature: 20,
                conditionCode: 0,
                conditionText: 'Atmosphere Stable (Simulated)',
                isDay: true,
                windSpeed: 0,
            },
            status: 'online',
        };
    }
};

/**
 * Returns the current system time in HH:MM:SS format (24-hour).
 */
export const getSystemTime = (): string => {
    return new Date().toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
    });
};

