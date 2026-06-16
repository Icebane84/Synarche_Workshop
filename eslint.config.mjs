/**
 * Synarche Sovereign Workspace ESLint Configuration Bridge
 * Re-exports the canonical governance config from axion-core/standards/.
 * This file exists at the workspace root so ESLint flat config
 * discovery finds it automatically for any sub-project.
 */
export { default } from "./axion-core/standards/eslint.config.mjs";
