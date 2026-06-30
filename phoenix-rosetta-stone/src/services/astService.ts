import { AnalysisReport, LocalFile } from '@essence/types';
import { analyzeProjectStructureAsync } from './AnalysisService';

/**
 * The Structural Eye [OMEGA v15.0 Facade].
 * Delegating to the High-Velocity AnalysisService for parallel AST introspection.
 * 
 * @deprecated Use analyzeProjectStructureAsync directly for new modules.
 */

// Maintaining the legacy synchronous signature for compatibility where possible,
// but marking as async-ready.
export const analyzeProjectStructure = async (files: LocalFile[]): Promise<AnalysisReport> => {
    try {
        return await analyzeProjectStructureAsync(files);
    } catch (error) {
        console.error('[astService] Sovereign analysis failure:', error);
        return {
            violations: [{
                file: 'system',
                line: 0,
                type: 'SYSTEM_FAILURE',
                message: `Critical Analysis Failure: ${error instanceof Error ? error.message : String(error)}`
            }],
            dependencyGraph: {},
            cycles: [],
            propDrillingPaths: [],
            styleMetrics: {
                totalClasses: 0,
                variablesUsed: 0,
                hardcodedColors: 0,
                deepSelectors: 0,
            },
            stats: {
                filesParsed: 0,
                totalImports: 0,
            },
        };
    }
};

