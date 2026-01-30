---
name: python-coding-standards
description: Python coding standards for production code. Use when writing, reviewing, or refactoring Python modules, classes, or functions. Provides opinionated standards for maintainable, readable, well-structured Python code.
---

# Python Coding Standards

Standards for writing production-quality Python code that is maintainable, readable, and well-structured.

## Contents

- [Core Principles](#core-principles)
- [Module Layout](#module-layout)
- [Naming Conventions](#naming-conventions)
- [Type Hints & Documentation](#type-hints--documentation)
- [Functions](#functions) - Design and structure
- [Classes](#classes) - Definition and patterns
- [Error Handling](#error-handling)
- [Testing](#testing)
- [Code Review Checklist](#code-review-checklist)
- [Anti-Patterns](#anti-patterns)
- [Advanced Patterns](#advanced-patterns)

## Core Principles

1. **Explicit over implicit** - Name things, use keyword args, type hints
2. **Flat over nested** - Guard clauses, early returns
3. **Simple over complex** - Start minimal, add complexity when proven needed
4. **Immutable by default** - `frozen=True`, return copies not references
5. **Fail fast** - Validate at construction, raise early with context
6. **One way to do things** - Don't provide multiple APIs for same operation
7. **Parse don't validate** - Transform raw data to types at boundaries
8. **Explicit dependencies** - Pass dependencies, avoid globals/singletons
9. **Delete dead code** - Version control remembers
10. **Boring technology** - Use simplest tool that works

---

## Module Layout

```
my_package/
├── __init__.py          # Public API exports only
├── _types.py            # Dataclasses, enums, type aliases
├── _exceptions.py       # Exception hierarchy
├── _constants.py        # Configuration, defaults
├── _core.py             # Main implementation
└── _utils.py            # Internal helpers
```

- Prefix internal modules with `_`
- Keep files under 300 lines
- One responsibility per module

---

## Naming Conventions

| Element | Convention | Example |
|---------|------------|---------|
| Modules | `_snake_case.py` | `_scheduler.py` |
| Classes | `PascalCase` | `TaskQueue` |
| Functions | `snake_case` | `find_worker` |
| Constants | `UPPER_SNAKE` | `MAX_RETRIES` |
| Private | `_prefix` | `_validate` |

### Good Names

```python
# Clear, descriptive
def calculate_total_price(items: list[Item]) -> Decimal:
    ...

# Intention-revealing
is_valid = validator.check(input_data)
has_permission = user.can_access(resource)

# Domain-appropriate
class OrderProcessor:
    def submit_order(self, order: Order) -> Confirmation:
        ...
```

### Bad Names

```python
# Too short, cryptic
def calc(i):  # What is i? What does calc do?
    ...

# Misleading
def validate(data):  # But it also transforms data!
    ...

# Generic
def process(x):  # Process what? How?
    ...
```

---

## Type Hints

Always annotate public APIs:

```python
def schedule_task(
    self,
    task: Task,
    *,
    priority: Priority = Priority.NORMAL,
    run_at: datetime | None = None,
) -> ScheduledTask:
    """Schedule a task for execution.

    Args:
        task: The task to schedule.
        priority: Execution priority (default: NORMAL).
        run_at: When to run (default: immediately).

    Returns:
        The scheduled task with assigned ID.

    Raises:
        ValidationError: If task is invalid.
        DuplicateError: If task ID already exists.
    """
```

### Type Hint Patterns

```python
from typing import Any, Iterator, Callable, TypeVar

# Optional values
def find(id: str) -> Item | None:
    ...

# Collections
def process_all(items: list[Item]) -> dict[str, Result]:
    ...

# Callbacks
def on_complete(callback: Callable[[Result], None]) -> None:
    ...

# Generics
T = TypeVar('T')
def first(items: list[T]) -> T | None:
    return items[0] if items else None
```

---

## Dataclasses

Use `frozen=True` for value objects:

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass(frozen=True)
class Task:
    """A unit of work to be executed."""

    id: str
    type: TaskType
    payload: dict[str, Any]
    priority: Priority = Priority.NORMAL
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self) -> None:
        if not self.id:
            raise ValidationError("Task ID cannot be empty")

    def with_priority(self, priority: Priority) -> "Task":
        """Return a copy with different priority."""
        return dataclasses.replace(self, priority=priority)
```

### When to Use Dataclasses

- Value objects (immutable data carriers)
- Configuration objects
- API request/response models
- Domain entities

### When NOT to Use Dataclasses

- Services with behavior (use regular classes)
- Singletons
- Abstract base classes

---

## Exceptions

One base per domain, include context:

```python
class SchedulerError(Exception):
    """Base for all scheduler errors."""


class TaskNotFoundError(SchedulerError):
    """Requested task does not exist."""

    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Task not found: {task_id}")


class ValidationError(SchedulerError):
    """Input validation failed."""

    def __init__(self, field: str, message: str):
        self.field = field
        self.message = message
        super().__init__(f"Validation failed for {field}: {message}")
```

### Exception Guidelines

- Include context (what went wrong, with what data)
- Don't catch and re-raise without adding information
- Use specific exception types, not generic Exception
- Document exceptions in docstrings

---

## Function Structure

Validate -> Do -> Return:

```python
def submit_task(self, task: Task) -> ScheduledTask:
    """Submit a task for scheduling.

    Args:
        task: The task to submit.

    Returns:
        The scheduled task.

    Raises:
        ValidationError: If task is invalid.
        DuplicateTaskError: If task ID exists.
    """
    # 1. Validate
    self._validate_task(task)
    if self._tasks.exists(task.id):
        raise DuplicateTaskError(task.id)

    # 2. Do
    scheduled = ScheduledTask(task=task, submitted_at=datetime.now())
    self._tasks.save(task)
    self._queue.push(scheduled)

    # 3. Return
    return scheduled
```

---

## Guard Clauses

Return early, keep happy path flat:

```python
# Good: Flat structure with guards
def execute(self, task: Task) -> ExecutionResult:
    if task.is_cancelled:
        return ExecutionResult.skipped("cancelled")

    if task.is_expired:
        return ExecutionResult.skipped("expired")

    worker = self._find_worker(task)
    if worker is None:
        return ExecutionResult.no_worker()

    return worker.run(task)


# Bad: Deeply nested
def execute(self, task: Task) -> ExecutionResult:
    if not task.is_cancelled:
        if not task.is_expired:
            worker = self._find_worker(task)
            if worker is not None:
                return worker.run(task)
            else:
                return ExecutionResult.no_worker()
        else:
            return ExecutionResult.skipped("expired")
    else:
        return ExecutionResult.skipped("cancelled")
```

---

## Keyword-Only Arguments

Use `*` for non-obvious parameters:

```python
def retry_task(
    self,
    task_id: str,
    *,
    reset_attempts: bool = False,
    priority_boost: int = 0,
) -> ScheduledTask:
    """Retry a failed task.

    Args:
        task_id: ID of the task to retry.
        reset_attempts: If True, reset attempt counter to 0.
        priority_boost: Increase priority by this amount.
    """
```

### When to Use Keyword-Only

- Boolean flags
- Optional configuration
- Parameters that need names for clarity
- Functions with 3+ parameters

---

## Error Handling

```python
def fetch_with_retry(self, url: str) -> Response:
    """Fetch URL with automatic retry on transient failures."""
    last_error: Exception | None = None

    for attempt in range(self.max_retries + 1):
        try:
            return self._client.get(url)

        except TransientError as e:
            last_error = e
            logger.warning(
                "fetch_retry",
                url=url,
                attempt=attempt + 1,
                error=str(e),
            )
            time.sleep(2 ** attempt)

        except FatalError:
            logger.error("fetch_failed_fatal", url=url)
            raise

    # Exhausted retries
    raise RetryExhaustedError(url, attempts=self.max_retries + 1) from last_error
```

### Error Handling Guidelines

- Never silence errors without explanation
- Always include context in exceptions
- Use `from` to chain exceptions
- Log at appropriate levels

---

## Logging

One logger per module:

```python
import logging

logger = logging.getLogger(__name__)

class Scheduler:
    def schedule(self, task: Task) -> ScheduledTask:
        logger.info("task_scheduled", extra={
            "task_id": task.id,
            "priority": task.priority.value,
        })
```

### Log Levels

| Level | Use For |
|-------|---------|
| DEBUG | Internal details, loop progress |
| INFO | Normal operations, state changes |
| WARNING | Recoverable issues, retries |
| ERROR | Failures requiring attention |

---

## Quick Checklist

Before committing code:

- [ ] Type hints on all public APIs
- [ ] Docstrings on all public APIs
- [ ] No cryptic names (no `t`, `w`, `a`)
- [ ] Guard clauses used (flat structure)
- [ ] Errors don't pass silently
- [ ] Keyword-only for optional params
- [ ] One responsibility per function
- [ ] Tests for key behaviors
