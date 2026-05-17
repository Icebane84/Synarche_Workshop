/**
 * Plugin Index: Entry point for the local-phoenix ESLint plugin.
 */
import usePhoenixLogger from './rules/phoenix-logger.mjs';
import requireArtifactAnchor from './rules/require-artifact-anchor.mjs';
import enforceSovereignAliases from './rules/enforce-sovereign-aliases.mjs';
import markdownLintRule from './rules/markdownlint.mjs';

const plugin = {
    // Metadata for the plugin (useful for flat config identification)
    meta: {
        name: "localPhoenixPlugin",
    },
    rules: {
        'use-phoenix-logger': usePhoenixLogger,
        'require-artifact-anchor': requireArtifactAnchor,
        'enforce-sovereign-aliases': enforceSovereignAliases,
        'markdownlint': markdownLintRule,
    },
};

export default plugin;