import { useSharedConsciousness } from '../store/sharedConsciousness';

interface Theme {
    name: string;
    primary: string; // Main accent color (e.g., 'cyan')
    secondary: string; // Secondary accent (e.g., 'blue')
    font: string; // 'font-sans' or 'font-mono'
    bgGradient: string; // Tailwind gradient classes
}

const themes: Record<string, Theme> = {
    void: {
        name: 'The Void',
        primary: 'cyan',
        secondary: 'indigo',
        font: 'font-sans',
        bgGradient: 'from-gray-900 via-cyan-900/50 to-gray-900',
    },
    Standard: {
        name: 'Luminous Coherence',
        primary: 'cyan',
        secondary: 'blue',
        font: 'font-sans',
        bgGradient: 'from-gray-900 via-cyan-900/50 to-gray-900',
    },
    'Security Audit': {
        name: 'Matrix Protocol',
        primary: 'emerald',
        secondary: 'green',
        font: 'font-mono', // Monospace for code/security focus
        bgGradient: 'from-black via-green-900/40 to-black',
    },
    'Creative Ideation': {
        name: 'Nebula Drift',
        primary: 'violet', // or fuchsia
        secondary: 'fuchsia',
        font: 'font-sans',
        bgGradient: 'from-gray-900 via-violet-900/50 to-gray-900',
    },
    Strategy: {
        name: 'Command Amber',
        primary: 'amber',
        secondary: 'orange',
        font: 'font-sans',
        bgGradient: 'from-gray-900 via-amber-900/30 to-black',
    },
};

export const useTheme = () => {
    const activeTheme = useSharedConsciousness((state) => state.stats.activeTheme);
    return themes[activeTheme] || themes['void'];
};
