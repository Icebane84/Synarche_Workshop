/**
 * Custom ESLint Rule to enforce PhoenixLogger over standard console methods.
 * Provides an auto-fixer that maps methods and injects the necessary import.
 */

export const meta = {
	type: 'problem',
	docs: {
		description: 'Enforce PhoenixLogger instead of console methods and auto-inject import',
		category: 'Best Practices',
		recommended: true,
	},
	fixable: 'code', // This unlocks the IDE's quick-fix lightbulb and --fix capabilities
	schema: [], // No custom options required
	messages: {
		usePhoenix: 'Use PhoenixLogger.{{ mappedMethod }} instead of console.{{ method }}.',
	},
};

export function create(context) {
	const sourceCode = context.sourceCode || context.getSourceCode(); // Support ESLint v8 and v9
	let hasPhoenixImport = false;
	let quoteChar = "'";
	let lastImportNode = null;

	// Pre-scan the AST for existing imports and quote styles
	const ast = sourceCode.ast;
	ast.body.forEach((node) => {
		if (node.type === 'ImportDeclaration') {
			lastImportNode = node;

			// Detect if PhoenixLogger is already imported
			if (node.source.value === '@system/logging') {
				node.specifiers.forEach((spec) => {
					if (spec.imported?.name === 'PhoenixLogger')
						hasPhoenixImport = true;
				});
			}
			if (node.source.raw.startsWith('"')) {
				quoteChar = '"';
			}
		}
	});

	return {
		CallExpression(node) {
			if (
				node.callee.type === 'MemberExpression' &&
				node.callee.object.type === 'Identifier' &&
				node.callee.object.name === 'console' &&
				node.callee.property.type === 'Identifier'
			) {
				const method = node.callee.property.name;
				if (['log', 'info', 'warn', 'error', 'debug'].includes(method)) {
					let mappedMethod = 'info';
					if (method === 'error') mappedMethod = 'error';
					if (method === 'debug') mappedMethod = 'debug';

					context.report({
						node,
						messageId: 'usePhoenix',
						data: { method, mappedMethod },
						fix(fixer) {
							const fixes = [];
							// Replace 'console.log' with 'PhoenixLogger.info'
							fixes.push(fixer.replaceText(node.callee, `PhoenixLogger.${mappedMethod}`));

							// Inject the import statement if we haven't already
							if (!hasPhoenixImport) {
								const importCode = `import { PhoenixLogger } from ${quoteChar}@system/logging${quoteChar};\n`;
								if (lastImportNode) {
									// Add immediately after the last existing import
									fixes.push(fixer.insertTextAfter(lastImportNode, '\n' + importCode.trim()));
								} else {
									// No imports exist, add to the very top of the file
									fixes.push(fixer.insertTextBeforeRange([0, 0], importCode));
								}
								// Toggle flag so subsequent console auto-fixes in this pass don't duplicate the import
								hasPhoenixImport = true;
							}
							return fixes;
						},
					});
				}
			}
		},
	};
}

export default { meta, create };