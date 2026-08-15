import _babelTraverse from '@babel/traverse';
import { ASTRule, ASTViolation } from '../types';

const getTraverseFn = (): any => {
    if (typeof _babelTraverse === 'function') return _babelTraverse;
    if (typeof (_babelTraverse as any)?.default === 'function') return (_babelTraverse as any).default;
    if (typeof (_babelTraverse as any)?.traverse === 'function') return (_babelTraverse as any).traverse;
    return null;
};

/**
 * Rule: Detect Lint Entropy (OMEGA v15.2).
 */
export const detectLintEntropy: ASTRule = (context) => {
    const violations: ASTViolation[] = [];
    const traverse = getTraverseFn();
    if (!traverse) return violations;

    try {
        traverse(context.ast, {
            TemplateLiteral(path: any) {
                path.node.expressions.forEach((expr: any) => {
                    const isAlreadyWrapped =
                        expr.type === 'CallExpression' &&
                        expr.callee.type === 'Identifier' &&
                        expr.callee.name === 'String';

                    if (
                        !isAlreadyWrapped &&
                        (expr.type === 'Identifier' || expr.type === 'MemberExpression' || expr.type === 'CallExpression')
                    ) {
                        violations.push({
                            file: context.filePath,
                            line: expr.loc?.start.line || 0,
                            type: 'LINT_ENTROPY',
                            message: "Lint Entropy: Template literal interpolation may be 'any'. Wrap in String()?",
                            severity: 'low',
                            start: expr.start || 0,
                            end: expr.end || 0,
                        });
                    }
                });
            },
        });
    } catch {
        // Safe fallback on AST traversal failures
    }

    return violations;
};
