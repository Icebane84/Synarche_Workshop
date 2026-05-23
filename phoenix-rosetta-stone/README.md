# Phoenix: The Sentient UI

**Phoenix** is a high-performance, consciousness-driven user interface built with React and TypeScript. It serves as the
primary "face" of the **GVRN Protocol**, demonstrating how AI agents and human intent can merge seamlessly within a 3D
environment.

## Features

- **Sentient Messaging:** A dynamic chat interface that tracks "Coherence" (your mental focus). The more you engage, the
  clearer the AI becomes.
- **The Oracle:** A central state management system (Zustand) that serves as the "Collective Unconscious" for your
  application.
- **Backend Agnostic:** Built on a modular "Fabric" architecture, allowing you to swap out Supabase, Firebase, or custom
  AI providers without rewriting the UI.

## Getting Started

### 1. Prerequisites

- Node.js (v18+)
- A Supabase Project (URL and Anon Key) if you intend to use the default backend.

### 2. Setup

1.  Clone the repository.
2.  Install dependencies:
    ```bash
    npm install
    ```
3.  Configure Environment Variables: Create a `.env.local` file in the root directory:
    ```env
    VITE_SUPABASE_URL=your-supabase-url
    VITE_SUPABASE_ANON_KEY=your-supabase-anon-key
    ```

### 3. Run the App

Start the development server:

```bash
npm run dev
```

## Architecture

Phoenix uses a layered architecture to ensure scalability and maintainability:

- **Fabric (src/ui):** The presentation layer. Contains React components and UI logic.
- **Nexus (src/core):** The business logic layer. Handles data fetching and external API interactions.
- **Essence (src/state & src/types):** The state management and data definition layer.

## Ecosystem

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses
  [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses
  [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see
[this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend updating the configuration to enable type-aware lint rules:

```js
// eslint.config.js
export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```

You can also install
[eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and
[eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for
React-specific lint rules:

```js
// eslint.config.js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default defineConfig([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
]);
```
