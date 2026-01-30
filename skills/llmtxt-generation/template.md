# llmtxt Template

Use this template when creating llmtxt documentation for adopted packages.

---

## Template

```markdown
# [Package Name] llmtxt

> [One-line description: what problem this package solves]

## Overview

[2-3 sentences explaining:
- What the package does
- When to use it
- Key characteristics (sync/async, typed, performance, etc.)]

## Installation

```bash
pip install [package-name]
```

## Core API

### [Primary Class/Function 1]

```python
from [package] import [Class]

# Signature with types
def method(
    arg1: Type1,
    arg2: Type2,
    *,
    optional: Type3 = default,
) -> ReturnType:
    """Brief description."""
```

### [Primary Class/Function 2]

```python
# Another key API
```

### [Primary Class/Function 3]

```python
# Third key API (limit to 3-5 most important)
```

## Common Patterns

### Pattern 1: [Descriptive Name]

```python
# Minimal working example for common use case
from [package] import [needed]

# Show complete, runnable code
result = do_thing()
```

### Pattern 2: [Descriptive Name]

```python
# Another common pattern from your actual usage
```

### Pattern 3: [Descriptive Name] (Optional)

```python
# Third pattern if space permits
```

## Gotchas

- **[Issue 1]**: [Brief description and how to avoid]
- **[Issue 2]**: [Brief description and how to avoid]
- **[Issue 3]**: [Brief description and how to avoid]

## Quick Reference

| Operation | Code |
|-----------|------|
| [Common action 1] | `function()` |
| [Common action 2] | `function(arg)` |
| [Common action 3] | `Class.method()` |
| [Common action 4] | `result.attribute` |

## See Also

- [Official Documentation](https://package.readthedocs.io/)
- [GitHub Repository](https://github.com/org/package)
```

---

## Guidelines

### Content Priority (in order)

1. **Core API signatures** - Most important functions/classes with types
2. **Common patterns** - How YOU use the package in this project
3. **Gotchas** - Mistakes you made or edge cases you discovered
4. **Quick reference** - Lookup table for common operations

### Token Budget

| Document Type | Target Tokens | Max Lines |
|---------------|---------------|-----------|
| Simple package | 1500-2000 | ~100 |
| Medium package | 2500-3500 | ~200 |
| Complex package | 3500-4000 | ~300 |

### What to Include

- Type annotations (always)
- Minimal complete examples (not snippets)
- YOUR patterns (may differ from official docs)
- Discovered gotchas and workarounds
- Context managers and cleanup requirements

### What to Exclude

- Implementation details (how it works internally)
- History and rationale (why it was built)
- Exhaustive API listings (link to full docs)
- Rarely-used features
- Features you don't use

### Style Guidelines

- **Imperative voice**: "Use `foo()` to..." not "You can use..."
- **Code-first**: Show code, then explain if needed
- **Specific examples**: Concrete over abstract
- **Type everything**: Include type hints in all signatures

---

## Example: Completed llmtxt

See the httpx example in the `llmtxt-generation` skill for a complete, well-formatted llmtxt document.

---

## Storage Location

Store completed llmtxt files in one of:

```
project/
├── docs/
│   └── llmtxt/
│       └── [package].md     # Project-level
└── .claude/
    └── llmtxt/
        └── [package].md     # Alternative location
```

File naming: `{package_name}.md` (lowercase, hyphens for multi-word)

---

## Checklist

Before finalizing llmtxt:

- [ ] Overview explains what and when
- [ ] Core API covers 3-5 most important interfaces
- [ ] Patterns are complete and runnable
- [ ] Gotchas include real issues discovered
- [ ] Quick reference covers common operations
- [ ] Token count is under 4000
- [ ] All signatures include types
- [ ] Examples are from actual project usage
