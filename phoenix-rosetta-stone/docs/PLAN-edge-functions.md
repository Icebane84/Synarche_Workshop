# Project Plan: Sovereign Edge Functions (Cognitive Processor)

---

## 1. Overview

---

This plan outlines the creation and deployment of the Supabase Edge Function (`phoenix-cognitive-processor`) that serves
as the AI backend for the Phoenix Rosetta Stone App. The function will receive user prompts from the frontend, process
them (via an LLM/RAG pipeline), and return the synthesized response alongside a calculated `coherenceIndex`.

## 2. Agent Assignments

---

- **Project Planner**: Define the implementation steps (This Document).
- **Backend / Infra Agent**: Setup the Supabase Edge Function environment, integrate Deno dependencies, and write the
  cognitive loop logic.
- **Validation Agent**: TEST the Edge Function locally using Supabase CLI before production deployment.

## 3. Task Breakdown

---

### Phase 1: Environment & Scaffolding

---

- [ ] Initialize Supabase local environment (`supabase init`) if not already present.
- [ ] Scaffold the new edge function: `supabase functions new phoenix-cognitive-processor`.
- [ ] Set up the `deno.json` import map for necessary Deno dependencies (e.g., standard library, Supabase client, LLM
      SDK).

### Phase 2: CORE Processing Logic

---

- [ ] Implement CORS handling for the Edge Function so the Vite frontend can communicate with it.
- [ ] Parse the incoming JSON payload (extracting `messages` history and the new `prompt`).
- [ ] **Cognitive Synthesis**: Integrate the chosen LLM provider to generate a response based on the prompt and history.
- [ ] **Coherence Calculation**: Analyze the conversation/prompt to determine the new `coherenceIndex` (e.g., semantic
      analysis or a simple heuristic logic for the prototype).
- [ ] Return the structured response: `{ text: string, sender: 'ai', coherenceIndex: number }`.

### Phase 3: Integration & Testing

---

- [ ] Serve the function locally using `supabase functions serve`.
- [ ] Wire the local Vite frontend `.env.local` to point to the local Supabase edge function URL.
- [ ] Verify the end-to-end flow: User types in the `ChatInterface` -> Frontend hits Edge Function -> Edge Function
      responds -> `PhoenixGeode` visually reacts to the new coherence.

### Phase 4: Production Deployment

---

- [ ] Set production environment variables in the Supabase Dashboard (API keys for the LLM).
- [ ] Deploy the function using `supabase functions deploy phoenix-cognitive-processor`.

---

## 4. Verification Checklist

---

- [ ] The Edge Function accepts POST requests and handles CORS properly.
- [ ] The LLM integration successfully returns a contextual response.
- [ ] The returned `coherenceIndex` correctly updates the frontend Zustand store and triggers the D3.js Geode
      transformation.
- [ ] Zero TypeScript errors in the Deno environment.
