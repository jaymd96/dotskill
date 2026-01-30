---
name: python-layout
description: Python project and module structure guidance. Use when creating new Python projects, organizing modules, structuring packages, setting up file layouts, or deciding where code should live. Provides consistent conventions for project structure, module organization, file naming, and code organization within files.
---

# Python Code Layout Standards

Consistent code layout makes codebases navigable, maintainable, and predictable. These conventions apply to all Python projects.

## Contents

- [Core Principles](#core-principles)
- [Project Structure](#project-structure) - Directory layouts
- [Module Organization](#module-organization) - File naming and purpose
- [Import Ordering](#import-ordering) - Standard import sequences
- [Naming Conventions](#naming-conventions) - Consistent names
- [File Size Limits](#file-size-limits) - When to split files
- [Public API Definition](#public-api-definition) - `__init__.py` exports
- [Internal Modules](#internal-modules) - Private implementation
- [Submodules](#submodules) - Feature organization
- [Package Layout Checklist](#package-layout-checklist) - Verification

## Core Principles

1. **Predictable structure** - Know where to find things without searching
2. **Single responsibility** - Each file has one purpose
3. **Public/private separation** - Underscore prefix for internal modules
4. **Flat over nested** - Avoid deep directory hierarchies
5. **Convention over configuration** - Standard names, standard places

---

## Project Structure

### Standard Layout (src-layout)

```
project-name/
├── pyproject.toml           # Project configuration (single source)
├── README.md                # Project documentation
├── src/
│   └── package_name/        # Main package
│       ├── __init__.py      # Public API exports
│       ├── _types.py        # Type definitions
│       ├── _exceptions.py   # Exception hierarchy
│       ├── _constants.py    # Configuration constants
│       ├── _core.py         # Main implementation
│       ├── _utils.py        # Internal utilities
│       └── submodule/       # Feature submodule (if needed)
│           ├── __init__.py
│           └── ...
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   └── test_*.py            # Test modules
├── playground/              # Exploration code (part of project!)
│   ├── __init__.py
│   └── *_exploration.py     # Interactive experiments
└── docs/                    # Documentation (if extensive)
```

### Flat Layout (simpler projects)

```
project-name/
├── pyproject.toml
├── README.md
├── package_name/
│   ├── __init__.py
│   ├── _types.py
│   ├── _exceptions.py
│   └── _core.py
├── tests/
└── playground/
```

### When to Use Each

| Layout | Use When |
|--------|----------|
| **src-layout** | Publishing to PyPI, complex projects, multiple packages |
| **flat layout** | Simple projects, internal tools, scripts |

---

## Module Organization

### Standard Module Files

Every non-trivial module should have:

| File | Purpose | Contents |
|------|---------|----------|
| `__init__.py` | Public API | Exports only, no implementation |
| `_types.py` | Type definitions | Dataclasses, enums, TypedDicts, type aliases |
| `_exceptions.py` | Error handling | Exception hierarchy for this module |
| `_constants.py` | Configuration | Constants, defaults, magic numbers |
| `_core.py` | Main logic | Primary implementation |
| `_utils.py` | Internal helpers | Private utility functions |

### Optional Files (when needed)

| File | Purpose | When to Add |
|------|---------|-------------|
| `_crud.py` | Database operations | Database/storage layer |
| `_validators.py` | Input validation | Complex validation logic |
| `_serializers.py` | Serialization | JSON/YAML/Protobuf conversion |
| `_api.py` | External API calls | Third-party integrations |
| `_cache.py` | Caching logic | Performance optimization |

### Example Module

```
mypackage/
├── __init__.py              # from ._core import Processor
├── _types.py                # @dataclass ProcessorConfig
├── _exceptions.py           # class ProcessorError(Exception)
├── _constants.py            # MAX_BATCH_SIZE = 1000
├── _core.py                 # class Processor: ...
└── _utils.py                # def _validate_input(data): ...
```

---

## File Naming Conventions

### Module Files

| Pattern | Meaning | Example |
|---------|---------|---------|
| `_name.py` | Private/internal module | `_utils.py`, `_types.py` |
| `name.py` | Public module (rare) | `api.py` (public API entry) |
| `__init__.py` | Package marker | Always required |

### Test Files

| Pattern | Meaning | Example |
|---------|---------|---------|
| `test_*.py` | Test module | `test_processor.py` |
| `conftest.py` | Shared fixtures | One per test directory |

### Playground Files

| Pattern | Meaning | Example |
|---------|---------|---------|
| `*_exploration.py` | Feature exploration | `processor_exploration.py` |
| `*_experiments.py` | Experimental scenarios | `batch_experiments.py` |
| `test_*.py` | Playground tests (informal) | `test_new_feature.py` |

---

## `__init__.py` Patterns

### Public API Exports Only

```python
"""Package public API.

This module exposes the public interface. All implementation
is in private modules prefixed with underscore.

Public API:
    Processor: Main processing class
    ProcessorConfig: Configuration dataclass
    ProcessorError: Base exception for processor errors
"""

from ._core import Processor
from ._types import ProcessorConfig
from ._exceptions import ProcessorError

__all__ = [
    "Processor",
    "ProcessorConfig",
    "ProcessorError",
]
```

### What NOT to Put in `__init__.py`

```python
# BAD: Implementation in __init__.py
class Processor:
    def __init__(self):
        ...

# BAD: Complex logic
def configure_logging():
    ...

# BAD: Side effects on import
logging.basicConfig(...)
```

---

## `_types.py` Patterns

### Type Definitions

```python
"""Type definitions for the processor module.

Contains:
- Dataclasses for configuration and data transfer
- Enums for categorical values
- Type aliases for complex types
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, TypeAlias

# Type aliases
ItemId: TypeAlias = str
Metadata: TypeAlias = dict[str, Any]


class ProcessingMode(Enum):
    """Processing mode options."""
    SYNC = auto()
    ASYNC = auto()
    BATCH = auto()


class Priority(Enum):
    """Task priority levels."""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass(frozen=True)
class ProcessorConfig:
    """Configuration for Processor.

    Attributes:
        mode: Processing mode (default: SYNC)
        max_batch_size: Maximum items per batch (default: 100)
        timeout_seconds: Operation timeout (default: 30)
    """
    mode: ProcessingMode = ProcessingMode.SYNC
    max_batch_size: int = 100
    timeout_seconds: float = 30.0

    def __post_init__(self) -> None:
        if self.max_batch_size < 1:
            raise ValueError("max_batch_size must be positive")


@dataclass(frozen=True)
class ProcessingResult:
    """Result of a processing operation.

    Attributes:
        success: Whether processing succeeded
        item_id: ID of processed item
        output: Processing output (if successful)
        error: Error message (if failed)
        duration_ms: Processing duration in milliseconds
    """
    success: bool
    item_id: ItemId
    output: Any = None
    error: str | None = None
    duration_ms: float = 0.0
    processed_at: datetime = field(default_factory=datetime.now)
```

---

## `_exceptions.py` Patterns

### Exception Hierarchy

```python
"""Exception hierarchy for the processor module.

Base exception: ProcessorError
All module-specific exceptions inherit from it.
"""

from typing import Any


class ProcessorError(Exception):
    """Base exception for all processor errors.

    Catch this to handle any processor-related error.
    """


class ConfigurationError(ProcessorError):
    """Invalid configuration provided.

    Attributes:
        field: The invalid configuration field
        value: The invalid value
        message: Explanation of what's wrong
    """

    def __init__(self, field: str, value: Any, message: str):
        self.field = field
        self.value = value
        self.message = message
        super().__init__(f"Invalid {field}={value!r}: {message}")


class ProcessingError(ProcessorError):
    """Error during item processing.

    Attributes:
        item_id: ID of the item that failed
        reason: Why processing failed
    """

    def __init__(self, item_id: str, reason: str):
        self.item_id = item_id
        self.reason = reason
        super().__init__(f"Failed to process {item_id}: {reason}")


class TimeoutError(ProcessorError):
    """Operation timed out.

    Attributes:
        operation: What operation timed out
        timeout_seconds: The timeout value
    """

    def __init__(self, operation: str, timeout_seconds: float):
        self.operation = operation
        self.timeout_seconds = timeout_seconds
        super().__init__(f"{operation} timed out after {timeout_seconds}s")


class ItemNotFoundError(ProcessorError):
    """Requested item does not exist.

    Attributes:
        item_id: ID of the missing item
    """

    def __init__(self, item_id: str):
        self.item_id = item_id
        super().__init__(f"Item not found: {item_id}")
```

---

## `_constants.py` Patterns

### Module Constants

```python
"""Constants for the processor module.

Configuration defaults and magic numbers.
"""

from typing import Final

# Processing limits
MAX_BATCH_SIZE: Final[int] = 1000
DEFAULT_BATCH_SIZE: Final[int] = 100
MAX_RETRIES: Final[int] = 3
RETRY_BACKOFF_SECONDS: Final[float] = 1.0

# Timeouts (seconds)
DEFAULT_TIMEOUT: Final[float] = 30.0
MAX_TIMEOUT: Final[float] = 300.0
CONNECT_TIMEOUT: Final[float] = 5.0

# API endpoints (if applicable)
API_BASE_URL: Final[str] = "https://api.example.com/v1"
API_VERSION: Final[str] = "2024-01"

# Feature flags
ENABLE_CACHING: Final[bool] = True
ENABLE_METRICS: Final[bool] = True

# File paths (relative to package)
DEFAULT_CONFIG_PATH: Final[str] = "config/defaults.yaml"
```

---

## Import Ordering

### Standard Order

```python
"""Module docstring."""

# 1. Future imports (if needed)
from __future__ import annotations

# 2. Standard library
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, TypeVar

# 3. Third-party packages
import httpx
from pydantic import BaseModel

# 4. Local imports (absolute)
from mypackage.utils import helper
from mypackage.models import Item

# 5. Local imports (relative) - same package only
from ._types import ProcessorConfig, ProcessingResult
from ._exceptions import ProcessorError
from ._constants import MAX_BATCH_SIZE
```

### Import Guidelines

| Type | Example | Notes |
|------|---------|-------|
| Module import | `import json` | Prefer for stdlib |
| From import | `from pathlib import Path` | For specific items |
| Relative import | `from ._types import Config` | Same package only |
| Alias import | `import numpy as np` | Well-known aliases only |

---

## Code Organization Within Files

### File Structure Template

```python
"""Module docstring explaining purpose.

Provides:
    MainClass: Primary functionality
    helper_function: Supporting operation
"""

from __future__ import annotations

# Imports (ordered as above)
import logging
from typing import Any

from ._types import Config, Result
from ._exceptions import ModuleError
from ._constants import DEFAULT_VALUE

# Module-level logger
logger = logging.getLogger(__name__)

# Type variables (if needed)
T = TypeVar("T")

# Module-level constants (private to this file)
_INTERNAL_LIMIT = 100


# Public classes (alphabetical or logical order)
class MainClass:
    """Primary class for this module.

    Attributes:
        config: Configuration object
    """

    def __init__(self, config: Config) -> None:
        """Initialize with configuration."""
        self._config = config
        self._state: dict[str, Any] = {}

    # Public methods
    def do_thing(self, item: str) -> Result:
        """Perform the main operation."""
        self._validate(item)
        return self._process(item)

    # Private methods (after public)
    def _validate(self, item: str) -> None:
        """Validate input."""
        if not item:
            raise ModuleError("Item cannot be empty")

    def _process(self, item: str) -> Result:
        """Internal processing logic."""
        return Result(value=item.upper())


# Supporting classes
class SupportingClass:
    """Secondary class used by MainClass."""
    pass


# Public functions
def helper_function(data: Any) -> str:
    """Helper function for common operations."""
    return str(data)


# Private functions
def _internal_helper() -> None:
    """Internal helper not part of public API."""
    pass
```

### Method Ordering Within Classes

```python
class WellOrganizedClass:
    """Class with proper method ordering."""

    # 1. Class variables
    default_value: int = 0

    # 2. __init__
    def __init__(self, value: int) -> None:
        self._value = value

    # 3. Properties
    @property
    def value(self) -> int:
        return self._value

    # 4. Public methods (most important first)
    def primary_operation(self) -> None:
        """Main functionality."""
        pass

    def secondary_operation(self) -> None:
        """Supporting functionality."""
        pass

    # 5. Private methods
    def _validate(self) -> None:
        """Internal validation."""
        pass

    def _helper(self) -> None:
        """Internal helper."""
        pass

    # 6. Magic methods (at end)
    def __repr__(self) -> str:
        return f"WellOrganizedClass({self._value})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, WellOrganizedClass):
            return NotImplemented
        return self._value == other._value
```

---

## When to Split vs Combine

### Split When

| Situation | Action |
|-----------|--------|
| File > 300 lines | Split into logical modules |
| Multiple unrelated classes | Separate by responsibility |
| Complex subfeature | Create subpackage |
| Circular imports | Reorganize dependencies |

### Combine When

| Situation | Action |
|-----------|--------|
| < 50 lines each | Merge related small files |
| Always used together | Keep in same module |
| Tight coupling | Single module is clearer |

### Splitting Example

```
# Before: One large file
mypackage/
└── processor.py  (500 lines, mixed concerns)

# After: Split by responsibility
mypackage/
├── __init__.py           # Public API
├── _types.py             # ProcessorConfig, Result
├── _exceptions.py        # ProcessorError hierarchy
├── _processor.py         # Processor class (200 lines)
├── _validator.py         # Validation logic (100 lines)
└── _serializer.py        # JSON/YAML conversion (100 lines)
```

---

## Subpackage Patterns

### When to Create Subpackages

Create a subpackage when a feature:
- Has multiple files (3+)
- Has its own types/exceptions
- Could be used independently
- Has different maintainers

### Subpackage Structure

```
mypackage/
├── __init__.py
├── _types.py
├── _core.py
└── subfeature/           # Subpackage
    ├── __init__.py       # Subpackage public API
    ├── _types.py         # Subfeature types
    ├── _exceptions.py    # Subfeature exceptions
    └── _implementation.py
```

### Exposing Subpackage API

```python
# mypackage/__init__.py
from ._core import MainClass
from .subfeature import SubFeature, SubFeatureConfig

__all__ = ["MainClass", "SubFeature", "SubFeatureConfig"]
```

---

## Checklist

Before committing code organization changes:

- [ ] `__init__.py` exports public API only
- [ ] Private modules prefixed with `_`
- [ ] Types in `_types.py`
- [ ] Exceptions in `_exceptions.py`
- [ ] Constants in `_constants.py`
- [ ] Imports ordered correctly
- [ ] No circular imports
- [ ] Files under 300 lines
- [ ] One responsibility per file
- [ ] Class methods ordered consistently

---

## Quick Reference

```
__init__.py     -> Public exports only
_types.py       -> Dataclasses, enums, TypeAlias
_exceptions.py  -> Exception hierarchy
_constants.py   -> UPPER_CASE constants
_core.py        -> Main implementation
_utils.py       -> Internal helpers
_crud.py        -> Database operations (optional)

Imports: stdlib -> third-party -> local absolute -> local relative

File size: < 300 lines
Class methods: properties -> public -> private -> magic
```
