# 🔐 InsForge Authentication SDK Integration

Patterns for user session and profile management.

## Sign Up

```javascript
const { data, error } = await insforge.auth.signUp({
  email: "user@example.com",
  password: "password123",
  name: "User Name",
});
```

## Sign In (Password)

```javascript
const { data, error } = await insforge.auth.signInWithPassword({
  email: "user@example.com",
  password: "password123",
});
```

## Sign In (OAuth)

```javascript
await insforge.auth.signInWithOAuth({
  provider: "google",
  redirectTo: window.location.origin + "/dashboard",
});
```

## Session Recovery

```javascript
const { data, error } = await insforge.auth.getCurrentSession();
if (data.session) {
  // User is logged in
}
```

---

`[OMNI-ANCHOR] ID: SYNG.SKILL.InsForgeAuth VER: v15.0 [OMEGA]`
