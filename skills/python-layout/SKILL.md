---
name: python-layout
description: Python project and module structure guidance. Use when creating new Python projects, organizing modules, structuring packages, setting up file layouts, or deciding where code should live. Provides consistent conventions for project structure, module organization, file naming, and code organization within files.
---

# Python Code Layout Standards

Consistent code layout makes codebases navigable, maintainable, and predictable. These conventions apply to all Python projects.

## Core Principles

1. **Predictable structure** - Know where to find things without searching
2. **Single responsibility** - Each file has one purpose
3. **Public/private separation** - Underscore prefix for internal modules
4. **Flat over nested** - Avoid deep directory hierarchies
5. **Convention over configuration** - Standard names, standard places

---

## Project Structure

### Choose Your Layout

**src-layout** (recommended for published packages):
```
project-name/
├── pyproject.toml
├── src/
│   └── package_name/
│       ├── __init__.py
│       ├── _core.py
│       ├── _types.py
│       └── ...
├── tests/
└── playground/
```

**flat-layout** (for simple projects, internal tools):
```
project-name/
├── pyproject.toml
├── package_name/
│   ├── __init__.py
│   ├── _core.py
│   └── ...
├── tests/
└── playground/
```

| Layout | Use When |
|--------|----------|
| **src-layout** | Publishing to PyPI, complex projects, multiple packages |
| **flat layout** | Simple projects, internal tools, scripts |

See: [references/layouts.md](references/layouts.md) for detailed examples.

---

## Standard Module Files

Every non-trivial module should have:

| File | Purpose |
|------|---------|
| `__init__.py` | Public API exports only |
| `_types.py` | Dataclasses, enums, type aliases |
| `_exceptions.py` | Exception hierarchy |
| `_constants.py` | Configuration, defaults |
| `_core.py` | Main implementation |
| `_utils.py` | Internal helpers |

**Example structure:**
```
mypackage/
├── __init__.py       # from ._core import Processor
├── _types.py         # ProcessorConfig, Result
├── _exceptions.py    # ProcessorError hierarchy
├── _constants.py     # MAX_BATCH_SIZE = 1000
├── _core.py          # class Processor: ...
└── _utils.py         # def validate_input(): ...
```

---

## File Naming Conventions

| Pattern | Meaning | Example |
|---------|---------|---------|
| `_name.py` | Private/internal | `_utils.py`, `_types.py` |
| `name.py` | Public (rare) | `api.py` (public entry) |
| `test_*.py` | Test module | `test_processor.py` |
| `*_exploration.py` | Playground | `processor_exploration.py` |

---

## Import Ordering

Always order imports as:

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import json
from pathlib import Path

# 3. Third-party packages
import httpx

# 4. Local imports (absolute)
from mypackage.utils import helper

# 5. Local imports (relative)
from ._types import Config
```

See: [references/imports.md](references/imports.md) for detailed rules.

---

## Code Organization

### File Structure

```python
"""Module docstring."""

from __future__ import annotations

# Imports (in order above)

# Module-level logger
logger = logging.getLogger(__name__)

# Public classes (alphabetically or logically)
class MainClass:
    def __init__(self): ...
    def public_method(self): ...
    def _private_method(self): ...

# Supporting classes
class Helper:
    pass

# Public functions
def public_function(): ...

# Private functions
def _internal_function(): ...
```

### Class Method Ordering

1. Class variables
2. `__init__`
3. Properties (`@property`)
4. Public methods (most important first)
5. Private methods
6. Magic methods (`__repr__`, `__eq__`, etc.)

See: [references/code-organization.md](references/code-organization.md) for detailed examples.

---

## File Size Limits

- **Keep files under 300 lines** - When hitting 300, split into separate files
- **One responsibility per file** - Each file does one thing well
- **Functions under 50 lines** - Most functions should be concise
- **Classes under 25 methods** - If longer, extract helpers

See: [references/splitting.md](references/splitting.md) for when to split vs. combine.

---

## Package Patterns

### `__init__.py` - Exports Only

```python
"""Public API."""

from ._core import MainClass
from ._types import Config
from ._exceptions import CustomError

__all__ = ["MainClass", "Config", "CustomError"]
```

### Subpackages

Create subpackages when:
- Feature has 3+ files
- Has its own types/exceptions
- Could be used independently
- Has different maintainers

See: [references/patterns.md](references/patterns.md) for all standard patterns with code examples.

---

## Layout Checklist

Before considering code "done":

- [ ] `__init__.py` exports public API only
- [ ] Private modules prefixed with `_`
- [ ] Types in `_types.py`, exceptions in `_exceptions.py`
- [ ] Imports ordered: stdlib → third-party → local
- [ ] No circular imports
- [ ] Files under 300 lines
- [ ] One responsibility per file
- [ ] Class methods ordered consistently

---

## Quick Reference

```
__init__.py     → Public exports only
_types.py       → Dataclasses, enums, TypeAlias
_exceptions.py  → Exception hierarchy
_constants.py   → UPPER_CASE constants
_core.py        → Main implementation
_utils.py       → Internal helpers

Imports: stdlib → third-party → local absolute → local relative

File size: < 300 lines
Class methods: properties → public → private → magic
```

---

## Related Resources

- **[references/layouts.md](references/layouts.md)** - src-layout vs flat-layout with examples
- **[references/patterns.md](references/patterns.md)** - Standard patterns (__init__, _types, _exceptions, _constants)
- **[references/imports.md](references/imports.md)** - Import ordering rules and guidelines
- **[references/code-organization.md](references/code-organization.md)** - File structure and method ordering
- **[references/splitting.md](references/splitting.md)** - When to split vs combine, subpackage patterns
