import type { ReactElement } from 'react';
import { useEffect } from 'react';
import { useSharedConsciousness } from '../../store/sharedConsciousness';

export const ThemeGovernor = (): ReactElement | null => {
    const activeTheme = useSharedConsciousness((state) => state.stats.activeTheme);

    useEffect(() => {
        // Remove known theme classes
        document.body.classList.remove(
            'theme-void',
            'theme-chaos',
            'theme-structure',
            'theme-balance',
            'theme-destruction',
            'theme-creation' // Anticipatory
        );

        // Add the active theme class
        if (activeTheme) {
            document.body.classList.add(`theme-${activeTheme}`);
        }
    }, [activeTheme]);

    // This component renders nothing; it only governs the body class
    return null;
};
