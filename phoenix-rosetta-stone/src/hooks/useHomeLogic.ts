import { useState } from 'react';

const TUTORIAL_STORAGE_KEY = 'phoenix_tutorial_dismissed';

/**
 * @fileoverview Hook for managing HomePage high-level UI state (tutorial).
 */
export const useHomeLogic = () => {
    const [showTutorial, setShowTutorial] = useState(() => {
        return !localStorage.getItem(TUTORIAL_STORAGE_KEY);
    });

    const handleDismissTutorial = () => {
        setShowTutorial(false);
        localStorage.setItem(TUTORIAL_STORAGE_KEY, 'true');
    };

    return {
        showTutorial,
        handleDismissTutorial,
    };
};
