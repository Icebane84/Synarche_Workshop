// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { GoogleGenAI, Modality } from '@google/genai';
import { useCoherenceStore } from '../store/coherenceStore';
import { SpeechRecognitionErrorEvent, SpeechRecognitionEvent } from '@essence/types';
import { systemConfig } from './configService';

/**
 * @fileoverview The Aural Interface Service (Subspace Comms).
 * Implements high-fidelity TTS using gemini-2.5-flash-preview-tts
 * and custom PCM decoding logic.
 */

const ai = new GoogleGenAI({ apiKey: systemConfig.api.geminiKey });
let synthesisVoice: SpeechSynthesisVoice | null = null;
let audioContext: AudioContext | null = null;

const initBrowserVoice = () => {
    if (typeof window === 'undefined') return;
    const voices = window.speechSynthesis.getVoices();
    synthesisVoice =
        voices.find((v) => v.name.includes('Google US English')) ??
        voices.find((v) => v.name.includes('Zira')) ??
        voices.find((v) => v.name.includes('Samantha')) ??
        voices[0];
};

if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    window.speechSynthesis.onvoiceschanged = initBrowserVoice;
}

/**
 * Manual Base64 to Uint8Array decoding.
 */
function decodeBase64(base64: string) {
    const binaryString = atob(base64);
    const len = binaryString.length;
    const bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binaryString.charCodeAt(i);
    }
    return bytes;
}

/**
 * Decodes raw 16-bit PCM data returned by Gemini TTS.
 * Browser AudioContext.decodeAudioData does not support raw streams.
 */
function decodeAudioData(
    data: Uint8Array,
    ctx: AudioContext,
    sampleRate: number,
    numChannels: number,
): AudioBuffer {
    const dataInt16 = new Int16Array(data.buffer);
    const frameCount = dataInt16.length / numChannels;
    const buffer = ctx.createBuffer(numChannels, frameCount, sampleRate);

    for (let channel = 0; channel < numChannels; channel++) {
        const channelData = buffer.getChannelData(channel);
        for (let i = 0; i < frameCount; i++) {
            channelData[i] = dataInt16[i * numChannels + channel] / 32768.0;
        }
    }
    return buffer;
}

// Circuit Breaker State
let isRateLimited = false;
let rateLimitResetTime = 0;

const playGeminiSpeech = async (text: string) => {
    if (!systemConfig.api.geminiKey) return false;

    // Circuit Breaker Check
    if (isRateLimited) {
        if (Date.now() < rateLimitResetTime) {
            console.warn('[Voice of the Machine] Rate limit active. Using browser fallback.');
            return false;
        }
        isRateLimited = false; // Reset if time passed
    }

    const focus = useCoherenceStore.getState().cognitiveFocus;
    let voiceName = 'Zephyr';
    let emotionPrefix = 'Say calmly: ';

    // Personality Mapping based on Cognitive Focus
    if (focus === 'Security Audit') {
        voiceName = 'Charon';
        emotionPrefix = 'Say strictly and clearly: ';
    } else if (focus === 'Creative Ideation') {
        voiceName = 'Kore';
        emotionPrefix = 'Say inspirationally and melodic: ';
    } else if (focus === 'Strategy') {
        voiceName = 'Fenrir';
        emotionPrefix = 'Say authoritative and resonant: ';
    }

    try {
        const response = await ai.models.generateContent({
            model: 'gemini-2.0-flash-lite-001', // Trying Flash Lite for better quota
            contents: [{ parts: [{ text: `${emotionPrefix}${text}` }] }],
            config: {
                responseModalities: [Modality.AUDIO],
                speechConfig: {
                    voiceConfig: {
                        prebuiltVoiceConfig: { voiceName },
                    },
                },
            },
        });

        const base64Audio = response.data;
        if (!base64Audio) return false;

        let ctx = audioContext;
        if (!ctx) {
            const AudioContextClass = window.AudioContext || window.webkitAudioContext;
            ctx = new AudioContextClass({ sampleRate: 24000 });
            audioContext = ctx;
        }

        const audioBuffer = decodeAudioData(decodeBase64(base64Audio), ctx, 24000, 1);

        const source = ctx.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(ctx.destination);
        source.start();
        return true;
    } catch (err: unknown) {
        const errorMessage = err instanceof Error ? err.message : String(err);
        const isRateLimit = errorMessage.includes('429') || 
                           errorMessage.includes('RESOURCE_EXHAUSTED') ||
                           (typeof err === 'object' && err !== null && 'status' in err && (err as {status: number}).status === 429);

        if (isRateLimit) {
            console.warn(
                '[Voice of the Machine] Gemini TTS Rate Limit Exceeded. Switching to local synthesis for 60 seconds.',
            );
            isRateLimited = true;
            rateLimitResetTime = Date.now() + 60000; // 60s cooldown
        } else {
            console.warn('[Voice of the Machine] Gemini TTS failed, falling back to browser synthesis.', err);
        }
        return false;
    }
};

export const stopAuralResponse = () => {
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
        window.speechSynthesis.cancel();
    }
    if (audioContext) {
        try {
            void audioContext.close();
            audioContext = null;
        } catch {
            // Ignore close errors
        }
    }
};

export const transmitAuralResponse = async (text: string) => {
    stopAuralResponse();
    const success = await playGeminiSpeech(text);
    if (success) return;

    if (!('speechSynthesis' in window)) return;

    // Clean markdown symbols from text for clearer speech synthesis
    const cleanText = text
        .replace(/`{1,3}[\s\S]*?`{1,3}/g, '')
        .replace(/[*#_~[\]()]/g, ' ')
        .replace(/TOOL_CALL:.*$/gm, '')
        .trim();

    if (!cleanText) return;

    const utterance = new SpeechSynthesisUtterance(cleanText);
    if (!synthesisVoice) initBrowserVoice();
    if (synthesisVoice) utterance.voice = synthesisVoice;

    utterance.pitch = 1.0;
    utterance.rate = 1.05;
    utterance.volume = 0.9;

    window.speechSynthesis.speak(utterance);
};

export interface SpeechRecognitionHandler {
    start: () => void;
    stop: () => void;
    onResult: (transcript: string) => void;
    onEnd: () => void;
    onError: (error: string) => void;
}

export const createRecognitionSession = (
    onResult: (text: string) => void,
    onEnd: () => void,
    onError: (err: string) => void,
): SpeechRecognitionHandler | null => {
    const SpeechRecognitionClass = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

    if (!SpeechRecognitionClass) {
        console.warn('[Aural Interface] Speech Recognition not supported.');
        return null;
    }

    const recognition = new SpeechRecognitionClass();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onresult = (event: SpeechRecognitionEvent) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            finalTranscript += event.results[i][0].transcript;
        }
        if (finalTranscript) {
            onResult(finalTranscript);
        }
    };

    recognition.onend = () => {
        onEnd();
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
        console.error('[Aural Interface] Error:', event.error);
        onError(event.error);
    };

    return {
        start: () => { recognition.start(); },
        stop: () => { recognition.stop(); },
        onResult,
        onEnd,
        onError,
    };
};

