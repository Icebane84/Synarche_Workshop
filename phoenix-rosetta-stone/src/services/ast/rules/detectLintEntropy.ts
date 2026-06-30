import traverse from '@babel/traverse';
import { ASTRule, ASTViolation } from '../types';

/**
 * Rule: Detect Lint Entropy (OMEGA v15.2).
 * Specifically targets "Invalid type 'any' of template literal expression"
 * and other safe-to-fix patterns identified in the Entropy Report.
 */
export const detectLintEntropy: ASTRule = (context) => {
    const violations: ASTViolation[] = [];

    traverse(context.ast, {
        TemplateLiteral(path) {
            // Check for expressions within template literals that might need explicit casting
            path.node.expressions.forEach((expr) => {
                // If it's a simple identifier or member expression, we can suggest a String() wrap
                // In a real TS-aware environment, we'd check types, but here we target
                // patterns that are known to cause the 'any' template lint error.
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

    return violations;
};
