const markdownlint = require("markdownlint");
const axionRules = require("./axion-rules.cjs");

// Extract just the PF004 rule for testing
const rulePF004 = axionRules.find((rule) => rule.names.includes("PF004"));

describe("PF004: heading-hierarchy", () => {
    const lint = (markdown) => {
        return markdownlint.sync({
            strings: { document: markdown },
            customRules: [rulePF004],
        }).document;
    };

    it("should pass for valid heading hierarchy", () => {
        const markdown = ["# H1 Heading", "## H2 Heading", "### H3 Heading", "## Another H2"].join("\n");
        const results = lint(markdown);
        expect(results).toHaveLength(0);
    });

    it("should fail and provide autofix info if the first heading is not H1", () => {
        const markdown = ["## H2 Heading", "### H3 Heading"].join("\n");
        const results = lint(markdown);

        expect(results.length).toBeGreaterThan(0);
        expect(results[0].ruleNames).toContain("PF004");
        expect(results[0].errorDetail).toBe("The first heading in the file must be a level 1 (H1) heading.");
        expect(results[0].fixInfo).toBeDefined();
    });

    it("should fail and provide autofix info if heading levels skip", () => {
        const markdown = ["# H1 Heading", "### H3 Heading (Skipped H2)"].join("\n");
        const results = lint(markdown);

        expect(results.length).toBeGreaterThan(0);
        expect(results[0].ruleNames).toContain("PF004");
        expect(results[0].errorDetail).toBe("Heading level incremented by more than one. Went from H1 to H3.");
        expect(results[0].fixInfo).toBeDefined();
    });
});
