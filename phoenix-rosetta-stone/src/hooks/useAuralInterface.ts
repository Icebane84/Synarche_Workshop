import { useState, useEffect, useRef, useCallback } from 'react';
import { createRecognitionSession, SpeechRecognitionHandler, transmitAuralResponse } from '../services/audioService';
import { useSignal } from './useSignal';
import { SignalType } from '@system/signalBus';

interface UseAuralInterfaceReturn {
  isListening: boolean;
  transcript: string;
  error: string | null;
  startListening: () => void;
  stopListening: () => void;
  speak: (text: string) => void;
  resetTranscript: () => void;
}

export const useAuralInterface = (): UseAuralInterfaceReturn => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [error, setError] = useState<string | null>(null);
  
  const recognitionRef = useRef<SpeechRecognitionHandler | null>(null);

  // --- [NEURAL FEEDBACK LOGIC] ---
  const playNeuralPing = useCallback((type: 'neutral' | 'resonant' | 'echo' = 'neutral') => {
    // Basic Web Audio Oscillator for zero-dependency feedback
    const AudioContextClass = window.AudioContext || window.webkitAudioContext;
    const ctx = new AudioContextClass();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();

    osc.type = 'sine';
    // Frequency based on signal type
    const frequencies = { neutral: 880, resonant: 1320, echo: 440 };
    osc.frequency.setValueAtTime(frequencies[type], ctx.currentTime);
    
    gain.gain.setValueAtTime(0, ctx.currentTime);
    gain.gain.linearRampToValueAtTime(0.05, ctx.currentTime + 0.05); // Subtle ping
    gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.3);

    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.start();
    osc.stop(ctx.currentTime + 0.3);
  }, []);

  useSignal(SignalType.AURAL_ECHO, (data) => {
    if (!data.meta?.isGlobal) return;
    playNeuralPing((data.payload?.type as any) || 'neutral');
  }, [playNeuralPing]);
  // -------------------------------

  useEffect(() => {
    // Initialize recognition session logic
    recognitionRef.current = createRecognitionSession(
      (text) => { setTranscript(text); },
      () => { setIsListening(false); },
      (err) => {
        setError(err);
        setIsListening(false);
      }
    );
  }, []);

  const startListening = useCallback(() => {
    if (recognitionRef.current && !isListening) {
      setError(null);
      setTranscript(''); // Clear previous input
      try {
        recognitionRef.current.start();
        setIsListening(true);
        // Audio cue for listening start
        // transmitAuralResponse("Listening."); 
      } catch (e) {
        console.error("Failed to start listening:", e);
      }
    }
  }, [isListening]);

  const stopListening = useCallback(() => {
    if (recognitionRef.current && isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    }
  }, [isListening]);

  const speak = useCallback((text: string) => {
    transmitAuralResponse(text);
  }, []);

  const resetTranscript = useCallback(() => {
      setTranscript('');
  }, []);

  return {
    isListening,
    transcript,
    error,
    startListening,
    stopListening,
    speak,
    resetTranscript
  };
};