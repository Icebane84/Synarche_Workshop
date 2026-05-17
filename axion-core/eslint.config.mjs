/**
 * Axion Core ESLint Configuration Bridge
 * Re-exports the canonical governance config from standards/.
 * This file exists at the project root so ESLint 8.x flat config
 * discovery finds it automatically (no --config flag needed).
 */
export { default } from "./standards/eslint.config.mjs";
