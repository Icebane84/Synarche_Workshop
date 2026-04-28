/**
 * @nexus/useNexusHandshake.ts — Sovereign Gateway Hook
 * ==================================================
 * [OMNI-ARTIFACT-ANCHOR] ID: NEXUS.Hook.Handshake VER: v3.1.0 STATUS: ACTIVE
 * Objective: Initialize SharedWorker, solve @shield challenge, and sync StateVector.
 */

import { useState, useEffect, useCallback } from 'react';

const SYSTEMIC_SECRET = "PHOENIX_INIT_VECTOR_001";

export const useNexusHandshake = () => {
    const [isAuthorized, setIsAuthorized] = useState(false);
    const [nexusState, setNexusState] = useState({ syncCount: 0, lastEvent: "BOOTING" });
    const [worker, setWorker] = useState<SharedWorker | null>(null);

    // I. Cryptographic Solve Engine
    const solveChallenge = useCallback(async (challenge: string) => {
        const encoder = new TextEncoder();
        const data = encoder.encode(challenge + SYSTEMIC_SECRET);
        const hash = await crypto.subtle.digest('SHA-256', data);
        return btoa(String.fromCharCode(...new Uint8Array(hash)));
    }, []);

    useEffect(() => {
        // II. Initialize Nexus Worker
        // Note: Using relative path from the compiled location or resolving via URL
        const nexusWorker = new SharedWorker(new URL('./nexus_handshake.js', import.meta.url));
        const port = nexusWorker.port;
        port.start();

        port.onmessage = async (msg) => {
            const { type, challenge, payload } = msg.data;

            switch (type) {
                case 'AUTH_CHALLENGE':
                    const signature = await solveChallenge(challenge);
                    port.postMessage({ type: 'HANDSHAKE_RESPONSE', payload: { challenge }, signature });
                    break;

                case 'AUTH_SUCCESS':
                    setIsAuthorized(true);
                    setNexusState(payload);
                    break;

                case 'STATE_UPDATE':
                    setNexusState(payload.state);
                    break;

                case 'AUTH_FAIL':
                    console.error("Nexus Handshake Failed: Invalid Signature");
                    port.close();
                    break;
            }
        };

        setWorker(nexusWorker);
        return () => port.close();
    }, [solveChallenge]);

    // III. Authorized Command: SYNC
    const triggerSync = useCallback(() => {
        if (isAuthorized && worker) {
            worker.port.postMessage({ type: 'SYNC' });
        }
    }, [isAuthorized, worker]);

    return { isAuthorized, nexusState, triggerSync };
};
