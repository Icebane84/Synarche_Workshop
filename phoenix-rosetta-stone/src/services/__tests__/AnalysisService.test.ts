import { describe, it, expect, vi } from 'vitest';
import { analyzeProjectStructureAsync } from '../AnalysisService';
import { LocalFile } from '@essence/types';

describe('AnalysisService [Iron Resolve - OMEGA v15.0]', () => {
    const mockFile: LocalFile = {
        path: 'src/components/Test.tsx',
        name: 'Test.tsx',
        content: `
            import React from 'react';
            import { Button } from './Button';
            
            export const Test = () => {
                const color = '#ff0000'; // Hardcoded!
                console.log('Test');
                return <div style={{ color }}>Hello</div>;
            };
        `,
        handle: {} as any
    };

    it('should perform parallel analysis (Async/Await)', async () => {
        const result = await analyzeProjectStructureAsync([mockFile]);
        expect(result).toBeDefined();
        expect(result.stats.filesParsed).toBe(1);
    });

    it('should detect COMPONENT_BLOAT for files exceeding 300 lines', async () => {
        const largeContent = Array(301).fill('// line').join('\n');
        const largeFile: LocalFile = { ...mockFile, content: largeContent };
        
        const result = await analyzeProjectStructureAsync([largeFile]);
        const bloat = result.violations.find(v => v.type === 'COMPONENT_BLOAT');
        expect(bloat).toBeDefined();
        expect(bloat?.message).toContain('exceeds 300 lines');
    });

    it('should calculate OMEGA v15.0 metrics: totalImports', async () => {
        const result = await analyzeProjectStructureAsync([mockFile]);
        // The mock file has 2 imports (React, Button)
        expect(result.stats.totalImports).toBe(2);
    });

    it('should calculate OMEGA v15.0 metrics: hardcodedColors', async () => {
        const result = await analyzeProjectStructureAsync([mockFile]);
        // The mock file has 1 hex code (#ff0000)
        expect(result.styleMetrics.hardcodedColors).toBeGreaterThan(0);
    });

    it('should delegate to ASTAnalyzer for deep violations', async () => {
        const result = await analyzeProjectStructureAsync([mockFile]);
        // ASTAnalyzer-specific rule check (detectConsoleLog)
        const logViolation = result.violations.find(v => v.type === 'CONSOLE_LOG_DETECTION' || v.type === 'DISALLOWED_LOG');
        expect(logViolation).toBeDefined();
    });
});

