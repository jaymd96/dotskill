# Closing the Feedback Loop

How eyeball enables LLMs to verify their own work and create better code through structured feedback.

---

## The Problem: LLMs Can't See

LLMs write code but can't directly observe:
- Whether it actually runs
- What errors occur at runtime
- If the output matches expectations
- How it integrates with existing code

**Result:** Code that "looks right" but fails in practice.

---

## The Solution: Structured Verification

Eyeball provides the eyes LLMs need:

```
┌─────────────────────────────────────────────────────────┐
│                    LLM Writes Code                       │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              eyeball probe "assert ..."                  │
│                                                          │
│  Returns structured JSON:                                │
│  - status: success/failed/error                          │
│  - checks: [{passed: true/false, error: "..."}]          │
│  - stdout/stderr capture                                 │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│          LLM Reads Result, Adjusts Code                  │
│                                                          │
│  If failed → Fix implementation                          │
│  If error → Fix syntax/import                            │
│  If passed → Continue to next check                      │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
                      Repeat until all pass
```

---

## Pattern 1: Implement-Probe-Fix Loop

The most common pattern for iterative development.

### Step 1: Write Initial Implementation

```python
# mypackage/calculator.py
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax on an amount."""
    return amount * rate
```

### Step 2: Probe to Verify

```bash
eyeball probe "
from mypackage.calculator import calculate_tax
result = calculate_tax(100, 0.1)
assert result == 10.0, f'Expected 10.0, got {result}'
"
```

### Step 3: Read Result

**If success:**
```json
{"status": "success", "checks": [{"name": "probe", "passed": true}]}
```
→ Move to next scenario

**If failed:**
```json
{"status": "failed", "checks": [{"name": "probe", "passed": false, "error": "Expected 10.0, got 10.000000000000002"}]}
```
→ Fix the implementation (use `round()` or `Decimal`)

### Step 4: Fix and Repeat

```python
def calculate_tax(amount: float, rate: float) -> float:
    """Calculate tax on an amount."""
    return round(amount * rate, 2)
```

```bash
eyeball probe "from mypackage.calculator import calculate_tax; assert calculate_tax(100, 0.1) == 10.0"
# {"status": "success", ...}
```

---

## Pattern 2: Explore-Understand-Implement

Before writing new code, understand the patterns.

### Step 1: Explore Existing Code

```bash
# What functions exist?
eyeball discover mypackage.utils

# How is a similar function implemented?
eyeball -p inspect mypackage.utils:existing_validator
```

### Step 2: Understand the Pattern

```json
{
  "type": "function",
  "signature": "(value: str, *, min_length: int = 1, max_length: int = 100) -> str",
  "docstring": "Validate and return a string value.",
  "parameters": [
    {"name": "value", "type": "str", "required": true},
    {"name": "min_length", "type": "int", "default": "1", "kind": "KEYWORD_ONLY"},
    {"name": "max_length", "type": "int", "default": "100", "kind": "KEYWORD_ONLY"}
  ]
}
```

### Step 3: Implement Following Pattern

```python
def new_validator(value: str, *, pattern: str = r".*") -> str:
    """Validate string matches pattern."""
    # Follow same structure as existing_validator
    ...
```

### Step 4: Verify Match

```bash
eyeball -p inspect mypackage.utils:new_validator
# Compare structure with existing_validator
```

---

## Pattern 3: Verify-Before-Using

Check third-party APIs before using them.

### Step 1: Search for Functionality

```bash
eyeball search-api httpx client
```

### Step 2: Get Full Documentation

```bash
eyeball -p api httpx:AsyncClient.get
```

### Step 3: Probe to Confirm Understanding

```bash
eyeball probe "
import httpx
# Verify the signature matches our understanding
import inspect
sig = inspect.signature(httpx.AsyncClient.get)
params = list(sig.parameters.keys())
assert 'url' in params, 'Missing url parameter'
assert 'params' in params, 'Missing params parameter'
print('API verified:', params)
"
```

### Step 4: Write Code with Confidence

Now you know exactly how to call it.

---

## Pattern 4: Regression Prevention

After changes, verify nothing broke.

### Step 1: Find What Uses Changed Code

```bash
eyeball callers mypackage.models:User
```

### Step 2: Probe Each Caller

```bash
# For each file that uses User
eyeball probe "
from mypackage.services.user_service import create_user
# Verify still works with new User signature
user = create_user('test', 'test@example.com')
assert user.name == 'test'
"
```

### Step 3: Run Full Test Suite

```bash
eyeball test mypackage
```

---

## Pattern 5: Multi-Check Verification

Group related checks with labels.

```bash
eyeball probe "
from mypackage.models import User

# @check: constructor accepts required fields
user = User(name='Alice', email='alice@example.com')
assert user.name == 'Alice'

# @check: email validation works
try:
    User(name='Bob', email='not-an-email')
    assert False, 'Should reject invalid email'
except ValueError:
    pass

# @check: name cannot be empty
try:
    User(name='', email='bob@example.com')
    assert False, 'Should reject empty name'
except ValueError:
    pass

# @check: default values applied
user2 = User(name='Carol', email='carol@example.com')
assert user2.active == True  # default value

# @check: repr is readable
assert 'Alice' in repr(user)
"
```

**Output:**
```json
{
  "status": "success",
  "checks": [
    {"name": "constructor accepts required fields", "passed": true},
    {"name": "email validation works", "passed": true},
    {"name": "name cannot be empty", "passed": true},
    {"name": "default values applied", "passed": true},
    {"name": "repr is readable", "passed": true}
  ],
  "summary": {"total": 5, "passed": 5, "failed": 0}
}
```

---

## Defining Custom Fixtures

For complex setups, define project-specific fixtures.

### Best Practices for Fixtures

**1. Keep fixtures focused** - One fixture, one purpose.

```python
# Good: focused fixtures
@Fixtures.register("test_user")
def test_user_fixture():
    """A single test user."""
    return {"user": User(name="Test", email="test@example.com")}

@Fixtures.register("test_db")
def test_db_fixture():
    """In-memory database connection."""
    return {"db": create_test_db()}
```

```python
# Bad: kitchen sink fixture
@Fixtures.register("everything")
def everything_fixture():
    """Too much stuff."""
    return {"user": User(...), "db": create_db(), "api": API(), ...}
```

**2. Return dictionaries** - All fixtures return `dict[str, Any]`.

```python
@Fixtures.register("sample_orders")
def sample_orders_fixture():
    """Sample order data for testing."""
    return {
        "orders": [Order(id=1, total=99.99), Order(id=2, total=149.99)],
        "Order": Order,  # Include class for convenience
        "total_value": 249.98,
    }
```

**3. Document what's provided** - Docstring explains the fixture.

```python
@Fixtures.register("auth_context")
def auth_context_fixture():
    """
    Authenticated user context for testing.

    Provides:
        user: Authenticated User instance
        token: Valid JWT token
        session: Active session object
    """
    user = User(id=1, name="Test User")
    token = create_token(user)
    session = Session(user=user)
    return {"user": user, "token": token, "session": session}
```

**4. Fixtures can use other fixtures** - Compose when needed.

```python
@Fixtures.register("full_context")
def full_context_fixture():
    """Complete test context combining other fixtures."""
    db = Fixtures.get("test_db")["db"]
    user = Fixtures.get("test_user")["user"]
    db.save(user)
    return {"db": db, "user": user, "saved": True}
```

**5. Clean up resources** - If fixture creates resources, document cleanup.

```python
@Fixtures.register("temp_workspace")
def temp_workspace_fixture():
    """
    Temporary workspace directory.

    Note: Directory is created fresh each time.
    Caller should clean up if needed.
    """
    import tempfile
    from pathlib import Path

    workspace = Path(tempfile.mkdtemp(prefix="test_"))
    return {
        "workspace": workspace,
        "create_file": lambda name, content: (workspace / name).write_text(content),
    }
```

### Fixture File Organization

```python
# mypackage/fixtures.py
"""Test fixtures for eyeball probes.

Configure in pyproject.toml:
    [tool.eyeball]
    fixtures_module = "mypackage.fixtures"
"""

from eyeball.harness import Fixtures

# Domain-specific fixtures
@Fixtures.register("test_user")
def test_user_fixture():
    """A test user for authentication tests."""
    from mypackage.models import User
    return {"user": User(name="Test", email="test@example.com")}


@Fixtures.register("test_db")
def test_db_fixture():
    """In-memory SQLite database."""
    from mypackage.db import create_engine, Base
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return {"engine": engine, "db": Session(engine)}


@Fixtures.register("api_client")
def api_client_fixture():
    """Configured API client for integration tests."""
    from mypackage.client import APIClient
    return {"client": APIClient(base_url="http://test.local")}


# Utility fixtures
@Fixtures.register("sample_data")
def sample_data_fixture():
    """Common test data."""
    return {
        "valid_emails": ["user@example.com", "test@test.org"],
        "invalid_emails": ["not-an-email", "@missing.com", "spaces in@email.com"],
        "valid_names": ["Alice", "Bob", "Carol"],
        "invalid_names": ["", "   ", None],
    }
```

### Using Fixtures in Probes

```bash
# Single fixture
eyeball probe --fixture test_user "assert user.name == 'Test'"

# Multiple fixtures
eyeball probe --fixture test_db --fixture test_user "
db.save(user)
loaded = db.get_user(user.id)
assert loaded.name == user.name
"

# With sample data
eyeball probe --fixture sample_data "
from mypackage.validators import validate_email
for email in valid_emails:
    assert validate_email(email), f'{email} should be valid'
for email in invalid_emails:
    assert not validate_email(email), f'{email} should be invalid'
"
```

---

## Debugging Failures

When probes fail, use the output to fix issues.

### Assertion Failure

```json
{
  "status": "failed",
  "checks": [{"passed": false, "error": "assert 20 == 25", "line": 3}],
  "stdout": "Debug: intermediate value is 20"
}
```

**Fix:** The implementation returns 20 but should return 25. Check the calculation logic.

### Import Error

```json
{
  "status": "error",
  "error": "ImportError: cannot import name 'NewClass' from 'mypackage'",
  "traceback": "..."
}
```

**Fix:** The class wasn't exported. Add to `__all__` or check the import path.

### Runtime Error

```json
{
  "status": "error",
  "error": "TypeError: missing 1 required positional argument: 'email'",
  "traceback": "..."
}
```

**Fix:** The function signature changed. Update the probe call.

### Use stdout for Debugging

```bash
eyeball probe "
from mypackage import process
data = [1, 2, 3]
print(f'Input: {data}')
result = process(data)
print(f'Output: {result}')
assert result == [2, 4, 6], f'Expected [2, 4, 6], got {result}'
"
```

Output includes stdout for debugging:
```json
{
  "status": "failed",
  "stdout": "Input: [1, 2, 3]\nOutput: [1, 4, 9]",
  "checks": [{"error": "Expected [2, 4, 6], got [1, 4, 9]"}]
}
```

Now you can see the actual output and fix the bug (squares instead of doubles).

---

## Integration with Quality Gates

Eyeball probes directly support workflow quality gates.

### Minimum Scenario Requirement

Quality gates require >= 5 scenarios tested. Use labeled checks:

```bash
eyeball probe "
from mypackage.models import Order

# @check: Scenario 1 - Create valid order
order = Order(user_id=1, items=[{'sku': 'A', 'qty': 2}])
assert order.total > 0

# @check: Scenario 2 - Empty items rejected
try:
    Order(user_id=1, items=[])
    assert False
except ValueError:
    pass

# @check: Scenario 3 - Negative quantity rejected
try:
    Order(user_id=1, items=[{'sku': 'A', 'qty': -1}])
    assert False
except ValueError:
    pass

# @check: Scenario 4 - Calculate total correctly
order = Order(user_id=1, items=[{'sku': 'A', 'qty': 2, 'price': 10.0}])
assert order.total == 20.0

# @check: Scenario 5 - Apply discount
order = Order(user_id=1, items=[{'sku': 'A', 'qty': 2, 'price': 10.0}], discount=0.1)
assert order.total == 18.0
"
```

### Zero Runtime Errors Gate

```bash
eyeball probe "
from mypackage import module_under_test

# Test all public functions don't raise unexpected errors
import inspect
for name, func in inspect.getmembers(module_under_test, inspect.isfunction):
    if name.startswith('_'):
        continue
    # Each function should have at least a docstring
    assert func.__doc__, f'{name} missing docstring'
    print(f'{name}: OK')
"
```

---

## Summary: The Feedback Loop

1. **Write code** - Implement functionality
2. **Probe immediately** - `eyeball probe "assert ..."`
3. **Read structured output** - JSON tells you exactly what happened
4. **Fix issues** - Adjust implementation based on feedback
5. **Repeat** - Until all probes pass
6. **Formal tests** - Convert stable probes to pytest

**The loop closes because:**
- Output is structured (parseable, not just text)
- Errors include line numbers and messages
- stdout/stderr captured for debugging
- Multiple checks can run in one probe
- Fixtures provide consistent test data

This creates a tight feedback loop where each iteration produces concrete, actionable information.
