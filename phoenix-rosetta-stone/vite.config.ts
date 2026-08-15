// <reference types="vitest/config" />
import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { storybookTest } from "@storybook/addon-vitest/vitest-plugin";
import { playwright } from "@vitest/browser-playwright";

const dirname =
  typeof __dirname === "undefined"
    ? path.dirname(fileURLToPath(import.meta.url))
    : __dirname;

// More info at: https://storybook.js.org/docs/next/writing-tests/integrations/vitest-addon
export default defineConfig(({ mode }) => {
  // Load ALL env vars (including NEXT_PUBLIC_* and VITE_*) from .env.local
  const env = loadEnv(mode, process.cwd(), "");

  return {
    plugins: [react(), tailwindcss()],

    server: {
      proxy: {
        "/api": {
          target: "http://localhost:8000",
          changeOrigin: true,
          secure: false,
        },
      },
    },

    resolve: {
      tsconfigPaths: true,
      alias: {
        "@synarche/supabase": path.resolve(dirname, "../packages/supabase/src/index.ts"),
        "@": path.resolve(dirname, "src"),
        "@components": path.resolve(dirname, "src/components"),
        "@core": path.resolve(dirname, "src/core"),
        "@store": path.resolve(dirname, "src/store"),
        "@state": path.resolve(dirname, "src/store"),
        "@services": path.resolve(dirname, "src/services"),
      },
    },

    // Inject env vars into the browser bundle.
    // Populates process.env so pre-compiled @synarche/supabase dist/client.js
    // can read NEXT_PUBLIC_* values at runtime.
    define: {
      "process.env": JSON.stringify({
        NEXT_PUBLIC_SUPABASE_URL: env.NEXT_PUBLIC_SUPABASE_URL || env.VITE_SUPABASE_URL || "",
        NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY:
          env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_DEFAULT_KEY ||
          env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
          env.VITE_SUPABASE_ANON_KEY ||
          "",
        SUPABASE_ANON_KEY:
          env.SUPABASE_ANON_KEY ||
          env.NEXT_PUBLIC_SUPABASE_ANON_KEY ||
          env.VITE_SUPABASE_ANON_KEY ||
          "",
      }),
      "process.platform": JSON.stringify("browser"),
      "process.version": JSON.stringify(""),
    },

    test: {
      projects: [
        {
          extends: true,
          plugins: [
            storybookTest({
              configDir: path.join(dirname, ".storybook"),
            }),
          ],
          test: {
            name: "storybook",
            browser: {
              enabled: true,
              headless: true,
              provider: playwright({}),
              instances: [{ browser: "chromium" }],
            },
          },
        },
      ],
    },
  };
});
