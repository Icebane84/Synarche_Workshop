// [OMEGA AST Cleaned]: Tokenized design standards applied.
import { ASTViolation, RuleConfig } from './types';

// Valid file extensions for AST analysis
const VALID_EXTENSIONS = ['.ts', '.tsx', '.js', '.jsx'];

/**
 * The Structural Eye.
 * A Sovereign Module for deep architectural introspection using Abstract Syntax Trees.
 * Refactored to use a Web Worker for non-blocking analysis.
 */
export class ASTAnalyzer {
    private readonly config: RuleConfig;
    private worker: Worker | null = null;
    private readonly pendingRequests: Map<string, (violations: ASTViolation[]) => void> = new Map();

    constructor(config: RuleConfig = { enabled: true, maxPropDepth: 3 }) {
        this.config = config;
        this.initWorker();
    }

    private initWorker() {
        if (typeof window !== 'undefined') {
            try {
                // Use Vite's worker import syntax
                this.worker = new Worker(new URL('./ast.worker.ts', import.meta.url), {
                    type: 'module'
                });

                this.worker.onmessage = (event) => {
                    const { filePath, violations, success, error } = event.data;
                    if (!success) {
                        console.warn(`[ASTAnalyzer] Analysis deferred for ${filePath}:`, error);
                    }

                    const resolve = this.pendingRequests.get(filePath);
                    if (resolve) {
                        resolve(violations || []);
                        this.pendingRequests.delete(filePath);
                    }
                };
            } catch (err) {
                console.error('[ASTAnalyzer] Failed to initialize worker:', err);
            }
        }
    }

    /**
     * Performs a deep architectural scan of a file asynchronously via Web Worker.
     */
    public async analyzeFile(filePath: string, content: string): Promise<ASTViolation[]> {
        if (!this.config.enabled || !this.isValidFile(filePath)) {
            return [];
        }

        if (!this.worker) {
            console.warn('[ASTAnalyzer] Worker not initialized, falling back to empty results.');
            return [];
        }

        return new Promise((resolve) => {
            this.pendingRequests.set(filePath, resolve);
            this.worker?.postMessage({
                filePath,
                content,
                config: this.config
            });
        });
    }

    private isValidFile(filePath: string): boolean {
        const ignoredPaths = ['.trunk', '.archives', '_archive', 'node_modules', '.git'];
        if (ignoredPaths.some(ignored => filePath.includes(ignored))) {
            return false;
        }
        return VALID_EXTENSIONS.some(ext => filePath.endsWith(ext));
    }
}

// Singleton Instance
export const astAnalyzer = new ASTAnalyzer();
