import { describe, it, expect } from 'vitest';
import { ARCHETYPES } from './Archetypes';

describe('Archetypes Engine', () => {
    it('should load the archetype registry', () => {
        expect(ARCHETYPES.length).toBeGreaterThan(0);
    });

    it('should have unique IDs for all archetypes', () => {
        const ids = ARCHETYPES.map((a) => a.id);
        const uniqueIds = new Set(ids);
        expect(uniqueIds.size).toBe(ids.length);
    });

    it('should have valid unlock levels', () => {
        ARCHETYPES.forEach((card) => {
            expect(card.unlockLevel).toBeGreaterThanOrEqual(0);
        });
    });

    it('should define a valid theme for every card', () => {
        ARCHETYPES.forEach((card) => {
            expect(card.theme).toBeDefined();
            expect(typeof card.theme).toBe('string');
        });
    });
});
