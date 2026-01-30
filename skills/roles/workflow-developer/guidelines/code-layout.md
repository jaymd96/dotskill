# Code Layout Guidelines

Follow consistent file and module organization.

See also: [python-layout skill](../../foundations/python-layout.md) for comprehensive guide.

---

## Standard Module Structure

Every non-trivial module should have this structure:

```
my_package/
├── __init__.py          # Public API exports only
├── _types.py            # Dataclasses, enums, type aliases
├── _exceptions.py       # Exception hierarchy
├── _constants.py        # Configuration, defaults
├── _core.py             # Main implementation
└── _utils.py            # Internal helpers
```

### `__init__.py` - Public API Only

```python
"""Public API for my_package."""

from ._core import MainClass, process_data
from ._exceptions import ProcessingError
from ._types import Config, Result

__all__ = [
    "MainClass",
    "process_data",
    "ProcessingError",
    "Config",
    "Result",
]
```

### `_types.py` - Type Definitions

```python
"""Type definitions for my_package."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    """Configuration object."""
    timeout: int = 30
    retries: int = 3

@dataclass
class Result:
    """Processing result."""
    success: bool
    data: dict
```

### `_exceptions.py` - Exception Hierarchy

```python
"""Exceptions for my_package."""

class PackageError(Exception):
    """Base exception for my_package."""
    pass

class ConfigurationError(PackageError):
    """Invalid configuration."""
    pass

class ProcessingError(PackageError):
    """Processing failed."""
    pass
```

### `_core.py` - Main Implementation

```python
"""Core functionality."""
from ._types import Config, Result
from ._exceptions import ProcessingError

class MainClass:
    """Main class for processing."""

    def __init__(self, config: Config) -> None:
        self.config = config

    def process(self, data: dict) -> Result:
        """Process data."""
        try:
            # Implementation
            return Result(success=True, data=data)
        except Exception as e:
            raise ProcessingError(f"Failed: {e}")
```

---

## Import Ordering

**Always order imports as follows:**

```python
# 1. Future imports
from __future__ import annotations

# 2. Standard library
import json
import logging
from pathlib import Path
from typing import Optional

# 3. Third-party packages
import httpx
import pydantic

# 4. Local imports (absolute paths)
from mypackage.utils import helper
from mypackage._types import Config

# 5. Local imports (relative paths, within package)
from ._core import MainClass
from ._types import Result
```

---

## File Size Limits

- **Keep files under 300 lines** - When hitting 300, split into separate files
- **One responsibility per file** - Each file does one thing well
- **Functions under 50 lines** - Most functions should be concise
- **Methods under 25 lines** - Classes with short, focused methods

If you're hitting 300 lines, you have too much responsibility.

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | `_snake_case.py` | `_scheduler.py` |
| Classes | `PascalCase` | `TaskQueue` |
| Functions | `snake_case` | `process_data` |
| Constants | `UPPER_SNAKE` | `MAX_RETRIES` |
| Private | `_prefix` | `_internal_method` |
| Protected | `_prefix` | `_validate` |

---

## Layout Checklist

Before considering code "done":

- [ ] `__init__.py` exports public API only
- [ ] Private modules prefixed with `_`
- [ ] Types in `_types.py`
- [ ] Exceptions in `_exceptions.py`
- [ ] Constants in `_constants.py` (if many)
- [ ] Main logic in `_core.py`
- [ ] Helpers in `_utils.py`
- [ ] Imports ordered: stdlib → third-party → local
- [ ] Files under 300 lines
- [ ] No circular dependencies
- [ ] Package structure matches codebase patterns

---

## Example: Well-Organized Package

```
analytics/
├── __init__.py
│   # Exports: Analyzer, AnalysisResult, AnalysisError
├── _types.py
│   # Config, AnalysisResult, MetricType
├── _exceptions.py
│   # AnalysisError, ConfigurationError
├── _constants.py
│   # DEFAULT_BATCH_SIZE, SUPPORTED_FORMATS
├── _core.py
│   # Analyzer class, core logic
├── _processing.py
│   # Data processing functions
├── _validators.py
│   # Validation functions
└── _utils.py
    # Helper utilities
```

---

## When Organizing Your Code

1. **Identify responsibilities** - What distinct jobs does the code do?
2. **Group by responsibility** - Put related code in same module
3. **Create clear interfaces** - Public APIs in `__init__.py`
4. **Hide implementation** - Use `_prefix` for internal modules
5. **Keep modules focused** - Each module does one thing well
6. **Name clearly** - Names should reflect responsibility

Result: Code that's easy to navigate, understand, and maintain.
