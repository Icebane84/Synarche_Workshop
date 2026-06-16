/**
 * @fileoverview Entry point for eslint-plugin-phoenix.
 * Exports Phoenix-Class custom rules for ESLint.
 */

const requireGenesisStamp = require("./rules/require-genesis-stamp.cjs");

module.exports = {
    rules: {
        "require-genesis-stamp": requireGenesisStamp,
    },
};
