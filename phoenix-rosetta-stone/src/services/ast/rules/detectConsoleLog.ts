import { ASTRule, ASTViolation } from '../types';
import _babelTraverse from '@babel/traverse';

const getTraverseFn = (): any => {
    if (typeof _babelTraverse === 'function') return _babelTraverse;
    if (typeof (_babelTraverse as any)?.default === 'function') return (_babelTraverse as any).default;
    if (typeof (_babelTraverse as any)?.traverse === 'function') return (_babelTraverse as any).traverse;
    return null;
};

/**
 * Rule: Detect console.log statements.
 * Part of the "Zero Entropy" standard.
 */
export const detectConsoleLog: ASTRule = (context) => {
    const violations: ASTViolation[] = [];
    const traverse = getTraverseFn();
    if (!traverse) return violations;

    try {
        traverse(context.ast, {
            CallExpression(path: any) {
                const node = path.node;
                if (
                    node.callee.type === 'MemberExpression' &&
                    node.callee.object.type === 'Identifier' &&
                    node.callee.object.name === 'console' &&
                    node.callee.property.type === 'Identifier' &&
                    node.callee.property.name === 'log'
                ) {
                    violations.push({
                        file: context.filePath,
                        line: node.loc?.start.line || 0,
                        type: 'CONSOLE_LOG',
                        message: "Debug residue found: console.log",
                        severity: 'low',
                        start: node.start || 0,
                        end: node.end || 0
                    });
                }
            }
        });
    } catch {
        // Safe fallback on AST traversal failures
    }

    return violations;
};
