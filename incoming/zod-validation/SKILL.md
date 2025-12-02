---
name: zod-validation
description: "Enforces Zod schema validation at all external data boundaries. Use when: (1) consuming any API response, (2) processing user form input, (3) loading environment variables, (4) reading from localStorage or URL params. Mandated by style_guide.md and GEMINI.md."
---

# Zod Validation Skill

Apply Zod schemas at every trust boundary. Data is `unknown` until proven otherwise. This skill prevents the `any` escape hatch and guarantees runtime type safety.

## Quick Reference

| Boundary       | Use            | Throws? |
| -------------- | -------------- | ------- |
| API `fetch()`  | `.parse()`     | Yes     |
| Form input     | `.safeParse()` | No      |
| Env vars       | `.parse()`     | Yes     |
| `localStorage` | `.safeParse()` | No      |
| URL params     | `.safeParse()` | No      |

## Naming Rules

- Schema: `PascalCase` + `Schema` suffix → `UserSchema`, `ProjectSchema`.
- Derived type: `z.infer<typeof Schema>` — **never** duplicate the interface manually.
- Import from `'zod'` directly — no barrel-file re-exports.

## Patterns

### API Response (Throwing)

Use when a failure is a fatal error (e.g., a critical data load):

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
  role: z.enum(["admin", "user", "guest"]),
});

/** Derived type — never write this manually */
type User = z.infer<typeof UserSchema>;

/**
 * Fetches a user and validates the response shape.
 * Throws ZodError if the API returns an unexpected shape.
 */
const fetchUser = async (id: string): Promise<User> => {
  const res = await fetch(`/api/users/${id}`);
  const data: unknown = await res.json();
  return UserSchema.parse(data);
};
```

### Form / User Input (Non-Throwing)

Use when a graceful error message is appropriate:

```typescript
const result = UserSchema.safeParse(formData);

if (!result.success) {
  const errors = result.error.format();
  // e.g. errors.email._errors === ['Invalid email']
  return { errors };
}

const user = result.data; // fully typed, safe to use
```

### Environment Variables

Validate once at startup — fail fast if config is wrong:

```typescript
const EnvSchema = z.object({
  VITE_API_URL: z.string().url(),
  VITE_APP_ENV: z.enum(["development", "staging", "production"]),
  VITE_TIMEOUT_MS: z.coerce.number().int().positive().default(5000),
});

/** Throws at module load if env is misconfigured */
export const env = EnvSchema.parse(import.meta.env);
```

### Nested & Optional Fields

```typescript
const ProjectSchema = z.object({
  id: z.string().uuid(),
  name: z.string(),
  owner: UserSchema, // nested schema
  tags: z.array(z.string()).default([]), // array with default
  metadata: z.record(z.string()).optional(), // optional map
  createdAt: z.string().datetime(),
});
```

## Constraints (Non-Negotiable)

1. **No `any`** — Raw `JSON.parse()` or untyped `fetch()` returns are a violation.
2. **Validate at the boundary** — Never validate inside a component render or event handler. Do it in the service/fetch layer.
3. **Schema is the source of truth** — Delete any manually written `interface` that duplicates a Zod schema shape.
4. **Handle ZodError explicitly** — Never swallow it silently. Log with `error.format()` or re-throw.
