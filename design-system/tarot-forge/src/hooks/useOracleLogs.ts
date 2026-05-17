import { useState, useCallback } from 'react';

export type LogEntry = {
    id: string;
    timestamp: string;
    content: string;
    type: 'info' | 'success' | 'error' | 'system';
};

export function useOracleLogs(): {
    logs: LogEntry[];
    addLog: (content: string, type?: 'info' | 'success' | 'error' | 'system') => void;
    clearLogs: () => void;
} {
    const [logs, setLogs] = useState<LogEntry[]>([
        {
            id: 'init',
            timestamp: new Date().toLocaleTimeString(),
            content: 'Synarche KERNEL INITIALIZED...',
            type: 'system',
        },
    ]);

    const addLog = useCallback((content: string, type: 'info' | 'success' | 'error' | 'system' = 'info'): void => {
        const newLog: LogEntry = {
            id: Math.random().toString(36).substr(2, 9),
            timestamp: new Date().toLocaleTimeString(),
            content,
            type,
        };
        setLogs((prev) => [...prev, newLog]);
    }, []);

    const clearLogs = useCallback((): void => {
        setLogs([]);
    }, []);

    return { logs, addLog, clearLogs };
}
