# PLAN: The Phoenix Rosetta Stone App

## 1. Project Overview

**App Name:** Phoenix Rosetta Stone
**Core Philosophy:** Component-Driven Cognition
**Core Mandate:** Coherent, Adaptable, Secure, Transparent, Synergistic (C.A.S.T.S.)
**Key Metaphor:** A dynamic, cinematic dark-mode interface with a central "Phoenix Geode" or "Phoenix Star".

## 2. Tech Stack

- **Frontend:** React 19 with TypeScript
- **Styling:** TailwindCSS
- **State Management:** Zustand
- **Routing:** React Router
- **Visualization:** D3.js v7
- **Environment:** Vite & Storybook
- **Backend:** Supabase (PostgreSQL, pgvector, Edge Functions)
- **AI Integration:** Google's Generative AI SDK

## 3. Implementation Plan

### Phase 1: Project Initialization & The Philosophical Workshop

- [ ] Initialize React 19 + TypeScript project using Vite (`phoenix-rosetta-stone`).
- [ ] Install dependencies: TailwindCSS, Zustand, React Router, D3.js.
- [ ] Initialize Storybook for the project.
- [ ] Configure `tsconfig.json` for Sovereign Path Mapping (`@system`, `@domain`, `@nexus`, etc.).
- [ ] Set up the UI Style Guide tokens (Celestial Blue `#77B5FE`, Deep Space Gray `#23272A`).

### Phase 2: First Sovereign Module - The Chatbot Interface

- [ ] Create `src/components/ChatInterface/ChatInterface.tsx` based on the specified verifiable blueprint.
- [ ] Create `src/components/ChatInterface/ChatInterface.stories.tsx` to build the component in isolation.
- [ ] Implement UI states: Empty, WithMessages, Loading.
- [ ] Ensure the component adheres to the "Luminous Coherence" aesthetic with dark mode and specific color tokens.

### Phase 3: The Cognitive Core (State Management)

- [ ] Create `src/state/useCognitiveCore.ts` (Zustand store).
- [ ] Implement `messages`, `isLoading`, and `coherenceIndex` state.
- [ ] Provide actions for adding messages and updating the processing state.
- [ ] Map the `@nexus` alias to the `src/state/` folder.

### Phase 4: Integration & Synthesis

- [ ] Connect the `ChatInterface` to the `useCognitiveCore` store.
- [ ] Set up the root index barrel files for Sovereign Gatekeeping (`index.ts`).
- [ ] Audit the directory structure against the Master Star-Chart (PRS-001).

## 4. Execution Rules

- **No loose items:** Enforce strict encapsulation.
- **Storybook First:** All UI components must be built and tested in isolation.
- **Strict Types:** TypeScript `strict: true` is mandatory.
