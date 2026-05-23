
exports.parseForESLint = function (code) {


    return {
        ast: {
            type: "Program",
            start: 0,
            end: code.length,
            loc: { start: { line: 1, column: 0 }, end: { line: 1, column: 0 } },
            range: [0, code.length],
            body: [],
            tokens: [],
            comments: [],
        },
        services: {},
        scopeManager: null,
        visitorKeys: {
            Program: [],
        },
    };
};
