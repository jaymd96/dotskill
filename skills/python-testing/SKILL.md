---
name: python-testing
description: Write effective Python tests using pytest. Use when creating tests for Python code, designing test strategies, writing fixtures, or improving test quality. Triggers on requests to write tests, add test coverage, create fixtures, or design testing approaches for Python modules/functions/classes.
---

# Python Testing with Eyeball + Pytest

> **Probe first, test second.**

Use eyeball for rapid iteration during development. Convert stable patterns to pytest for regression prevention.

---

## The Testing Workflow

```
Development:  eyeball probe → verify → iterate → working code
Formalization: working code → pytest tests → CI/CD protection
```

| Tool | Purpose | When |
|------|---------|------|
| `eyeball probe` | Quick verification | During development |
| `eyeball test` | Structured pytest output | LLM feedback loop |
| `pytest` | Formal test suite | CI/CD, regression |

---

## Quick Start

### 1. Install eyeball as dev dependency

```bash
pip install jaymd96-eyeball
# or
hatch add jaymd96-eyeball --dev
```

### 2. Configure (optional)

```toml
# pyproject.toml
[tool.eyeball]
package_name = "mypackage"
tests_dir = "tests"
fixtures_module = "mypackage.fixtures"
```

### 3. Probe during development

```bash
# Quick verification while coding
eyeball probe "from mypackage import func; assert func(1) == 2"

# With setup code
eyeball probe --setup "from mypackage.db import connect" "assert connect().is_ready"

# With fixtures
eyeball probe --fixture mocks "assert Mock is not None"
```

### 4. Run formal tests with structured output

```bash
# JSON output for LLM consumption
eyeball test mypackage.models

# With coverage
eyeball test mypackage --coverage

# Filter specific tests
eyeball test mypackage -k "test_validation"
```

---

## Probe-First Development

### The Pattern

```python
# 1. Write implementation
def calculate_tax(amount: float, rate: float) -> float:
    return amount * rate

# 2. Probe to verify
# $ eyeball probe "from mypackage import calculate_tax; assert calculate_tax(100, 0.1) == 10.0"

# 3. See result
# {"status": "success", "checks": [{"name": "probe", "passed": true}]}

# 4. If fails, fix and probe again
# 5. When stable, write formal test
```

### When to Probe vs Test

| Use Probe | Use Pytest |
|-----------|------------|
| Exploring implementation | Documenting behavior |
| Quick sanity checks | Regression prevention |
| Debugging specific issues | CI/CD pipeline |
| Verifying API usage | Coverage tracking |
| Interactive development | Permanent test suite |

### Probe Best Practices

```bash
# Good: Single focused assertion
eyeball probe "from mypackage import User; u = User('test'); assert u.name == 'test'"

# Good: With descriptive setup
eyeball probe --setup "from mypackage import db; db.connect()" "assert db.is_connected()"

# Bad: Too many assertions (hard to diagnose failures)
eyeball probe "assert a == 1; assert b == 2; assert c == 3"

# Better: One probe per assertion during debugging
eyeball probe "assert a == 1"
eyeball probe "assert b == 2"
```

---

## Converting Probes to Tests

When a probe is stable and tests important behavior, convert it to a formal test:

### Probe

```bash
eyeball probe "from mypackage.models import User; u = User(name='alice'); assert u.name == 'alice'"
```

### Formal Test

```python
# tests/unit/test_user.py
def test_user_stores_name():
    # Arrange
    name = "alice"

    # Act
    user = User(name=name)

    # Assert
    assert user.name == name
```

### Conversion Checklist

- [ ] Add descriptive test name (`test_<unit>_<scenario>_<outcome>`)
- [ ] Use Arrange-Act-Assert structure
- [ ] Add to appropriate test file
- [ ] Consider parametrizing for multiple cases
- [ ] Remove magic values, use meaningful names

---

## Pytest Standards

### Test Structure (Arrange-Act-Assert)

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

### Naming Tests

```python
# Good: describes behavior
def test_schedule_task_with_high_priority_runs_first(): ...
def test_worker_rejects_task_outside_capabilities(): ...

# Bad: describes implementation
def test_schedule(): ...
def test_worker_check(): ...
```

**Pattern**: `test_<unit>_<scenario>_<expected_outcome>`

### What to Test

| Priority | Type | Example |
|----------|------|---------|
| 1 | Happy path | Task executes successfully |
| 2 | Error paths | Invalid input raises error |
| 3 | Edge cases | Empty input, max values |
| 4 | Integration | Scheduler assigns to worker |

---

## Fixtures

### Pytest Fixtures (for formal tests)

```python
# tests/conftest.py
import pytest

@pytest.fixture
def user():
    """A standard user for testing."""
    return User(id="test-user", name="Alice")

@pytest.fixture
def database(tmp_path):
    """In-memory database for testing."""
    db = Database(path=tmp_path / "test.db")
    db.initialize()
    yield db
    db.close()
```

### Eyeball Fixtures (for probes)

```python
# mypackage/fixtures.py
from eyeball.harness import Fixtures

@Fixtures.register("test_db")
def test_db_fixture():
    """In-memory database for probes."""
    from mypackage.db import create_test_db
    return {"db": create_test_db()}

@Fixtures.register("sample_users")
def sample_users_fixture():
    """Pre-populated user data."""
    return {
        "users": [
            User(id=1, name="Alice"),
            User(id=2, name="Bob"),
        ]
    }
```

Configure in pyproject.toml:
```toml
[tool.eyeball]
fixtures_module = "mypackage.fixtures"
```

Use in probes:
```bash
eyeball probe --fixture test_db "assert db.get_user(1) is not None"
eyeball probe --fixture sample_users "assert len(users) == 2"
```

### Built-in Eyeball Fixtures

| Fixture | Provides |
|---------|----------|
| `mocks` | `Mock`, `MagicMock`, `patch` |
| `async_helpers` | `asyncio`, `run_async` |
| `temp_files` | `temp_dir`, `temp_file`, `Path` |

---

## Factory Functions

For creating test objects with variations:

```python
# tests/factories.py
def make_user(
    *,
    id: str = "test-user",
    name: str = "Test User",
    email: str | None = None,
    **overrides,
) -> User:
    """Create a user with sensible defaults."""
    return User(id=id, name=name, email=email, **overrides)


# In tests
def test_user_with_email_is_verified():
    user = make_user(email="test@example.com")
    assert user.is_verified
```

---

## Testing Patterns

### Testing Exceptions

```python
def test_empty_name_raises_validation_error():
    with pytest.raises(ValidationError, match="Name cannot be empty"):
        User(name="")
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", "HELLO"),
    ("World", "WORLD"),
    ("", ""),
])
def test_uppercase_conversion(input, expected):
    assert to_upper(input) == expected
```

### Testing Async Code

```python
@pytest.mark.asyncio
async def test_async_fetch_returns_data():
    result = await fetch_data("https://api.example.com")
    assert result.status == 200
```

### Testing with Mocks

```python
def test_service_calls_repository():
    repo = Mock(spec=UserRepository)
    repo.find.return_value = User(id="1", name="Alice")

    service = UserService(repository=repo)
    user = service.get_user("1")

    repo.find.assert_called_once_with("1")
    assert user.name == "Alice"
```

---

## Test Organization

```
tests/
├── conftest.py              # Shared pytest fixtures
├── factories.py             # Object factories
│
├── unit/                    # Fast, isolated tests
│   ├── test_user.py
│   ├── test_order.py
│   └── test_validators.py
│
├── integration/             # Component interaction
│   ├── test_user_service.py
│   └── test_database.py
│
└── e2e/                     # End-to-end (if needed)
    └── test_api.py
```

---

## LLM Feedback Loop

Use eyeball's structured output to verify your own work:

```bash
# Run tests and parse results
eyeball test mypackage.models
```

```json
{
  "status": "success",
  "summary": {
    "total": 15,
    "passed": 14,
    "failed": 1,
    "skipped": 0
  },
  "failures": [
    {
      "name": "test_user_email_validation",
      "message": "AssertionError: assert None == 'test@example.com'"
    }
  ]
}
```

**Workflow**:
1. Write code
2. `eyeball probe` to verify
3. `eyeball test` to run full suite
4. Parse JSON output
5. Fix failures
6. Repeat until green

---

## Quick Reference

```bash
# Probing (development)
eyeball probe "assert 1 + 1 == 2"
eyeball probe --fixture mocks "assert Mock is not None"
eyeball probe --setup "import os" "assert os.getcwd()"
eyeball probe --timeout 30 "slow_operation()"

# Testing (formal)
eyeball test mypackage                    # Run all tests
eyeball test mypackage.models             # Run module tests
eyeball test mypackage -k "validation"    # Filter tests
eyeball test mypackage --coverage         # With coverage
eyeball test mypackage --discover         # List without running

# Exploring (before testing)
eyeball discover mypackage.models         # What's in module?
eyeball inspect mypackage.models:User     # How does it work?
eyeball api pytest:raises                 # How to use pytest?
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Instead |
|--------------|---------|---------|
| Skip probing | Slower feedback | Probe first, test later |
| Test implementation | Brittle on refactor | Test behavior/outcomes |
| One giant test | Hard to diagnose | One focus per test |
| Magic values | Unclear significance | Named constants |
| 100% coverage goal | Tests without value | Cover behavior |
| No structured output | LLM can't parse | Use `eyeball test` |

---

## Migration from pytest-only

See: [references/migration-guide.md](references/migration-guide.md)

1. Install eyeball
2. Configure pyproject.toml
3. Create probe fixtures
4. Start probing during development
5. Keep existing pytest tests
6. Use `eyeball test` for structured output

---

## Related Skills

- **eyeball-introspection** - Full eyeball documentation
- **playground-exploration** - Discovery patterns
- **python-coding-standards** - Code quality
