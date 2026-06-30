import { File } from '@babel/types';

export type ASTNode = File; // Root node type from Babel

export type ViolationType = 
    | 'PROP_DRILLING' 
    | 'CIRCULAR_DEPENDENCY' 
    | 'COMPONENT_BLOAT' 
    | 'HOOK_VIOLATION'
    | 'CONSOLE_LOG'
    | 'LINT_ENTROPY'
    | 'UNUSED_IMPORT'
    | 'ARCHITECTURAL_DISSONANCE';

export interface ASTViolation {
    file: string;
    line: number;
    type: ViolationType;
    message: string;
    severity: 'low' | 'medium' | 'high' | 'critical';
    codeSnippet?: string;
    start?: number; // Byte offset start
    end?: number;   // Byte offset end
    nodeData?: any; // Original node metadata
}

export interface RuleConfig {
    enabled: boolean;
    maxPropDepth?: number;
    maxComponentLines?: number;
}

export interface InspectionContext {
    filePath: string;
    content: string;
    ast: ASTNode;
}

export type ASTRule = (context: InspectionContext, config: RuleConfig) => ASTViolation[];
