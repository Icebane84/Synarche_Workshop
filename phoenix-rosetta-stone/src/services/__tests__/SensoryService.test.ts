import { beforeEach, describe, expect, it, vi } from 'vitest';
import { fetchEnvironmentalData, getSystemTime } from '../sensoryService';

describe('SensoryService [Iron Resolve - OMEGA v15.0]', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Mock Geolocation
        const mockGeolocation = {
            getCurrentPosition: vi.fn().mockImplementation((success: (pos: any) => void) => {
                success({
                    coords: {
                        latitude: 40.7128,
                        longitude: -74.006,
                    },
                });
            }),
        };
        (global.navigator as never).geolocation = mockGeolocation;

        // Mock Fetch
        global.fetch = vi.fn().mockResolvedValue({
            json: () => ({
                current_weather: {
                    temperature: 22,
                    weathercode: 0,
                    is_day: 1,
                    windspeed: 10,
                },
            }),
        });
    });

    it('should fetch environmental data (Mocked Geolocation + Fetch)', async () => {
        const result = await fetchEnvironmentalData();
        expect(result.status).toBe('online');
        expect(result.location?.lat).toBe(40.7128);
        expect(result.weather?.temperature).toBe(22);
    });

    it('should fallback to Digital Void if Geolocation fails', async () => {
        (global.navigator.geolocation.getCurrentPosition as never).mockImplementation(
            (success: any, error: (err: any) => void) => {
                error(new Error('Permission Denied'));
            },
        );

        const result = await fetchEnvironmentalData();
        expect(result.location?.description).toContain('Digital Void');
        expect(result.location?.lat).toBe(0);
    });

    it('should implement 15-minute caching logic', async () => {
        // First call
        await fetchEnvironmentalData();
        expect(global.fetch).toHaveBeenCalledTimes(1);

        // Second call immediately after should NOT call fetch again
        await fetchEnvironmentalData();
        expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    it('should provide formatted system time', () => {
        const time = getSystemTime();
        // Regex for HH:MM:SS
        expect(time).toMatch(/\d{2}:\d{2}:\d{2}/);
    });
});
