// <reference types="vitest/config" />
import { defineConfig } from "vite";
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

export default defineConfig({
  plugins: [react(), tailwindcss()],
  envDir: "..",
  envPrefix: ["VITE_", "NEXT_PUBLIC_", "SUPABASE_"],
  resolve: {
    alias: {
      "@": path.resolve(dirname, "./src"),
      "@supabase-shared": path.resolve(dirname, "../../packages/supabase/src"),
    },
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
});
