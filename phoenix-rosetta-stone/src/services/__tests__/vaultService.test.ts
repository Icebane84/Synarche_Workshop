/**
 * @fileoverview VaultService TDD Specification [PRS-003]
 * Follows OMEGA v15.1 Isolation-First Protocol.
 */
import { describe, it, expect, vi, beforeEach, Mock } from 'vitest';
import { vaultService } from '@/services/vaultService';
import { signalBus, SignalType } from '@system/signalBus';

// Mock the SignalBus to verify decoupled communication
vi.mock('@system/signalBus', () => ({
    signalBus: {
        emit: vi.fn(),
    },
    SignalType: {
        VAULT_CONTEXT_READY: 'VAULT_CONTEXT_READY',
    },
}));

// Mock global fetch
global.fetch = vi.fn();
const mockedFetch = vi.mocked(fetch);

describe('VaultService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('should successfully fetch context and emit a signal', async () => {
        const mockResponse = {
            ok: true,
            json: () => Promise.resolve([
                { path: 'note1.md', content: 'note content', score: 0.9 }
            ]),
        } as Response;
        
        mockedFetch.mockResolvedValue(mockResponse);

        const context = await vaultService.getGraphContext('Synarche');

        expect(context).toBeDefined();
        // Since we are checking JSON output, we parse it back
        const parsed = JSON.parse(context);
        expect(parsed[0].path).toBe('note1.md');
        
        expect(signalBus.emit).toHaveBeenCalledWith(
            SignalType.VAULT_CONTEXT_READY,
            expect.objectContaining({ query: 'Synarche' })
        );
    });

    it('should handle API errors gracefully', async () => {
        mockedFetch.mockResolvedValue({ ok: false, status: 500 } as Response);

        const context = await vaultService.getGraphContext('ErrorQuery');

        expect(context).toBe('No vault context found.');
        expect(signalBus.emit).not.toHaveBeenCalled();
    });
});
