/**
 * @fileoverview Enforces that all Markdown documents contain a Genesis Stamp.
 * Targeting the custom MarkdownDocument AST node.
 */
module.exports = {
    meta: {
        type: "problem",
        docs: {
            description: "Require a 'Genesis Stamp' in Phoenix-Class Markdown documents.",
            category: "Phoenix Governance",
            recommended: true,
        },
        messages: {
            missingStamp: "[AOP-PGPS-001 Violation] Document is missing the required 'Genesis Stamp:' metadata.",
        },
        schema: [], // no options
    },

    create(context) {
        return {
            // Target the custom node we injected via markdown-parser.cjs
            MarkdownDocument(node) {
                const text = node.value;
                if (!text.includes("Genesis Stamp:")) {
                    context.report({
                        node,
                        messageId: "missingStamp",
                    });
                }
            },
        };
    },
};
