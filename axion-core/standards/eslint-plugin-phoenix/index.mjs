/**
 * Plugin Index: Entry point for the local-phoenix ESLint plugin.
 */

import * as markdownParser from "./markdown-parser.cjs";
import enforceSovereignAliases from "./rules/enforce-sovereign-aliases.mjs";
import markdownlint from "./rules/markdownlint.mjs";
import usePhoenixLogger from "./rules/phoenix-logger.mjs";
import requireArtifactAnchor from "./rules/require-artifact-anchor.mjs";

const plugin = {
    meta: {
        name: "phoenix-plugin",
    },
    parsers: {
        markdown: markdownParser,
    },
    rules: {
        "use-phoenix-logger": usePhoenixLogger,
        "require-artifact-anchor": requireArtifactAnchor,
        "enforce-sovereign-aliases": enforceSovereignAliases,
        markdownlint: markdownlint,
    },
};

export default plugin;
