import typescriptEslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export default [
    {
        ignores: ["out/**", "dist/**", "node_modules/**", "**/*.d.ts"]
    },
    {
        files: ["src/**/*.ts", "tools/**/*.js", "tools/**/*.cjs"],
        languageOptions: {
            parser: tsParser,
            parserOptions: {
                ecmaVersion: "latest",
                sourceType: "module",
                project: "./tsconfig.json",
                tsconfigRootDir: __dirname,
            },
        },
        plugins: {
            "@typescript-eslint": typescriptEslint,
        },
        rules: {
            // Core ESLint
            "no-var": "error",
            "prefer-const": "error",
            "camelcase": ["warn", { "properties": "never" }],
            "eqeqeq": "error",
            
            // TypeScript (Agent Style Guide)
            "@typescript-eslint/no-explicit-any": "warn",
            "@typescript-eslint/explicit-function-return-type": ["warn", { 
                "allowExpressions": true 
            }],
            "@typescript-eslint/no-floating-promises": "error",
            "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],
            
            // Async/Await Safety
            "no-return-await": "off",
            "@typescript-eslint/return-await": "error",
        }
    }
];
