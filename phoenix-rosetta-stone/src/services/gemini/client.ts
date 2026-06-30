import { GoogleGenAI } from '@google/genai';
import { systemConfig } from '../configService';

/**
 * @fileoverview Low-level client configuration and shared logic for Gemini API.
 */

export const getGeminiClient = () => {
    if (!systemConfig.api.geminiKey) {
        throw new Error('Gemini Service is not available. Please configure the API Key.');
    }
    return new GoogleGenAI({ apiKey: systemConfig.api.geminiKey as string });
};

/**
 * Executes a call to the Gemini API with retry logic for rate limits (429).
 */
export const callGeminiWithRetry = async <T>(
    operation: () => Promise<T>,
    maxRetries = 3,
): Promise<T> => {
    let attempts = 0;
    while (attempts < maxRetries) {
        try {
            return await operation();
        } catch (err: unknown) {
            const apiErr = err as { status?: number; code?: number; message?: string };
            if (
                apiErr.status === 429 ||
                apiErr.code === 429 ||
                apiErr.message?.includes('429') ||
                apiErr.message?.includes('quota')
            ) {
                attempts++;
                if (attempts >= maxRetries) throw err;
                const waitTime = attempts * 5000; // 5s, 10s...
                console.warn(`[Gemini] Rate Limit Hit (429). Retrying in ${String(waitTime)}ms...`);
                await new Promise((resolve) => setTimeout(resolve, waitTime));
                continue;
            }
            throw err;
        }
    }
    throw new Error('Failed to generate response after retries.');
};
