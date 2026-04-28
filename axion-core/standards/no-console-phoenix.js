/**
 * GUCA-AXN-003: PhoenixLogger AST Auto-Fixer
 * Custom ESLint rule to enforce T201 compliance and automatically fix 
 * console methods to PhoenixLogger with proper AST transformations.
 */
module.exports = {
    meta: {
        type: 'problem',
        docs: {
            description: 'Enforce PhoenixLogger over console methods to maintain Radical Coherence.',
            category: 'Best Practices',
            recommended: true,
        },
        fixable: 'code',
        messages: {
            usePhoenixLogger: '[Sovereignty Violation] (T201): Use PhoenixLogger.{{method}} instead of console.{{consoleMethod}}.'
        }
    },
    create: function(context) {
        return {
            CallExpression(node) {
                if (
                    node.callee.type === 'MemberExpression' &&
                    node.callee.object.type === 'Identifier' &&
                    node.callee.object.name === 'console' &&
                    node.callee.property.type === 'Identifier'
                ) {
                    const consoleMethod = node.callee.property.name;
                    const validMethods = ['log', 'info', 'warn', 'error', 'debug'];

                    if (validMethods.includes(consoleMethod)) {
                        // Map to PhoenixLogger streams (e.g. log/warn -> info)
                        let method = consoleMethod;
                        if (method === 'log' || method === 'warn') method = 'info';

                        context.report({
                            node,
                            messageId: 'usePhoenixLogger',
                            data: { method, consoleMethod },
                            fix: function(fixer) {
                                const sourceCode = context.sourceCode || context.getSourceCode();
                                const ast = sourceCode.ast;
                                const fixes = [
                                    fixer.replaceText(node.callee, `PhoenixLogger.${method}`)
                                ];

                                // Safely check if the import already exists using AST
                                const hasImport = ast.body.some(n => 
                                    n.type === 'ImportDeclaration' &&
                                    n.source.value === '@system/logging' &&
                                    n.specifiers.some(spec => spec.local && spec.local.name === 'PhoenixLogger')
                                );

                                if (!hasImport && ast.body.length > 0) {
                                    const importStatement = "import { PhoenixLogger } from '@system/logging';\n";
                                    fixes.push(fixer.insertTextBefore(ast.body[0], importStatement));
                                }

                                return fixes;
                            }
                        });
                    }
                }
            }
        };
    }
};
