/**
 * Custom ESLint Rule: enforce-sovereign-aliases
 * Prevents relative paths and auto-fixes them into tsconfig.json aliases. This rule is designed to be run in an environment where the tsconfig.json is available at a known relative path relative to the workspace root. It dynamically loads the tsconfig.json to determine the available aliases.
 */
import { dirname, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync } from 'node:fs';

// Dynamically load tsconfig.json aliases
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const tsconfigPath = resolve(__dirname, '../../../tsconfig.json');
const tsconfigRaw = readFileSync(tsconfigPath, 'utf8');
const tsconfigClean = tsconfigRaw.replaceAll(/\/\/.*$/gm, '').replaceAll(/\/\*[\s\S]*?\*\//g, '');
const tsconfigData = JSON.parse(tsconfigClean);
const tsPaths = tsconfigData.compilerOptions?.paths || {};

// Pre-calculate the physical target paths and sort by length for deepest-first matching
const ALIAS_MAP = Object.entries(tsPaths).map(([aliasKey, pathArr]) => {
    const alias = aliasKey.replace(/\/\*$/, '');
    const target = pathArr[0].replace(/^\.\//, '').replace(/\/\*$/, '');
    const hasWildcard = aliasKey.endsWith('/*');

    // Escape regex characters and create a pattern that captures the wildcard part if present
    const escapedTarget = target.replaceAll(/[.*+?^${}()|[\]\\]/g, String.raw`\$&`);
    const pattern = new RegExp(`^${escapedTarget}${hasWildcard ? '/(.*)$' : '$'}`);

    return { alias, pattern, hasWildcard, targetLength: target.length };
}).sort((a, b) => b.targetLength - a.targetLength);

export const meta = {
	type: 'problem',
	docs: {
		description: 'Enforce Sovereign path aliases from tsconfig.json over relative imports.',
		category: 'Governance',
		recommended: true,
	},
	fixable: 'code',
	schema: [],
	messages: {
		useAlias: "Use the Sovereign alias '{{ aliasPath }}' instead of the relative path '{{ importPath }}'."
	}
};
export function create(context) { // The context object is provided by ESLint and contains useful utilities
	return {
		ImportDeclaration(node) {
			const importPath = node.source.value;

			// Only evaluate relative paths
			if (!importPath.startsWith('.')) return;

			// Get absolute physical path of the file currently being linted
			const currentFilePath = context.getFilename ? context.getFilename() : context.filename;
			if (!currentFilePath || currentFilePath === '<input>') return;

			// Get absolute physical path of the target file being imported
			const absoluteImportPath = resolve(dirname(currentFilePath), importPath);
			const normalizedImportPath = absoluteImportPath.replaceAll(sep, '/');

			// Root where ESLint is being executed
			const workspaceRoot = (context.getCwd ? context.getCwd() : process.cwd()).replaceAll('\\', '/');

			// Target path relative to workspace root (assuming baseUrl: ".")
			const relativeToRoot = normalizedImportPath.substring(workspaceRoot.length).replace(/^\//, '');

			// Check if the imported file falls under any of our Sovereign aliases
			for (const { alias, pattern, hasWildcard } of ALIAS_MAP) {
				const match = relativeToRoot.match(pattern);

				if (match) {
					const finalAliasPath = hasWildcard ? `${alias}/${match[1]}` : alias;

					context.report({
						node: node.source,
						messageId: 'useAlias',
						data: { aliasPath: finalAliasPath, importPath: importPath },
						fix: (fixer) => fixer.replaceText(node.source, `"${finalAliasPath}"`)
					});
					break;
				}
			}
		}
	};
}

export default { meta, create };