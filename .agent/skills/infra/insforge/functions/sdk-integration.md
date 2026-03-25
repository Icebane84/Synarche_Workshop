# ⚡ InsForge Functions SDK Integration

Patterns for invoking serverless edge functions.

## Basic Invocation (POST)

```javascript
const { data, error } = await insforge.functions.invoke("hello-world", {
  body: { name: "Antigravity" },
});
```

## GET Request

```javascript
const { data, error } = await insforge.functions.invoke("get-stats", {
  method: "GET",
});
```

## Custom Headers

```javascript
const { data, error } = await insforge.functions.invoke("secure-endpoint", {
  headers: { "X-Custom-Auth": "..." },
});
```

---

`[OMNI-ANCHOR] ID: SYNG.SKILL.InsForgeFunc VER: v15.0 [OMEGA]`
