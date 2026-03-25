# 📊 InsForge Database SDK Integration

Patterns for type-safe database operations.

## Queries

```javascript
const { data, error } = await insforge.database
  .from("posts")
  .select("id, title, comments(content)")
  .eq("status", "published")
  .order("created_at", { ascending: false });
```

## Insert

```javascript
const { data, error } = await insforge.database
  .from("posts")
  .insert([{ title: "New Post", content: "..." }])
  .select();
```

## Update

```javascript
const { data, error } = await insforge.database
  .from("posts")
  .update({ status: "archived" })
  .eq("id", postId);
```

## Filters

- `.eq('col', 'val')`
- `.neq('col', 'val')`
- `.gt('col', 10)`
- `.in('col', ['a', 'b'])`
- `.is('col', null)`

---

`[OMNI-ANCHOR] ID: SYNG.SKILL.InsForgeDB VER: v15.0 [OMEGA]`
