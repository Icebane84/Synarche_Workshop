import { createRequire } from 'module';
const require = createRequire(import.meta.url);
const markdownlint = require('markdownlint/sync').lint;
const axionRules = require('../markdownlint-rules/axion-rules.cjs');
const phoenixRules = require('../markdownlint-rules/phoenix-rules.cjs');

export default {
    meta: {
        type: 'problem',
        docs: {
            description: 'Run Phoenix markdownlint rules natively inside ESLint',
            recommended: true,
        },
        schema: [],
    },
    create(context) {
        return {
            Program(node) {
                // Ensure we only process markdown files
                const fileName = context.filename || context.getFilename();
                if (!fileName.endsWith('.md')) {
                    return;
                }

                // Retrieve the raw markdown text
                const sourceCode = context.sourceCode ? context.sourceCode.text : context.getSourceCode().text;

                // Replicate the legacy .markdownlint.cjs config
                const options = {
                    strings: {
                        [fileName]: sourceCode
                    },
                    config: {
                        default: true,
                        MD001: { level: 1 },
                        MD003: { style: "atx" },
                        MD004: { style: "dash" },
                        MD005: true,
                        MD007: { indent: 4 },
                        MD009: { br_spaces: 0 },
                        MD010: { code_blocks: false, tabs: false },
                        MD013: { line_length: 120, code_blocks: false, tables: false },
                        MD022: true,
                        MD024: { allow_different_nesting: true },
                        MD025: { level: 1, front_matter_title: "" },
                        MD026: { punctuation: ".,;:!?" },
                        MD029: { style: "ordered" },
                        MD030: false,
                        MD032: true,
                        MD041: true,
                        MD047: true,
                        MD033: {
                            allowed_elements: ["br", "details", "summary", "sub", "sup", "u", "integer"],
                        },
                        MD034: true,
                        MD036: false,
                        MD040: true,
                        MD046: { style: "fenced" },
                        MD048: { style: "backtick" },
                        MD051: true,
                        MD052: true,
                        MD053: true
                    },
                    customRules: [...axionRules, ...phoenixRules],
                    markdownItFactory: require('markdown-it')
                };

                let results;
                try {
                    results = markdownlint(options);
                } catch (error) {
                    context.report({
                        loc: { line: 1, column: 1 },
                        message: `Markdownlint execution failed: ${error.message}`
                    });
                    return;
                }

                const fileResults = results[fileName] || [];

                for (const result of fileResults) {
                    const ruleNames = result.ruleNames.join('/');
                    const description = result.ruleDescription;
                    const detail = result.errorDetail ? `: ${result.errorDetail}` : '';
                    
                    const loc = {
                        line: result.lineNumber || 1,
                        column: result.errorRange ? result.errorRange[0] : 1
                    };

                    context.report({
                        loc: loc,
                        message: `[${ruleNames}] ${description}${detail}`
                    });
                }
            }
        };
    }
};
