---
name: llmtxt-generation
description: Create concise documentation for LLM consumption using the llms.txt standard. Use when onboarding new packages, documenting APIs for AI assistants, or creating context-efficient reference materials. Guides format, content selection, and storage conventions.
---

# llmtxt Generation Skill

Create concise, context-efficient documentation for LLM consumption following the llms.txt standard.

## What is llmtxt?

The llms.txt standard provides a format for creating documentation optimized for AI assistants:

- **Concise**: Fits within context windows (2000-4000 tokens)
- **Structured**: Consistent sections for quick parsing
- **Actionable**: Focus on "how to use" over "how it works"
- **Current**: Captures gotchas and patterns from actual usage

---

## When to Use This Skill

- After adopting a new package (see: `package-research` skill)
- Documenting internal APIs for AI-assisted development
- Creating quick-reference guides for complex libraries
- Onboarding to a new codebase or domain

---

## Quick Reference

```
1. Identify Scope       -> What needs documenting?
2. Gather Information   -> Docs, source, experiments
3. Write Core Sections  -> Overview, Install, API, Patterns
4. Add Gotchas          -> Common mistakes, edge cases
5. Validate Size        -> Keep under 4000 tokens
6. Store Appropriately  -> docs/llmtxt/ or .claude/llmtxt/
```

---

## llmtxt Format

### Required Sections

```markdown
# [Package Name] llmtxt

> One-line description of what this package does.

## Overview

2-3 sentences explaining:
- What problem it solves
- When to use it
- Key characteristics (sync/async, typed, etc.)

## Installation

```bash
pip install package-name
```

## Core API

### Primary Classes/Functions

[The 3-5 most important APIs with signatures and brief descriptions]

## Common Patterns

### Pattern 1: [Name]

```python
# Minimal working example
```

### Pattern 2: [Name]

```python
# Another common use case
```

## Gotchas

- [Common mistake 1 and how to avoid it]
- [Common mistake 2 and how to avoid it]
- [Edge case to watch for]

## Quick Reference

| Operation | Code |
|-----------|------|
| [action] | `function()` |
| [action] | `function(arg)` |
```

### Optional Sections

Add only if valuable and within budget:

- **Configuration** - If package has complex setup
- **Error Handling** - If exceptions are non-obvious
- **Integration** - If combining with other packages
- **Performance** - If optimization is critical

---

## Content Guidelines

### What to Include

1. **Signatures with Types**
   ```python
   def fetch(url: str, *, timeout: float = 30.0) -> Response:
   ```

2. **Minimal Working Examples**
   ```python
   # Show the simplest complete usage
   from package import Client
   client = Client()
   result = client.do_thing("input")
   ```

3. **Common Patterns from Your Codebase**
   ```python
   # How WE use this package
   # (may differ from official docs)
   ```

4. **Discovered Gotchas**
   - Thread safety issues
   - Surprising default behavior
   - Version-specific quirks

### What to Exclude

- Implementation details (how it works internally)
- Historical context (why it was built)
- Exhaustive API listings (link to full docs instead)
- Rarely-used features
- Theoretical explanations

### Writing Style

- **Imperative**: "Use `foo()` to..." not "You can use `foo()` to..."
- **Direct**: State facts, skip hedging
- **Code-first**: Show code, then explain if needed
- **Specific**: Concrete examples over abstract descriptions

---

## Token Budget Management

### Target Sizes

| Document Type | Token Target | Max Lines |
|---------------|--------------|-----------|
| Simple package | 1500-2000 | ~100 |
| Medium package | 2500-3500 | ~200 |
| Complex package | 3500-4000 | ~300 |

### Estimation

Rough token estimation:
- ~4 characters per token (English text)
- ~3 characters per token (code)
- A 200-line file is typically 2000-3000 tokens

### Staying Within Budget

1. **Prioritize ruthlessly** - Core API > Patterns > Gotchas > Edge cases
2. **Use tables** - More compact than prose
3. **Inline docs** - `# comment` in code vs separate explanation
4. **Link out** - "See official docs for [advanced topic]"

---

## Creating llmtxt for a Package

### Step 1: Gather Information

```bash
# Read official docs
open https://package.readthedocs.io/

# Check source for signatures
python -c "import package; help(package.main_class)"

# Find examples in tests
grep -r "def test_" ./venv/lib/python*/site-packages/package/
```

### Step 2: Identify Core APIs

List the classes/functions you actually use:

```markdown
## APIs to Document

### Must Document
- [ ] `Client` - Main entry point
- [ ] `Client.fetch()` - Primary method
- [ ] `Response` - Return type

### Maybe Document (if space)
- [ ] `Client.configure()` - Setup options
- [ ] `ClientError` - Exception type

### Skip
- [ ] Internal helpers
- [ ] Deprecated APIs
- [ ] Advanced features we don't use
```

### Step 3: Write and Iterate

1. Write first draft focusing on core API
2. Add patterns from your actual usage
3. Include gotchas you discovered
4. Check token count
5. Cut until within budget

### Step 4: Validate

```python
# Quick validation script
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")

with open("docs/llmtxt/package.md") as f:
    content = f.read()

tokens = len(enc.encode(content))
print(f"Token count: {tokens}")

if tokens > 4000:
    print("WARNING: Over budget, needs trimming")
```

---

## Storage Conventions

### Project-Level llmtxt

Store in `docs/llmtxt/` or `.claude/llmtxt/`:

```
project/
├── docs/
│   └── llmtxt/
│       ├── httpx.md           # External package docs
│       ├── pydantic.md        # External package docs
│       └── our_api.md         # Internal API docs
└── ...
```

### Organization-Level llmtxt

For shared documentation across projects:

```
~/.claude/llmtxt/
├── common/
│   ├── httpx.md
│   ├── pytest.md
│   └── pydantic.md
└── domain/
    ├── automotive_terms.md
    └── k8s_patterns.md
```

### Naming Convention

- External packages: `{package_name}.md`
- Internal modules: `{module_name}.md`
- Domain knowledge: `{domain}_terms.md` or `{domain}_patterns.md`

---

## Example: httpx llmtxt

```markdown
# httpx llmtxt

> Modern async/sync HTTP client for Python with connection pooling.

## Overview

httpx provides HTTP/1.1 and HTTP/2 support with both sync and async APIs.
Use for making HTTP requests with automatic connection pooling, timeouts,
and redirect handling. Typed, well-documented, actively maintained.

## Installation

```bash
pip install httpx
```

## Core API

### Client (sync)

```python
import httpx

# Simple request
response = httpx.get("https://api.example.com/items")

# With client (connection pooling)
with httpx.Client(base_url="https://api.example.com") as client:
    response = client.get("/items")
    response.raise_for_status()
    data = response.json()
```

### AsyncClient

```python
import httpx

async with httpx.AsyncClient(base_url="https://api.example.com") as client:
    response = await client.get("/items")
    data = response.json()
```

### Response

```python
response.status_code      # int
response.headers          # Headers dict-like
response.json()           # Parse JSON body
response.text             # Body as string
response.raise_for_status()  # Raise on 4xx/5xx
```

## Common Patterns

### POST with JSON

```python
response = client.post("/items", json={"name": "foo", "value": 42})
```

### Headers and Auth

```python
client = httpx.Client(
    headers={"X-API-Key": "secret"},
    auth=("user", "pass"),  # Basic auth
)
```

### Timeout Configuration

```python
client = httpx.Client(timeout=httpx.Timeout(10.0, connect=5.0))
```

### Retry Pattern (with tenacity)

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential())
def fetch_with_retry(client: httpx.Client, url: str) -> dict:
    response = client.get(url)
    response.raise_for_status()
    return response.json()
```

## Gotchas

- **Always use context manager**: `Client()` without `with` leaks connections
- **Default timeout is None**: Always set explicit timeouts in production
- **raise_for_status() doesn't return**: It returns None, not the response
- **Connection pooling requires Client**: Bare `httpx.get()` creates new connection each time

## Quick Reference

| Operation | Code |
|-----------|------|
| GET | `client.get(url)` |
| POST JSON | `client.post(url, json=data)` |
| POST form | `client.post(url, data=data)` |
| Headers | `client.get(url, headers={...})` |
| Query params | `client.get(url, params={...})` |
| Check status | `response.raise_for_status()` |
| Parse JSON | `response.json()` |
```

---

## Integration with Workflow

### After Package Research (Phase 0)

```
Step 0.2: Package Research
├── ...
├── Make Decision: COMPOSE
└── Create llmtxt documentation  <-- THIS SKILL
    ├── Gather package information
    ├── Identify core APIs used
    ├── Write llmtxt document
    └── Store in docs/llmtxt/
```

### During Development (Phase 1)

Reference llmtxt when using adopted packages:

```
Step 1: Implementation
├── Read relevant llmtxt files
├── Follow documented patterns
├── Update llmtxt if discovering new gotchas
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Copy-paste full docs | Blows context budget | Curate essential parts |
| Skip gotchas | Repeat mistakes | Document discoveries |
| Out-of-date | Misleads future work | Update when upgrading |
| Generic examples | Not actionable | Use project-specific patterns |
| Missing types | Less useful for AI | Include signatures with types |

---

## Templates

See: [template.md](template.md) for a starting template to structure your llmtxt documentation.

---

## References

- [llms.txt specification](https://llmstxt.org/)
- `package-research` skill - Finding packages to document
- `unix-philosophy` skill - Composition principles
