import typescriptEslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import globals from "globals";
import { createRequire } from "node:module";
import { dirname } from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
import phoenixPlugin from "./eslint-plugin-phoenix/index.mjs";
const require = createRequire(import.meta.url);
const markdownParser = require("./eslint-plugin-phoenix/markdown-parser.cjs");

export default [
    {
        ignores: [
            "**/out/**",
            "**/dist/**",
            "**/node_modules/**",
            "**/.venv/**",
            "**/venv/**",
            "**/_governance/**",
            "**/.archives/**",
            "**/.git/**",
            "**/.mypy_cache/**",
            "**/.ruff_cache/**",
            "**/scratch/**",
            "**/incoming/**",
            "**/*.d.ts"
        ]
    },
    {
        files: ["src/**/*.ts", "tools/**/*.js", "tools/**/*.cjs"],
        languageOptions: {
            parser: tsParser,
            parserOptions: {
                ecmaVersion: "latest",
                sourceType: "module",
                project: "../tsconfig.json",
                tsconfigRootDir: __dirname,
            },
        },
        plugins: {
            "@typescript-eslint": typescriptEslint,
            "phoenix": phoenixPlugin
        },
        rules: {
            // Core ESLint
            "no-var": "error",
            "prefer-const": "error",
            "camelcase": ["warn", { "properties": "never" }],
            "eqeqeq": "error",

            // TypeScript (Agent Style Guide)
            "@typescript-eslint/no-explicit-any": "error",
            "@typescript-eslint/explicit-function-return-type": ["warn", {
                "allowExpressions": true
            }],

            "@typescript-eslint/no-floating-promises": "error",
            "@typescript-eslint/no-unused-vars": ["warn", { "argsIgnorePattern": "^_" }],

            // Async/Await Safety
            "no-return-await": "off",
            "@typescript-eslint/return-await": "error",

            // Governance Enforcement (Phoenix Protocol)
            "phoenix/use-phoenix-logger": "error",
            "phoenix/require-artifact-anchor": "error",
            "phoenix/enforce-sovereign-aliases": "error"
        }
    },
    {
        files: ["**/*.tsx", "**/react-app/**/*.ts"],
        languageOptions: {
            parser: tsParser,
            globals: globals.browser,
            parserOptions: {
                ecmaVersion: "latest",
                sourceType: "module",
            },
        },
        plugins: {
            "react-hooks": reactHooks,
            "react-refresh": reactRefresh,
            "phoenix": phoenixPlugin
        },
        rules: {
            ...reactHooks.configs.recommended.rules,
            'react-refresh/only-export-components': [
                'warn',
                { allowConstantExport: true },
            ],
            "phoenix/require-artifact-anchor": "error"
        }
    },
    {
        files: ["**/*.md"],
        languageOptions: {
            parser: markdownParser
        },
        plugins: {
            phoenix: phoenixPlugin
        },
        rules: {
            "phoenix/markdownlint": "error"
        }
    }
];
