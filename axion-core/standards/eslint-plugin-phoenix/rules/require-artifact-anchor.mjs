/**
 * Custom ESLint Rule: require-artifact-anchor
 * Enforces that every TypeScript file contains an 'artifact_anchor' block.
 */
export const meta = {
	type: 'problem',
	docs: {
		description: "Ensures every TypeScript file contains an 'artifact_anchor' metadata block.",
		category: 'Governance',
		recommended: true,
	},
	fixable: 'code',
	schema: [],
	messages: {
		missingAnchor: "Missing mandatory 'artifact_anchor:' metadata block in a documentation comment.",
	},
};
export function create(context) {
	return {
		Program(node) {
			const sourceCode = context.sourceCode || context.getSourceCode();
			const comments = sourceCode.getAllComments();

			const hasAnchor = comments.some(comment => comment.type === 'Block' && comment.value.includes('artifact_anchor:')
			);

			if (!hasAnchor) {
				context.report({
					node,
					messageId: 'missingAnchor',
					fix(fixer) {
						const template = "/**\n * artifact_anchor:\n * - id: \n * - type: \n */\n";
						return fixer.insertTextBeforeRange([0, 0], template);
					}
				});
			}
		}
	};
}

export default { meta, create };