# Migration Guide: Adding Eyeball to Your Python Project

This guide helps you adopt the probe-first testing workflow in an existing Python project.

---

## Overview

**What you're adding:**
- `eyeball probe` for rapid iteration during development
- `eyeball test` for structured pytest output
- Custom fixtures for your domain

**What stays the same:**
- Your existing pytest tests
- Your CI/CD pipeline
- Your test organization

---

## Step 1: Install Eyeball

```bash
# Using pip
pip install jaymd96-eyeball

# Using hatch
hatch add jaymd96-eyeball --dev

# Using poetry
poetry add jaymd96-eyeball --group dev

# Using uv
uv add jaymd96-eyeball --dev
```

Verify installation:
```bash
eyeball --help
```

---

## Step 2: Configure pyproject.toml

Add the `[tool.eyeball]` section:

```toml
[tool.eyeball]
package_name = "mypackage"           # Your package name (auto-detected if not set)
tests_dir = "tests"                  # Test directory (default: "tests")
fixtures_module = "mypackage.fixtures"  # Optional: custom fixtures module
```

**Auto-detection**: If `package_name` is not set, eyeball reads it from `project.name`.

---

## Step 3: Verify Setup

Test basic functionality:

```bash
# Discover your package
eyeball discover mypackage

# Inspect a class
eyeball -p inspect mypackage.models:User

# Run a simple probe
eyeball probe "from mypackage import __version__; assert __version__"

# Run existing tests with structured output
eyeball test mypackage
```

---

## Step 4: Create Custom Fixtures (Optional)

If you have common test setup, create eyeball fixtures:

### Create fixtures module

```python
# mypackage/fixtures.py
from eyeball.harness import Fixtures

@Fixtures.register("test_db")
def test_database():
    """In-memory database for testing."""
    from mypackage.db import Database
    db = Database(":memory:")
    db.initialize()
    return {
        "db": db,
        "create_user": db.create_user,
        "get_user": db.get_user,
    }

@Fixtures.register("sample_data")
def sample_data():
    """Common test data."""
    from mypackage.models import User, Order
    return {
        "users": [
            User(id=1, name="Alice"),
            User(id=2, name="Bob"),
        ],
        "orders": [
            Order(id=1, user_id=1, total=99.99),
        ],
    }

@Fixtures.register("api_client")
def api_client():
    """Configured API client for testing."""
    from mypackage.api import Client
    return {
        "client": Client(base_url="http://test.local"),
        "auth_headers": {"Authorization": "Bearer test-token"},
    }
```

### Configure pyproject.toml

```toml
[tool.eyeball]
fixtures_module = "mypackage.fixtures"
```

### Use in probes

```bash
eyeball probe --fixture test_db "user = create_user('alice'); assert get_user(user.id).name == 'alice'"
eyeball probe --fixture sample_data "assert len(users) == 2"
eyeball probe --fixture api_client "resp = client.get('/health'); assert resp.ok"
```

---

## Step 5: Integrate into Development Workflow

### During implementation

Replace manual `python -c` testing with probes:

```bash
# Before: manual testing
python -c "from mypackage import func; print(func(1))"

# After: structured verification
eyeball probe "from mypackage import func; assert func(1) == expected"
```

### During debugging

```bash
# Inspect what you're working with
eyeball -p inspect mypackage.models:User

# Check dependencies
eyeball -p deps mypackage.models:User

# Quick verification
eyeball probe "from mypackage.models import User; u = User(name='test'); print(u)"
```

### Before committing

```bash
# Run tests with structured output
eyeball test mypackage

# Check coverage
eyeball test mypackage --coverage
```

---

## Step 6: Update CI/CD (Optional)

You can use `eyeball test` in CI for structured output, though regular pytest works too:

```yaml
# .github/workflows/test.yml
- name: Run tests
  run: |
    eyeball test mypackage --coverage > test-results.json
    # Parse JSON for structured reporting
```

Or keep using pytest directly:

```yaml
- name: Run tests
  run: pytest tests/ --cov=mypackage
```

---

## Common Migration Scenarios

### Scenario: Large existing test suite

**Approach**: Keep everything, add eyeball for new development.

```bash
# Existing tests still work
pytest tests/

# New development uses probes
eyeball probe "from mypackage.new_module import func; assert func(x) == y"

# Structured output for CI
eyeball test mypackage
```

### Scenario: No fixtures yet

**Approach**: Start with built-in fixtures, add custom ones as needed.

```bash
# Built-in fixtures
eyeball probe --fixture mocks "assert Mock is not None"
eyeball probe --fixture temp_files "assert temp_dir.exists()"

# Add custom fixtures when patterns emerge
```

### Scenario: Complex test setup

**Approach**: Mirror pytest fixtures as eyeball fixtures.

```python
# If you have this pytest fixture:
@pytest.fixture
def database():
    db = Database(":memory:")
    db.initialize()
    yield db
    db.close()

# Create equivalent eyeball fixture:
@Fixtures.register("database")
def database_fixture():
    db = Database(":memory:")
    db.initialize()
    return {"db": db}
```

### Scenario: Monorepo with multiple packages

**Approach**: Configure each package separately.

```toml
# packages/core/pyproject.toml
[tool.eyeball]
package_name = "core"

# packages/api/pyproject.toml
[tool.eyeball]
package_name = "api"
```

---

## Troubleshooting

### "Module not found"

```bash
# Ensure package is installed in editable mode
pip install -e .

# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "Fixture not found"

```bash
# Check available fixtures
eyeball fixtures

# Verify fixtures_module is configured
grep fixtures_module pyproject.toml
```

### Probe timeout

```bash
# Increase timeout for slow operations
eyeball probe --timeout 60 "slow_operation()"
```

### Tests not discovered

```bash
# Check test directory
eyeball test mypackage --discover

# Verify tests_dir configuration
grep tests_dir pyproject.toml
```

---

## Checklist

- [ ] Installed `jaymd96-eyeball` as dev dependency
- [ ] Added `[tool.eyeball]` to pyproject.toml
- [ ] Verified `eyeball discover mypackage` works
- [ ] Verified `eyeball test mypackage` runs tests
- [ ] Created custom fixtures (if needed)
- [ ] Team knows to use `eyeball probe` during development
- [ ] Updated development documentation

---

## Next Steps

1. **Read the full skill**: See [../SKILL.md](../SKILL.md) for complete testing patterns
2. **Explore eyeball**: See **eyeball-introspection** skill for all commands
3. **Practice**: Use probes for your next feature implementation
