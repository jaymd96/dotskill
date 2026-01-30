---
name: eyeball-introspection
description: Dynamic CLI for code introspection and verification. Use when exploring codebases, verifying API usage, analyzing dependencies, running quick probes, or closing the feedback loop during development. Essential for LLM-assisted development where structured JSON output enables programmatic verification.
---

# Eyeball: Code Introspection for LLMs

> "Close the loop between implementation and verification."

**eyeball** gives LLMs "eyes" to see into code. It provides structured JSON output for exploring modules, verifying API usage, and running quick verification probes—all without leaving the development flow.

---

## Installation

**Check if installed:**
```bash
eyeball --help
```

**If not found, install as dev dependency:**
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

**Configuration** (optional, in `pyproject.toml`):
```toml
[tool.eyeball]
package_name = "mypackage"      # Auto-detected from project.name
tests_dir = "tests"             # Default test directory
fixtures_module = "mypackage.fixtures"  # Custom probe fixtures
```

---

## Why Eyeball Matters for LLM Development

LLMs write code but can't directly verify it works. Eyeball closes this gap:

| Problem | Eyeball Solution |
|---------|------------------|
| "Did I use this API correctly?" | `eyeball api requests:get` - shows signature, params, examples |
| "What does this class do?" | `eyeball inspect mypackage:MyClass` - full introspection |
| "Does my code actually work?" | `eyeball probe "assert func(x) == y"` - quick verification |
| "What depends on this?" | `eyeball callers mypackage:Entity` - reverse dependencies |
| "Did my changes break anything?" | `eyeball test mypackage.models` - structured test output |

**All output is JSON** - parseable, structured, actionable.

---

## Quick Reference

```bash
# Explore what's in a module
eyeball discover mypackage.models

# Get detailed info on a class/function
eyeball inspect mypackage.models:User

# Verify correct third-party API usage
eyeball api requests:Session.get
eyeball search-api pandas merge

# Quick verification probe
eyeball probe "from mypackage import func; assert func(1) == 2"

# Analyze dependencies
eyeball deps mypackage.models:User      # What does User depend on?
eyeball callers mypackage.models:User   # What uses User?

# Run tests with structured output
eyeball test mypackage.models -v

# Execute and see results
eyeball run mypackage.utils:process --kwargs '{"data": [1,2,3]}'
```

**Always use `-p` for pretty-printed JSON when debugging:**
```bash
eyeball -p inspect mypackage.models:User
```

---

## Core Use Cases

### 1. Verify Third-Party API Usage

Before using a library function, verify correct usage:

```bash
# Search for the right function
eyeball search-api requests get

# Get full documentation
eyeball -p api requests:get
```

Output includes:
- Function signature with types
- Parameter descriptions from docstring
- Return type
- Usage examples
- Source code preview

**When to use:** Phase 0 (Discovery), Phase 1 Step 1 (Implementation)

### 2. Explore Your Own Code

Understand existing code before modifying:

```bash
# What's in this module?
eyeball discover mypackage.models

# How does this class work?
eyeball -p inspect mypackage.models:Entity

# Show me the source
eyeball source mypackage.models:Entity.validate
```

**When to use:** Phase 0 (Discovery), before any modification

### 3. Quick Verification Probes

Test code without writing formal tests:

```bash
# Simple assertion
eyeball probe "assert 1 + 1 == 2"

# Test your implementation
eyeball probe "from mypackage.models import User; u = User(name='test'); assert u.name == 'test'"

# With fixtures
eyeball probe --fixture mocks "assert Mock is not None"

# With setup code
eyeball probe --setup "from mypackage import db; db.connect()" "assert db.is_connected()"
```

**When to use:** Phase 1 Step 5 (Experimentation), debugging, quick checks

### 4. Dependency Analysis

Understand code relationships:

```bash
# What does this function call/import?
eyeball -p deps mypackage.services:process_order

# What files use this class?
eyeball -p callers mypackage.models:Order

# What does this module import?
eyeball -p module-deps mypackage.services
```

**When to use:** Phase 0 (understanding impact), refactoring, debugging

### 5. Structured Test Execution

Run tests with JSON output for programmatic evaluation:

```bash
# Run tests for a module
eyeball test mypackage.models

# Discover tests without running
eyeball test mypackage.models --discover

# With coverage
eyeball test mypackage.models --coverage

# Filter specific tests
eyeball test mypackage.models -k "test_validation"
```

**When to use:** Phase 1 Step 6 (Testing), Phase 3 (Completion)

---

## Integration with Development Workflow

See: [references/workflow-integration.md](references/workflow-integration.md) for detailed phase-by-phase usage.

### Phase 0: Discovery
- `eyeball discover` - Explore existing modules
- `eyeball inspect` - Understand key classes/functions
- `eyeball api` - Verify third-party library usage
- `eyeball deps` - Understand what code depends on

### Phase 1: Development
- **Step 1 (Implementation):** `eyeball api` for correct API usage
- **Step 4 (Review):** `eyeball deps` to understand impact
- **Step 5 (Experimentation):** `eyeball probe` for quick tests
- **Step 6 (Testing):** `eyeball test` for formal verification

### Phase 2: Refinement
- `eyeball probe` - Verify specific fixes
- `eyeball test -k` - Run targeted tests
- `eyeball callers` - Verify no regressions

### Phase 3: Completion
- `eyeball test --coverage` - Full test suite
- `eyeball module-deps` - Document dependencies

---

## Closing the Feedback Loop

Eyeball enables the LLM to verify its own work:

```
Write Code → eyeball probe → Verify → Fix → Repeat
     ↓              ↓           ↓
  Generate      Execute      Compare
   output        probe       expected
                             vs actual
```

See: [references/closing-the-loop.md](references/closing-the-loop.md) for patterns.

### Pattern: Implement-Probe-Fix

```bash
# 1. Write implementation
# 2. Probe to verify
eyeball probe "from mypackage import new_func; result = new_func(5); assert result == 25"

# 3. If fails, see the error
{"status": "failed", "checks": [{"name": "probe", "passed": false, "error": "assert 20 == 25"}]}

# 4. Fix implementation
# 5. Probe again until passes
{"status": "success", "checks": [{"name": "probe", "passed": true}]}
```

### Pattern: Explore-Understand-Implement

```bash
# 1. See what exists
eyeball discover mypackage.utils

# 2. Understand the pattern
eyeball -p inspect mypackage.utils:existing_helper

# 3. Implement following the pattern
# 4. Verify your implementation matches
eyeball -p inspect mypackage.utils:new_helper
```

### Pattern: Verify-Before-Commit

```bash
# 1. Check all tests pass
eyeball test mypackage

# 2. Verify no new dependencies break things
eyeball callers mypackage.models:ChangedClass

# 3. Confirm API is correct
eyeball -p api mypackage.models:ChangedClass
```

---

## Command Reference

See: [references/command-reference.md](references/command-reference.md) for full details.

| Command | Purpose | Example |
|---------|---------|---------|
| `discover` | List module contents | `eyeball discover mypackage.models` |
| `inspect` | Detailed introspection | `eyeball inspect mypackage:Class` |
| `api` | Full API documentation | `eyeball api requests:get` |
| `search-api` | Find items in module | `eyeball search-api pandas merge` |
| `run` | Execute function/class | `eyeball run mypackage:func --args '[1]'` |
| `exec` | Run arbitrary code | `eyeball exec 'print(1+1)'` |
| `probe` | Quick verification | `eyeball probe 'assert x == y'` |
| `deps` | Analyze dependencies | `eyeball deps mypackage:func` |
| `callers` | Find usages | `eyeball callers mypackage:Class` |
| `module-deps` | Module imports | `eyeball module-deps mypackage` |
| `test` | Run pytest | `eyeball test mypackage` |
| `source` | Show source code | `eyeball source mypackage:func` |
| `reload` | Hot-reload module | `eyeball reload mypackage.models` |
| `fixtures` | List probe fixtures | `eyeball fixtures` |

---

## Best Practices

### Do
- Use `-p` flag when reading output manually
- Probe early and often during implementation
- Check `api` before using unfamiliar libraries
- Use `deps` before refactoring to understand impact
- Run `test` before committing

### Don't
- Skip verification because "it looks right"
- Ignore probe failures
- Forget to check third-party API usage
- Assume code works without testing

---

## Custom Fixtures

Create project-specific fixtures for probes:

```python
# mypackage/fixtures.py
from eyeball.harness import Fixtures

@Fixtures.register("test_db")
def test_db_fixture():
    """In-memory database for testing."""
    from mypackage.db import create_test_db
    return {"db": create_test_db(), "User": User, "Order": Order}

@Fixtures.register("sample_data")
def sample_data_fixture():
    """Pre-populated test data."""
    return {
        "users": [User(id=1, name="Alice"), User(id=2, name="Bob")],
        "orders": [Order(id=1, user_id=1, total=99.99)],
    }
```

Configure in `pyproject.toml`:
```toml
[tool.eyeball]
fixtures_module = "mypackage.fixtures"
```

Use in probes:
```bash
eyeball probe --fixture test_db "assert db.get_user(1).name == 'Alice'"
eyeball probe --fixture sample_data "assert len(users) == 2"
```

---

## Troubleshooting

### "Module not found"
```bash
# Ensure you're in the project root with package installed
pip install -e .
# Or add to PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### "Cannot get source"
Some built-in or C extension modules don't have Python source.
Use `eyeball inspect` instead of `eyeball source`.

### Probe timeout
```bash
# Increase timeout for slow operations
eyeball probe --timeout 60 "slow_operation()"
```

---

## Related Skills

- **playground-exploration** - Dogfooding philosophy, discovery patterns
- **python-testing-standards** - Formal test writing with pytest
- **python-coding-standards** - Code quality standards
- **workflow-developer** - Development workflow integration
