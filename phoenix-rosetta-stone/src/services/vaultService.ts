// -----------------------------------------------------------------------------
// PHOENIX SYNARCHE PROTOCOL - VAULT SERVICE
// -----------------------------------------------------------------------------
//
// UNIVERSAL IDENTIFICATION & PROVENANCE (UIP)
// 1. Artifact ID:    SRVC-VAULT-001
// 2. Official Name:  VaultService
// 3. Version:        v15.1 (Resonant)
// 4. Domain:         NEXUS
// 5. Celestial Class: [STAR]
// 6. Status:         [ACTIVE]
//
// -----------------------------------------------------------------------------

import { signalBus, SignalType } from '../system/signalBus';

/**
 * Interface representing a result entry from the Obsidian Vault API.
 */
interface VaultResult {
    path: string;
    content: string;
    score?: number;
}

class VaultService {
    private static instance: VaultService;
    
    // Type casting environment variables to ensure string integrity
    private readonly API_KEY = (import.meta.env.VITE_OBSIDIAN_API_KEY as string) ?? ""; 
    private readonly BASE_URL = (import.meta.env.VITE_OBSIDIAN_URL as string) ?? "https://127.0.0.1:27124";

    private constructor() {
        // Constructor remains private for singleton pattern
    }

    public static getInstance(): VaultService {
        if (!VaultService.instance) {
            VaultService.instance = new VaultService();
        }
        return VaultService.instance;
    }

    /**
     * Executes a semantic search against the Obsidian Vault.
     * Emits VAULT_CONTEXT_READY on success.
     */
    public async getGraphContext(query: string): Promise<string> {
        try {
            const searchUrl = `${this.BASE_URL}/search/simple/?query=${encodeURIComponent(query)}`;
            const response = await fetch(searchUrl, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.API_KEY}`,
                    'Content-Type': 'application/json'
                }
            });

            if (!response.ok) {
                return "No vault context found.";
            }

            // Typing the response data
            const results = (await response.json()) as VaultResult[];
            
            // Emit signal to let the UI react
            signalBus.emit(SignalType.VAULT_CONTEXT_READY, {
                query,
                resultsCount: results.length,
                data: results
            });

            return JSON.stringify(results);
        } catch (error) {
            console.error("Vault retrieval error:", error);
            return "No vault context found.";
        }
    }
}

export const vaultService = VaultService.getInstance();
