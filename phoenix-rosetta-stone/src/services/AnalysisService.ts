import { AnalysisReport, LocalFile, Violation } from '@essence/types';
import { astAnalyzer } from './ast/ASTAnalyzer';

/**
 * AnalysisService [OMEGA v15.0]
 * High-velocity, asynchronous architectural introspection.
 */

export const analyzeProjectStructureAsync = async (files: LocalFile[]): Promise<AnalysisReport> => {
    const violations: Violation[] = [];
    let filesParsed = 0;
    let totalImports = 0;
    let hardcodedColors = 0;

    const dependencyGraph: Record<string, string[]> = {};
    let totalClasses = 0;

    // Parallel processing
    await Promise.all(files.map(async (file) => {
        if (!shouldAnalyze(file.path)) return;

        filesParsed++;

        // 1. Structural Checks (Bloat)
        const lines = file.content.split('\n');
        if (lines.length > 300) {
            violations.push({
                file: file.path,
                line: 0,
                type: 'COMPONENT_BLOAT',
                message: `File exceeds 300 lines (${String(lines.length)}). Consider splitting into subobidient modules.`,
                severity: 'medium'
            });
        }

        // 2. OMEGA v15.1 Metrics
        // Dependency Graph Extraction
        const importMatches = Array.from(file.content.matchAll(/import\s+.*?\s+from\s+['"](.*?)['"]/g));
        const deps: string[] = [];
        for (const match of importMatches) {
            totalImports++;
            deps.push(match[1]);
        }
        dependencyGraph[file.path] = deps;

        // Count Classes (JSX className)
        const classMatches = file.content.match(/className=["']([^"']+)["']/g);
        if (classMatches) totalClasses += classMatches.length;

        // Count Hardcoded Colors (Hex)
        const colorMatches = file.content.match(/#([a-fA-F0-9]{3}){1,2}\b/g);
        if (colorMatches) {
            hardcodedColors += colorMatches.length;
            violations.push({
                file: file.path,
                line: 0,
                type: 'HARDCODED_COLOR',
                message: `Hardcoded color values detected (${String(colorMatches.length)}). Use theme tokens.`,
                severity: 'low'
            });
        }

        // 3. Deep AST Analysis
        try {
            // Offloaded to Web Worker via ASTAnalyzer
            const astViolations = await astAnalyzer.analyzeFile(file.path, file.content);
            astViolations.forEach((v) => {
                violations.push({
                    file: v.file, // v.file is guaranteed by ASTViolation type
                    line: v.line,
                    type: v.type,
                    message: v.message,
                    severity: v.severity || 'low'
                });
            });
        } catch (error) {
            console.error(`[AnalysisService] AST failure on ${file.path}:`, error);
        }
    }));

    return {
        violations,
        dependencyGraph,
        cycles: [], // Cycles require DFS/Tarjan's - placeholder for now (Packet C)
        propDrillingPaths: [],
        styleMetrics: {
            totalClasses,
            variablesUsed: 0,
            hardcodedColors,
            deepSelectors: 0,
        },
        stats: {
            filesParsed,
            totalImports,
        },
    };
};

const shouldAnalyze = (path: string): boolean => {
    return (/\.(ts|tsx|js|jsx)$/.exec(path)) !== null && !path.includes('node_modules');
};

