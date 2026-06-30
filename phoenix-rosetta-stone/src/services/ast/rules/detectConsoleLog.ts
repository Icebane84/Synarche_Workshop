import { ASTRule, ASTViolation } from '../types';
import traverse from '@babel/traverse';

/**
 * Rule: Detect console.log statements.
 * Part of the "Zero Entropy" standard.
 */
export const detectConsoleLog: ASTRule = (context) => {
    const violations: ASTViolation[] = [];
    
    traverse(context.ast, {
        CallExpression(path) {
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

    return violations;
};
