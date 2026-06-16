exports.parseForESLint = (code) => {
    const lines = code.split(/\r?\n/);
    const lineCount = lines.length;
    const lastLineLength = lines[lineCount - 1] ? lines[lineCount - 1].length : 0;

    return {
        ast: {
            type: "Program",
            start: 0,
            end: code.length,
            loc: { start: { line: 1, column: 0 }, end: { line: lineCount, column: lastLineLength } },
            range: [0, code.length],
            body: [
                {
                    type: "MarkdownDocument",
                    value: code,
                    start: 0,
                    end: code.length,
                    loc: { start: { line: 1, column: 0 }, end: { line: lineCount, column: lastLineLength } },
                    range: [0, code.length],
                },
            ],
            tokens: [],
            comments: [],
        },
        services: {},
        scopeManager: null,
        visitorKeys: {
            program: ["body"],
            markdownDocument: [],
        },
    };
};
