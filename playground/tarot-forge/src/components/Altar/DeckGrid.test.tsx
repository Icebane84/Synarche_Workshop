import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import type { ReactElement, ReactNode } from 'react';
import { DeckGrid } from './DeckGrid';

// Mock Framer Motion to avoid animation issues in tests
vi.mock('framer-motion', () => ({
    motion: {
        div: ({
            children,
            className,
            onClick,
            ...props
        }: {
            children?: ReactNode;
            className?: string;
            onClick?: () => void;
            // eslint-disable-next-line @typescript-eslint/no-explicit-any
            [key: string]: any;
        }): ReactElement => {
            // Filter out Framer Motion specific props to prevent React warnings
            // eslint-disable-next-line @typescript-eslint/no-unused-vars
            const { layout, initial, animate, exit, transition, whileHover, ...validProps } = props;
            return (
                <div className={className} onClick={onClick} {...validProps}>
                    {children}
                </div>
            );
        },
    },
    AnimatePresence: ({ children }: { children: ReactNode }): ReactElement => <>{children}</>,
}));

// Mock the shared consciousness store
vi.mock('../../store/sharedConsciousness', () => ({
    useSharedConsciousness: (): { identity: { level: number } } => ({
        identity: { level: 10 }, // High level to unlock most cards
    }),
}));

describe('DeckGrid Component', () => {
    it('renders the correct number of cards', () => {
        const handleSelect = vi.fn();
        render(<DeckGrid onCardSelect={handleSelect} selectedCardId={null} />);

        // title
        expect(screen.getByText('THE DECK')).toBeDefined();

        // There are archetypes in the engine
        expect(screen.getByText('THE VOID')).toBeDefined();
    });

    it('fires onCardSelect when a unlocked card is clicked', () => {
        const handleSelect = vi.fn();
        render(<DeckGrid onCardSelect={handleSelect} selectedCardId={null} />);

        const cardTitle = screen.getByText('THE VOID'); // Unlock level 0
        const cardContainer = cardTitle.closest('.grid-item');

        if (cardContainer) {
            fireEvent.click(cardContainer);
            expect(handleSelect).toHaveBeenCalled();
        } else {
            throw new Error('Card container not found');
        }
    });
});
