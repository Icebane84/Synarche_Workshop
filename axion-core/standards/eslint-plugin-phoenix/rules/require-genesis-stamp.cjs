/**
 * @fileoverview Enforces that all Markdown documents contain a Genesis Stamp.
 * Targeting the custom MarkdownDocument AST node.
 */

module.exports = {
    meta: {
        type: "problem",
        fixable: "code", // <-- REQUIRED: Tells ESLint this rule can automatically fix the code
        docs: {
            description: "Require a 'Genesis Stamp' in Phoenix-Class Markdown documents.",
            category: "Phoenix Governance",
            recommended: true,
        },
        messages: {
            missingStamp: "[AOP-PGPS-001 Violation] Document is missing the required 'Genesis Stamp:' metadata.",
            outdatedStamp:
                "[AOP-PGPS-001 Violation] Document 'Genesis Stamp:' date is outdated. Expected today's date.",
        },
        schema: [],
    },

    create(context) {
        return {
            MarkdownDocument(node) {
                const text = node.value;
                if (!text.includes("Genesis Stamp:")) {
                    context.report({
                        node,
                        messageId: "missingStamp",
                        fix(fixer) {
                            // Dynamically generate today's date for the stamp
                            const today = new Date().toISOString().split("T")[0];
                            const defaultStamp = `\n\n## Genesis Stamp: ${today} | Domain: TBD | State: DRAFT | Criticality: Standard\n\n`;

                            // Locate the first H1 heading (e.g. "# Title")
                            const h1Match = text.match(/^#[ \t]+[^\r\n]+/m);

                            if (h1Match) {
                                const insertPos = h1Match.index + h1Match[0].length;
                                return fixer.insertTextAfterRange([insertPos, insertPos], defaultStamp);
                            }
                            return fixer.insertTextBeforeRange([0, 0], defaultStamp); // Fallback
                        },
                    });
                }
            },
        };
    },
};
