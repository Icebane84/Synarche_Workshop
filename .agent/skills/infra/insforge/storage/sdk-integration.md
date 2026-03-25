# 📁 InsForge Storage SDK Integration

Patterns for file upload and management.

## Bucket Access

```javascript
const images = insforge.storage.from("images");
```

## Upload (Manual Key)

```javascript
const { data, error } = await images.upload("folder/file.png", fileObject);
```

## Upload (Auto Key)

```javascript
const { data, error } = await images.uploadAuto(fileObject);
```

## Download

```javascript
const { data: blob, error } = await images.download("folder/file.png");
```

## Delete

```javascript
const { data, error } = await images.remove("folder/file.png");
```

---

`[OMNI-ANCHOR] ID: SYNG.SKILL.InsForgeStorage VER: v15.0 [OMEGA]`
