# Dual Artifact: Zod Validation

---

## 👤 Human Perspective: The "Boundary Guard"

**Objective**
Never let untrusted data enter the application without a shape check. Every API response, form submission, and environment variable gets validated at the point it crosses a trust boundary.

**Impact**

- Runtime crashes from unexpected API shapes become compile-time catches.
- Eliminates the `any` escape hatch — data either fits the schema or throws a typed error.
- Enforces the `style_guide.md` mandate without requiring manual code review.

**Analogy**
Like a customs checkpoint — everything entering the country gets inspected against a known manifest. What passes is safe to use. What doesn't is rejected with a clear reason.

---

## 🤖 AI Perspective: The "Schema Enforcement Protocol"

**Technical Goal**
Apply Zod schemas at all external data boundaries: API responses, user input forms, and environment config. No raw `JSON.parse()` or untyped `fetch()` responses in TypeScript files.

**Pattern: API Response Validation**

```typescript
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1),
  email: z.string().email(),
});

type User = z.infer<typeof UserSchema>;

const fetchUser = async (id: string): Promise<User> => {
  const res = await fetch(`/api/users/${id}`);
  const data: unknown = await res.json();
  return UserSchema.parse(data); // throws ZodError if invalid
};
```

**Pattern: Safe Parse (Non-Throwing)**

```typescript
const result = UserSchema.safeParse(data);
if (!result.success) {
  console.error("[Validation Error]", result.error.format());
  return null;
}
const user = result.data; // fully typed
```

**Pattern: Environment Variables**

```typescript
const EnvSchema = z.object({
  VITE_API_URL: z.string().url(),
  VITE_APP_ENV: z.enum(["development", "staging", "production"]),
});

export const env = EnvSchema.parse(import.meta.env);
```

**Boundary Checklist**
| Boundary | Method | Throws? |
| ----------------- | --------------- | ------- |
| API fetch() | `.parse()` | Yes |
| Form submission | `.safeParse()` | No |
| env vars | `.parse()` | Yes |
| localStorage | `.safeParse()` | No |

**Constraints**

- Import from `'zod'` only — no re-exports from barrel files.
- Schema names: `PascalCase` + `Schema` suffix (e.g., `UserSchema`).
- Always derive types via `z.infer<typeof Schema>` — never duplicate type definitions.
- Never use `.parse()` inside a render function — validate at the data-fetching layer.
