# CLAUDE.md
> **Domain**: GVRN
> **Evolution**: Omega Ascension
> **Signal**: OMEGA

## **Genesis Stamp: 2026-02-04** **Domain: GVRN** **State: [ACTIVE]** **Tags:** `OGLN_v13, GVRN, Reforged` **Criticality: Operational**

---

###### **[ARTIFACT START]**

### **Block A: The Identification Lock (UIP-V13)**

| Key | Value | Description |
| :--- | :--- | :--- |
| **Artifact ID** | `GVRN-CLAUDE-001` | The Sovereign ID. |
| **Official Name** | `CLAUDE.md` | The Filename. |
| **Version** | **v13.1 [OMEGA]** | The Standard. |
| **Domain** | `GVRN` | The Subject. |
| **Celestial Class** | `[PLANET]` | The Weight. |
| **Evolution** | `Omega Ascension` | The Maturity. |
| **Status** | `[ACTIVE]` | The Lifecycle. |
| **Relations** | `GOVERNED_BY: CORE-CODEX-001` | The Network. |

# Providers

AI model provider implementations organized by capability type.

## Submodules

- **[llm/](llm/CLAUDE.md)**: Language model providers (chat completion, text generation)
- **[embedding/](embedding/CLAUDE.md)**: Embedding providers (text-to-vector conversion)
- **[reranker/](reranker/CLAUDE.md)**: Reranker providers (relevance-based document ranking)
- **[stt/](stt/CLAUDE.md)**: Speech-to-text providers (audio transcription)
- **[tts/](tts/CLAUDE.md)**: Text-to-speech providers (audio generation)

## Architecture

All provider types follow a consistent pattern:

1. **Base class** in each subdirectory defines the interface
2. **Provider implementations** inherit from base and implement required methods
3. **Registration** happens in `factory.py` for discovery
4. **Consistent error handling** and configuration management

## Common Patterns Across All Provider Types

### Inheritance Hierarchy

```
TimeoutMixin, SSLMixin
    └── BaseModel (e.g., LanguageModel, EmbeddingModel)
        └── ProviderImplementation (e.g., OpenAILanguageModel)
```

All provider base classes inherit from:

- `TimeoutMixin`: Provides configurable HTTP timeouts
- `SSLMixin`: Provides configurable SSL verification

### Configuration Pattern

Every provider follows this `__post_init__()` pattern:

```python
def __post_init__(self):
    super().__post_init__()  # Initialize _config and extract params
    self.api_key = self.api_key or os.getenv("PROVIDER_API_KEY")
    self.base_url = self.base_url or "https://api.provider.com/v1"
    self._create_http_clients()  # Last step - creates httpx clients
```

### HTTP Client Creation

All providers use httpx for HTTP requests:

- `self.client`: Synchronous httpx.Client
- `self.async_client`: Async httpx.AsyncClient
- Both configured with timeout and SSL settings from mixins
- Created via `_create_http_clients()` method (inherited from base class)

### Model Discovery

All providers implement:

- `_get_models()`: Internal method returning `List[Model]`
- `_get_default_model()`: Returns default model name as string
- `.models` property: Deprecated, emits warning, calls `_get_models()`

Use `AIFactory.get_provider_models(provider_name)` instead of `.models`.

### Error Handling Convention

Providers raise `RuntimeError` for API errors:

```python
try:
    response.raise_for_status()
except httpx.HTTPStatusError as e:
    raise RuntimeError(f"{Provider} API error: {e.response.text}")
```

### LangChain Integration

All language and embedding providers implement:

- `to_langchain()`: Converts to LangChain-compatible model
- Handles optional LangChain dependency gracefully
- Raises `ImportError` if LangChain not installed

## Integration with Factory

The `AIFactory` class in `factory.py` provides the unified interface:

- Maintains `_provider_modules` dict mapping provider names to module paths
- Implements dynamic import to avoid loading unused providers
- Provides `create_language()`, `create_embedding()`, etc. factory methods
- Provides `get_provider_models()` for static model discovery

Provider registration format:

```python
_provider_modules = {
    "language": {
        "openai": "esperanto.providers.llm.openai:OpenAILanguageModel",
        ...
    },
    "embedding": {
        "openai": "esperanto.providers.embedding.openai:OpenAIEmbeddingModel",
        ...
    },
    ...
}
```

## Gotchas

- **Import order**: Providers are imported lazily by factory to avoid dependency issues
- **Environment variables**: Follow pattern `{PROVIDER}_API_KEY` (all caps)
- **Base URL trailing slashes**: Strip them to avoid `//` in URLs
- **API key validation**: Always validate in `__post_init__` and raise helpful ValueError
- **Config dict**: Base `__post_init__()` initializes `_config` - always call `super().__post_init__()` first
- **Client creation timing**: Call `_create_http_clients()` last (requires api_key and base_url)
- **Provider name**: Must match key in `factory._provider_modules`
- **Optional imports**: Make provider imports optional in `src/esperanto/__init__.py` to handle missing dependencies

## When Adding a New Provider Type

If adding an entirely new provider type (not just a new provider for existing type):

1. Create new directory under `src/esperanto/providers/{type}/`
2. Create `base.py` with abstract base class
3. Implement base class inheriting from `TimeoutMixin`, `SSLMixin`
4. Define required abstract methods
5. Create `__init__.py` exporting base class
6. Add provider implementations
7. Add to `factory._provider_modules` with new type key
8. Add `create_{type}()` method to `AIFactory`
9. Create CLAUDE.md for the new directory
10. Update this file to reference new subdirectory

---

### **Block D: Standardized Synergy Block (The Loom Signature)**

Synergistic Artifact ID, Relationship Type, Synergistic Impact
CORE-CODEX-001, GOVERNS, The Codex provides the Supreme Law for this artifact.
GVRN.Registry.Master, INDEXES, This artifact is indexed in the Master Registry.
