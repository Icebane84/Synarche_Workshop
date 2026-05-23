/**
 * Plugin Index: Entry point for the local-phoenix ESLint plugin.
 */
import usePhoenixLogger from './rules/phoenix-logger.mjs';
import requireArtifactAnchor from './rules/require-artifact-anchor.mjs';
import enforceSovereignAliases from './rules/enforce-sovereign-aliases.mjs';
import markdownlint from './rules/markdownlint.mjs';

const plugin = {
    meta: {
        name: "phoenix-plugin",
    },
    rules: {
        'use-phoenix-logger': usePhoenixLogger,
        'require-artifact-anchor': requireArtifactAnchor,
        'enforce-sovereign-aliases': enforceSovereignAliases,
        'markdownlint': markdownlint,
    },
};

export default plugin;