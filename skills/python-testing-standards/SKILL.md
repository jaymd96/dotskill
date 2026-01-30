---
name: python-testing-standards
description: Python testing standards using pytest. Use when writing tests, designing test strategies, creating fixtures, or evaluating test quality. Provides guidance for effective, maintainable tests.
---

# Python Testing Standards

Write tests that verify behavior, document intent, and catch regressions - without becoming a maintenance burden.

## Core Principle

> **Tests are executable documentation.**

A reader should understand what the code does by reading the tests. Optimize for clarity, not coverage metrics.

---

## Test Structure (Arrange-Act-Assert)

Every test has three parts. Make them visually distinct:

```python
def test_task_execution_succeeds():
    # Arrange: set up preconditions
    task = Task(id="task-1", type=TaskType.COMPUTE)
    worker = Worker(id="worker-1", capabilities={TaskType.COMPUTE})

    # Act: perform the operation
    result = worker.execute(task)

    # Assert: verify the outcome
    assert result.status == ExecutionStatus.SUCCESS
    assert result.task_id == "task-1"
```

For simple tests, compress while keeping logical separation:

```python
def test_empty_queue_returns_none():
    queue = TaskQueue()
    assert queue.pop() is None
```

---

## Naming Tests

Test names should read as behavior specifications:

```python
# Good: describes behavior
def test_schedule_task_with_high_priority_runs_first(): ...
def test_worker_rejects_task_outside_capabilities(): ...
def test_retry_exhausted_returns_failure_with_last_error(): ...

# Bad: describes implementation
def test_schedule(): ...
def test_worker_check(): ...
def test_retry_loop(): ...
```

**Pattern**: `test_<unit>_<scenario>_<expected_outcome>`

---

## What to Test

| Test Type | Purpose | Example |
|-----------|---------|---------|
| Happy path | Core functionality works | Task executes successfully |
| Edge cases | Boundaries behave correctly | Empty input, max values |
| Error paths | Failures are handled | Invalid input raises error |
| Integration | Components work together | Scheduler assigns to worker |

**Priority Order**:
1. Happy paths (must work)
2. Error paths (must fail gracefully)
3. Edge cases (prevent regressions)
4. Integration (verify wiring)

---

## Fixtures for Reusable Setup

Use fixtures for objects needed across multiple tests:

```python
# conftest.py
import pytest

@pytest.fixture
def task():
    """A standard task for testing."""
    return Task(
        id="test-task",
        type=TaskType.COMPUTE,
        priority=Priority.NORMAL,
    )

@pytest.fixture
def worker():
    """A worker with standard capabilities."""
    return Worker(
        id="test-worker",
        capabilities={TaskType.COMPUTE, TaskType.IO},
    )

@pytest.fixture
def scheduler(task_queue, worker_pool):
    """Fully wired scheduler for integration tests."""
    return Scheduler(queue=task_queue, pool=worker_pool)
```

**Fixture Guidelines**:
- Keep fixtures simple
- Name after what they are, not what they're for
- Use `conftest.py` for shared fixtures
- Prefer function scope unless setup is expensive

---

## Factory Functions for Variations

When you need many similar objects with slight variations:

```python
# tests/factories.py
def make_task(
    *,
    id: str = "test-task",
    type: TaskType = TaskType.COMPUTE,
    priority: Priority = Priority.NORMAL,
    **overrides,
) -> Task:
    """Create a task with sensible defaults."""
    return Task(id=id, type=type, priority=priority, **overrides)


# In tests
def test_high_priority_scheduled_first():
    low = make_task(id="low", priority=Priority.LOW)
    high = make_task(id="high", priority=Priority.HIGH)

    queue = TaskQueue()
    queue.push(low)
    queue.push(high)

    assert queue.pop().id == "high"
```

---

## Testing Exceptions

Use `pytest.raises` with context manager:

```python
def test_empty_task_id_raises_validation_error():
    with pytest.raises(ValidationError, match="Task ID cannot be empty"):
        Task(id="", type=TaskType.COMPUTE)


def test_negative_timeout_raises_value_error():
    with pytest.raises(ValueError) as exc_info:
        Task(id="task-1", timeout_seconds=-1)

    assert "positive" in str(exc_info.value)
```

---

## Parametrized Tests

When testing same behavior with different inputs:

```python
@pytest.mark.parametrize("priority,expected_value", [
    (Priority.LOW, 10),
    (Priority.NORMAL, 50),
    (Priority.HIGH, 80),
    (Priority.CRITICAL, 100),
])
def test_priority_values(priority, expected_value):
    assert priority.value == expected_value


@pytest.mark.parametrize("status,can_execute", [
    (TaskStatus.PENDING, True),
    (TaskStatus.RUNNING, False),
    (TaskStatus.COMPLETED, False),
    (TaskStatus.CANCELLED, False),
])
def test_task_executability_by_status(status, can_execute):
    task = make_task(status=status)
    assert task.can_execute == can_execute
```

---

## Testing with Mocks

Mock external dependencies, not the code under test:

```python
from unittest.mock import Mock, patch

def test_scheduler_logs_assignment():
    worker = Mock(spec=Worker)
    worker.is_available = True
    worker.can_handle.return_value = True

    task = make_task()
    scheduler = Scheduler(workers=[worker])

    with patch.object(scheduler, '_logger') as mock_logger:
        scheduler.assign(task)

        mock_logger.info.assert_called_once()
        assert "assigned" in mock_logger.info.call_args[0][0].lower()
```

**Mock Guidelines**:
- Use `spec=` to catch typos
- Mock at boundaries (HTTP, database, filesystem)
- Don't mock the code you're testing
- Prefer dependency injection over patching

---

## Test File Organization

```
tests/
├── conftest.py              # Shared fixtures
├── factories.py             # Object factories
│
├── unit/                    # Fast, isolated tests
│   ├── test_task.py
│   ├── test_worker.py
│   └── test_queue.py
│
├── integration/             # Component interaction tests
│   ├── test_scheduler.py
│   └── test_persistence.py
│
└── e2e/                     # End-to-end tests (if needed)
    └── test_workflow.py
```

---

## Common Patterns

### Testing Dataclasses

```python
def test_task_is_immutable():
    task = make_task()

    with pytest.raises(AttributeError):
        task.id = "new-id"


def test_task_with_modified_priority():
    original = make_task(priority=Priority.LOW)
    modified = original.with_priority(Priority.HIGH)

    assert original.priority == Priority.LOW  # unchanged
    assert modified.priority == Priority.HIGH
```

### Testing Generators

```python
def test_iter_records_yields_all_batches():
    store = RecordStore()
    for i in range(250):
        store.save(make_record(id=f"record-{i}"))

    records = list(store.iter_records(batch_size=100))

    assert len(records) == 250
```

### Testing Async Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_task_execution():
    task = make_task()
    worker = AsyncWorker()

    result = await worker.execute(task)

    assert result.status == ExecutionStatus.SUCCESS
```

---

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Testing implementation | Brittle on refactor | Test behavior/outcomes |
| One giant test | Hard to diagnose | One assertion focus per test |
| Shared mutable state | Tests affect each other | Fresh fixtures per test |
| Magic values | Unclear significance | Named constants/comments |
| 100% coverage goal | Tests without value | Cover behavior, not lines |

---

## Test Scenarios Checklist

For each function/method, consider testing:

**Happy Path**
- [ ] Normal input produces expected output
- [ ] Valid edge of input range works

**Edge Cases**
- [ ] Empty input (empty list, empty string, None)
- [ ] Single item
- [ ] Maximum allowed values
- [ ] Minimum allowed values

**Error Cases**
- [ ] Invalid input raises appropriate error
- [ ] Missing required parameters
- [ ] Type mismatches

**State Changes**
- [ ] Side effects occur as expected
- [ ] State is modified correctly
- [ ] Cleanup happens on error

---

## Quick Checklist

Before committing tests:

- [ ] Test names describe behavior
- [ ] Arrange-Act-Assert structure is clear
- [ ] Happy path is tested
- [ ] Key error paths are tested
- [ ] No shared mutable state
- [ ] Mocks are at boundaries
- [ ] Tests run fast
- [ ] No flaky tests
